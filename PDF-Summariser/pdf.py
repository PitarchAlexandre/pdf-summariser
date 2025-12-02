from tkinter import messagebox
import os
import tkinter as tk
from tkinter import filedialog
from pypdf import PdfReader
from tkinter import simpledialog
import pytesseract
from pdf2image import convert_from_path
import os
import time
from concurrent.futures import ThreadPoolExecutor
from tkinter import ttk

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
#https://github.com/tesseract-ocr/tesseract/blob/main/doc/tesseract.1.asc#options
#https://tesseract-ocr.github.io/tessdoc/Command-Line-Usage

class PdfFile():

    # Open the file explorateur to choose a PDF file
    @staticmethod
    def select_pdf_file():
        pdf_file = filedialog.askopenfilename(initialdir = "Documents", title = "Sélectionnez un fichier", filetypes = (("pdf files", "*.pdf"), ("all files", "*.*")))
        return pdf_file

    @staticmethod
    def warning_msg_ocr():
        tk.messagebox.showwarning(title="In process", message="Les lectures de fichiers OCR peuvent prendre plus de temps.\n"
                                  + "Votre fichier PDF a probablement été scanné. C'est pour cela que cette opération risque"
                                  + " de prendre du temps.\nLe programme doit convertir les images en texte.")

    @staticmethod
    def convert_ocr_text(pdf_file, language):
        text_data = ''

        time.sleep(1)

        script_dir = os.path.dirname(os.path.abspath(__file__))  
        tesseract_path = os.path.join(script_dir, "Tesseract-OCR", "tesseract.exe")
        poppler_path = os.path.join(script_dir, "poppler-24.08.0", "Library", "bin")

        pytesseract.pytesseract.tesseract_cmd = tesseract_path

        os.environ["PATH"] += os.pathsep + poppler_path  

        # The dpi is on 300dpi by default, but to optimize and make it run faster, it is on 100 dpi
        # The default format is png but to put it in jpeg, it makes it faster.
        pages = convert_from_path(pdf_file, dpi=100, fmt="jpeg", poppler_path=poppler_path)
        text_data = ''

        try:
            # Use multithread to run faster
            with ThreadPoolExecutor(max_workers=4) as executor:
                #https://tesseract-ocr.github.io/tessdoc/Command-Line-Usage
                #https://pyimagesearch.com/2021/11/15/tesseract-page-segmentation-modes-psms-explained-how-to-improve-your-ocr-accuracy/
                ocr_config = '--oem 3 --psm 6'
                # this line is mostly made with chatgpt, it made my code 5 times smaller...
                # Lambda function: for each page in 'pages', apply Tesseract OCR to extract text
                text_data = list(executor.map(lambda page: pytesseract.image_to_string(page, lang=language, config=ocr_config), pages))

            if not text_data:
                tk.messagebox.showerror(title="Error", message="Erreur {text}")
            return text_data
        
        except Exception as e:
            tk.messagebox.showerror(title="Error", message=f"Erreur {e}")
            print(f"Erreur : {e}")

    # Convert the pdfile in txt file with an OCR
    @staticmethod
    def get_ocr_text(pdf_file, language):
        
        progressbar = ttk.Progressbar(mode="indeterminate")
        progressbar.place(x=30, y=60, width=200)
        # Start moving the indeterminate progress bar.
        progressbar.start(5)
        
        PdfFile.warning_msg_ocr()
        
        with ThreadPoolExecutor() as executor:
            future = executor.submit(PdfFile.convert_ocr_text, pdf_file, language)
            result = future.result()
        
        progressbar.after(3000, progressbar.destroy)
        
        return result
        
        
    # Convert the pdf file in txt file
    @staticmethod
    def convert_pdf_text(pdf_file, language):
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
                document = PdfFile.get_ocr_text(pdf_file,language)
                print(f"L'OCR terminé. \n")
                if document == None:
                    tk.messagebox.showerror(title="Error", message="Le document est vide. Il y a probablement eu une erreur.")
                    print("Le document est vide. Il y a probablement eu une erreur.")
                else:
                    print(f"Le texte du pdf a été chargé.")
            except Exception as e:
                print(f"Erreur lors de l'OCR : {e}")
                tk.messagebox.showerror(title="Error", message=f"Erreur lors de l'OCR : {e}")
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

