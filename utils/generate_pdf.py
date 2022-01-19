import os

from fpdf import FPDF


class PdfReport:
    def __init__(self, filename: str, guesses: list) -> None:
        self.filename = filename
        self.guesses = guesses

    def generate(self):
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
