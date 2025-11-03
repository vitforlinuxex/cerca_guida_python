import tkinter as tk
from tkinter import ttk, messagebox
import pydoc

class PythonDocViewer(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Python Guide Viewer")
        self.geometry("800x600")

        # Barra di ricerca
        frame_search = ttk.Frame(self)
        frame_search.pack(fill=tk.X, padx=10, pady=5)

        ttk.Label(frame_search, text="Cerca modulo/funzione/oggetto:").pack(side=tk.LEFT, padx=(0,5))

        self.search_var = tk.StringVar()
        self.entry_search = ttk.Entry(frame_search, textvariable=self.search_var)
        self.entry_search.pack(side=tk.LEFT, fill=tk.X, expand=True)

        self.button_search = ttk.Button(frame_search, text="Cerca", command=self.show_doc)
        self.button_search.pack(side=tk.LEFT, padx=5)

        # Area di testo per mostrare la documentazione
        self.text = tk.Text(self, wrap=tk.WORD)
        self.text.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Scrollbar verticale
        scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.text.config(yscrollcommand=scrollbar.set)

    def show_doc(self):
        query = self.search_var.get().strip()
        if not query:
            messagebox.showwarning("Attenzione", "Inserisci il nome di un modulo, funzione o oggetto.")
            return

        try:
            # Ottengo la documentazione tramite pydoc
            doc = pydoc.render_doc(query)
            # Alternativa più semplice: pydoc.plain(pydoc.render_doc(query))
            doc_plain = pydoc.plain(pydoc.render_doc(query))
        except ImportError:
            doc_plain = f"Impossibile trovare la documentazione per '{query}'."
        except Exception as e:
            doc_plain = f"Errore durante il recupero documentazione:\n{str(e)}"

        # Mostro la documentazione nell'area di testo
        self.text.delete("1.0", tk.END)
        self.text.insert(tk.END, doc_plain)

if __name__ == "__main__":
    app = PythonDocViewer()
    app.mainloop()