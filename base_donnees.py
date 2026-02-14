# base_donnees.py
import sqlite3

DB_FILE = "ventes.db"

# ========================
# Connexion
# ========================
def get_connexion():
    return sqlite3.connect(DB_FILE)

# ========================
# Création des tables
# ========================
def creer_tables():
    conn = get_connexion()
    cur = conn.cursor()

    # Table ventes
    cur.execute("""
        CREATE TABLE IF NOT EXISTS ventes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            client TEXT NOT NULL,
            adresse TEXT,
            prix REAL NOT NULL,
            livraison REAL DEFAULT 0,
            tracking TEXT,
            date_vente TEXT,
            date_envoi TEXT,
            paiement TEXT,
            commentaire TEXT
        )
    """)

    # Table dépenses
    cur.execute("""
        CREATE TABLE IF NOT EXISTS depenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            description TEXT
            categorie TEXT NOT NULL,
            montant REAL NOT NULL,
            date_depense TEXT NOT NULL,
            commentaire TEXT
        )
    """)

    conn.commit()
    conn.close()

# ========================
# Fonctions Ventes
# ========================
def ajouter_vente(client, adresse, prix, frais_livraison, tracking, date_vente, date_envoi, paiement, commentaire):
    conn = get_connexion()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO ventes (client, adresse, prix, frais_livraison, tracking, date_vente, date_envoi, paiement, commentaire)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (client, adresse, prix, frais_livraison, tracking, date_vente, date_envoi, paiement, commentaire))
    conn.commit()
    conn.close()

def lister_ventes(filtre=None):
    conn = get_connexion()
    cur = conn.cursor()
    if filtre:
        cur.execute("""
            SELECT * FROM ventes
            WHERE client LIKE ? OR adresse LIKE ? OR tracking LIKE ? OR commentaire LIKE ?
        """, (f"%{filtre}%", f"%{filtre}%", f"%{filtre}%", f"%{filtre}%"))
    else:
        cur.execute("SELECT * FROM ventes")
    rows = cur.fetchall()
    conn.close()
    return rows

def modifier_vente(vente_id, client, adresse, prix, frais_livraison, tracking, date_vente, date_envoi, paiement, commentaire):
    conn = get_connexion()
    cur = conn.cursor()
    cur.execute("""
        UPDATE ventes
        SET client=?, adresse=?, prix=?, frais_livraison=?, tracking=?, date_vente=?, date_envoi=?, paiement=?, commentaire=?
        WHERE id=?
    """, (client, adresse, prix, frais_livraison, tracking, date_vente, date_envoi, paiement, commentaire, vente_id))
    conn.commit()
    conn.close()

def supprimer_vente(vente_id):
    conn = get_connexion()
    cur = conn.cursor()
    cur.execute("DELETE FROM ventes WHERE id=?", (vente_id,))
    conn.commit()
    conn.close()

# ========================
# Fonctions Dépenses
# ========================
def ajouter_depense(description, categorie, montant, date_depense, commentaire):
    conn = get_connexion()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO depenses (description, categorie, montant, date_depense, commentaire)
        VALUES (?, ?, ?, ?, ?)
    """, (description, categorie, montant, date_depense, commentaire))
    conn.commit()
    conn.close()

def lister_depenses(filtre=None):
    conn = get_connexion()
    cur = conn.cursor()
    if filtre:
        cur.execute("""
            SELECT * FROM depenses
            WHERE categorie LIKE ? OR description LIKE ?
        """, (f"%{filtre}%", f"%{filtre}%"))
    else:
        cur.execute("SELECT * FROM depenses")
    rows = cur.fetchall()
    conn.close()
    return rows

def modifier_depense(depense_id, description, categorie, montant, date_depense, commentaire):
    conn = get_connexion()
    cur = conn.cursor()
    cur.execute("""
        UPDATE depenses
        SET description=?, categorie=?, montant=?, date_depense=?, commentaire=?
        WHERE id=?
    """, (description, categorie, montant, date_depense, commentaire, depense_id))
    conn.commit()
    conn.close()

def supprimer_depense(depense_id):
    conn = get_connexion()
    cur = conn.cursor()
    cur.execute("DELETE FROM depenses WHERE id=?", (depense_id,))
    conn.commit()
    conn.close()

# ========================
# Fonctions Totaux
# ========================
def total_ventes():
    conn = get_connexion()
    cur = conn.cursor()
    cur.execute("SELECT IFNULL(SUM(prix), 0) FROM ventes")
    total = cur.fetchone()[0]
    conn.close()
    return total

def total_frais_livraison():
    conn = get_connexion()
    cur = conn.cursor()
    cur.execute("SELECT IFNULL(SUM(frais_livraison), 0) FROM ventes")
    total = cur.fetchone()[0]
    conn.close()
    return total

def total_depenses():
    conn = get_connexion()
    cur = conn.cursor()
    cur.execute("SELECT IFNULL(SUM(montant), 0) FROM depenses")
    total = cur.fetchone()[0]
    conn.close()
    return total
