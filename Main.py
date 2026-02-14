import tkinter as tk
from tkinter import ttk, messagebox
from base_donnees import (
    creer_tables,
    lister_ventes, ajouter_vente, modifier_vente, supprimer_vente,
    lister_depenses, ajouter_depense, modifier_depense, supprimer_depense,
    total_ventes, total_frais_livraison, total_depenses
)
from formulaire import FormulaireVente, FormulaireDepense


class GestionApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Gestion des ventes et dépenses")
        self.geometry("1400x700")

        # Déclaration des attributs utilisés plus tard
        self.recherche_ventes = None
        self.recherche_depenses = None
        self.tree_ventes = None
        self.tree_depenses = None
        self.label_ventes = None
        self.label_frais = None
        self.label_depenses = None
        self.label_net = None

        notebook = ttk.Notebook(self)
        notebook.pack(fill=tk.BOTH, expand=True)

        self.onglet_ventes = tk.Frame(notebook)
        self.onglet_depenses = tk.Frame(notebook)
        self.onglet_bilan = tk.Frame(notebook)

        notebook.add(self.onglet_ventes, text="Ventes")
        notebook.add(self.onglet_depenses, text="Dépenses")
        notebook.add(self.onglet_bilan, text="Bilan")

        self.creer_interface_ventes()
        self.creer_interface_depenses()
        self.creer_interface_bilan()

    # =========================
    # Onglet Ventes
    # =========================
    def creer_interface_ventes(self):
        frame_recherche = tk.Frame(self.onglet_ventes)
        frame_recherche.pack(fill=tk.X, pady=5)

        tk.Label(frame_recherche, text="Recherche :").pack(side=tk.LEFT, padx=5)
        self.recherche_ventes = tk.StringVar()
        tk.Entry(frame_recherche, textvariable=self.recherche_ventes, width=50).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_recherche, text="Filtrer", command=self.filtrer_ventes).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_recherche, text="Réinitialiser", command=self.charger_ventes).pack(side=tk.LEFT, padx=5)

        colonnes = ("id", "Client", "Adresse", "Prix", "Livraison", "Tracking", "Date_vente",
                    "Date_envoi", "Paiement", "Commentaire")

        frame_tree_ventes = tk.Frame(self.onglet_ventes)
        frame_tree_ventes.pack(fill=tk.BOTH, expand=True)

        self.tree_ventes = ttk.Treeview(frame_tree_ventes, columns=colonnes, show="headings")
        scrollbar_ventes = ttk.Scrollbar(frame_tree_ventes, orient="vertical", command=self.tree_ventes.yview)
        self.tree_ventes.configure(yscrollcommand=scrollbar_ventes.set)

        self.tree_ventes.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar_ventes.pack(side=tk.RIGHT, fill=tk.Y)

        # Double-clic pour modifier
        self.tree_ventes.bind("<Double-1>", self.on_double_click_vente)

        largeurs = {
            "id": 40,
            "Client": 150,
            "Adresse": 250,
            "Prix": 80,
            "Livraison": 100,
            "Tracking": 150,
            "Date_vente": 100,
            "Date_envoi": 100,
            "Paiement": 200,
            "Commentaire": 300
        }

        for col in colonnes:
            self.tree_ventes.heading(col, text=col, command=lambda c=col: self.trier_tree(self.tree_ventes, c, False))
            self.tree_ventes.column(col, width=largeurs.get(col, 100))

        frame_btn = tk.Frame(self.onglet_ventes)
        frame_btn.pack(pady=10)

        tk.Button(frame_btn, text="Ajouter", command=self.ajouter_vente_popup, width=15).grid(row=0, column=0, padx=5)
        tk.Button(frame_btn, text="Modifier", command=self.modifier_vente_popup, width=15).grid(row=0, column=1, padx=5)
        tk.Button(frame_btn, text="Supprimer", command=self.supprimer_vente, width=15).grid(row=0, column=2, padx=5)
        tk.Button(frame_btn, text="Rafraîchir", command=self.charger_ventes, width=15).grid(row=0, column=3, padx=5)

        self.charger_ventes()

    def charger_ventes(self):
        for row in self.tree_ventes.get_children():
            self.tree_ventes.delete(row)
        for vente in lister_ventes():
            commentaire_affiche = vente[9].replace("\n", " ") if vente[9] else ""
            self.tree_ventes.insert("", tk.END, values=vente[:9] + (commentaire_affiche,))

    def filtrer_ventes(self):
        filtre = self.recherche_ventes.get().strip()
        for row in self.tree_ventes.get_children():
            self.tree_ventes.delete(row)
        for vente in lister_ventes(filtre):
            commentaire_affiche = vente[9].replace("\n", " ") if vente[9] else ""
            self.tree_ventes.insert("", tk.END, values=vente[:9] + (commentaire_affiche,))

    def ajouter_vente_popup(self):
        FormulaireVente(self, "Ajouter une vente", self.ajouter_vente_cb)

    def ajouter_vente_cb(self, data):
        ajouter_vente(*data)
        self.charger_ventes()

    def modifier_vente_popup(self):
        selected = self.tree_ventes.selection()
        if not selected:
            messagebox.showwarning("Attention", "Sélectionne une vente à modifier.")
            return
        values = self.tree_ventes.item(selected[0], "values")
        FormulaireVente(self, "Modifier la vente", self.modifier_vente_cb, values)

    def modifier_vente_cb(self, data, vente_id):
        modifier_vente(vente_id, *data)
        self.charger_ventes()

    def supprimer_vente(self):
        selected = self.tree_ventes.selection()
        if not selected:
            messagebox.showwarning("Attention", "Sélectionne une vente à supprimer.")
            return
        vente_id = self.tree_ventes.item(selected[0], "values")[0]
        supprimer_vente(vente_id)
        self.charger_ventes()

    def on_double_click_vente(self, event):
        item_id = self.tree_ventes.identify_row(event.y)
        if not item_id:
            return
        self.tree_ventes.selection_set(item_id)
        values = self.tree_ventes.item(item_id, "values")
        FormulaireVente(self, "Modifier la vente", self.modifier_vente_cb, values)

    # =========================
    # Onglet Dépenses
    # =========================
    def creer_interface_depenses(self):
        frame_recherche = tk.Frame(self.onglet_depenses)
        frame_recherche.pack(fill=tk.X, pady=5)

        tk.Label(frame_recherche, text="Recherche :").pack(side=tk.LEFT, padx=5)
        self.recherche_depenses = tk.StringVar()
        tk.Entry(frame_recherche, textvariable=self.recherche_depenses, width=50).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_recherche, text="Filtrer", command=self.filtrer_depenses).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_recherche, text="Réinitialiser", command=self.charger_depenses).pack(side=tk.LEFT, padx=5)

        colonnes = ("id", "Description", "Categorie", "Montant", "Date_depense", "Commentaire")

        frame_tree_depenses = tk.Frame(self.onglet_depenses)
        frame_tree_depenses.pack(fill=tk.BOTH, expand=True)

        self.tree_depenses = ttk.Treeview(frame_tree_depenses, columns=colonnes, show="headings")
        scrollbar_depenses = ttk.Scrollbar(frame_tree_depenses, orient="vertical", command=self.tree_depenses.yview)
        self.tree_depenses.configure(yscrollcommand=scrollbar_depenses.set)

        self.tree_depenses.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar_depenses.pack(side=tk.RIGHT, fill=tk.Y)

        # Double-clic pour modifier
        self.tree_depenses.bind("<Double-1>", self.on_double_click_depense)

        largeurs = {
            "id": 40,
            "Description": 250,
            "Categorie": 150,
            "Montant": 80,
            "Date_depense": 120,
            "Commentaire": 250
        }

        for col in colonnes:
            self.tree_depenses.heading(col, text=col,
                                       command=lambda c=col: self.trier_tree(self.tree_depenses, c, False))
            self.tree_depenses.column(col, width=largeurs.get(col, 100))

        frame_btn = tk.Frame(self.onglet_depenses)
        frame_btn.pack(pady=10)

        tk.Button(frame_btn, text="Ajouter", command=self.ajouter_depense_popup, width=15).grid(row=0, column=0, padx=5)
        tk.Button(frame_btn, text="Modifier", command=self.modifier_depense_popup, width=15).grid(row=0, column=1,
                                                                                                  padx=5)
        tk.Button(frame_btn, text="Supprimer", command=self.supprimer_depense, width=15).grid(row=0, column=2, padx=5)
        tk.Button(frame_btn, text="Rafraîchir", command=self.charger_depenses, width=15).grid(row=0, column=3, padx=5)

        self.charger_depenses()

    def charger_depenses(self):
        for row in self.tree_depenses.get_children():
            self.tree_depenses.delete(row)
        for depense in lister_depenses():
            self.tree_depenses.insert("", tk.END, values=depense)

    def filtrer_depenses(self):
        filtre = self.recherche_depenses.get().strip()
        for row in self.tree_depenses.get_children():
            self.tree_depenses.delete(row)
        for depense in lister_depenses(filtre):
            self.tree_depenses.insert("", tk.END, values=depense)

    def ajouter_depense_popup(self):
        FormulaireDepense(self, "Ajouter une dépense", self.ajouter_depense_cb)

    def ajouter_depense_cb(self, data):
        ajouter_depense(*data)
        self.charger_depenses()

    def modifier_depense_popup(self):
        selected = self.tree_depenses.selection()
        if not selected:
            messagebox.showwarning("Attention", "Sélectionne une dépense à modifier.")
            return
        values = self.tree_depenses.item(selected[0], "values")
        FormulaireDepense(self, "Modifier la dépense", self.modifier_depense_cb, values)

    def modifier_depense_cb(self, data, depense_id):
        modifier_depense(depense_id, *data)
        self.charger_depenses()

    def supprimer_depense(self):
        selected = self.tree_depenses.selection()
        if not selected:
            messagebox.showwarning("Attention", "Sélectionne une dépense à supprimer.")
            return
        depense_id = self.tree_depenses.item(selected[0], "values")[0]
        supprimer_depense(depense_id)
        self.charger_depenses()

    def on_double_click_depense(self, event):
        item_id = self.tree_depenses.identify_row(event.y)
        if not item_id:
            return
        self.tree_depenses.selection_set(item_id)
        values = self.tree_depenses.item(item_id, "values")
        FormulaireDepense(self, "Modifier la dépense", self.modifier_depense_cb, values)

    # =========================
    # Onglet Bilan
    # =========================
    def creer_interface_bilan(self):
        frame_bilan = tk.Frame(self.onglet_bilan)
        frame_bilan.pack(pady=30)

        self.label_ventes = tk.Label(frame_bilan, text="", font=("Arial", 14))
        self.label_ventes.grid(row=0, column=0, pady=10, sticky="w")

        self.label_frais = tk.Label(frame_bilan, text="", font=("Arial", 14))
        self.label_frais.grid(row=1, column=0, pady=10, sticky="w")

        self.label_depenses = tk.Label(frame_bilan, text="", font=("Arial", 14))
        self.label_depenses.grid(row=2, column=0, pady=10, sticky="w")

        self.label_net = tk.Label(frame_bilan, text="", font=("Arial", 16, "bold"))
        self.label_net.grid(row=3, column=0, pady=20, sticky="w")

        tk.Button(frame_bilan, text="Rafraîchir bilan", command=self.afficher_bilan, width=20).grid(row=4, column=0,
                                                                                                    pady=20)

        self.afficher_bilan()

    def afficher_bilan(self):
        ventes = total_ventes()
        frais = total_frais_livraison()
        depenses = total_depenses()
        net = ventes - (frais + depenses)

        self.label_ventes.config(text=f"Total ventes : {ventes:,.2f} $")
        self.label_frais.config(text=f"Total frais de livraison : {frais:,.2f} $")
        self.label_depenses.config(text=f"Total dépenses : {depenses:,.2f} $")
        self.label_net.config(text=f"Résultat net : {net:,.2f} $")

    # =========================
    # Fonction de tri
    # =========================
    def trier_tree(self, tree, col, reverse):
        data = [(tree.set(k, col), k) for k in tree.get_children("")]
        try:
            data.sort(key=lambda t: float(t[0]), reverse=reverse)
        except ValueError:
            data.sort(key=lambda t: t[0], reverse=reverse)

        for index, (val, k) in enumerate(data):
            tree.move(k, "", index)

        tree.heading(col, command=lambda: self.trier_tree(tree, col, not reverse))


if __name__ == "__main__":
    creer_tables()
    app = GestionApp()
    app.mainloop()
