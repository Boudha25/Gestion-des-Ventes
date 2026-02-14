# 📊 Gestion des Ventes, Dépenses et Bilan

Une application Python avec interface graphique **Tkinter** pour gérer vos ventes, vos dépenses et suivre facilement vos bilans financiers.  
Elle permet d'enregistrer, modifier, supprimer et filtrer des ventes et des dépenses, tout en calculant automatiquement un **bilan net**.

---

## 🚀 Fonctionnalités

### Gestion des ventes
- Ajouter, modifier, supprimer des ventes
- Saisie des informations client, prix, frais de livraison, date, mode de paiement, etc.
- Recherche par mot-clé
- Tri croissant/décroissant par clic sur l'entête de colonne
- Double-clic sur une ligne pour ouvrir directement le formulaire de modification

### Gestion des dépenses
- Ajouter, modifier, supprimer des dépenses
- Catégorisation des dépenses
- Recherche par mot-clé
- Tri par colonne
- Double-clic sur une ligne pour modifier

### Bilan
- Affichage des totaux :
  - 💰 **Total ventes**
  - 📦 **Total frais de livraison**
  - 🧾 **Total dépenses**
  - 📈 **Résultat net**
- Calcul automatique :  
- Bouton pour **rafraîchir le bilan**

---

## 🛠 Installation

### 1) Prérequis
- Python 3.8 ou plus récent
- Bibliothèques Python :
```bash
pip install tkcalendar

Récupération du projet
git clone https://github.com/votre-utilisateur/gestion-ventes.git
cd gestion-ventes

Structure du projet
gestion-ventes/
│
├── Main.py              # Interface principale avec onglets Ventes, Dépenses et Bilan
├── base_donnees.py      # Gestion de la base SQLite (création tables, requêtes, calculs totaux)
├── formulaire.py        # Formulaires Tkinter pour saisie et modification
├── Vente.db             # Base SQLite générée automatiquement
└── README.md            # Documentation du projet

Utilisation
python Main.py


