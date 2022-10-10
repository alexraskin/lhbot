import os

from fpdf import FPDF


class PdfReport:
    def __init__(self, filename: str, guesses: list) -> None:
        """
        Create a new PdfReport object.
        :param filename:str: Used to store the name of the file that is being read.
        :param guesses:list: Used to store the guesses pulled from the database.
        """
        self.filename = filename
        self.guesses = guesses

    def generate(self) -> FPDF:
        """
        The generate function creates a PDF file with the guesses from the database.

        :param self: Used to access the class attributes.
        :return: the pdf object.
        """
        pdf = FPDF(orientation="P", unit="pt", format="A4")
        pdf.add_page()
        pdf.set_font(family="Times", size=25, style="B")
        pdf.cell(w=0, h=80, txt="LhGuess Report", border=0, align="C", ln=1)

        pdf.set_font(family="Times", size=12)
        for guess in self.guesses:
            guess = guess["guess"].encode("latin-1", "replace").decode("latin-1")
            pdf.multi_cell(w=100, h=20, txt=guess, border=0, align="C")
        os.chdir("./bot/files")
        pdf.output(self.filename)
