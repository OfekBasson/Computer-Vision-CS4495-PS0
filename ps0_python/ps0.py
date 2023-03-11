from io import BytesIO
from PIL import Image
import numpy as np
import requests
from fpdf import FPDF
import os

#Preparing PDF
pdf = FPDF()
pdf.add_page()
pdf.set_font('helvetica', '', 16)

#Saving wide image
first_response = requests.get('https://img.mako.co.il/2023/03/06/ANGRY_BIBI_LEVIN_1502_re_autoOrient_x6.jpg')
wide_img = Image.open(BytesIO(first_response.content))
new_wide_image_size = (512, 288)
resized_wide_img = wide_img.resize(new_wide_image_size)
resized_wide_img.save('output/ps0-1-a-1.png')

#Saving tall image
second_response = requests.get('https://images.pexels.com/photos/699466/pexels-photo-699466.jpeg?auto=compress&cs=tinysrgb&w=1600')
tall_img = Image.open(BytesIO(second_response.content))
new_tall_image_size = (384, 512)
resized_tall_img = tall_img.resize(new_tall_image_size)
resized_tall_img.save('output/ps0-1-a-2.png')

#Swapping red and blue
resized_wide_image_as_ndarray = np.asarray(resized_wide_img)
swapped_blue_red_resized_wide_image_as_ndarray = resized_wide_image_as_ndarray[:,:,[2,1,0]]
swapped_blue_red_resized_wide_image = Image.fromarray(swapped_blue_red_resized_wide_image_as_ndarray, 'RGB')
swapped_blue_red_resized_wide_image.save('output/ps0-2-a-1.png')

#Monochrome image - only green
wide_image_as_ndarray = np.asarray(resized_wide_img)
monochrome_wide_green_image_as_ndarray = wide_image_as_ndarray[:,:,1]
monochrome_wide_image = Image.fromarray(monochrome_wide_green_image_as_ndarray, 'L')
monochrome_wide_image.save('output/ps0-2-b-1.png')

#Monochrome image - only red
wide_image_as_ndarray = np.asarray(resized_wide_img)
monochrome_wide_red_image_as_ndarray = wide_image_as_ndarray[:,:,0]
monochrome_wide_image = Image.fromarray(monochrome_wide_red_image_as_ndarray, 'L')
monochrome_wide_image.save('output/ps0-2-c-1.png')

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
new_monochrome_wide_red_image = Image.fromarray(new_monochrome_wide_red_image_as_ndarray)
new_monochrome_wide_red_image.save('output/ps0-3-a-1.png')


#Arithmetic and geometric operations:
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
normalized_wide_green_image = Image.fromarray(normalized_wide_green_image_as_ndarray, 'L')
normalized_wide_green_image.save('output/ps0-4-b-1.png')



#Adding images to pdf
directory = 'output'
for filename in reversed(os.listdir(directory)):
    potential_file = os.path.join(directory, filename)
    if os.path.isfile(potential_file):
        pdf.cell(50, 10, filename, ln=True)
        pdf.image(potential_file, w=105)

pdf.output('ps0_report.pdf')











