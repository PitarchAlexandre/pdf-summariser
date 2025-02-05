from openai import OpenAI
from tkinter import messagebox
import tkinter as tk
#https://platform.openai.com/docs/api-reference/introduction
#https://platform.openai.com/docs/overview
#https://github.com/openai/openai-python
#https://ollama.com/

class IAClient:
    def __init__(self, api_key, base_url, language):
        self.api_key = api_key
        self.base_url = base_url
        self.language = language

    def create_bot(self):
        """Initialise le client OpenAI avec les informations d'API."""
        try:
            client = OpenAI(
                base_url=self.base_url,
                api_key=self.api_key
            )
            return client
        except Exception as e:
            raise ValueError(f"Erreur lors de l'initialisation du client OpenAI : {e}")
    
    def parameter_prompt(self, number_max_word, document, language):
        try:
            if number_max_word > 0:
                number_word = f" en maximum {number_max_word} mots "
            else:
                number_word=""
            prompt=[        
                        {"role": "system", "content": f"""You are a bot which translate texts. You receive texts. Your sole aim is to make summaries. 
                                                        These summaries should help you understand the text."You receive texts that were previously in PDF files,
                                                        but have now been converted into text files. If there are chapters, you don't have to name them one by one,
                                                        but summarize the whole text. You must not give your opinion or interpret in your own way.
                                                        You have to start your sentence by "Here is a word summary in {number_word} words" in {language}.
                                                        You must not exceed the word count. Do not write more than {number_word}""" },
                        {"role": "user", "content": f"Summarize the following text in maximum {number_word} words. :\n{document}." }
            ]
            return prompt
        except Exception as e:
            ValueError(f"Erreur de l'initianlisation du prompt : {e}")

    def generate_summary(self, client, ia_model, prompt, text_box):
        stream = client.chat.completions.create(
                    model=ia_model,
                    messages=prompt,
                    temperature=0,
                    #max_tokens=1000,
                    stream=True,
        )
        summary = ''
        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                text_part = chunk.choices[0].delta.content
                # Add text into the textbox
                text_box.insert(tk.END, text_part)
                # Refresh the textbox 
                text_box.update()
                summary += text_part
                
        if not summary:
            messagebox.showerror("Error", "L'application n'a pas pu traiter de document.")
            return None
        else:
           return summary




