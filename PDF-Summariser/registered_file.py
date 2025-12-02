from tkinter import filedialog, messagebox 

class DocFile():

    def __init__(self, file_name, summary):
        self.file_name = file_name
        self.text = summary
        
    def create_file(self):

        if self.text == None:
            messagebox.showerror(title="Error", message="Erreur : \n  Aucun texte n'a été selectionné.")

        file = filedialog.asksaveasfile(master=None,
                                 mode="w", 
                                 title="Enregister résumé", 
                                 initialdir="Document",
                                 initialfile=f"resume_{self.file_name}.txt",
                                 filetypes=(("All Files", "*.*"), ("Document Files", "*.doc"), ("Text Files", "*.txt")), 
                                 defaultextension=".doc")
        try:
            if file:
                file.write(self.text)
                file.close()

        except Exception as e:
            messagebox.showerror(title="Error", message=f"Erreur {e}")
            print(f"Erreur : {e}")