import tkinter as tk
from tkcalendar import DateEntry


class FormulaireVente(tk.Toplevel):
    def __init__(self, parent, titre, callback, values=None):
        super().__init__(parent)
        self.title(titre)
        self.callback = callback
        self.values = values

        labels = [
            "Client", "Adresse", "Prix", "Frais livraison",
            "Tracking", "Date vente", "Date envoi",
            "Paiement", "Commentaire"
        ]

        self.entries = {}
        for i, label in enumerate(labels):
            tk.Label(self, text=label).grid(row=i, column=0, padx=5, pady=5, sticky="w")

            if label in ("Date vente", "Date envoi"):
                entry = DateEntry(self, date_pattern='yyyy-mm-dd')
            elif label == "Commentaire":
                entry = tk.Entry(self, width=50)
            elif label in ("Prix", "Frais livraison"):
                entry = tk.Entry(self)
            else:
                entry = tk.Entry(self, width=40)

            entry.grid(row=i, column=1, padx=5, pady=5, sticky="w")
            self.entries[label] = entry

        # Valeurs par défaut
        if values:
            # Mode modification
            self.vente_id = values[0]
            self.entries["Client"].insert(0, values[1])
            self.entries["Adresse"].insert(0, values[2])
            self.entries["Prix"].insert(0, values[3])
            self.entries["Frais livraison"].insert(0, values[4])
            self.entries["Tracking"].insert(0, values[5])
            self.entries["Date vente"].set_date(values[6])
            self.entries["Date envoi"].set_date(values[7])
            self.entries["Paiement"].insert(0, values[8])
            self.entries["Commentaire"].insert(0, values[9])
            tk.Button(self, text="Enregistrer", command=self.enregistrer_modif).grid(row=len(labels), column=0, columnspan=2, pady=10)
        else:
            # Mode ajout
            self.vente_id = None
            self.entries["Frais livraison"].insert(0, "0")
            tk.Button(self, text="Ajouter", command=self.enregistrer_ajout).grid(row=len(labels), column=0, columnspan=2, pady=10)

    def enregistrer_ajout(self):
        data = [self.entries["Client"].get(),
                self.entries["Adresse"].get(),
                float(self.entries["Prix"].get() or 0),
                float(self.entries["Frais livraison"].get() or 0),
                self.entries["Tracking"].get(),
                self.entries["Date vente"].get(),
                self.entries["Date envoi"].get(),
                self.entries["Paiement"].get(),
                self.entries["Commentaire"].get()]
        self.callback(data)
        self.destroy()

    def enregistrer_modif(self):
        data = [self.entries["Client"].get(),
                self.entries["Adresse"].get(),
                float(self.entries["Prix"].get() or 0),
                float(self.entries["Frais livraison"].get() or 0),
                self.entries["Tracking"].get(),
                self.entries["Date vente"].get(),
                self.entries["Date envoi"].get(),
                self.entries["Paiement"].get(),
                self.entries["Commentaire"].get()]
        self.callback(data, self.vente_id)
        self.destroy()


class FormulaireDepense(tk.Toplevel):
    def __init__(self, parent, titre, callback, values=None):
        super().__init__(parent)
        self.title(titre)
        self.callback = callback
        self.values = values

        labels = [
            "Catégorie", "Montant", "Date dépense", "Commentaire"
        ]

        self.entries = {}
        for i, label in enumerate(labels):
            tk.Label(self, text=label).grid(row=i, column=0, padx=5, pady=5, sticky="w")

            if label == "Date dépense":
                entry = DateEntry(self, date_pattern='yyyy-mm-dd')
            elif label == "Commentaire":
                entry = tk.Entry(self, width=50)
            elif label == "Montant":
                entry = tk.Entry(self)
            else:
                entry = tk.Entry(self, width=40)

            entry.grid(row=i, column=1, padx=5, pady=5, sticky="w")
            self.entries[label] = entry

        # Valeurs par défaut
        if values:
            # Mode modification
            self.depense_id = values[0]
            self.entries["Catégorie"].insert(0, values[1])
            self.entries["Montant"].insert(0, values[2])
            self.entries["Date dépense"].set_date(values[3])
            self.entries["Commentaire"].insert(0, values[4])
            tk.Button(self, text="Enregistrer", command=self.enregistrer_modif).grid(row=len(labels), column=0, columnspan=2, pady=10)
        else:
            # Mode ajout
            self.depense_id = None
            tk.Button(self, text="Ajouter", command=self.enregistrer_ajout).grid(row=len(labels), column=0, columnspan=2, pady=10)

    def enregistrer_ajout(self):
        data = [self.entries["Catégorie"].get(),
                float(self.entries["Montant"].get() or 0),
                self.entries["Date dépense"].get(),
                self.entries["Commentaire"].get()]
        self.callback(data)
        self.destroy()

    def enregistrer_modif(self):
        data = [self.entries["Catégorie"].get(),
                float(self.entries["Montant"].get() or 0),
                self.entries["Date dépense"].get(),
                self.entries["Commentaire"].get()]
        self.callback(data, self.depense_id)
        self.destroy()
