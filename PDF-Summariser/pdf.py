from tkinter import messagebox
import os
import tkinter as tk
from tkinter import filedialog
from pypdf import PdfReader
from tkinter import simpledialog
from PyPDF2 import PdfFileReader
from config_ocr import OcrConfig
import ocrmypdf
import requests
import aspose.pdf as ap

#https://docs.python.org/3/library/tkinter.messagebox.html
#https://github.com/py-pdf/pypdf
#https://pdfreader.readthedocs.io/en/latest/tutorial.html
#https://courspython.com/classes-et-objets.html
#https://datacorner.fr/pdf/
#https://jonathansoma.com/everything/pdfs/ocr-tools/
#https://ocr.space/ocrapi 
#https://www.docstring.fr/formations/faq/fichiers/comment-manipuler-des-fichiers-json-en-python/
#https://docs.aspose.com/pdf/python-net/optimize-pdf/#reduce-size-pdf

class PdfFile():

    # Open the file explorateur to choose a PDF file
    @staticmethod
    def select_pdf_file():
        pdf_file = filedialog.askopenfilename(initialdir = "/", title = "Select file", filetypes = (("pdf files", "*.pdf"), ("all files", "*.*")))
        return pdf_file
    
    # Convert the pdfile in txt file with an OCR
    @staticmethod
    def convert_ocr_text(pdf_file, language):
        # Get the api key from the json file (config_ocr.json)
        print("Function ocr to text")
        api_key = OcrConfig("config_ocr.json").get_default_key
        print(api_key)

        try:
            # Open document
            document = ap.Document(pdf_file)
            # Optimize PDF document. Note, though, that this method cannot guarantee document shrinking
            document.optimize_resources()
            # Initialize OptimizationOptions
            optimizeOptions = ap.optimization.OptimizationOptions()
            # Set CompressImages option
            optimizeOptions.image_compression_options.compress_images = True
            # Set ImageQuality option
            optimizeOptions.image_compression_options.image_quality = 50
            # Optimize PDF document using OptimizationOptions
            document.optimize_resources(optimizeOptions)
            # Save updated document
            document.save(pdf_file)


            payload = {'isOverlayRequired': False,
                    'apikey': 'helloworld',
                    'language': language,
                    }
            with open(pdf_file, 'rb') as f:
                r = requests.post('https://api.ocr.space/parse/image',
                                files={pdf_file: f},
                                data=payload,
                                )
            r.content.decode()
            print(r.json)

            if r.content.decode() == 'The API key is invalid':
                renderer = ChromePdfRenderer()
                pdf_file = renderer.RenderUrlAsPdf(pdf_file)
                
                payload = {'isOverlayRequired': False,
                    'apikey': 'helloworld',
                    'language': language,
                    }
                with open(pdf_file, 'rb') as f:
                    r = requests.post('https://api.ocr.space/parse/image',
                                files={pdf_file: f},
                                data=payload,
                                )
                return r.content.decode()
            else:
                return r.content.decode()
            
        except Exception as e:
            print(f"Erreur : {e}")
        

    # Convert the pdf file in txt file
    @staticmethod
    def convert_pdf_text(pdf_file, langague):
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
                document = PdfFile.convert_ocr_text(pdf_file, langague)
                print(f"OCR terminé ! Le texte du pdf contient : \n {document}")
            except Exception as e:
                print(f"Erreur lors de l'OCR : {e}")

        return document
    
    @staticmethod
    def max_word():
        tk.messagebox.showwarning(title="Infos", message="Les fichiers doivent contenir un maximum de 1400 mots")
        try:
            warning_message = ""
            while False:
                # l'avantage de la fonction askinteger, c'est qu'elle controle directement que le nombre soit un int et évite les mauvaises entrées
                number_max_word = simpledialog.askinteger(title="Nombre de mots", prompt=f"{warning_message}Inserérez le nombre maximum de mots du résumé : ")
                if number_max_word >= 0 and number_max_word <= 1400:   
                    return number_max_word
                else:
                    warning_message += "Entrez un nombre entre 0 et 1400.\n"
                    True
        except ValueError as e:
            print(f"An error occured: {e}. La valeur inséré n'est pas valide.")
            tk.messagebox.showerror(title="Error", message=f"La valeur inséré n'est pas valide.\n{e}"  ) 

