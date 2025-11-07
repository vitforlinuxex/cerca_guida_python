import tkinter as tk
from tkinter import scrolledtext, messagebox
import sys
import io

"""
genera un programma in python e tkinker che aiuti a fare ricerche nell help interno di python, il campo delle ricerche deve supportare il tasto invio, il pulsante cerca e il tasto per chiudere il programma devono essere a fianco del campo di ricerca, ci deve essere un secondo campo di ricerca per cercare all'interno del testo trovato e ci deve essere l'evidenziazione del testo trovato che deve essere subito visibile
"""  

class HelpSearcher(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Ricerca help interno di Python")
        self.geometry("800x600")

        # Frame principale con campo ricerca + bottoni
        top_frame = tk.Frame(self)
        top_frame.pack(padx=10, pady=10, fill=tk.X)

        # Campo principale ricerca help interno con bind Invio
        self.entry_help = tk.Entry(top_frame, width=50)
        self.entry_help.pack(side=tk.LEFT, padx=(0,5))
        self.entry_help.bind("<Return>", self.cerca_help)

        # Pulsante Cerca
        btn_cerca = tk.Button(top_frame, text="Cerca", command=self.cerca_help)
        btn_cerca.pack(side=tk.LEFT, padx=(0,5))

        # Pulsante Chiudi
        btn_chiudi = tk.Button(top_frame, text="Chiudi", command=self.destroy)
        btn_chiudi.pack(side=tk.LEFT)

        # Frame per campo ricerca nel testo risultato
        search_frame = tk.Frame(self)
        search_frame.pack(padx=10, pady=(0,10), fill=tk.X)

        tk.Label(search_frame, text="Cerca nel testo:").pack(side=tk.LEFT)

        self.entry_interno = tk.Entry(search_frame, width=40)
        self.entry_interno.pack(side=tk.LEFT, padx=(5,5))
        self.entry_interno.bind("<KeyRelease>", self.evidenzia_testo)

        # Area testo scrollabile per mostrare l'help
        self.text_area = scrolledtext.ScrolledText(self, wrap=tk.WORD, state=tk.DISABLED, font=("Consolas", 11))
        self.text_area.pack(expand=True, fill=tk.BOTH, padx=10, pady=5)

        # Tag per evidenziazione
        self.text_area.tag_configure("evidenzia", background="yellow")

    def cerca_help(self, event=None):
        termine = self.entry_help.get().strip()
        if not termine:
            messagebox.showwarning("Attenzione", "Inserisci un termine da cercare.")
            return

        # Reindirizzo stdout/stderr su un buffer per catturare output di help()
        buffer = io.StringIO()
        sys.stdout = buffer
        sys.stderr = buffer
        try:
            help(termine)
        except Exception as e:
            messagebox.showerror("Errore", f"Errore nella ricerca: {e}")
            sys.stdout = sys.__stdout__
            sys.stderr = sys.__stderr__
            return
        finally:
            sys.stdout = sys.__stdout__
            sys.stderr = sys.__stderr__

        risultato = buffer.getvalue()
        buffer.close()

        self.text_area.config(state=tk.NORMAL)
        self.text_area.delete(1.0, tk.END)
        self.text_area.insert(tk.END, risultato)
        self.text_area.config(state=tk.DISABLED)

        # Pulisce il campo ricerca interna e togli evidenziazioni precedenti
        self.entry_interno.delete(0, tk.END)
        self.rimuovi_evidenziazione()

    def evidenzia_testo(self, event=None):
        self.rimuovi_evidenziazione()

        ricerca = self.entry_interno.get().strip()
        if not ricerca:
            return

        testo = self.text_area.get(1.0, tk.END).lower()
        ricerca_lower = ricerca.lower()

        start = 0
        first_match_pos = None
        while True:
            start = testo.find(ricerca_lower, start)
            if start == -1:
                break
            start_idx = f"1.0 + {start} chars"
            end_idx = f"1.0 + {start + len(ricerca)} chars"
            self.text_area.tag_add("evidenzia", start_idx, end_idx)
            if first_match_pos is None:
                first_match_pos = start_idx
            start += len(ricerca)

        if first_match_pos:
            # Scrolla per portare subito in vista la prima occorrenza
            self.text_area.see(first_match_pos)

    def rimuovi_evidenziazione(self):
        self.text_area.tag_remove("evidenzia", "1.0", tk.END)

if __name__ == "__main__":
    app = HelpSearcher()
    app.mainloop()
