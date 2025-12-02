from ia_client import IAClient
from tkinter import messagebox
import tkinter as tk

class ChatBot(IAClient):
    
    def __init__(self, api_key, ia_model, base_url, language, document, summary):
        super().__init__(api_key, ia_model, base_url, language, document)    
        self.summary = summary

    def receive_context(self, prompt_used):
        if self.summary:
            prompt_used.append({"role": "system", "content": "To get more context, that"
                                " is the summary you have just done :" + self.summary })
            prompt_used.append({"role": "system", "content": "Now the user has entered in"
                                " the chat mode. He might ask you questions about the "
                                "text he sent you (the one that you also summarized). You"
                                " should only answer questions that are linked with the document "
                                "but it might get out of context. No need to rewrite the summary"
                                " or things you've already mentioned, unless it helps to get more context, "
                                f"to answer the user's following question. You have to answer {self.language}" })
            prompt_used.append({"role": "system", "content": f"Your name is SumBot. Answer in {self.language}."})

        context = prompt_used
        
        return context

    def answer(self, client, ia_model, prompt, user_text, text_box):
        text_box.insert(tk.END, "\n SumBot : ")
        
        prompt.append({"role": "user", "content": f"Answer just to this question now :\n {user_text}."})
        # this one is used to answer, not to generate a summary, there are the function to make it happen
        self.generate_summary(client, ia_model, prompt, text_box)