from io import BytesIO
from PIL import Image
import numpy as np
import requests
from pdf_organizer import PDF_Organizer

#Preparing PDF
pdf = PDF_Organizer()

#Saving wide image
first_response = requests.get('https://img.mako.co.il/2023/03/06/ANGRY_BIBI_LEVIN_1502_re_autoOrient_x6.jpg')
wide_img = Image.open(BytesIO(first_response.content))
new_wide_image_size = (512, 288)
resized_wide_img = wide_img.resize(new_wide_image_size)
pdf.save_and_add_title_and_image_to_pdf(resized_wide_img, 'ps0-1-a-1.png', 'RGB', section='1.a.')

#Saving tall image
second_response = requests.get('https://images.pexels.com/photos/699466/pexels-photo-699466.jpeg?auto=compress&cs=tinysrgb&w=1600')
tall_img = Image.open(BytesIO(second_response.content))
new_tall_image_size = (384, 512)
resized_tall_img = tall_img.resize(new_tall_image_size)
pdf.save_and_add_title_and_image_to_pdf(resized_tall_img, 'ps0-1-a-2.png', 'RGB')

#Swapping red and blue
resized_wide_image_as_ndarray = np.asarray(resized_wide_img)
swapped_blue_red_resized_wide_image_as_ndarray = resized_wide_image_as_ndarray[:, :, [2, 1, 0]]
pdf.save_and_add_title_and_image_to_pdf(swapped_blue_red_resized_wide_image_as_ndarray, 'ps0-2-a-1.png', 'RGB', section='2.a.')

#Monochrome image - only green
monochrome_wide_green_image_as_ndarray = resized_wide_image_as_ndarray[:, :, 1]
pdf.save_and_add_title_and_image_to_pdf(monochrome_wide_green_image_as_ndarray, 'ps0-2-b-1.png', 'L', '2.b.')

#Monochrome image - only red
monochrome_wide_red_image_as_ndarray = resized_wide_image_as_ndarray[:, :, 0]
pdf.save_and_add_title_and_image_to_pdf(monochrome_wide_red_image_as_ndarray, 'ps0-2-c-1.png', 'L', '2.c.')

#Replacement of pixels
shape_of_wide_image = monochrome_wide_green_image_as_ndarray.shape
center_coordinates_of_wide_image = tuple(int(coordinate/2) for coordinate in shape_of_wide_image)
center_square_coordinates_of_wide_image = list([coordinate - 50, coordinate + 50] for coordinate in center_coordinates_of_wide_image)

lower_border = center_square_coordinates_of_wide_image[0][0]
upper_border = center_square_coordinates_of_wide_image[0][1]
left_border = center_square_coordinates_of_wide_image[1][0]
right_border = center_square_coordinates_of_wide_image[1][1]

center_square_region_of_red_monochrome_image = monochrome_wide_green_image_as_ndarray[lower_border:upper_border, left_border:right_border]

new_monochrome_wide_red_image_as_ndarray = np.copy(monochrome_wide_red_image_as_ndarray)
new_monochrome_wide_red_image_as_ndarray[lower_border:upper_border, left_border:right_border] = center_square_region_of_red_monochrome_image

pdf.save_and_add_title_and_image_to_pdf(new_monochrome_wide_red_image_as_ndarray, 'ps0-3-a-1.png', 'L', '3.a.')

#Arithmetic and geometric operations:
pdf.cell(10, 10, '4.a.')
max_pixel_value_of_img1_green = np.amax(monochrome_wide_green_image_as_ndarray)
pdf.cell(100, 10, f'Max pixel value of img1 green is: {max_pixel_value_of_img1_green}', ln=True)
mean_pixel_value_of_img1_green = np.mean(monochrome_wide_green_image_as_ndarray)
pdf.cell(100, 10, f'Mean pixel value of img1 green is: {mean_pixel_value_of_img1_green}', ln=True)
std_value_of_img1_green = np.std(monochrome_wide_green_image_as_ndarray)
pdf.cell(100, 10, f'Std value of img1 green is: {std_value_of_img1_green}', ln=True)

normalized_wide_green_image_as_ndarray = np.copy(monochrome_wide_green_image_as_ndarray)
normalized_wide_green_image_as_ndarray -= int(mean_pixel_value_of_img1_green)
normalized_wide_green_image_as_ndarray = normalized_wide_green_image_as_ndarray / std_value_of_img1_green
normalized_wide_green_image_as_ndarray *= 10
normalized_wide_green_image_as_ndarray += int(mean_pixel_value_of_img1_green)
pdf.save_and_add_title_and_image_to_pdf(normalized_wide_green_image_as_ndarray, 'ps0-4-b-1.png', 'L', '4.b.')

#Shifted_green_image_as_ndarray = np.copy(monochrome_wide_green_image_as_ndarray)
shifted_green_image_as_ndarray = np.zeros((monochrome_wide_green_image_as_ndarray.shape[0], monochrome_wide_green_image_as_ndarray.shape[1]), dtype=np.uint8)
shifted_green_image_as_ndarray[:, :-2] = monochrome_wide_green_image_as_ndarray[:, 2:]
pdf.save_and_add_title_and_image_to_pdf(shifted_green_image_as_ndarray, 'ps0-4-c-1.png', 'L', '4.c.')

#Substract shifted version of green img from the original
substracted_image_as_ndarray = monochrome_wide_green_image_as_ndarray - shifted_green_image_as_ndarray
pdf.save_and_add_title_and_image_to_pdf(substracted_image_as_ndarray, 'ps0-4-d-1.png', 'L', '4.d.')
pdf.cell(100, 10, 'Negative values become 0.', ln=True)

#Noise
noise = np.random.normal(loc=0, scale=25, size=resized_wide_image_as_ndarray.shape[:2])

image_green_channel_with_noise_as_ndarray = np.clip(resized_wide_image_as_ndarray[:, :, 1] + noise, 0, 255).astype(np.uint8)
image_with_noise_on_green_channel_as_ndarray = np.copy(resized_wide_image_as_ndarray)
image_with_noise_on_green_channel_as_ndarray[:, :, 1] = image_green_channel_with_noise_as_ndarray
image_with_noise_on_green_channel = Image.fromarray(image_with_noise_on_green_channel_as_ndarray, 'RGB')
pdf.save_and_add_title_and_image_to_pdf(image_with_noise_on_green_channel, 'ps0-5-a-1.png', 'RGB', '5.a.')
pdf.cell(100, 10, "I had to use sigma=25", ln=True)

image_blue_channel_with_noise_as_ndarray = np.clip(resized_wide_image_as_ndarray[:, :, 2] + noise, 0, 255).astype(np.uint8)
image_with_noise_on_blue_channel_as_ndarray = np.copy(resized_wide_image_as_ndarray)
image_with_noise_on_blue_channel_as_ndarray[:, :, 2] = image_blue_channel_with_noise_as_ndarray
image_with_noise_on_blue_channel = Image.fromarray(image_with_noise_on_blue_channel_as_ndarray, 'RGB')
pdf.save_and_add_title_and_image_to_pdf(image_with_noise_on_blue_channel, 'ps0-5-b-1.png', 'RGB', '5.b.')
pdf.cell(150, 30, "5.c. The human eye is less sensitive to changes in the blue channel.")



pdf.output('ps0_report.pdf')











