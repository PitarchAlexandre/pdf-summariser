from tkinter import messagebox
import os
import tkinter as tk
from tkinter import filedialog
from pypdf import PdfReader
from tkinter import simpledialog
import pytesseract
from pdf2image import convert_from_path
import os

#https://docs.python.org/3/library/tkinter.messagebox.html
#https://github.com/py-pdf/pypdf
#https://pdfreader.readthedocs.io/en/latest/tutorial.html
#https://courspython.com/classes-et-objets.html
#https://datacorner.fr/pdf/
#https://jonathansoma.com/everything/pdfs/ocr-tools/
#https://ocr.space/ocrapi 
#https://www.docstring.fr/formations/faq/fichiers/comment-manipuler-des-fichiers-json-en-python/
#https://docs.aspose.com/pdf/python-net/optimize-pdf/#reduce-size-pdf
#https://vitalflux.com/python-tesseract-pdf-ocr-example/
#https://stackoverflow.com/questions/50951955/pytesseract-tesseractnotfound-error-tesseract-is-not-installed-or-its-not-i
#https://github.com/oschwartz10612/poppler-windows/releases/tag/v24.08.0-0

class PdfFile():

    # Open the file explorateur to choose a PDF file
    @staticmethod
    def select_pdf_file():
        pdf_file = filedialog.askopenfilename(initialdir = "/", title = "Select file", filetypes = (("pdf files", "*.pdf"), ("all files", "*.*")))
        return pdf_file
    
    # Convert the pdfile in txt file with an OCR
    @staticmethod
    def convert_ocr_text(pdf_file):
        # Get the api key from the json file (config_ocr.json)
        print("Function ocr to text")
        
        script_dir = os.path.dirname(os.path.abspath(__file__))  
        tesseract_path = os.path.join(script_dir, "Tesseract-OCR", "tesseract.exe")
        poppler_path = os.path.join(script_dir, "poppler-24.08.0", "Library", "bin")

        pytesseract.pytesseract.tesseract_cmd = tesseract_path

        os.environ["PATH"] += os.pathsep + poppler_path  

        pages = convert_from_path(pdf_file, poppler_path=poppler_path)
        text_data = ''

        try:
            for page in pages:
               text = pytesseract.image_to_string(page)
               text_data += text + '\n'
            print(text_data)
            return text_data
        
        except Exception as e:
            print(f"Erreur : {e}")
        
    # Convert the pdf file in txt file
    @staticmethod
    def convert_pdf_text(pdf_file):
        if not pdf_file:
            raise ValueError("Aucun fichier PDF selectionnné.")
        reader = PdfReader(pdf_file)
        page = reader.pages
        document = ""
        for p in page:
            text = p.extract_text()
            document+=text
        
        # If the document is empty, the pdf is readen with an OCR reader 
        if document == "":
            try:
                # in pyhton, you have to write the class name + the function to call a function into the fucntion
                document = PdfFile.convert_ocr_text(pdf_file)
                print(f"L'OCR terminé. \n")
                if document == None:
                    print("Le document est vide. Il y a probablement eu une erreur.")
                else:
                    print(f"Le texte du pdf contient : \n {document}")
            except Exception as e:
                print(f"Erreur lors de l'OCR : {e}")

        return document
    
    @staticmethod
    def max_word():
        tk.messagebox.showwarning(title="Infos", message="Les fichiers doivent contenir un maximum de 1400 mots")
        try:
            warning_message = ""
            while True:
                # l'avantage de la fonction askinteger, c'est qu'elle controle directement que le nombre soit un int et évite les mauvaises entrées
                number_max_word = simpledialog.askinteger(title="Nombre de mots", prompt=f"{warning_message}Inserérez le nombre maximum de mots du résumé : ")
                if number_max_word >= 0 and number_max_word <= 1400:   
                    return number_max_word
                else:
                    warning_message = "Entrez un nombre entre 0 et 1400.\n"
                    True
        except ValueError as e:
            print(f"An error occured: {e}. La valeur inséré n'est pas valide.")
            tk.messagebox.showerror(title="Error", message=f"La valeur inséré n'est pas valide.\n{e}"  ) 

