from fpdf import FPDF
import os
from PIL import Image



class PDF_Organizer(FPDF):
    def __init__(self):
        FPDF.__init__(self)
        self.add_page()
        self.set_font('helvetica', '', 16)

    # Adding images to pdf
    def save_and_add_title_and_image_to_pdf(self, img, filename, mode, section=None):
        file_path = os.path.join('output', filename)
        if type(img) is not Image.Image:
            img = Image.fromarray(img, mode)
        img.save(file_path)
        if section is not None:
            self.cell(10, 10, section, ln=True)
        self.cell(50, 10, filename, ln=True)
        self.image(file_path, w=120)