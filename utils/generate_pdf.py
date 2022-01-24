import os

from fpdf import FPDF


class PdfReport:
    def __init__(self, filename: str, guesses: list) -> None:
        """
        The __init__ function is the constructor for a class. It initializes the attributes of an object. In this case, it initializes
        the filename and guesses attributes.

        :param self: Used to refer to the object itself.
        :param filename:str: Used to store the name of the file that is being read.
        :param guesses:list: Used to store the guesses made by the user.
        :return: nothing.

        """
        self.filename = filename
        self.guesses = guesses

    def generate(self):
        """
        The generate function creates a PDF file with the guesses from the user.

        :param self: Used to access the class attributes.
        :return: the pdf object.

        """
        pdf = FPDF(orientation="P", unit="pt", format="A4")
        pdf.add_page()
        pdf.set_font(family="Times", size=25, style="B")
        pdf.cell(w=0, h=80, txt="LhGuess Report", border=0, align="C", ln=1)
        pdf.image("files/lhcloudy.jpeg", w=100, h=100)

        pdf.set_font(family="Times", size=12)
        for guess in self.guesses:
            pdf.multi_cell(w=100, h=20, txt=guess, border=0, align="C")

        os.chdir("files")
        pdf.output(self.filename)
