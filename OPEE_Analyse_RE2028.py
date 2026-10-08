# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "libsql-experimental==0.0.55",
#     "plotly",
#     "polars",
#     "xlsxwriter==3.2.9",
# ]
# ///

import marimo

__generated_with = "0.25.1"
app = marimo.App(width="medium", auto_download=["html"])


@app.cell(hide_code=True)
def entete_et_imports():
    # ---- Imports (partagés par tout le notebook) ----------------------------
    import marimo as mo
    import plotly.express as px
    import plotly.graph_objects as go
    import polars as pl

    # ============================================================================
    # CELLULE — En-tête : visuel HUB, version, date/heure d'édition + historique.
    # (Cadre recopié de OPEE_by_GM.py v0.94.)
    #
    # À CHAQUE ÉDITION DU FICHIER :
    #   1. incrémenter VERSION de 0.01 (0.5 -> 0.51 -> 0.52 ...)
    #   2. mettre à jour DATE_EDITION (date et heure de l'édition, heure de Paris)
    #   3. AJOUTER EN TÊTE de HISTORIQUE_VERSIONS une ligne ("version", "résumé")
    #      avec une phrase de synthèse des changements.
    # ============================================================================

    # ---- Variables (regroupées en début de cellule) -----------------------
    TITRE = "Analyse RE2028"
    BASELINE_Y = 145          # ordonnée de la 1re ligne de la baseline (SVG 1000x500) : réduire pour la remonter
    SIGNATURE = "des prescripteurs bas carbone"
    VERSION = "0.54"          # à ajuster : +0.01 à chaque édition du script
    DATE_EDITION = "09/10/2026 02:20"
    HISTORIQUE_VERSIONS = [
        # (version, synthèse des changements), la plus récente en premier
        (VERSION, "Analyse3 réorganisée : 3b = cascade par lot (lots à plus de 5 kg d'écart + autres lots "
                  "regroupés), 3c = lot 8 par sous-lot, 3d = nature des fiches tous lots (FDES, PEP, DED…), "
                  "3e = nature des fiches du 8.1, avec le nombre de fiches ; familles de générateur et "
                  "effet puissance / donnée retirés ; une seule requête composant pour 3d et 3e"),
        ("0.53", "Analyse3 : macro-lots par classe et cascade, lot 8 par sous-lot, sous-lot 8.1 par "
                  "famille de générateur, effet puissance (W/m²) contre effet donnée (kg/kW), nature des "
                  "fiches 8.1 (table composant, sur demande) ; booléens lus de façon robuste"),
        ("0.52", "Analyse2 : profil des classes (médianes par classe en dégradé, choix constructifs "
                  "et techniques, tornade A contre B en écarts interquartiles), lots 8, 8.1 et 9 inclus ; "
                  "sélecteur de période (toutes, 2022-2023, 2024-2025, comparaison des deux)"),
        ("0.51", "Analyse1 : classes d'écart au budget composant 2028, nombre et part des projets "
                  "(ou bâtiments) par classe, indice de difficulté ; couleurs des classes accessibles "
                  "(bleu = conforme, rouge clair à foncé) ; % ajoutés au tableau des exclusions"),
        ("0.5", "Socle : en-tête, sommaire, connexion, extraction des logements collectifs, "
                  "colonnes calculées (budget composant 2028, écart, classes), exclusions permanentes, "
                  "filtres et bilan du nombre de bâtiments"),
    ]

    # Palette du HUB (relevée sur le visuel du webinaire)
    JAUNE = "#FDB913"         # jaune du logo HUB
    JAUNE_CLAIR = "#FBBF4D"   # bande diagonale à gauche
    ORANGE = "#EE7D00"        # bandeau du titre
    NOIR = "#000000"

    # Logos (hébergés par l'IFPEB)
    URL_LOGO_HUB = "https://www.ifpeb.fr/wp-content/uploads/2026/10/HUB-BC-ST_logo.png"
    URL_LOGO_IFPEB = "https://www.ifpeb.fr/wp-content/uploads/2026/10/ifpeb_logo.jpg"
    URL_LOGO_CARBONE4 = "https://www.ifpeb.fr/wp-content/uploads/2026/10/carbone4_logo.jpg"
    ECHELLE_LOGO_IFPEB = 0.7  # 1 = taille initiale

    # Liens vers le HUB des prescripteurs bas carbone
    URL_HUB = "https://www.ifpeb.fr/nos-expertises/la-technique/le-hub-des-prescripteurs-bas-carbone/"
    URL_RESSOURCES_HUB = "https://www.ifpeb.fr/ressources/?categories=bas-carbone-economie-circulaire"
    URL_OPEE = "https://www.data.gouv.fr/datasets/opee-observatoire-des-performances-energetiques-et-environnementales-des-batiments-neufs"
    URL_LEVIERS_2028 = "https://www.ifpeb.fr/ressources/re2028-les-leviers-gratuits-ou-presque/"
    LIENS = [
        ("HUB des prescripteurs bas carbone", URL_HUB),
        ("Ressources du HUB", URL_RESSOURCES_HUB),
        ("RE2028 : les leviers gratuits (ou presque !)", URL_LEVIERS_2028),
        ("Données OPEE (data.gouv.fr)", URL_OPEE),
    ]

    # Textes explicatifs (une ligne chacun)
    TXT_OPEE = (
        "<b>OPEE</b> : l'Observatoire des Performances Énergétiques et "
        "Environnementales des bâtiments neufs, la base ouverte des données "
        "RE2020 (énergie, carbone, confort d'été) des projets déposés."
    )
    TXT_BASE_FILLE = (
        "<b>La base fille (BF)</b> : seconde base, consolidée par le CSTB pour la DGALN/DHUP "
        "à partir de la « base mère » (import brut des données saisies dans le modèle RSEE)."
    )
    TXT_ANALYSE = (
        "<b>L'analyse RE2028</b> : à quel point le seuil 2028 de l'IC construction est-il "
        "facile à atteindre en logement collectif, et quels leviers font la différence ?"
    )

    # ---- Visuel d'en-tête : un seul SVG (viewBox 1000 x 500) qui s'adapte à la largeur ----
    # Largeur fixe en px + max-width:100% : fonctionne même si marimo place le HTML
    # dans un conteneur « shrink-to-fit ».
    _visuel = f"""
    <div style="width:960px;max-width:100%;border-radius:14px;overflow:hidden;line-height:0;">
    <svg viewBox="0 0 1000 500" xmlns="http://www.w3.org/2000/svg"
         style="display:block;width:100%;height:auto;background:#fff;
                font-family:Calibri,'Segoe UI',Arial,sans-serif;">

      <!-- bande jaune diagonale (gauche) -->
      <polygon points="0,0 30,0 115,500 0,500" fill="{JAUNE_CLAIR}"/>

      <!-- zone noire : colonne droite + biseau du bas -->
      <polygon points="850,0 1000,0 1000,500 115,500 805,355 850,355" fill="{NOIR}"/>

      <!-- grand « HUB » vertical -->
      <g fill="#fff" font-family="'Arial Black',Arial,sans-serif" font-weight="900"
         font-size="140" text-anchor="middle">
        <text x="925" y="122">H</text>
        <text x="925" y="237">U</text>
        <text x="925" y="352">B</text>
      </g>

      <!-- logo HUB -->
      <image href="{URL_LOGO_HUB}" x="345" y="0" width="130" height="165"
             preserveAspectRatio="xMidYMin meet"/>

      <!-- baseline, juste sous le logo HUB -->
      <g font-size="14.5" font-weight="700" text-anchor="middle" letter-spacing="0.6">
        <text x="410" y="{BASELINE_Y}">LA PLATEFORME DE COLLABORATION POUR</text>
        <text x="410" y="{BASELINE_Y + 20}">DÉTECTER, SUSCITER ET METTRE EN ŒUVRE DES</text>
        <text x="410" y="{BASELINE_Y + 40}">SOLUTIONS BAS CARBONE POUR LE BÂTIMENT</text>
      </g>

      <!-- bandeau orange : titre seul -->
      <rect x="137" y="240" width="546" height="80" fill="{ORANGE}"/>
      <text x="410" y="294" fill="#fff" text-anchor="middle" font-size="38" font-weight="800"
            stroke="#fff" stroke-width="1">{TITRE}</text>

      <!-- logos IFPEB (à gauche) et Carbone 4 (à droite), inclinés comme le biseau noir -->
      <g transform="translate(190 476) rotate(-11)">
        <image href="{URL_LOGO_IFPEB}" x="-20" y="{-65 * ECHELLE_LOGO_IFPEB}"
               width="{150 * ECHELLE_LOGO_IFPEB}" height="{65 * ECHELLE_LOGO_IFPEB}"
               preserveAspectRatio="xMinYMax meet"/>
        <image href="{URL_LOGO_CARBONE4}" x="100" y="-55" width="220" height="55"
               preserveAspectRatio="xMinYMax meet"/>
      </g>

      <!-- signature en bas à droite -->
      <text x="950" y="488" fill="#fff" font-family="Arial,sans-serif" font-weight="700"
            font-size="31" text-anchor="end">{SIGNATURE}</text>
    </svg>
    </div>"""


    # ---- Encarts numérotés (lisibles en thème clair comme sombre) ----
    def _carte(numero, texte):
        return f"""
        <div style="flex:1;min-width:260px;display:flex;gap:14px;align-items:flex-start;
                    padding:16px 18px;border-radius:12px;
                    background:rgba(253,185,19,.14);border:1px solid rgba(253,185,19,.55);">
          <div style="flex:none;width:30px;height:30px;border-radius:50%;
                      background:{ORANGE};color:#fff;font-weight:700;
                      display:flex;align-items:center;justify-content:center;">{numero}</div>
          <div style="font-size:14px;line-height:1.45;">{texte}</div>
        </div>"""


    _cartes = f"""
    <div style="display:flex;gap:16px;flex-wrap:wrap;margin-top:16px;">
      {_carte(1, TXT_OPEE)}
      {_carte(2, TXT_BASE_FILLE)}
      {_carte(3, TXT_ANALYSE)}
    </div>"""

    # ---- Rangée de liens vers le HUB (flèches ➔) ----
    _liens = "".join(
        f'<a href="{_url}" target="_blank" rel="noopener" '
        f'style="text-decoration:none;font-weight:600;font-size:13px;'
        f'padding:7px 14px;border-radius:999px;color:{ORANGE};'
        f'border:1.5px solid {ORANGE};">➔ {_nom}</a>'
        for _nom, _url in LIENS
    )
    _rangee_liens = (
        f'<div style="display:flex;gap:10px;flex-wrap:wrap;margin-top:16px;">{_liens}</div>'
    )
    _version = (
        f'<div style="font-size:12px;opacity:.65;margin-top:8px;">'
        f'Version {VERSION} · édité le {DATE_EDITION}</div>'
    )

    # ---- Historique des versions, masqué dans un accordéon ----
    _lignes = "\n".join(f"- **{_v}** · {_t}" for _v, _t in HISTORIQUE_VERSIONS)
    _historique = mo.accordion({"Historique des versions": mo.md(_lignes)})

    mo.vstack([mo.Html(_visuel + _version + _cartes + _rangee_liens), _historique])
    return go, mo, pl, px


@app.cell(hide_code=True)
def sommaire_analyses(mo):
    # ============================================================================
    # CELLULE — Sommaire : liste des analyses (numéro + titre) et hypothèses.
    #
    # SOURCE UNIQUE des numéros et titres : chaque cellule d'analyse lit son titre
    # dans ANALYSES. Pour renommer ou renuméroter une analyse, c'est ICI.
    # ANALYSES_PRETES : analyses déjà construites (les autres sont marquées « à venir »).
    # ============================================================================

    ANALYSES = {
        1: "Classes d'écart au budget composant 2028 et indice de difficulté",
        2: "Profil des classes : forme, programme, technique et méthode",
        3: "Macro-lots et lots par classe, lot 8 et nature des fiches environnementales",
        4: "Évolution par année de dépôt",
        5: "Simulateur de leviers",
        6: "Effet propre de chaque levier (régression)",
    }
    ANALYSES_PRETES = {1, 2, 3} # analyses déjà construites

    _lignes = "\n".join(
        f"- **Analyse{_n}** — {_titre}" + ("" if _n in ANALYSES_PRETES else " *(à venir)*")
        for _n, _titre in ANALYSES.items()
    )
    mo.md(
        "### Analyses\n\n"
        + _lignes
        + "\n\n### Hypothèses de calcul\n\n"
        "- Seul l'**IC construction** est étudié, à travers l'**IC composant** : l'IC chantier est retiré.\n"
        "- **Budget composant 2028** = `ic_construction_max_2028 − ic_chantier` (seuil propre à chaque bâtiment).\n"
        "- **Écart au budget** = `ic_composant − budget composant 2028` (négatif ou nul = conforme 2028).\n"
        "- **Macro-lots** (grille du HUB) : gros œuvre = lots 1 à 3 ; second œuvre = lots 4 à 7 ; "
        "lots techniques = lots 8 à 13.\n"
        "- **Périmètre** : logements collectifs, hors petit collectif (sref < 200 m²) et hors IGH "
        "(hauteur > 50 m). Le seuil 2031 n'est pas étudié."
    )
    return (ANALYSES,)


@app.cell(hide_code=True)
def saisie_jeton(mo):
    # ============================================================================
    # CELLULE — Jeton Turso (COPIE DE OPEE_by_GM v0.94). Il n'est JAMAIS écrit
    # dans le code (dépôt GitHub) :
    #   1. variable d'environnement TURSO_TOKEN si elle existe (local / molab),
    #   2. sinon, champ de saisie masqué ci-dessous.
    # ============================================================================
    import os

    champ_jeton = mo.ui.text(kind="password", label="Jeton Turso", full_width=True)
    (
        mo.md("*Jeton Turso lu dans la variable d'environnement `TURSO_TOKEN`.*")
        if os.environ.get("TURSO_TOKEN")
        else mo.vstack([mo.md("### Connexion à la base OPEE"), champ_jeton])
    )
    return (champ_jeton,)


@app.cell(hide_code=True)
def creation_connect(champ_jeton, mo):
    # ============================================================================
    # CELLULE — Connexion à la base Turso (COPIE DE OPEE_by_GM v0.94, simplifiée :
    # seul le nombre de tables est affiché).
    # ============================================================================
    import os as _os
    import libsql_experimental as libsql

    # ---- Variables ---------------------------------------------------------
    _URL_BASE = "libsql://opee-alliages.aws-eu-west-1.turso.io"
    _turso_token = _os.environ.get("TURSO_TOKEN") or champ_jeton.value

    mo.stop(not _turso_token, mo.md("*Saisir le jeton Turso ci-dessus pour lancer le notebook.*"))

    turso_conn = libsql.connect(_URL_BASE, auth_token=_turso_token)

    # Vérification de la connexion : liste des tables (un seul appel)
    _tables = turso_conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
    mo.md(f"*Connexion établie : {len(_tables)} tables disponibles.*")
    return (turso_conn,)


@app.cell(hide_code=True)
def exports(mo, pl):
    # ============================================================================
    # CELLULE — Export CSV / JSON, COMMUN à toutes les analyses (COPIE DE OPEE_by_GM v0.94)
    #
    # boutons_export(df, nom) -> deux boutons de téléchargement (CSV + JSON).
    # ============================================================================

    def boutons_export(df, nom):
        # Le CSV ne supporte pas les colonnes "liste" : converties en texte
        # (valeurs séparées par des virgules) pour le CSV uniquement.
        _colonnes_liste = [c for c, t in df.schema.items() if isinstance(t, pl.List)]
        _df_csv = df.with_columns(
            [pl.col(c).list.eval(pl.element().cast(pl.Utf8)).list.join(",") for c in _colonnes_liste]
        )
        _csv_download = mo.download(
            data=_df_csv.write_csv().encode("utf-8-sig"),
            filename=f"{nom}.csv",
            mimetype="text/csv",
            label="Télécharger en CSV",
        )
        _json_download = mo.download(
            data=df.write_json().encode("utf-8"),
            filename=f"{nom}.json",
            mimetype="application/json",
            label="Télécharger en JSON",
        )
        return mo.hstack([_csv_download, _json_download], justify="start")

    return (boutons_export,)


@app.cell(hide_code=True)
def fonction_retrouver_sref(pl):
    # ============================================================================
    # CELLULE — Fonction "retrouver sref" (COPIE DE OPEE_by_GM v0.94) : reconstitue
    # la surface de référence (colonne `sref`) des LOGEMENTS COLLECTIFS à partir de
    # misurf_tot et mbsurf_tot (table zone_open_data).
    #
    # Retourne une EXPRESSION polars, évaluée ligne par ligne.
    #
    # Fonctions directes (sref -> misurf_tot) :
    #     sref <= 1300        : misurf_tot = -0.104  + 0.00008  * sref
    #     1300 < sref < 4000  : misurf_tot =  0.0455 - 0.000035 * sref
    #     sref >= 4000        : misurf_tot = -0.0945
    # mbsurf_tot sert à lever l'ambiguïté : > 0 si sref < 1300, = 0 si sref >= 1300.
    #
    # Une ligne incohérente (ou avec un NULL) reçoit sref = NULL.
    # SREF_PLATEAU est aussi utilisé par l'analyse (bâtiments « plateau » >= 4000 m²).
    # ============================================================================


    # ============================================================================
    # PARAMÈTRES (toutes les variables au même endroit)
    # ============================================================================

    # Tranche 2 : misurf_tot = A2 - B2 * sref
    A2, B2 = 0.0455, 0.000035
    # Tranche 3 (plateau) : valeur constante de misurf_tot
    PLATEAU = -0.0945
    SREF_PLATEAU = 5000       # m² : valeur de sref renvoyée sur le plateau (sref >= 4000)

    # Tranche 1 : rétro-ingénierie grâce à mbsurf_tot
    #   sref = ((misurf_tot + RETRO_A) * 10000) / RETRO_K
    RETRO_A = 0.169           # ordonnée à l'origine (valeur absolue)
    RETRO_K = 1.3             # pente exprimée pour 10000 m²

    TOL = 1e-9                # tolérance pour les comparaisons de flottants


    def retrouver_sref(col_misurf="misurf_tot", col_mbsurf="mbsurf_tot"):
        m = pl.col(col_misurf)
        mb = pl.col(col_mbsurf)

        # Conditions de chaque branche (mutuellement exclusives)
        _tranche1 = (mb > TOL) & m.is_between(-RETRO_A - TOL, TOL)          # sref < 1300
        _plateau = (mb <= TOL) & ((m - PLATEAU).abs() <= TOL)                # sref >= 4000
        _tranche2 = (mb <= TOL) & (m > PLATEAU + TOL) & (m <= TOL)           # 1300 <= sref < 4000

        return (
            pl.when(_tranche1).then(((m + RETRO_A) * 10000) / RETRO_K)
            .when(_plateau).then(pl.lit(float(SREF_PLATEAU)))
            .when(_tranche2).then((A2 - m) / B2)
            .otherwise(None)                                                 # incohérent -> NULL
        )

    return SREF_PLATEAU, retrouver_sref


@app.cell(hide_code=True)
def constantes_analyse(pl):
    # ============================================================================
    # CELLULE — Constantes de l'analyse, définies en UN seul endroit
    #
    #   - Périmètre et exclusions permanentes (petit collectif, IGH)
    #   - Estimation du nombre de logements
    #   - Classes d'écart au budget composant 2028 (+ couleurs) et indice de difficulté
    #   - Macro-lots (grille du HUB) et liste des lots / sous-lots
    #   - Options du filtre matériau (COPIE DE OPEE_by_GM v0.94)
    #   - expr_classe_2028() : expression polars donnant la classe de chaque bâtiment
    # ============================================================================

    # --- Périmètre et exclusions permanentes ---------------------------------------
    USAGE_LOGEMENT_COLLECTIF = "Logement collectif"
    SREF_MIN_COLLECTIF = 200        # m² : sref < 200 -> petit collectif, exclu
    HAUTEUR_IGH = 50                # m : hauteur_hors_toiture > 50 -> IGH, exclu
    EXCLURE_SREF_INCONNUE = True    # sref non reconstituée -> taille inconnue -> exclu

    # --- Nombre de logements estimé -------------------------------------------------
    SURFACE_PAR_LOGEMENT = 70       # m² de sref par logement (le nb de logements n'est pas dans la base)

    # --- Classes d'écart au budget composant 2028 -----------------------------------
    # Écart = ic_composant - budget composant 2028 (kgCO2e/m²). Bornes hautes exclusives.
    BORNES_CLASSES = [30, 80, 130]
    CLASSES_2028 = ["Conforme 2028", "< 30 kg", "30 à 80 kg", "80 à 130 kg", "> 130 kg"]
    CLASSE_INCONNUE = "Inconnu"     # écart non calculable (donnée manquante)
    # Échelle ordonnée « divergente » : bleu = conforme ; rampe d'un seul rouge,
    # du clair au foncé, pour l'éloignement au budget ; gris = inconnu.
    # Rampe rouge validée (skill dataviz, validate_palette.js --ordinal : PASS) ;
    # l'identité des classes est aussi portée par les étiquettes (pas la couleur seule).
    COULEURS_CLASSES = {
        "Conforme 2028": "#2a78d6",
        "< 30 kg": "#ec8f72",
        "30 à 80 kg": "#d9583a",
        "80 à 130 kg": "#ad321b",
        "> 130 kg": "#76190c",
        "Inconnu": "#b5b4b0",
    }
    # Indice de difficulté = part des projets au-delà de SEUIL_DIFFICULTE kg
    # (au-delà des leviers « gratuits » du HUB)
    SEUIL_DIFFICULTE = 30
    CLASSES_DIFFICILES = CLASSES_2028[2:]

    # --- Lots, sous-lots et macro-lots (grille du HUB) ------------------------------
    NB_SOUS_LOTS = {1: 3, 2: 3, 3: 8, 4: 3, 5: 5, 6: 3, 7: 3, 8: 7, 9: 2, 10: 6, 11: 3, 12: 1, 13: 1}
    COLS_LOTS = [f"ic_composant_lot_{i}" for i in NB_SOUS_LOTS]
    COLS_SOUS_LOTS = [
        f"ic_composant_sous_lot_{i}_{j}" for i, n in NB_SOUS_LOTS.items() for j in range(1, n + 1)
    ]
    MACRO_LOTS = {
        "Gros œuvre": [1, 2, 3],
        "Second œuvre": [4, 5, 6, 7],
        "Lots techniques": [8, 9, 10, 11, 12, 13],
    }
    # Nom de colonne de chaque macro-lot dans le DataFrame
    COLS_MACRO_LOTS = {
        "Gros œuvre": "ic_gros_oeuvre",
        "Second œuvre": "ic_second_oeuvre",
        "Lots techniques": "ic_lots_techniques",
    }

    # --- Filtre matériau (COPIE DE OPEE_by_GM v0.94) --------------------------------
    LIBELLE_MATERIAU_NUL = "None"      # libellé de l'option "matériau non renseigné" (NULL)
    MATERIAUX_OPTIONS = [
        LIBELLE_MATERIAU_NUL,
        "Acier", "Autre", "Béton", "Béton cellulaire", "Béton de bois", "Béton de chanvre",
        "Béton fibré", "Béton haute performance", "Mixte: bois-béton", "Mixte: béton-acier",
        "Pierre", "Terre crue", "Terre cuite", "Bois massif", "Bois massif reconstitué",
    ]


    def expr_classe_2028(col="ecart_2028"):
        """Classe d'écart au budget composant 2028. Bornes hautes exclusives,
        enchaînées : aucune valeur décimale ne tombe entre deux classes."""
        _e = pl.col(col)
        return (
            pl.when(_e.is_null()).then(pl.lit(CLASSE_INCONNUE))
            .when(_e <= 0).then(pl.lit(CLASSES_2028[0]))
            .when(_e < BORNES_CLASSES[0]).then(pl.lit(CLASSES_2028[1]))
            .when(_e < BORNES_CLASSES[1]).then(pl.lit(CLASSES_2028[2]))
            .when(_e < BORNES_CLASSES[2]).then(pl.lit(CLASSES_2028[3]))
            .otherwise(pl.lit(CLASSES_2028[4]))
        )

    return (
        BORNES_CLASSES,
        CLASSES_2028,
        CLASSES_DIFFICILES,
        CLASSE_INCONNUE,
        COLS_LOTS,
        COLS_MACRO_LOTS,
        COLS_SOUS_LOTS,
        COULEURS_CLASSES,
        EXCLURE_SREF_INCONNUE,
        HAUTEUR_IGH,
        LIBELLE_MATERIAU_NUL,
        MACRO_LOTS,
        MATERIAUX_OPTIONS,
        NB_SOUS_LOTS,
        SEUIL_DIFFICULTE,
        SREF_MIN_COLLECTIF,
        SURFACE_PAR_LOGEMENT,
        USAGE_LOGEMENT_COLLECTIF,
        expr_classe_2028,
    )


@app.cell(hide_code=True)
def lancement(mo):
    # Bouton de lancement de l'extraction (un seul appel réseau, cf. cellule suivante)
    bouton_lancer = mo.ui.run_button(label="---> lancer l'extraction <----")
    mo.vstack([
        mo.md("### Extraction des logements collectifs"),
        bouton_lancer,
        mo.md("*🔽 cliquer pour lancer si rien ne s'affiche 🔽*"),
    ])
    return (bouton_lancer,)


@app.cell(hide_code=True)
def extraction_unique(
    COLS_LOTS,
    COLS_SOUS_LOTS,
    USAGE_LOGEMENT_COLLECTIF,
    bouton_lancer,
    mo,
    pl,
    turso_conn,
):
    mo.stop(not bouton_lancer.value)
    # ============================================================================
    # CELLULE D'EXTRACTION UNIQUE — un seul appel réseau à Turso, partagé par
    # TOUTES les analyses. Une ligne par BÂTIMENT (identifiant "ID" =
    # projet_id_batiment_index), valeurs brutes (pas de AVG, pas d'exclusion).
    #
    # Seul filtre côté SQL : l'usage (logements collectifs). Exclusions et filtres
    # sont appliqués ensuite, en polars, sans appel réseau.
    # Résultat : DATA_extrait (brut) -> colonnes calculées dans la cellule suivante.
    # ============================================================================


    # ============================================================================
    # PARAMÈTRES (toutes les variables au même endroit)
    # ============================================================================

    # --- Tables et colonnes de base ---------------------------------------------
    _TABLE_BATIMENT = "batiment_open_data"
    _TABLE_PROJET = "projet_open_data"
    _TABLE_ZONE = "zone_open_data"
    _PID_COL = "projet_id"
    _USAGE_COL = "usage_principal_txt"

    # --- Colonnes ramenées de la table bâtiment, par thème ---------------------
    # Carbone : IC construction et sa décomposition, seuil 2028
    _COLS_CARBONE = [
        "ic_construction", "ic_composant", "ic_chantier", "ic_construction_max_2028",
        "seuil_ic_construction_atteint",
    ]
    # Forme et programme
    _COLS_FORME = [
        "hauteur_hors_toiture", "surface_baies_rset", "surface_murs_rset",
        "nb_place_parking_infra", "nb_place_parking_supra", "nb_place_parking_ext",
        "nb_ascenseur",
    ]
    # Constructif et technique
    _COLS_TECHNIQUE = [
        "dc_materiau_structure", "dc_type_structure_principale", "stock_c",
        "generateur_principal_ch", "generateur_principal_ecs",
        "famille_synthese_generateur_ch", "famille_synthese_generateur_ecs",
        "vecteur_energie_principal_ch", "presence_reseau",
        "puissance_thermique_max_restituable_ch_1", "l_type_ventilation_mecanique",
    ]
    # Méthodologie : données environnementales
    _COLS_METHODE = [
        "udd", "nb_total_fiche_acv", "nb_fdes", "nb_pep", "nb_ded",
        "nb_fiche_configuree", "nb_pep_extrapolee", "nb_conventionnelle",
    ]
    # Table zone : misurf_tot / mbsurf_tot (pour retrouver la sref)
    _COLS_ZONE = ["misurf_tot", "mbsurf_tot"]


    # ============================================================================
    # 1. REQUÊTE SQL
    # ============================================================================

    # Identifiant unique par bâtiment ; COALESCE évite qu'un batiment_index NULL
    # fasse disparaître le bâtiment du comptage.
    _ID_SQL = f"(b.{_PID_COL} || '_' || COALESCE(b.batiment_index, '0'))"

    _select = [
        f'{_ID_SQL} AS "ID"',
        f"b.{_PID_COL} AS projet_id",
        "b.batiment_index",
        "b.zone_climatique",
        "b.regle_validation_globale",
        *[f"b.{col}" for col in _COLS_CARBONE],
        *[f"b.{col}" for col in COLS_LOTS],
        *[f"b.{col}" for col in COLS_SOUS_LOTS],
        *[f"b.{col}" for col in _COLS_FORME],
        *[f"b.{col}" for col in _COLS_TECHNIQUE],
        *[f"b.{col}" for col in _COLS_METHODE],
        *[f"z.{col}" for col in _COLS_ZONE],
        f"b.{_USAGE_COL} AS usage",
        "pf.annees_depot_pc_json",
        "pf.types_attestation_json",
    ]
    _select_sql = ",\n        ".join(_select)

    # Clé de rattachement bâtiment <-> zones (batiment_index NULL -> 0, comparé en texte)
    _CLE_BATIMENT_ZONE = "CAST(COALESCE(batiment_index, 0) AS TEXT)"
    _CLE_BATIMENT_B = "CAST(COALESCE(b.batiment_index, 0) AS TEXT)"
    _agg_zone = ",\n                ".join(f"MAX({col}) AS {col}" for col in _COLS_ZONE)

    _requete = f"""
        WITH projets_info AS (
            -- par projet : toutes les années de dépôt et attestations (listes JSON)
            SELECT
                {_PID_COL},
                json_group_array(DISTINCT annee_depot_pc) AS annees_depot_pc_json,
                json_group_array(DISTINCT type_attestation) AS types_attestation_json
            FROM {_TABLE_PROJET}
            GROUP BY {_PID_COL}
        ),
        -- zone_open_data : plusieurs zones par bâtiment, qui portent la même valeur de
        -- misurf_tot / mbsurf_tot -> une seule valeur par bâtiment (MAX ignore les NULL)
        zones_info AS (
            SELECT
                {_PID_COL},
                {_CLE_BATIMENT_ZONE} AS cle_batiment,
                {_agg_zone}
            FROM {_TABLE_ZONE}
            GROUP BY {_PID_COL}, {_CLE_BATIMENT_ZONE}
        )
        SELECT
            {_select_sql}
        FROM {_TABLE_BATIMENT} b
        LEFT JOIN projets_info pf ON b.{_PID_COL} = pf.{_PID_COL}
        LEFT JOIN zones_info z
               ON b.{_PID_COL} = z.{_PID_COL}
              AND {_CLE_BATIMENT_B} = z.cle_batiment
        WHERE b.{_USAGE_COL} = '{USAGE_LOGEMENT_COLLECTIF}'
    """

    _cursor = turso_conn.execute(_requete)
    _col_names = [desc[0] for desc in _cursor.description]
    _lignes = _cursor.fetchall()


    # ============================================================================
    # 2. MISE EN FORME MINIMALE (polars, aucun appel réseau)
    # ============================================================================

    # Construction colonne par colonne avec un scan complet des lignes : évite une
    # inférence de type faite sur les premières lignes seulement.
    _df = pl.DataFrame(
        [dict(zip(_col_names, _row)) for _row in _lignes], infer_schema_length=None
    )

    # Textes : espaces parasites retirés une fois pour toutes
    _df = _df.with_columns(
        pl.col("dc_materiau_structure").cast(pl.Utf8).str.strip_chars(),
        pl.col("dc_type_structure_principale").cast(pl.Utf8).str.strip_chars(),
    )

    # Listes JSON -> vraies listes polars (filtrage propre ensuite)
    _df = _df.with_columns(
        pl.col("annees_depot_pc_json").cast(pl.Utf8).str.json_decode(pl.List(pl.Int64)).alias("annees_depot_pc"),
        pl.col("types_attestation_json").cast(pl.Utf8).str.json_decode(pl.List(pl.Utf8)).alias("types_attestation"),
    ).drop(["annees_depot_pc_json", "types_attestation_json"])

    DATA_extrait = _df
    print(f"Bâtiments extraits ({USAGE_LOGEMENT_COLLECTIF}) : {_df.height}")
    return (DATA_extrait,)


@app.cell(hide_code=True)
def colonnes_calculees(
    COLS_MACRO_LOTS,
    DATA_extrait,
    MACRO_LOTS,
    SREF_PLATEAU,
    SURFACE_PAR_LOGEMENT,
    expr_classe_2028,
    pl,
    retrouver_sref,
):
    # ============================================================================
    # CELLULE — Colonnes calculées (une fois pour toutes, partagées par les analyses)
    #
    #   sref                       : surface de référence reconstituée (retrouver_sref)
    #   sref_plateau               : True si sref >= 4000 m² (valeur forcée à 5000)
    #   budget_composant_2028      : ic_construction_max_2028 - ic_chantier
    #   ecart_2028 / ecart_2028_pct: ic_composant - budget (kg/m², % du budget)
    #   classe_2028                : classe d'écart (cf. constantes_analyse)
    #   nb_logements_estime        : sref / SURFACE_PAR_LOGEMENT
    #   taux_vitrage_pct           : surface_baies_rset / sref (%)
    #   ratio_facade               : surface_murs_rset / sref (m² de murs par m² de sref)
    #     (ces trois indicateurs sont NULL pour les bâtiments « plateau »)
    #   parking_infra_par_logement : nb_place_parking_infra / nb_logements_estime
    #   ic_gros_oeuvre, ic_second_oeuvre, ic_lots_techniques : sommes des lots
    #   annee_depot                : plus ancienne année de dépôt du projet
    # Résultat : DATA_brut.
    # ============================================================================

    # ---- Variables -------------------------------------------------------------
    _TOL_PLATEAU = 1e-6
    _sref = pl.col("sref")
    _nb_logements = pl.col("nb_logements_estime")

    _df = DATA_extrait

    # 1. Surface de référence reconstituée + repérage des bâtiments « plateau »
    _df = _df.with_columns(retrouver_sref().cast(pl.Float64).alias("sref"))
    _df = _df.with_columns(
        ((_sref - SREF_PLATEAU).abs() <= _TOL_PLATEAU).fill_null(False).alias("sref_plateau")
    )

    # 2. Budget composant 2028, écart et classe
    _df = _df.with_columns(
        (pl.col("ic_construction_max_2028") - pl.col("ic_chantier")).alias("budget_composant_2028")
    )
    _df = _df.with_columns(
        (pl.col("ic_composant") - pl.col("budget_composant_2028")).alias("ecart_2028")
    )
    _df = _df.with_columns(
        (pl.col("ecart_2028") / pl.col("budget_composant_2028") * 100).alias("ecart_2028_pct"),
        expr_classe_2028().alias("classe_2028"),
    )

    # 3. Indicateurs de forme et de programme, rapportés à la sref : NULL si sref
    #    inconnue ou « plateau » (sref forcée à 5000 m², ratio faux)
    _sref_fiable = pl.when(pl.col("sref_plateau")).then(None).otherwise(_sref)
    _df = _df.with_columns(
        (_sref_fiable / SURFACE_PAR_LOGEMENT).alias("nb_logements_estime"),
        (pl.col("surface_baies_rset") / _sref_fiable * 100).alias("taux_vitrage_pct"),
        (pl.col("surface_murs_rset") / _sref_fiable).alias("ratio_facade"),
    )
    _df = _df.with_columns(
        (pl.col("nb_place_parking_infra") / _nb_logements).alias("parking_infra_par_logement"),
    )

    # 4. Macro-lots : somme des lots (un lot NULL compte pour 0)
    _df = _df.with_columns([
        pl.sum_horizontal([pl.col(f"ic_composant_lot_{i}").fill_null(0) for i in _lots]).alias(COLS_MACRO_LOTS[_nom])
        for _nom, _lots in MACRO_LOTS.items()
    ])

    # 5. Année de dépôt unique (la plus ancienne du projet) pour l'analyse temporelle
    _df = _df.with_columns(pl.col("annees_depot_pc").list.min().alias("annee_depot"))

    DATA_brut = _df
    return (DATA_brut,)


@app.cell(hide_code=True)
def exclusions_permanentes(
    DATA_brut,
    EXCLURE_SREF_INCONNUE,
    HAUTEUR_IGH,
    SREF_MIN_COLLECTIF,
    pl,
):
    # ============================================================================
    # CELLULE — Exclusions PERMANENTES (périmètre de l'analyse, pas des filtres)
    #
    #   1. sref non reconstituée (taille inconnue)       [si EXCLURE_SREF_INCONNUE]
    #   2. petit collectif : sref < SREF_MIN_COLLECTIF m²
    #   3. IGH : hauteur_hors_toiture > HAUTEUR_IGH m
    #
    # Les bâtiments « plateau » (sref >= 4000 m²) ne sont PAS exclus : ils sont
    # seulement retirés des indicateurs par logement (nb_logements_estime = NULL).
    # Résultats : DATA_base (périmètre de l'analyse) et BILAN_EXCLUSIONS (comptages).
    # ============================================================================

    # ---- Liste des exclusions : (libellé, active ?, expression des bâtiments CONSERVÉS)
    _EXCLUSIONS = [
        ("sref non reconstituée (taille inconnue)", EXCLURE_SREF_INCONNUE,
         pl.col("sref").is_not_null()),
        (f"petit collectif (sref < {SREF_MIN_COLLECTIF} m²)", True,
         (pl.col("sref") >= SREF_MIN_COLLECTIF).fill_null(True)),
        (f"IGH (hauteur > {HAUTEUR_IGH} m)", True,
         (pl.col("hauteur_hors_toiture") <= HAUTEUR_IGH).fill_null(True)),
    ]

    _df = DATA_brut
    _lignes = [{
        "étape": "Bâtiments extraits (logements collectifs)",
        "bâtiments retirés": None,
        "bâtiments restants": _df.height,
        "projets restants": _df["projet_id"].n_unique(),
    }]
    for _libelle, _active, _garder in _EXCLUSIONS:
        if not _active:
            continue
        _avant = _df.height
        _df = _df.filter(_garder)
        _lignes.append({
            "étape": f"Exclusion : {_libelle}",
            "bâtiments retirés": _avant - _df.height,
            "bâtiments restants": _df.height,
            "projets restants": _df["projet_id"].n_unique(),
        })

    DATA_base = _df

    # ---- Pourcentages, rapportés aux bâtiments / projets EXTRAITS (1re ligne)
    _nb_bat = max(_lignes[0]["bâtiments restants"], 1)
    _nb_proj = max(_lignes[0]["projets restants"], 1)
    BILAN_EXCLUSIONS = pl.DataFrame(_lignes).with_columns(
        (pl.col("bâtiments retirés") / _nb_bat * 100).round(1).alias("% bâtiments retirés"),
        (pl.col("bâtiments restants") / _nb_bat * 100).round(1).alias("% bâtiments restants"),
        (pl.col("projets restants") / _nb_proj * 100).round(1).alias("% projets restants"),
    ).select(
        "étape", "bâtiments retirés", "% bâtiments retirés",
        "bâtiments restants", "% bâtiments restants",
        "projets restants", "% projets restants",
    )
    return BILAN_EXCLUSIONS, DATA_base


@app.cell(hide_code=True)
def widgets_filtres(MATERIAUX_OPTIONS, mo):
    # ============================================================================
    # CELLULE — Widgets des filtres COMMUNS à toutes les analyses
    # (COPIE DE OPEE_by_GM v0.94, sans le filtre de surface : le petit collectif
    # est exclu de façon permanente).
    # ============================================================================

    choix_de_la_date = mo.ui.multiselect(
        options=["2022", "2023", "2024", "2025"], label="choisissez les dates", value=["2022", "2023", "2024", "2025"]
    )
    choix_de_attestation = mo.ui.multiselect(
        options=["DAACT", "PC"], label="choisissez l'attestation", value=["DAACT", "PC"]
    )
    choix_valide_regles = mo.ui.switch(label="Valider pour regarder seulement les bons batiments ?", value=True)

    # Par défaut TOUT est coché (= pas de filtre) : voir `valeurs_actives`.
    _zones = ["H1a", "H1b", "H1c", "H2a", "H2b", "H2c", "H2d", "H3"]
    choix_zone_climatique = mo.ui.multiselect(options=_zones, value=_zones, label="Zone Climatique")
    choix_materiau_structure = mo.ui.multiselect(
        options=MATERIAUX_OPTIONS, value=MATERIAUX_OPTIONS, label="Quels Matériaux"
    )
    cacher_inconnu = mo.ui.switch(label="Masquer les inconnus ?", value=True)
    return (
        cacher_inconnu,
        choix_de_attestation,
        choix_de_la_date,
        choix_materiau_structure,
        choix_valide_regles,
        choix_zone_climatique,
    )


@app.cell(hide_code=True)
def panneau_filtres_def(
    cacher_inconnu,
    choix_de_attestation,
    choix_de_la_date,
    choix_materiau_structure,
    choix_valide_regles,
    choix_zone_climatique,
    mo,
):
    # ============================================================================
    # CELLULE — Panneau de filtres, construit UNE fois, répété avant chaque analyse
    # (COPIE DE OPEE_by_GM v0.94, bloc « Bâtiment » réduit au matériau).
    #
    #   1. Qualité des données (toujours visible, en haut) : règles de validation,
    #      masquer les inconnus
    #   2. Accordéons FERMÉS côte à côte : Période et lieu / Bâtiment / Analyse N
    #
    # Mise en page statique (ne lit aucune valeur de widget). Le résumé des filtres
    # et le bilan des bâtiments sont affichés à part, dans des cellules séparées.
    # ============================================================================

    # ---- Variables ---------------------------------------------------------
    _LIBELLE_PERIODE = "Période et lieu"
    _LIBELLE_BATIMENT = "Bâtiment"


    def panneau_filtres(parametres_analyse=None, *, avec_materiau=True, avec_inconnus=True, bascules_analyse=()):
        """Construit le panneau de filtres d'une analyse.

        - parametres_analyse : dict {libellé de l'accordéon: contenu} pour les paramètres
          propres à l'analyse (None = pas d'accordéon supplémentaire).
        - avec_materiau=False : analyse où le matériau est l'axe (pas de filtre matériau).
        - avec_inconnus=False : analyse qui n'applique pas « Masquer les inconnus ».
        - bascules_analyse : switchs propres à l'analyse, ajoutés dans la rangée du haut.
        """
        # 1. Qualité des données : toujours visible, en haut
        _qualite = mo.hstack(
            [choix_valide_regles] + ([cacher_inconnu] if avec_inconnus else []) + list(bascules_analyse),
            justify="start", gap=2,
        )

        # 2. Contenu des accordéons
        _bloc_periode = mo.vstack([
            mo.hstack([choix_de_la_date, choix_de_attestation], justify="start", wrap=True),
            choix_zone_climatique,
        ])
        _accordeons = [mo.accordion({_LIBELLE_PERIODE: _bloc_periode})]
        if avec_materiau:
            _accordeons.append(mo.accordion({_LIBELLE_BATIMENT: choix_materiau_structure}))
        if parametres_analyse:
            _accordeons.append(mo.accordion(parametres_analyse))

        return mo.vstack([
            _qualite,
            mo.hstack(_accordeons, justify="start", align="start", wrap=True, widths="equal"),
        ])

    return (panneau_filtres,)


@app.cell(hide_code=True)
def filtres_communs(
    BILAN_EXCLUSIONS,
    CLASSE_INCONNUE,
    DATA_brut,
    LIBELLE_MATERIAU_NUL,
    cacher_inconnu,
    choix_de_attestation,
    choix_de_la_date,
    choix_materiau_structure,
    choix_valide_regles,
    choix_zone_climatique,
    mo,
    pl,
):
    # ============================================================================
    # CELLULE — Filtres temps réel COMMUNS à toutes les analyses
    # (logique recopiée de OPEE_by_GM v0.94, adaptée). Fournit :
    #   - FILTRES            : dict des sélections actives
    #   - SOUS_TITRE_FILTRES : texte résumant les filtres (sous-titre des graphiques)
    #   - appliquer_filtres  : DataFrame -> DataFrame filtré
    #   - resume_filtres     : encadré « filtres actifs + exclusions + nombre de
    #                          bâtiments », affiché sous le panneau de chaque analyse
    #   - valeurs_actives    : "tout sélectionné = pas de filtre"
    #
    # « Inconnu » = bâtiment dont l'écart au budget 2028 ne peut pas être calculé
    # (ic_composant, ic_chantier ou ic_construction_max_2028 manquant).
    # ============================================================================

    # ============================================================================
    # PARAMÈTRES (toutes les variables au même endroit)
    # ============================================================================
    _VALID_REGLES = choix_valide_regles.value
    _CACHER_INCONNU = cacher_inconnu.value
    _NB_BATIMENTS_EXTRAITS = DATA_brut.height
    _NB_PROJETS_EXTRAITS = DATA_brut["projet_id"].n_unique()


    def valeurs_actives(widget):
        """Sélection d'un widget sous forme de liste, remplacée par [] si
        TOUTES les options sont sélectionnées (= pas de filtre réel)."""
        valeur = widget.value
        valeur = [valeur] if isinstance(valeur, str) else list(valeur) if valeur is not None else []
        options = widget.options
        toutes = list(options.keys()) if isinstance(options, dict) else list(options)
        return [] if set(valeur) == set(toutes) else valeur


    # Sélections actives. annees_depot_pc est stocké en Int64 : le multiselect
    # renvoie des chaînes -> conversion en entiers.
    FILTRES = {
        "regles_validation": _VALID_REGLES,
        "annees": [int(a) for a in valeurs_actives(choix_de_la_date)],
        "attestations": valeurs_actives(choix_de_attestation),
        "zones": valeurs_actives(choix_zone_climatique),
        "materiaux": valeurs_actives(choix_materiau_structure),
        "cacher_inconnu": _CACHER_INCONNU,
    }


    def _resume(valeurs, si_vide="toutes"):
        return ", ".join(str(v) for v in valeurs) if valeurs else si_vide


    SOUS_TITRE_FILTRES = (
        f"Années de dépôt PC : {_resume(FILTRES['annees'])} — "
        f"Types d'attestation : {_resume(FILTRES['attestations'])} — "
        f"Zone climatique : {_resume(FILTRES['zones'])} — "
        f"Matériau structure : {_resume(FILTRES['materiaux'], 'tous')}"
    )


    # --- Filtre matériau : l'option "None" correspond aux matériaux NON renseignés
    def _expr_materiau(selection):
        _materiau = pl.col("dc_materiau_structure")
        _valeurs = [m for m in selection if m != LIBELLE_MATERIAU_NUL]
        _expr = _materiau.is_in(_valeurs).fill_null(False)
        if LIBELLE_MATERIAU_NUL in selection:
            _expr = _expr | _materiau.is_null() | (_materiau == LIBELLE_MATERIAU_NUL)
        return _expr


    def _liste_filtres(filtre_materiau, filtre_inconnu):
        """Filtres actifs : (libellé, actif ?, expression des bâtiments CONSERVÉS)."""
        return [
            ("règles de validation", FILTRES["regles_validation"],
             pl.col("regle_validation_globale") == True),
            ("années de dépôt", bool(FILTRES["annees"]),
             pl.col("annees_depot_pc").list.eval(pl.element().is_in(FILTRES["annees"])).list.any().fill_null(False)),
            ("type d'attestation", bool(FILTRES["attestations"]),
             pl.col("types_attestation").list.eval(pl.element().is_in(FILTRES["attestations"])).list.any().fill_null(False)),
            ("zone climatique", bool(FILTRES["zones"]),
             pl.col("zone_climatique").is_in(FILTRES["zones"])),
            ("matériau de structure", filtre_materiau and bool(FILTRES["materiaux"]),
             _expr_materiau(FILTRES["materiaux"])),
            ("masquer « Inconnu » (écart non calculable)", filtre_inconnu and FILTRES["cacher_inconnu"],
             pl.col("classe_2028") != CLASSE_INCONNUE),
        ]


    def appliquer_filtres(df, *, filtre_materiau=True, filtre_inconnu=True, verbeux=True):
        """Applique les filtres temps réel (polars, aucun appel réseau).
        `df` = DATA_base (périmètre après exclusions permanentes)."""
        if verbeux:
            print(f"Bâtiments au départ : {df.height}")
        for _libelle, _actif, _expression in _liste_filtres(filtre_materiau, filtre_inconnu):
            if _actif:
                df = df.filter(_expression)
                if verbeux:
                    print(f"  après filtre {_libelle} : {df.height}")
        return df


    def resume_filtres(df_filtre, *, avec_materiau=True, avec_inconnus=True):
        """Encadré affiché SOUS le panneau de filtres de chaque analyse :
        filtres actifs, exclusions permanentes, nombre de bâtiments et de projets
        (extraits, après exclusions, après filtres).
        `df_filtre` = résultat de appliquer_filtres(DATA_base, ...)."""
        # 1. Filtres actifs
        _qualite = ["bâtiments validés seulement" if _VALID_REGLES else "tous les bâtiments (non validés inclus)"]
        if avec_inconnus:
            _qualite.append("« Inconnu » masqués" if _CACHER_INCONNU else "« Inconnu » inclus")
        _periode = [
            f"années {_resume(FILTRES['annees'])}",
            f"attestations {_resume(FILTRES['attestations'])}",
            f"zones {_resume(FILTRES['zones'])}",
        ]
        _batiment = [f"matériaux {_resume(FILTRES['materiaux'], 'tous')}"] if avec_materiau else ["matériaux : non filtré"]

        # 2. Exclusions permanentes (lignes 2 et suivantes de BILAN_EXCLUSIONS)
        _exclusions = [
            f"- {_l['étape'].replace('Exclusion : ', '')} : **−{_l['bâtiments retirés']}** bâtiments"
            for _l in BILAN_EXCLUSIONS.iter_rows(named=True) if _l["bâtiments retirés"] is not None
        ]
        _apres_exclusions = BILAN_EXCLUSIONS.row(-1, named=True)

        # 3. Nombre de bâtiments et de projets
        _nb_filtre = df_filtre.height
        _nb_projets_filtre = df_filtre["projet_id"].n_unique() if _nb_filtre else 0

        return mo.callout(
            mo.md(
                "**Filtres actifs**  \n"
                f"**Qualité** : {' · '.join(_qualite)}  \n"
                f"**Période et lieu** : {' · '.join(_periode)}  \n"
                f"**Bâtiment** : {' · '.join(_batiment)}\n\n"
                "**Exclu de l'analyse (permanent)**\n\n"
                + "\n".join(_exclusions)
                + "\n\n**Nombre de bâtiments**\n\n"
                f"- Extraits (logements collectifs) : **{_NB_BATIMENTS_EXTRAITS}** "
                f"({_NB_PROJETS_EXTRAITS} projets)\n"
                f"- Après exclusions : **{_apres_exclusions['bâtiments restants']}** "
                f"({_apres_exclusions['projets restants']} projets)\n"
                f"- **Après filtres : {_nb_filtre}** ({_nb_projets_filtre} projets)"
            ),
            kind="neutral",
        )

    return FILTRES, SOUS_TITRE_FILTRES, appliquer_filtres, resume_filtres, valeurs_actives


@app.cell(hide_code=True)
def param_socle(mo, panneau_filtres):
    # ============================================================================
    # CELLULE — Contrôle du socle (étape A) : panneau de filtres
    # ============================================================================
    mo.vstack([
        mo.md("## Contrôle du socle\n\n*À valider avant de construire les analyses.*"),
        panneau_filtres(),
    ])
    return


@app.cell(hide_code=True)
def resume_socle(DATA_base, appliquer_filtres, resume_filtres):
    # Résumé SOUS les filtres : filtres actifs, exclusions, nombre de bâtiments.
    # (Cellule séparée : elle lit les valeurs des widgets, le panneau reste statique.)
    DATA_socle = appliquer_filtres(DATA_base, verbeux=False)
    resume_filtres(DATA_socle)
    return (DATA_socle,)


@app.cell(hide_code=True)
def apercu_socle(
    BILAN_EXCLUSIONS,
    CLASSES_2028,
    CLASSE_INCONNUE,
    COLS_MACRO_LOTS,
    DATA_socle,
    boutons_export,
    mo,
    pl,
):
    # ============================================================================
    # CELLULE — Contrôle du socle : tableau des exclusions, statistiques des
    # colonnes calculées et aperçu ligne par ligne (bâtiments filtrés).
    # ============================================================================

    # ---- Variables -------------------------------------------------------------
    _COLS_CONTROLE = [
        "ic_construction", "ic_composant", "ic_chantier", "ic_construction_max_2028",
        "budget_composant_2028", "ecart_2028", "ecart_2028_pct",
        "sref", "nb_logements_estime", "taux_vitrage_pct", "ratio_facade",
        "parking_infra_par_logement", "hauteur_hors_toiture",
        *COLS_MACRO_LOTS.values(),
    ]
    _COLS_APERCU = ["ID", "projet_id", "annee_depot", "zone_climatique", "classe_2028", "sref_plateau", *_COLS_CONTROLE]

    # 1. Contrôles de cohérence (écart toléré : arrondis)
    #    a. ic_construction = ic_composant + ic_chantier ?
    #    b. ic_composant = gros œuvre + second œuvre + lots techniques ?
    _TOL_SOMME = 0.5     # kg/m²
    _nb_incoherents = DATA_socle.filter(
        (pl.col("ic_construction") - pl.col("ic_composant") - pl.col("ic_chantier")).abs() > _TOL_SOMME
    ).height
    _nb_incoherents_lots = DATA_socle.filter(
        (pl.sum_horizontal([pl.col(c) for c in COLS_MACRO_LOTS.values()]) - pl.col("ic_composant")).abs() > _TOL_SOMME
    ).height

    # 2. Répartition brute par classe (simple contrôle, l'Analyse1 viendra ensuite)
    _ordre = {c: i for i, c in enumerate(CLASSES_2028 + [CLASSE_INCONNUE])}
    _classes = (
        DATA_socle.group_by("classe_2028").agg(pl.len().alias("bâtiments"))
        .sort(pl.col("classe_2028").replace_strict(_ordre, default=99))
    )

    # 3. Statistiques des colonnes calculées
    _stats = DATA_socle.select(_COLS_CONTROLE).describe()

    mo.vstack([
        mo.md("### Exclusions permanentes"),
        mo.ui.table(BILAN_EXCLUSIONS, selection=None),
        mo.md(
            f"**Contrôles** (à {_TOL_SOMME} kg/m² près, sur {DATA_socle.height} bâtiments filtrés)  \n"
            f"- `ic_construction = ic_composant + ic_chantier` : **{_nb_incoherents}** bâtiment(s) incohérent(s)  \n"
            f"- `ic_composant = somme des 3 macro-lots` : **{_nb_incoherents_lots}** bâtiment(s) incohérent(s)"
        ),
        mo.md("### Répartition par classe (contrôle)"),
        mo.ui.table(_classes, selection=None),
        mo.md("### Statistiques des colonnes calculées"),
        mo.ui.table(_stats, selection=None),
        mo.md("### Aperçu des bâtiments filtrés"),
        mo.ui.table(DATA_socle.select(_COLS_APERCU), selection=None),
        boutons_export(DATA_socle, "socle_batiments_filtres"),
    ])
    return


# ================================================================================
# ANALYSE1 — Classes d'écart au budget composant 2028 et indice de difficulté
# ================================================================================


@app.cell(hide_code=True)
def widgets_analyse1(mo):
    # ============================================================================
    # CELLULE — Analyse1 : widget propre à l'analyse (défini à part pour que le
    # panneau reste statique et que le graphique lise sa valeur).
    # ============================================================================
    compter_par_batiment_a1 = mo.ui.switch(label="Compter par bâtiment (sinon par projet)", value=False)
    return (compter_par_batiment_a1,)


@app.cell(hide_code=True)
def param_analyse1(ANALYSES, compter_par_batiment_a1, mo, panneau_filtres):
    # ============================================================================
    # CELLULE — Analyse1 : titre, lecture et panneau de filtres
    # ============================================================================
    mo.vstack([
        mo.md(
            f"## Analyse1 — {ANALYSES[1]}\n\n"
            "Chaque projet est classé selon l'**écart de son IC composant au budget composant 2028** "
            "(`ic_composant − (ic_construction_max_2028 − ic_chantier)`). Un projet de plusieurs "
            "bâtiments est classé sur son bâtiment **le plus éloigné** du budget.  \n"
            "**Indice de difficulté** = part des projets à **plus de 30 kgCO₂e/m²** du budget "
            "(au-delà des leviers « simples »), calculée sur les projets classables (hors « Inconnu »)."
        ),
        panneau_filtres(bascules_analyse=(compter_par_batiment_a1,)),
    ])
    return


@app.cell(hide_code=True)
def resume_analyse1(DATA_base, appliquer_filtres, resume_filtres):
    # Résumé SOUS les filtres (cellule séparée : elle lit les valeurs des widgets).
    DATA_a1 = appliquer_filtres(DATA_base, verbeux=False)
    resume_filtres(DATA_a1)
    return (DATA_a1,)


@app.cell(hide_code=True)
def graphique_analyse1(
    ANALYSES,
    BORNES_CLASSES,
    CLASSES_2028,
    CLASSES_DIFFICILES,
    CLASSE_INCONNUE,
    COULEURS_CLASSES,
    DATA_a1,
    SEUIL_DIFFICULTE,
    SOUS_TITRE_FILTRES,
    boutons_export,
    compter_par_batiment_a1,
    expr_classe_2028,
    go,
    mo,
    pl,
):
    # ============================================================================
    # CELLULE — Analyse1 : nombre de projets par classe, part du total et indice
    # de difficulté.
    #
    #   1. Unité comptée : projet (classé sur son bâtiment le plus éloigné du
    #      budget) ou bâtiment (bascule « Compter par bâtiment »)
    #   2. Comptage par classe, part des classables, part cumulée
    #   3. Chiffres clés (nombre, part conforme, indice de difficulté)
    #   4. Graphique en barres : une barre par classe, étiquette « nombre + % »,
    #      accolade sur les classes « difficiles » (> 30 kg)
    #   5. Tableau et exports
    #
    # Les parts sont calculées sur les projets CLASSABLES : « Inconnu » (écart non
    # calculable) est compté à part et n'entre pas dans le dénominateur.
    # ============================================================================

    # ---- Variables -------------------------------------------------------------
    _PAR_BATIMENT = compter_par_batiment_a1.value
    _UNITE = "bâtiments" if _PAR_BATIMENT else "projets"
    _COULEUR_TEXTE = "#333333"
    _COULEUR_TEXTE_SECONDAIRE = "#6b6b6b"
    _BORNES_TEXTE = {
        CLASSES_2028[0]: "écart ≤ 0",
        CLASSES_2028[1]: f"0 < écart < {BORNES_CLASSES[0]}",
        CLASSES_2028[2]: f"{BORNES_CLASSES[0]} ≤ écart < {BORNES_CLASSES[1]}",
        CLASSES_2028[3]: f"{BORNES_CLASSES[1]} ≤ écart < {BORNES_CLASSES[2]}",
        CLASSES_2028[4]: f"écart ≥ {BORNES_CLASSES[2]}",
        CLASSE_INCONNUE: "écart non calculable",
    }

    # 1. Unité comptée ------------------------------------------------------------
    if _PAR_BATIMENT:
        _unites = DATA_a1.select("projet_id", "ID", "ecart_2028", "classe_2028")
    else:
        # max() ignore les NULL : un projet n'est « Inconnu » que si AUCUN de ses
        # bâtiments n'a d'écart calculable.
        _unites = (
            DATA_a1.group_by("projet_id")
            .agg(pl.col("ecart_2028").max(), pl.len().alias("nb_batiments"))
            .with_columns(expr_classe_2028().alias("classe_2028"))
        )

    # 2. Comptage par classe ------------------------------------------------------
    _ordre = CLASSES_2028 + [CLASSE_INCONNUE]
    _comptes = dict(_unites.group_by("classe_2028").len().iter_rows())
    _nb = {c: _comptes.get(c, 0) for c in _ordre}
    _nb_classables = sum(_nb[c] for c in CLASSES_2028)
    _nb_inconnus = _nb[CLASSE_INCONNUE]


    def _part(n):
        return 100 * n / _nb_classables if _nb_classables else 0.0


    _cumul, _lignes = 0, []
    for _c in CLASSES_2028:
        _cumul += _nb[_c]
        _lignes.append({
            "classe": _c, "bornes (kgCO₂e/m²)": _BORNES_TEXTE[_c], _UNITE: _nb[_c],
            "part (%)": round(_part(_nb[_c]), 1), "part cumulée (%)": round(_part(_cumul), 1),
        })
    _lignes.append({
        "classe": CLASSE_INCONNUE, "bornes (kgCO₂e/m²)": _BORNES_TEXTE[CLASSE_INCONNUE],
        _UNITE: _nb_inconnus, "part (%)": None, "part cumulée (%)": None,
    })
    TABLEAU_A1 = pl.DataFrame(_lignes)

    # 3. Chiffres clés ------------------------------------------------------------
    _part_conforme = _part(_nb[CLASSES_2028[0]])
    INDICE_DIFFICULTE = _part(sum(_nb[c] for c in CLASSES_DIFFICILES))
    _chiffres = mo.hstack([
        mo.stat(value=f"{_nb_classables}", label=f"{_UNITE.capitalize()} classés",
                caption=f"+ {_nb_inconnus} « Inconnu »" if _nb_inconnus else "aucun « Inconnu »"),
        mo.stat(value=f"{_part_conforme:.0f} %", label="Déjà conformes 2028",
                caption=f"{_nb[CLASSES_2028[0]]} {_UNITE}"),
        mo.stat(value=f"{INDICE_DIFFICULTE:.0f} %", label="Indice de difficulté",
                caption=f"{_UNITE} à plus de {SEUIL_DIFFICULTE} kg du budget"),
    ], justify="start", gap=2)

    # 4. Graphique ----------------------------------------------------------------
    _classes_tracees = CLASSES_2028 + ([CLASSE_INCONNUE] if _nb_inconnus else [])
    _y = [_nb[c] for c in _classes_tracees]
    _etiquettes = [
        f"<b>{_nb[c]}</b><br>{_part(_nb[c]):.0f} %" if c != CLASSE_INCONNUE else f"<b>{_nb[c]}</b>"
        for c in _classes_tracees
    ]
    _survol = [
        f"{_nb[c]} {_UNITE} — {_part(_nb[c]):.1f} % des classés" if c != CLASSE_INCONNUE
        else f"{_nb[c]} {_UNITE} — hors dénominateur"
        for c in _classes_tracees
    ]
    _fig = go.Figure(go.Bar(
        x=_classes_tracees, y=_y,
        marker={"color": [COULEURS_CLASSES[c] for c in _classes_tracees], "cornerradius": 4},
        text=_etiquettes, textposition="outside", cliponaxis=False,
        textfont={"color": _COULEUR_TEXTE, "size": 13},
        customdata=[[_BORNES_TEXTE[c], _s] for c, _s in zip(_classes_tracees, _survol)],
        hovertemplate="<b>%{x}</b> (%{customdata[0]} kgCO₂e/m²)<br>%{customdata[1]}<extra></extra>",
        showlegend=False,
    ))

    # Accolade au-dessus des classes « difficiles » : indice de difficulté
    _y_max = max(_y) if _y and max(_y) else 1
    _y_accolade = _y_max * 1.32
    # Axe catégoriel : la i-ème classe est à l'abscisse i -> accolade du bord
    # gauche de la 1re barre « difficile » au bord droit de la dernière.
    _x0 = _classes_tracees.index(CLASSES_DIFFICILES[0]) - 0.42
    _x1 = _classes_tracees.index(CLASSES_DIFFICILES[-1]) + 0.42
    _fig.add_shape(type="line", xref="x", yref="y", x0=_x0, x1=_x1, y0=_y_accolade, y1=_y_accolade,
                   line={"color": _COULEUR_TEXTE_SECONDAIRE, "width": 1.5})
    for _x in (_x0, _x1):
        _fig.add_shape(type="line", xref="x", yref="y", x0=_x, x1=_x,
                       y0=_y_accolade, y1=_y_accolade * 0.95,
                       line={"color": _COULEUR_TEXTE_SECONDAIRE, "width": 1.5})
    _fig.add_annotation(
        x=(_x0 + _x1) / 2, y=_y_accolade, yshift=14, showarrow=False,
        text=f"<b>Indice de difficulté : {INDICE_DIFFICULTE:.0f} %</b> des {_UNITE} à plus de {SEUIL_DIFFICULTE} kg",
        font={"color": _COULEUR_TEXTE, "size": 13},
    )

    _fig.update_layout(
        height=520, width=None, template="plotly_white", bargap=0.18,
        title={"text": (
            f"<b>Analyse1 — {ANALYSES[1]}</b> — par {_UNITE[:-1]}<br>"
            f"<sup>{SOUS_TITRE_FILTRES}</sup>"
        )},
        xaxis={"title": "Écart de l'IC composant au budget composant 2028 (kgCO₂e/m²)",
               "type": "category", "categoryorder": "array", "categoryarray": _classes_tracees},
        yaxis={"title": f"Nombre de {_UNITE}", "rangemode": "tozero",
               "range": [0, _y_max * 1.5], "gridcolor": "#ececec"},
        margin={"l": 60, "r": 20, "t": 90, "b": 60},
    )

    # 5. Affichage : chiffres clés, graphique, tableau, exports -------------------
    _detail = _unites.sort("ecart_2028", descending=True, nulls_last=True)
    mo.vstack([
        _chiffres,
        mo.ui.plotly(_fig),
        mo.accordion({"Tableau des classes": mo.vstack([
            mo.ui.table(TABLEAU_A1, selection=None),
            boutons_export(TABLEAU_A1, f"analyse1_classes_par_{_UNITE}"),
        ]), f"Détail des {_UNITE} classés": mo.vstack([
            mo.ui.table(_detail, selection=None),
            boutons_export(_detail, f"analyse1_detail_{_UNITE}"),
        ])}),
    ])
    return INDICE_DIFFICULTE, TABLEAU_A1


# ================================================================================
# ANALYSE2 — Profil des classes : forme, programme, technique et méthode
# ================================================================================


@app.cell(hide_code=True)
def widgets_analyse2(CLASSES_2028, CLASSES_DIFFICILES, mo):
    # ============================================================================
    # CELLULE — Analyse2 : widgets propres à l'analyse
    #   - groupe_a_a2 / groupe_b_a2 : groupes de classes comparés (tornade, et
    #     tableaux en mode « Comparer »)
    #   - periode_a2 : période étudiée, ou comparaison des deux périodes
    # PERIODES_A2 : découpage des années de dépôt (modifiable ICI).
    # ============================================================================

    # ---- Variables -------------------------------------------------------------
    PERIODES_A2 = {"2022-2023": [2022, 2023], "2024-2025": [2024, 2025]}
    MODE_TOUTES_A2 = "Toutes"
    MODE_COMPARER_A2 = "Comparer " + " / ".join(PERIODES_A2)
    _GROUPES_A = {
        "Conforme 2028": [CLASSES_2028[0]],
        "Conforme 2028 + < 30 kg": CLASSES_2028[:2],
    }
    _GROUPES_B = {
        "> 30 kg (30 à 80, 80 à 130, > 130)": CLASSES_DIFFICILES,
        "> 130 kg": [CLASSES_2028[4]],
        "80 à 130 kg + > 130 kg": CLASSES_2028[3:],
        "< 30 kg": [CLASSES_2028[1]],
    }

    groupe_a_a2 = mo.ui.dropdown(options=_GROUPES_A, value="Conforme 2028", label="Groupe de référence (A)")
    groupe_b_a2 = mo.ui.dropdown(
        options=_GROUPES_B, value="> 30 kg (30 à 80, 80 à 130, > 130)", label="Groupe comparé (B)"
    )
    periode_a2 = mo.ui.radio(
        options=[MODE_TOUTES_A2, *PERIODES_A2, MODE_COMPARER_A2], value=MODE_TOUTES_A2,
        inline=True, label="**Période de dépôt du PC**",
    )
    return MODE_COMPARER_A2, MODE_TOUTES_A2, PERIODES_A2, groupe_a_a2, groupe_b_a2, periode_a2


@app.cell(hide_code=True)
def param_analyse2(ANALYSES, groupe_a_a2, groupe_b_a2, mo, panneau_filtres):
    # ============================================================================
    # CELLULE — Analyse2 : titre, lecture et panneau de filtres
    # ============================================================================
    mo.vstack([
        mo.md(
            f"## Analyse2 — {ANALYSES[2]}\n\n"
            "Ce qui change quand on s'éloigne du budget composant 2028. Comptage **par bâtiment** "
            "(chaque bâtiment porte sa propre classe et ses propres indicateurs).  \n"
            "**2a.** Médiane de chaque indicateur par classe (dégradé ligne par ligne).  \n"
            "**2b.** Répartition des choix constructifs et techniques par classe (% des bâtiments).  \n"
            "**2c.** Tornade : écart de médiane entre deux groupes de classes, du plus fort au plus faible.  \n"
            "Le sélecteur **Période** (sous le résumé des filtres) restreint l'analyse à une période, "
            "ou compare les deux : un écart présent dans les deux périodes est un levier stable ; "
            "présent dans une seule, il traduit plutôt l'évolution des pratiques ou des données."
        ),
        panneau_filtres({
            "Analyse2 : groupes comparés": mo.vstack([
                groupe_a_a2, groupe_b_a2,
                mo.md("*Utilisés par la tornade, et par les tableaux en mode « Comparer ».*"),
            ]),
        }),
    ])
    return


@app.cell(hide_code=True)
def resume_analyse2(DATA_base, appliquer_filtres, resume_filtres):
    # Résumé SOUS les filtres (cellule séparée : elle lit les valeurs des widgets).
    DATA_a2 = appliquer_filtres(DATA_base, verbeux=False)
    resume_filtres(DATA_a2)
    return (DATA_a2,)


@app.cell(hide_code=True)
def selecteur_periode_a2(CLASSES_2028, DATA_a2, PERIODES_A2, mo, periode_a2, pl):
    # ============================================================================
    # CELLULE — Analyse2 : sélecteur de période, juste au-dessus des résultats,
    # avec le nombre de bâtiments classés par période (après filtres).
    # Année d'un bâtiment = plus ancienne année de dépôt de PC de son projet.
    # ============================================================================
    _classes = DATA_a2.filter(pl.col("classe_2028").is_in(CLASSES_2028))
    _effectifs = " · ".join(
        f"{_nom} : **{_classes.filter(pl.col('annee_depot').is_in(_annees)).height}** bâtiments"
        for _nom, _annees in PERIODES_A2.items()
    )
    mo.vstack([
        periode_a2,
        mo.md(f"<small>Bâtiments classés par période (après filtres) : {_effectifs}. "
              "Année = plus ancienne année de dépôt de PC du projet.</small>"),
    ])
    return


@app.cell(hide_code=True)
def calcul_analyse2(
    CLASSES_2028,
    COULEURS_CLASSES,
    DATA_a2,
    MODE_COMPARER_A2,
    MODE_TOUTES_A2,
    PERIODES_A2,
    groupe_a_a2,
    groupe_b_a2,
    periode_a2,
    pl,
):
    # ============================================================================
    # CELLULE — Analyse2 : calculs (aucun affichage)
    #
    #   1. Colonnes dérivées (sref hors plateau, udd en %, part de DED, catégories)
    #      et période de chaque bâtiment
    #   2. Colonnes des tableaux, selon la période choisie :
    #        - « Toutes » ou une période : une colonne par classe
    #        - « Comparer »              : A et B × deux périodes (4 colonnes)
    #   3. PROFIL_A2      : médiane de chaque indicateur numérique par colonne
    #      COMPOSITION_A2 : part des bâtiments par catégorie, par colonne
    #   4. TORNADE_A2     : écart de médiane B − A, rapporté à l'écart
    #      interquartile (IQR) de l'ensemble, pour chaque période comparée
    #
    # « Inconnu » (écart non calculable) n'a pas de profil : il est écarté.
    # Une médiane calculée sur moins de N_MIN_A2 bâtiments est grisée (tableaux)
    # ou écartée (tornade).
    # ============================================================================

    # ---- Variables -------------------------------------------------------------
    N_MIN_A2 = 5                       # bâtiments renseignés minimum
    _MODE = periode_a2.value
    COMPARER_A2 = _MODE == MODE_COMPARER_A2
    _CLASSES_A, _CLASSES_B = groupe_a_a2.value, groupe_b_a2.value
    NOM_A_A2, NOM_B_A2 = groupe_a_a2.selected_key, groupe_b_a2.selected_key

    # (famille, colonne, libellé, nombre de décimales)
    INDICATEURS_A2 = [
        ("Forme", "taux_vitrage_pct", "Taux de vitrage (% de la sref)", 1),
        ("Forme", "ratio_facade", "Murs / sref (m²/m²)", 2),
        ("Forme", "hauteur_hors_toiture", "Hauteur hors toiture (m)", 1),
        ("Forme", "sref_fiable", "Sref (m², hors « plateau »)", 0),
        ("Programme", "parking_infra_par_logement", "Places de parking en infra / logement", 2),
        ("Programme", "nb_ascenseur", "Nombre d'ascenseurs", 1),
        ("Programme", "nb_logements_estime", "Logements estimés (sref / 70)", 0),
        ("Constructif", "stock_c", "Stockage carbone (kgC/m²)", 1),
        ("Lots", "ic_composant_lot_8", "Lot 8 : CVC (kgCO₂e/m²)", 1),
        ("Lots", "ic_composant_sous_lot_8_1", "dont sous-lot 8.1 : production chaud / froid (kgCO₂e/m²)", 1),
        ("Lots", "ic_composant_lot_9", "Lot 9 : installations sanitaires (kgCO₂e/m²)", 1),
        ("Méthode", "udd_pct", "Part d'impact des données par défaut (udd, %)", 1),
        ("Méthode", "part_ded_pct", "Part de DED en nombre de fiches (%)", 1),
        ("Méthode", "nb_total_fiche_acv", "Nombre de fiches (total)", 0),
        ("Méthode", "nb_fdes", "Nombre de FDES", 0),
        ("Méthode", "nb_pep", "Nombre de PEP", 0),
    ]
    # Catégories : (famille, colonne, nombre de modalités gardées, les autres -> « Autres »)
    _CATEGORIES = [
        ("Structure (dc_, à lire avec prudence)", "structure", 5),
        ("Générateur de chauffage", "generateur", 5),
        ("Ventilation", "ventilation", 3),
        ("Réseau de chaleur", "reseau", 2),
    ]
    _LIBELLE_AUTRES = "Autres"
    _LIBELLE_NON_RENSEIGNE = "Non renseigné"

    # 1. Colonnes dérivées et période ---------------------------------------------
    _ventil = pl.col("l_type_ventilation_mecanique").cast(pl.Utf8)
    _periode = pl.lit(None, dtype=pl.Utf8)
    for _nom, _annees in reversed(list(PERIODES_A2.items())):
        _periode = pl.when(pl.col("annee_depot").is_in(_annees)).then(pl.lit(_nom)).otherwise(_periode)
    DATA_a2_profil = (
        DATA_a2.filter(pl.col("classe_2028").is_in(CLASSES_2028))
        .with_columns(
            _periode.alias("periode"),
            pl.when(pl.col("sref_plateau")).then(None).otherwise(pl.col("sref")).alias("sref_fiable"),
            (pl.col("udd") * 100).alias("udd_pct"),
            (pl.col("nb_ded") / pl.col("nb_total_fiche_acv") * 100).alias("part_ded_pct"),
            # Catégories (texte), NULL -> « Non renseigné »
            pl.col("dc_materiau_structure").fill_null(_LIBELLE_NON_RENSEIGNE).alias("structure"),
            pl.col("famille_synthese_generateur_ch").cast(pl.Utf8).fill_null(_LIBELLE_NON_RENSEIGNE).alias("generateur"),
            pl.when(_ventil.is_null()).then(pl.lit(_LIBELLE_NON_RENSEIGNE))
            .when(_ventil.str.contains("DF|[Dd]ouble")).then(pl.lit("Double flux"))
            .when(_ventil.str.contains("SF|[Ss]imple")).then(pl.lit("Simple flux"))
            .otherwise(pl.lit("Autre ventilation")).alias("ventilation"),
            pl.when(pl.col("presence_reseau").cast(pl.Utf8).str.to_lowercase().is_in(["1", "true", "vrai"]))
            .then(pl.lit("Raccordé à un réseau"))
            .otherwise(pl.lit("Non raccordé")).alias("reseau"),
        )
    )
    _df = DATA_a2_profil
    if _MODE not in (MODE_TOUTES_A2, MODE_COMPARER_A2):
        _df = _df.filter(pl.col("periode") == _MODE)

    # 2. Colonnes des tableaux : (libellé, expression de sélection, couleur) -------
    _classe = pl.col("classe_2028")
    if COMPARER_A2:
        COLONNES_A2 = [
            (f"{_lettre} · {_p}", _classe.is_in(_classes) & (pl.col("periode") == _p), _couleur)
            for _lettre, _classes, _couleur in (
                ("A", _CLASSES_A, COULEURS_CLASSES[_CLASSES_A[0]]),
                ("B", _CLASSES_B, COULEURS_CLASSES[_CLASSES_B[0]]),
            )
            for _p in PERIODES_A2
        ]
    else:
        COLONNES_A2 = [(_c, _classe == _c, COULEURS_CLASSES[_c]) for _c in CLASSES_2028]
    _sous_df = {_lib: _df.filter(_expr) for _lib, _expr, _ in COLONNES_A2}
    NB_PAR_COLONNE_A2 = {_lib: _d.height for _lib, _d in _sous_df.items()}

    # 3a. Médianes ------------------------------------------------------------------
    _lignes = []
    for _famille, _col, _libelle, _dec in INDICATEURS_A2:
        _ligne = {"famille": _famille, "indicateur": _libelle, "colonne": _col, "décimales": _dec}
        for _lib, _d in _sous_df.items():
            _serie = _d[_col].cast(pl.Float64).drop_nulls()
            _ligne[_lib] = _serie.median() if _serie.len() else None
            _ligne[f"n {_lib}"] = _serie.len()
        _lignes.append(_ligne)
    # Cast explicite : une colonne vide (aucun bâtiment) serait sinon de type Null
    _LIBELLES = [_lib for _lib, _, _ in COLONNES_A2]
    PROFIL_A2 = pl.DataFrame(_lignes).with_columns([pl.col(_lib).cast(pl.Float64) for _lib in _LIBELLES])

    # 3b. Parts des catégories (% des bâtiments de la colonne) -----------------------
    _lignes = []
    for _famille, _col, _nb_gardees in _CATEGORIES:
        _gardees = (
            _df.filter(pl.col(_col) != _LIBELLE_NON_RENSEIGNE)
            .group_by(_col).len().sort("len", descending=True)[_col].head(_nb_gardees).to_list()
        )
        _cat = (
            pl.when(pl.col(_col).is_in(_gardees + [_LIBELLE_NON_RENSEIGNE])).then(pl.col(_col))
            .otherwise(pl.lit(_LIBELLE_AUTRES))
        )
        for _modalite in _gardees + [_LIBELLE_AUTRES, _LIBELLE_NON_RENSEIGNE]:
            _ligne = {"famille": _famille, "modalité": _modalite}
            _presente = False
            for _lib, _d in _sous_df.items():
                _n = _d.filter(_cat == _modalite).height
                _ligne[_lib] = 100 * _n / _d.height if _d.height else None
                _ligne[f"n {_lib}"] = _d.height
                _presente = _presente or _n > 0
            if _presente:
                _lignes.append(_ligne)
    COMPOSITION_A2 = pl.DataFrame(_lignes).with_columns([pl.col(_lib).cast(pl.Float64) for _lib in _LIBELLES])

    # 4. Tornade : une comparaison A vs B par période (une seule hors « Comparer »)
    _periodes_tornade = list(PERIODES_A2) if COMPARER_A2 else [_MODE]
    _lignes, ECARTES_A2 = [], []
    for _p in _periodes_tornade:
        _dp = _df.filter(pl.col("periode") == _p) if _p in PERIODES_A2 else _df
        _df_a, _df_b = _dp.filter(_classe.is_in(_CLASSES_A)), _dp.filter(_classe.is_in(_CLASSES_B))
        for _famille, _col, _libelle, _dec in INDICATEURS_A2:
            _a = _df_a[_col].cast(pl.Float64).drop_nulls()
            _b = _df_b[_col].cast(pl.Float64).drop_nulls()
            _tout = _dp[_col].cast(pl.Float64).drop_nulls()
            _iqr = (_tout.quantile(0.75) - _tout.quantile(0.25)) if _tout.len() else None
            if _a.len() < N_MIN_A2 or _b.len() < N_MIN_A2 or not _iqr:
                ECARTES_A2.append(f"{_libelle} ({_p})" if COMPARER_A2 else _libelle)
                continue
            _med_a, _med_b = _a.median(), _b.median()
            _lignes.append({
                "période": _p, "famille": _famille, "indicateur": _libelle,
                "médiane A": round(_med_a, _dec), "médiane B": round(_med_b, _dec),
                "écart B − A": round(_med_b - _med_a, _dec), "IQR ensemble": round(_iqr, _dec),
                "écart en IQR": round((_med_b - _med_a) / _iqr, 2),
                "n A": _a.len(), "n B": _b.len(), "décimales": _dec,
            })
    TORNADE_A2 = pl.DataFrame(_lignes) if _lignes else pl.DataFrame(
        schema={"période": pl.Utf8, "indicateur": pl.Utf8, "écart en IQR": pl.Float64}
    )
    return (
        COLONNES_A2,
        COMPARER_A2,
        COMPOSITION_A2,
        ECARTES_A2,
        NB_PAR_COLONNE_A2,
        NOM_A_A2,
        NOM_B_A2,
        N_MIN_A2,
        PROFIL_A2,
        TORNADE_A2,
    )


@app.cell(hide_code=True)
def tableaux_analyse2(
    COLONNES_A2,
    COMPARER_A2,
    COMPOSITION_A2,
    NB_PAR_COLONNE_A2,
    NOM_A_A2,
    NOM_B_A2,
    N_MIN_A2,
    PROFIL_A2,
    boutons_export,
    mo,
    pl,
):
    # ============================================================================
    # CELLULE — Analyse2 : 2a (médianes) et 2b (répartition des catégories), en
    # tableaux à dégradé de couleur.
    #
    # Dégradé calculé LIGNE PAR LIGNE : la cellule la plus foncée est la colonne
    # où l'indicateur est le plus élevé. Une seule teinte (jaune du HUB) ; la
    # valeur est toujours écrite, la couleur n'est qu'un repère.
    # Cellule grisée = médiane calculée sur moins de N_MIN_A2 bâtiments.
    # ============================================================================

    # ---- Variables -------------------------------------------------------------
    _TEINTE_RVB = (253, 185, 19)       # jaune du HUB
    _OPACITE_MIN, _OPACITE_MAX = 0.06, 0.75
    _COULEUR_TEXTE = "#222222"
    _COULEUR_GRISE = "#b5b4b0"
    _LIBELLES = [_lib for _lib, _, _ in COLONNES_A2]


    def _style_degrade(df, effectifs, colonnes):
        """style_cell pour mo.ui.table : dégradé par ligne sur `colonnes`, en
        ignorant (et grisant) les cellules calculées sur trop peu de bâtiments."""
        _styles = {}
        for _i, (_valeurs, _n) in enumerate(zip(df.select(colonnes).iter_rows(), effectifs.iter_rows())):
            _fiables = [v for v, n in zip(_valeurs, _n) if v is not None and n >= N_MIN_A2]
            _bas, _haut = (min(_fiables), max(_fiables)) if _fiables else (0, 0)
            for _col, _v, _nb in zip(colonnes, _valeurs, _n):
                if _v is None:
                    continue
                if _nb < N_MIN_A2:
                    _styles[(str(_i), _col)] = {"color": _COULEUR_GRISE}
                    continue
                _t = (_v - _bas) / (_haut - _bas) if _haut > _bas else 0.0
                _a = _OPACITE_MIN + _t * (_OPACITE_MAX - _OPACITE_MIN)
                _styles[(str(_i), _col)] = {
                    "backgroundColor": f"rgba({_TEINTE_RVB[0]},{_TEINTE_RVB[1]},{_TEINTE_RVB[2]},{_a:.2f})",
                    "color": _COULEUR_TEXTE,
                }

        def _style(ligne, colonne, valeur):
            return _styles.get((str(ligne), colonne), {})
        return _style


    # En-têtes : libellé de colonne + nombre de bâtiments (change avec les filtres)
    _entetes = {_lib: f"{_lib} (n={NB_PAR_COLONNE_A2[_lib]})" for _lib in _LIBELLES}
    _cols = list(_entetes.values())
    _effectifs_profil = PROFIL_A2.select([f"n {_lib}" for _lib in _LIBELLES])
    _effectifs_compo = COMPOSITION_A2.select([f"n {_lib}" for _lib in _LIBELLES])

    # 2a. Médianes, arrondies selon l'indicateur
    _profil = PROFIL_A2.with_columns([
        pl.struct(_lib, "décimales").map_elements(
            lambda s, _lib=_lib: None if s[_lib] is None else round(s[_lib], s["décimales"]),
            return_dtype=pl.Float64,
        ).alias(_lib)
        for _lib in _LIBELLES
    ]).select("famille", "indicateur", *_LIBELLES).rename(_entetes)

    # 2b. Parts des catégories (%)
    _compo = COMPOSITION_A2.with_columns(
        [pl.col(_lib).round(0) for _lib in _LIBELLES]
    ).select("famille", "modalité", *_LIBELLES).rename(_entetes)

    _legende = (
        f"*Mode « Comparer » : **A** = {NOM_A_A2}, **B** = {NOM_B_A2}, pour chaque période.*  \n"
        if COMPARER_A2 else ""
    ) + f"*Cellule grisée : moins de {N_MIN_A2} bâtiments renseignés.*"

    mo.vstack([
        mo.md("### 2a. Médiane des indicateurs" + (" (A et B par période)" if COMPARER_A2 else " par classe")),
        mo.md(_legende),
        mo.ui.table(_profil, selection=None, pagination=False, show_download=False,
                    style_cell=_style_degrade(_profil, _effectifs_profil, _cols)),
        boutons_export(PROFIL_A2, "analyse2a_medianes"),
        mo.md("### 2b. Choix constructifs et techniques (% des bâtiments de la colonne)"),
        mo.ui.table(_compo, selection=None, pagination=False, show_download=False,
                    style_cell=_style_degrade(_compo, _effectifs_compo, _cols)),
        boutons_export(COMPOSITION_A2, "analyse2b_categories"),
    ])
    return


@app.cell(hide_code=True)
def tornade_analyse2(
    COMPARER_A2,
    COULEURS_CLASSES,
    ECARTES_A2,
    NOM_A_A2,
    NOM_B_A2,
    N_MIN_A2,
    PERIODES_A2,
    SOUS_TITRE_FILTRES,
    TORNADE_A2,
    boutons_export,
    go,
    mo,
    periode_a2,
    pl,
):
    # ============================================================================
    # CELLULE — Analyse2 : 2c. Tornade A vs B
    #
    # Longueur de barre = (médiane B − médiane A) / écart interquartile (IQR) de
    # l'ensemble : comparable entre indicateurs d'unités différentes, et défini
    # même quand la médiane A vaut 0. Tri du plus fort au plus faible écart.
    #   - une période (ou toutes) : rouge = plus élevé dans B, bleu = dans A
    #   - mode « Comparer »       : deux barres par indicateur, gris clair =
    #     1re période, gris foncé = 2e période ; le sens se lit à gauche / droite
    # ============================================================================

    # ---- Variables -------------------------------------------------------------
    _COULEUR_A = COULEURS_CLASSES["Conforme 2028"]
    _COULEUR_B = COULEURS_CLASSES["30 à 80 kg"]
    _COULEURS_PERIODES = dict(zip(PERIODES_A2, ["#a3a29d", "#45443f"]))   # rampe grise validée
    _COULEUR_TEXTE = "#333333"
    _HAUTEUR_LIGNE = 52 if COMPARER_A2 else 34


    def _fmt(v, d):
        return f"{v:,.{d}f}".replace(",", " ")


    if TORNADE_A2.height == 0:
        _sortie = mo.callout(mo.md(
            f"Pas assez de bâtiments pour comparer « {NOM_A_A2} » et « {NOM_B_A2} » "
            f"(minimum {N_MIN_A2} bâtiments renseignés par groupe)."
        ), kind="warn")
    else:
        # Ordre des indicateurs : plus fort écart (en valeur absolue, max des périodes)
        # en haut ; plotly trace de bas en haut -> tri croissant.
        _ordre = (
            TORNADE_A2.group_by("indicateur").agg(pl.col("écart en IQR").abs().max().alias("_tri"))
            .sort("_tri")["indicateur"].to_list()
        )
        _y_cat = [f"{_i}  " for _i in _ordre]
        _fig = go.Figure()
        # Barres groupées horizontales : plotly place la 1re trace en BAS du groupe
        # -> traces ajoutées de la plus récente à la plus ancienne (1re période en haut)
        for _p in reversed(TORNADE_A2["période"].unique(maintain_order=True).to_list()):
            _t = TORNADE_A2.filter(pl.col("période") == _p)
            _lignes = {r["indicateur"]: r for r in _t.iter_rows(named=True)}
            _rangs = [_lignes[_i] for _i in _ordre if _i in _lignes]
            if COMPARER_A2:
                _couleurs = _COULEURS_PERIODES[_p]
            else:
                _couleurs = [_COULEUR_B if r["écart en IQR"] > 0 else _COULEUR_A for r in _rangs]
            _fig.add_trace(go.Bar(
                y=[f"{r['indicateur']}  " for r in _rangs], x=[r["écart en IQR"] for r in _rangs],
                orientation="h", name=_p,
                marker={"color": _couleurs, "cornerradius": 4},
                text=[f"{_fmt(r['médiane A'], r['décimales'])} → {_fmt(r['médiane B'], r['décimales'])}"
                      for r in _rangs],
                textposition="outside", cliponaxis=False,
                textfont={"color": _COULEUR_TEXTE, "size": 11},
                customdata=[[r["famille"], r["médiane A"], r["médiane B"], r["n A"], r["n B"], _p]
                            for r in _rangs],
                hovertemplate=(
                    "<b>%{y}</b> (%{customdata[0]}) — %{customdata[5]}<br>"
                    f"Médiane A ({NOM_A_A2}) : %{{customdata[1]}} — n = %{{customdata[3]}}<br>"
                    f"Médiane B ({NOM_B_A2}) : %{{customdata[2]}} — n = %{{customdata[4]}}<br>"
                    "Écart : %{x:.2f} IQR<extra></extra>"
                ),
                showlegend=COMPARER_A2,
            ))

        _x_max = TORNADE_A2["écart en IQR"].abs().max() or 1
        _fig.add_vline(x=0, line={"color": "#9a9a96", "width": 1})
        for _x, _texte, _ancre, _couleur in (
            (-_x_max * 1.45, f"◀ plus élevé dans A : {NOM_A_A2}", "left", _COULEUR_A),
            (_x_max * 1.45, f"plus élevé dans B : {NOM_B_A2} ▶", "right", _COULEUR_B),
        ):
            _fig.add_annotation(x=_x, y=1.0, yref="paper", yanchor="bottom", xanchor=_ancre,
                                text=f"<b>{_texte}</b>", showarrow=False,
                                font={"color": _COULEUR_TEXTE, "size": 12})
        _titre_periode = (
            " — comparaison des périodes" if COMPARER_A2
            else ("" if periode_a2.value not in PERIODES_A2 else f" — dépôts {periode_a2.value}")
        )
        _fig.update_layout(
            height=max(400, _HAUTEUR_LIGNE * len(_ordre) + 180), width=None,
            template="plotly_white", barmode="group", bargap=0.25, bargroupgap=0.08,
            title={"text": (
                f"<b>Analyse2 — Tornade : {NOM_B_A2} contre {NOM_A_A2}{_titre_periode}</b><br>"
                f"<sup>{SOUS_TITRE_FILTRES}</sup>"
            )},
            xaxis={"title": "Écart des médianes (B − A), en écarts interquartiles de l'ensemble",
                   "range": [-_x_max * 1.5, _x_max * 1.5], "zeroline": False, "gridcolor": "#ececec"},
            yaxis={"automargin": True, "categoryorder": "array", "categoryarray": _y_cat},
            legend={"title": "Période de dépôt", "orientation": "h", "x": 0, "y": -0.12,
                    "traceorder": "reversed"},
            margin={"l": 20, "r": 20, "t": 110, "b": 90 if COMPARER_A2 else 60},
        )
        _sortie = mo.ui.plotly(_fig)

    _note = (
        f"*Indicateurs écartés (moins de {N_MIN_A2} bâtiments renseignés dans un groupe, "
        "ou dispersion nulle) : " + ", ".join(ECARTES_A2) + "*"
    ) if ECARTES_A2 else ""
    mo.vstack([
        mo.md(
            "### 2c. Tornade : ce qui distingue les groupes\n\n"
            "Étiquette = médiane A → médiane B. Longueur = écart rapporté à l'écart interquartile "
            "de l'ensemble des bâtiments (1 = un écart interquartile), pour comparer des indicateurs "
            "d'unités différentes."
            + ("  \nEn mode « Comparer » : deux barres de même sens et de même longueur = levier "
               "stable dans le temps." if COMPARER_A2 else "")
        ),
        _sortie,
        mo.md(_note),
        boutons_export(TORNADE_A2.drop("décimales", strict=False), "analyse2c_tornade"),
    ])
    return


# ================================================================================
# ANALYSE3 — Macro-lots et lots par classe, lot 8, nature des fiches
# ================================================================================


@app.cell(hide_code=True)
def widgets_analyse3(CLASSES_2028, mo):
    # ============================================================================
    # CELLULE — Analyse3 : widgets propres à l'analyse
    #   - classe_depart_a3 / classe_arrivee_a3 : classes comparées par les
    #     cascades 3a (macro-lots) et 3b (lots)
    #   - bouton_fiches_a3 : lance la 2e requête réseau (table composant),
    #     utilisée par 3d et 3e
    # ============================================================================
    classe_depart_a3 = mo.ui.dropdown(options=CLASSES_2028, value=CLASSES_2028[4], label="Cascades : de la classe")
    classe_arrivee_a3 = mo.ui.dropdown(options=CLASSES_2028, value=CLASSES_2028[0], label="vers la classe")
    bouton_fiches_a3 = mo.ui.run_button(label="Charger les fiches environnementales (table composant)")
    return bouton_fiches_a3, classe_arrivee_a3, classe_depart_a3


@app.cell(hide_code=True)
def param_analyse3(ANALYSES, classe_arrivee_a3, classe_depart_a3, mo, panneau_filtres):
    # ============================================================================
    # CELLULE — Analyse3 : titre, lecture et panneau de filtres
    # ============================================================================
    mo.vstack([
        mo.md(
            f"## Analyse3 — {ANALYSES[3]}\n\n"
            "Où se loge l'écart au budget 2028 ? Comptage **par bâtiment**, en **moyennes** "
            "(elles s'additionnent : la somme des lots donne l'IC composant).  \n"
            "**3a.** Macro-lots par classe, puis cascade par macro-lot d'une classe à l'autre.  \n"
            "**3b.** Cascade par lot : lots dont l'écart dépasse 5 kgCO₂e/m², les autres regroupés.  \n"
            "**3c.** Lot 8 décomposé en sous-lots 8.1 à 8.7.  \n"
            "**3d.** Nature des fiches environnementales, tous lots (FDES, PEP, DED…).  \n"
            "**3e.** Nature des fiches du sous-lot 8.1."
        ),
        panneau_filtres({"Analyse3 : cascades (3a, 3b)": mo.vstack([classe_depart_a3, classe_arrivee_a3])}),
    ])
    return


@app.cell(hide_code=True)
def resume_analyse3(DATA_base, appliquer_filtres, resume_filtres):
    # Résumé SOUS les filtres (cellule séparée : elle lit les valeurs des widgets).
    DATA_a3 = appliquer_filtres(DATA_base, verbeux=False)
    resume_filtres(DATA_a3)
    return (DATA_a3,)


@app.cell(hide_code=True)
def calcul_analyse3(CLASSES_2028, COLS_LOTS, COLS_MACRO_LOTS, DATA_a3, NB_SOUS_LOTS, pl):
    # ============================================================================
    # CELLULE — Analyse3 : calculs (aucun affichage)
    #
    #   DATA_a3_cl : bâtiments classés (hors « Inconnu »)
    #   MACRO_A3   : moyennes par classe des macro-lots, de l'IC composant et du
    #                budget composant 2028
    #   LOTS_A3    : moyennes par classe des lots 1 à 13
    #   LOT8_A3    : moyennes par classe des sous-lots 8.1 à 8.7
    #   NOMS_LOTS  : intitulés courts des lots (nomenclature RE2020)
    # Un lot ou sous-lot non renseigné compte pour 0 (comme pour les macro-lots).
    # ============================================================================

    # ---- Variables -------------------------------------------------------------
    COLS_SOUS_LOTS_8 = [f"ic_composant_sous_lot_8_{j}" for j in range(1, NB_SOUS_LOTS[8] + 1)]
    NOMS_LOTS = {
        1: "VRD", 2: "Fondations et infrastructure", 3: "Superstructure, maçonnerie",
        4: "Couverture, étanchéité, charpente", 5: "Cloisons, doublages, menuiseries int.",
        6: "Façades et menuiseries ext.", 7: "Revêtements, peintures", 8: "CVC",
        9: "Installations sanitaires", 10: "Réseaux d'énergie (courant fort)",
        11: "Réseaux de communication (courant faible)", 12: "Ascenseurs",
        13: "Production locale d'électricité",
    }

    DATA_a3_cl = DATA_a3.filter(pl.col("classe_2028").is_in(CLASSES_2028))
    _ordre = {c: i for i, c in enumerate(CLASSES_2028)}
    _tri = pl.col("classe_2028").replace_strict(_ordre, default=99)


    def _moyennes(colonnes, extra=()):
        """Moyenne par classe de `colonnes` (NULL -> 0) + agrégats `extra`."""
        return (
            DATA_a3_cl.group_by("classe_2028")
            .agg(pl.len().alias("n"), *[pl.col(c).fill_null(0).mean().alias(c) for c in colonnes], *extra)
            .sort(_tri)
        )


    MACRO_A3 = _moyennes(list(COLS_MACRO_LOTS.values()), (
        pl.col("ic_composant").mean().alias("ic_composant"),
        pl.col("budget_composant_2028").mean().alias("budget_composant_2028"),
    ))
    LOTS_A3 = _moyennes(COLS_LOTS, (pl.col("ic_composant").mean().alias("ic_composant"),))
    LOT8_A3 = _moyennes(COLS_SOUS_LOTS_8)
    return COLS_SOUS_LOTS_8, DATA_a3_cl, LOT8_A3, LOTS_A3, MACRO_A3, NOMS_LOTS


@app.cell(hide_code=True)
def fonction_cascade(COULEURS_CLASSES, go):
    # ============================================================================
    # CELLULE — Fonction commune aux cascades 3a (macro-lots) et 3b (lots)
    #
    # cascade(etapes, depart, arrivee, ...) : barre de départ = IC composant moyen
    # de la classe de départ ; une barre par étape (variation, bleu = baisse,
    # rouge = hausse) ; barre d'arrivée = IC composant moyen de la classe
    # d'arrivée. Si la somme des étapes n'explique pas tout l'écart (IC composant
    # hors lots 1 à 13), une étape « Hors lots 1 à 13 » ferme la cascade.
    # ============================================================================

    # ---- Variables -------------------------------------------------------------
    _COULEUR_TEXTE = "#333333"
    _COULEUR_BAISSE = COULEURS_CLASSES["Conforme 2028"]
    _COULEUR_HAUSSE = COULEURS_CLASSES["30 à 80 kg"]
    _COULEUR_TOTAL = "#52514e"
    _TOLERANCE_RESIDU = 0.5            # kgCO₂e/m²


    def cascade(etapes, depart, arrivee, titre, sous_titre, survols=None):
        """etapes : liste de (libellé, variation) ; depart / arrivee : (classe,
        IC composant moyen, n) ; survols : texte de survol par étape (optionnel)."""
        _residu = (arrivee[1] - depart[1]) - sum(v for _, v in etapes)
        _etapes = list(etapes) + ([("Hors lots 1 à 13", _residu)] if abs(_residu) > _TOLERANCE_RESIDU else [])
        _survols = list(survols or [""] * len(etapes)) + [""] * (len(_etapes) - len(etapes))
        _fig = go.Figure(go.Waterfall(
            x=[f"IC composant<br>{depart[0]}", *[l for l, _ in _etapes], f"IC composant<br>{arrivee[0]}"],
            measure=["absolute", *["relative"] * len(_etapes), "total"],
            y=[depart[1], *[v for _, v in _etapes], 0],
            text=[f"{depart[1]:.0f}", *[f"{v:+.0f}" for _, v in _etapes], f"{arrivee[1]:.0f}"],
            customdata=["", *_survols, ""],
            textposition="outside", cliponaxis=False,
            textfont={"color": _COULEUR_TEXTE, "size": 13},
            connector={"line": {"color": "#c3c2b7", "width": 1}},
            decreasing={"marker": {"color": _COULEUR_BAISSE}},
            increasing={"marker": {"color": _COULEUR_HAUSSE}},
            totals={"marker": {"color": _COULEUR_TOTAL}},
            hovertemplate="<b>%{x}</b><br>%{text} kgCO₂e/m²<br>%{customdata}<extra></extra>",
        ))
        _fig.update_layout(
            height=480, width=None, template="plotly_white", showlegend=False,
            title={"text": f"<b>{titre}</b><br><sup>{sous_titre}</sup>"},
            xaxis={"tickangle": 0, "automargin": True},
            yaxis={"title": "kgCO₂e/m² (moyenne)", "rangemode": "tozero", "gridcolor": "#ececec"},
            margin={"l": 60, "r": 20, "t": 90, "b": 60},
        )
        return _fig

    return (cascade,)


@app.cell(hide_code=True)
def graphique_3a(
    CLASSES_2028,
    COLS_MACRO_LOTS,
    MACRO_A3,
    SOUS_TITRE_FILTRES,
    boutons_export,
    cascade,
    classe_arrivee_a3,
    classe_depart_a3,
    go,
    mo,
    pl,
):
    # ============================================================================
    # CELLULE — Analyse3 : 3a. Macro-lots par classe + cascade par macro-lot
    #
    #   - Barres empilées : moyenne de chaque macro-lot par classe ; un trait
    #     noir marque le budget composant 2028 moyen de la classe.
    #   - Cascade : de l'IC composant moyen de la classe de départ à celui de la
    #     classe d'arrivée, macro-lot par macro-lot.
    # ============================================================================

    # ---- Variables -------------------------------------------------------------
    _COULEURS_MACRO = dict(zip(COLS_MACRO_LOTS, ["#2a78d6", "#eb6834", "#1baf7a"]))   # palette validée
    _COULEUR_TEXTE = "#333333"
    _COULEUR_BUDGET = "#0b0b0b"
    _DEPART, _ARRIVEE = classe_depart_a3.value, classe_arrivee_a3.value
    _N_MIN = 5

    _m = MACRO_A3.filter(pl.col("n") > 0)
    _classes = [c for c in CLASSES_2028 if c in _m["classe_2028"].to_list()]
    _lignes = {r["classe_2028"]: r for r in _m.iter_rows(named=True)}
    _x = [f"{c}<br><sub>n={_lignes[c]['n']}</sub>" for c in _classes]

    # 1. Barres empilées ------------------------------------------------------------
    _fig = go.Figure()
    for _nom, _col in COLS_MACRO_LOTS.items():
        _fig.add_trace(go.Bar(
            x=_x, y=[_lignes[c][_col] for c in _classes], name=_nom,
            marker={"color": _COULEURS_MACRO[_nom], "line": {"color": "#ffffff", "width": 2}},
            text=[f"{_lignes[c][_col]:.0f}" for c in _classes], textposition="inside",
            insidetextfont={"color": "#ffffff", "size": 12},
            hovertemplate=f"<b>%{{x}}</b><br>{_nom} : %{{y:.0f}} kgCO₂e/m²<extra></extra>",
        ))
    _fig.add_trace(go.Scatter(
        x=_x, y=[_lignes[c]["budget_composant_2028"] for c in _classes], mode="markers",
        name="Budget composant 2028 moyen",
        marker={"symbol": "line-ew", "size": 46, "line": {"color": _COULEUR_BUDGET, "width": 3}},
        hovertemplate="<b>%{x}</b><br>Budget composant 2028 moyen : %{y:.0f} kgCO₂e/m²<extra></extra>",
    ))
    for _xi, _c in zip(_x, _classes):
        _fig.add_annotation(x=_xi, y=_lignes[_c]["ic_composant"], text=f"<b>{_lignes[_c]['ic_composant']:.0f}</b>",
                            showarrow=False, yshift=12, font={"color": _COULEUR_TEXTE, "size": 13})
    _fig.update_layout(
        barmode="stack", height=520, width=None, template="plotly_white", bargap=0.35,
        title={"text": "<b>Analyse3a — IC composant moyen par macro-lot et par classe</b><br>"
                       f"<sup>{SOUS_TITRE_FILTRES}</sup>"},
        xaxis={"title": "Classe d'écart au budget composant 2028"},
        yaxis={"title": "kgCO₂e/m² (moyenne)", "rangemode": "tozero", "gridcolor": "#ececec"},
        legend={"orientation": "h", "x": 0, "y": -0.2, "traceorder": "normal"},
        margin={"l": 60, "r": 20, "t": 90, "b": 110},
    )

    # 2. Cascade par macro-lot ------------------------------------------------------------
    if _DEPART == _ARRIVEE or _DEPART not in _lignes or _ARRIVEE not in _lignes:
        _cascade = mo.callout(mo.md("Choisir deux classes différentes, chacune avec au moins un bâtiment."), kind="warn")
    else:
        _d, _a = _lignes[_DEPART], _lignes[_ARRIVEE]
        _fig2 = cascade(
            [(_nom, _a[_col] - _d[_col]) for _nom, _col in COLS_MACRO_LOTS.items()],
            (_DEPART, _d["ic_composant"], _d["n"]), (_ARRIVEE, _a["ic_composant"], _a["n"]),
            f"Analyse3a — Cascade par macro-lot : de « {_DEPART} » (n={_d['n']}) à « {_ARRIVEE} » (n={_a['n']})",
            "Variation de l'IC composant moyen, macro-lot par macro-lot (bleu = baisse, rouge = hausse)",
        )
        _alerte = (
            [mo.callout(mo.md(f"Moins de {_N_MIN} bâtiments dans une des deux classes : cascade fragile."), kind="warn")]
            if min(_d["n"], _a["n"]) < _N_MIN else []
        )
        _cascade = mo.vstack([*_alerte, mo.ui.plotly(_fig2)])

    mo.vstack([
        mo.md("### 3a. Macro-lots par classe"),
        mo.ui.plotly(_fig),
        _cascade,
        boutons_export(MACRO_A3, "analyse3a_macro_lots_par_classe"),
    ])
    return


@app.cell(hide_code=True)
def graphique_3b(
    COLS_LOTS,
    LOTS_A3,
    NOMS_LOTS,
    boutons_export,
    cascade,
    classe_arrivee_a3,
    classe_depart_a3,
    mo,
    pl,
):
    # ============================================================================
    # CELLULE — Analyse3 : 3b. Cascade par lot entre les deux classes choisies
    #
    # Une étape par lot dont l'écart (moyenne arrivée − moyenne départ) dépasse
    # _SEUIL_ECART_LOT en valeur absolue, dans l'ordre des lots ; les autres lots
    # sont regroupés en une seule étape « Autres lots » (détail au survol).
    # ============================================================================

    # ---- Variables -------------------------------------------------------------
    import textwrap

    _SEUIL_ECART_LOT = 5               # kgCO₂e/m²
    _LARGEUR_LIBELLE = 13              # caractères par ligne sous chaque barre
    _DEPART, _ARRIVEE = classe_depart_a3.value, classe_arrivee_a3.value

    _lignes = {r["classe_2028"]: r for r in LOTS_A3.filter(pl.col("n") > 0).iter_rows(named=True)}

    if _DEPART == _ARRIVEE or _DEPART not in _lignes or _ARRIVEE not in _lignes:
        _sortie = mo.callout(mo.md("Choisir deux classes différentes, chacune avec au moins un bâtiment."), kind="warn")
        _tableau = pl.DataFrame()
    else:
        _d, _a = _lignes[_DEPART], _lignes[_ARRIVEE]
        _ecarts = [
            (int(_col.rsplit("_", 1)[1]), _a[_col] - _d[_col], _d[_col], _a[_col]) for _col in COLS_LOTS
        ]
        _gardes = [e for e in _ecarts if abs(e[1]) > _SEUIL_ECART_LOT]
        _autres = [e for e in _ecarts if abs(e[1]) <= _SEUIL_ECART_LOT]

        # Intitulé coupé en lignes courtes : les étiquettes de l'axe ne se chevauchent pas
        _etapes = [
            (f"<b>Lot {n}</b><br>" + "<br>".join(textwrap.wrap(NOMS_LOTS.get(n, ""), _LARGEUR_LIBELLE, break_long_words=False)), v)
            for n, v, _, _ in _gardes
        ]
        _survols = [f"{dv:.1f} → {av:.1f} kgCO₂e/m²" for _, _, dv, av in _gardes]
        if _autres:
            _etapes.append((f"<b>Autres lots</b><br>(écart<br>≤ {_SEUIL_ECART_LOT} kg)", sum(v for _, v, _, _ in _autres)))
            _survols.append("Lots " + ", ".join(f"{n} ({v:+.1f})" for n, v, _, _ in _autres))

        _fig = cascade(
            _etapes, (_DEPART, _d["ic_composant"], _d["n"]), (_ARRIVEE, _a["ic_composant"], _a["n"]),
            f"Analyse3b — Cascade par lot : de « {_DEPART} » (n={_d['n']}) à « {_ARRIVEE} » (n={_a['n']})",
            f"Lots dont l'écart moyen dépasse {_SEUIL_ECART_LOT} kgCO₂e/m², les autres regroupés "
            "(bleu = baisse, rouge = hausse)",
            survols=_survols,
        )
        _fig.update_layout(height=560, xaxis={"tickfont": {"size": 11}, "tickangle": 0})
        _sortie = mo.ui.plotly(_fig)
        _tableau = pl.DataFrame(
            [{"lot": n, "intitulé": NOMS_LOTS.get(n, ""), f"moyenne {_DEPART}": round(dv, 1),
              f"moyenne {_ARRIVEE}": round(av, 1), "écart": round(v, 1),
              "affiché seul": abs(v) > _SEUIL_ECART_LOT} for n, v, dv, av in _ecarts]
        )

    mo.vstack([
        mo.md(f"### 3b. Cascade par lot\n\n*Mêmes classes que la cascade 3a. Un lot est affiché seul si son "
              f"écart moyen dépasse {_SEUIL_ECART_LOT} kgCO₂e/m² ; le survol de « Autres lots » donne le détail.*"),
        _sortie,
        boutons_export(_tableau, "analyse3b_cascade_par_lot") if _tableau.height else mo.md(""),
    ])
    return


@app.cell(hide_code=True)
def graphique_3c(CLASSES_2028, COLS_SOUS_LOTS_8, LOT8_A3, SOUS_TITRE_FILTRES, boutons_export, go, mo, pl):
    # ============================================================================
    # CELLULE — Analyse3 : 3c. Lot 8 décomposé en sous-lots, par classe (moyennes)
    # Le sous-lot 8.1 est en bas de la pile ; sa part du lot 8 est écrite
    # au-dessus de chaque barre.
    # ============================================================================

    # ---- Variables -------------------------------------------------------------
    _PALETTE = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#008300", "#4a3aa7", "#e34948"]
    _COULEUR_TEXTE = "#333333"

    _m = LOT8_A3.filter(pl.col("n") > 0)
    _classes = [c for c in CLASSES_2028 if c in _m["classe_2028"].to_list()]
    _lignes = {r["classe_2028"]: r for r in _m.iter_rows(named=True)}
    _x = [f"{c}<br><sub>n={_lignes[c]['n']}</sub>" for c in _classes]

    _fig = go.Figure()
    for _i, _col in enumerate(COLS_SOUS_LOTS_8):
        _nom = "Sous-lot " + _col.replace("ic_composant_sous_lot_", "").replace("_", ".")
        _valeurs = [_lignes[c][_col] for c in _classes]
        _fig.add_trace(go.Bar(
            x=_x, y=_valeurs, name=_nom,
            marker={"color": _PALETTE[_i % len(_PALETTE)], "line": {"color": "#ffffff", "width": 2}},
            text=[f"{v:.0f}" if _i == 0 else "" for v in _valeurs], textposition="inside",
            insidetextfont={"color": "#ffffff", "size": 12},
            hovertemplate=f"<b>%{{x}}</b><br>{_nom} : %{{y:.1f}} kgCO₂e/m²<extra></extra>",
        ))
    for _xi, _c in zip(_x, _classes):
        _total = sum(_lignes[_c][_col] for _col in COLS_SOUS_LOTS_8)
        _part = 100 * _lignes[_c][COLS_SOUS_LOTS_8[0]] / _total if _total else 0
        _fig.add_annotation(x=_xi, y=_total, yshift=24, showarrow=False,
                            text=f"<b>{_total:.0f}</b><br><sub>dont 8.1 : {_part:.0f} %</sub>",
                            font={"color": _COULEUR_TEXTE, "size": 13})
    _fig.update_layout(
        barmode="stack", height=540, width=None, template="plotly_white", bargap=0.35,
        title={"text": "<b>Analyse3c — Lot 8 (CVC) : sous-lots par classe</b><br>"
                       f"<sup>{SOUS_TITRE_FILTRES}</sup>"},
        xaxis={"title": "Classe d'écart au budget composant 2028"},
        yaxis={"title": "kgCO₂e/m² (moyenne)", "rangemode": "tozero", "gridcolor": "#ececec"},
        legend={"orientation": "h", "x": 0, "y": -0.2, "traceorder": "normal"},
        margin={"l": 60, "r": 20, "t": 110, "b": 110},
    )
    mo.vstack([
        mo.md("### 3c. Lot 8 décomposé\n\n*Moyennes par classe ; un sous-lot non renseigné compte pour 0. "
              "Intitulés des sous-lots : nomenclature RE2020 du lot 8.*"),
        mo.ui.plotly(_fig),
        boutons_export(LOT8_A3, "analyse3c_sous_lots_8_par_classe"),
    ])
    return


@app.cell(hide_code=True)
def extraction_fiches(USAGE_LOGEMENT_COLLECTIF, bouton_fiches_a3, mo, pl, turso_conn):
    # ============================================================================
    # CELLULE — 2e requête réseau (sur demande) : fiches environnementales
    #
    # Table composant : une ligne par composant (volumineuse). Agrégation CÔTÉ SQL :
    # nombre de fiches par bâtiment, nature de donnée et type de déclaration,
    # logements collectifs, avec un repère « sous-lot 8.1 » (lot 8, sous-lot 1).
    # Une seule requête sert 3d (tous lots) et 3e (sous-lot 8.1).
    # Résultat : DATA_fiches (une ligne par bâtiment x nature x repère 8.1).
    # ============================================================================
    mo.stop(not bouton_fiches_a3.value, mo.vstack([
        mo.md("### 3d et 3e. Nature des fiches environnementales"),
        bouton_fiches_a3,
        mo.md("*Requête supplémentaire sur la table composant (volumineuse) : cliquer pour charger.*"),
    ]))

    # ---- Variables -------------------------------------------------------------
    _LOT_8, _SOUS_LOT_1 = 8, 1
    _requete = f"""
        SELECT
            c.projet_id || '_' || COALESCE(c.batiment_index, '0') AS "ID",
            CASE WHEN c.lot_ref = {_LOT_8} AND c.sous_lot_ref = {_SOUS_LOT_1} THEN 1 ELSE 0 END AS est_8_1,
            c.type_donnees,
            c.type_declaration,
            COUNT(*) AS nb_fiches
        FROM composant_open_data c
        JOIN batiment_open_data b
          ON b.projet_id = c.projet_id
         AND CAST(COALESCE(b.batiment_index, 0) AS TEXT) = CAST(COALESCE(c.batiment_index, 0) AS TEXT)
        WHERE b.usage_principal_txt = '{USAGE_LOGEMENT_COLLECTIF}'
        GROUP BY 1, 2, 3, 4
    """
    _cursor = turso_conn.execute(_requete)
    _noms = [d[0] for d in _cursor.description]
    DATA_fiches = pl.DataFrame([dict(zip(_noms, _r)) for _r in _cursor.fetchall()], infer_schema_length=None)
    print(f"Fiches environnementales : {DATA_fiches.height} lignes (bâtiment x nature x repère 8.1)")
    return (DATA_fiches,)


@app.cell(hide_code=True)
def fonction_barres_fiches(CLASSES_2028, DATA_a3_cl, SOUS_TITRE_FILTRES, go, mo, pl):
    # ============================================================================
    # CELLULE — Fonction commune à 3d (tous lots) et 3e (sous-lot 8.1)
    #
    # NATURES_FICHES : 8 natures, même couleur dans 3d et 3e (palette
    # catégorielle validée, dans l'ordre d'empilement) :
    #   FDES individuelle | FDES collective | PEP individuelle | PEP collective |
    #   FDES / PEP sans déclaration | PEP extrapolée | Autres | DED
    #   (« Autres » = conventionnelle, fiche configurée, réemploi, composant vide)
    #
    # barres_fiches(fiches, titre, nom_export) renvoie :
    #   - barres empilées à 100 % : part des fiches par nature, par classe, avec
    #     le nombre de bâtiments et de fiches de chaque classe ;
    #   - tableau par classe : bâtiments, fiches, fiches par bâtiment (médiane),
    #     % DED, % individuelles, udd médian ;
    #   - le DataFrame des fiches par bâtiment et nature (pour d'autres tableaux).
    # Parts en NOMBRE de fiches : la table composant ne donne pas l'impact par fiche.
    # ============================================================================

    # ---- Variables -------------------------------------------------------------
    NATURES_FICHES = {
        "FDES individuelle": "#2a78d6",
        "FDES collective": "#eb6834",
        "PEP individuelle": "#1baf7a",
        "PEP collective": "#eda100",
        "FDES / PEP sans déclaration": "#e87ba4",
        "PEP extrapolée": "#008300",
        "Autres (conventionnelle, configurée…)": "#4a3aa7",
        "DED": "#e34948",
    }
    _SEUIL_ETIQUETTE = 6               # % : pas d'étiquette dans les segments plus fins

    _type = pl.col("type_donnees").cast(pl.Utf8).str.to_uppercase()
    _decl = pl.col("type_declaration").cast(pl.Utf8).str.to_lowercase()
    _nature = (
        pl.when(_type.is_in(["FDES", "PEP"]) & (_decl == "individuelle")).then(pl.concat_str(_type, pl.lit(" individuelle")))
        .when(_type.is_in(["FDES", "PEP"]) & (_decl == "collective")).then(pl.concat_str(_type, pl.lit(" collective")))
        .when(_type.is_in(["FDES", "PEP"])).then(pl.lit("FDES / PEP sans déclaration"))
        .when(_type == "PEP_EXTRAPOLEE").then(pl.lit("PEP extrapolée"))
        .when(_type == "DED").then(pl.lit("DED"))
        .otherwise(pl.lit("Autres (conventionnelle, configurée…)"))
    )


    def _milliers(n):
        """12345 -> « 12 345 » (espace fine insécable)."""
        return f"{int(n):,}".replace(",", "\u202f")


    def barres_fiches(fiches, titre):
        """`fiches` : lignes de DATA_fiches déjà filtrées (tous lots ou 8.1)."""
        _f = (
            fiches.with_columns(_nature.alias("nature"))
            .group_by("ID", "nature").agg(pl.col("nb_fiches").sum())
            .join(DATA_a3_cl.select("ID", "classe_2028", "udd", "ic_composant_sous_lot_8_1"), on="ID", how="inner")
        )
        if _f.height == 0:
            return mo.callout(mo.md("Aucune fiche pour les bâtiments filtrés."), kind="warn"), pl.DataFrame(), _f

        # Parts par classe
        _parts = (
            _f.group_by("classe_2028", "nature").agg(pl.col("nb_fiches").sum())
            .with_columns((100 * pl.col("nb_fiches") / pl.col("nb_fiches").sum().over("classe_2028")).alias("part"))
        )
        # Synthèse par classe (bâtiments, fiches, …)
        _par_bat = _f.group_by("ID", "classe_2028").agg(
            pl.col("nb_fiches").sum().alias("fiches"),
            pl.col("nb_fiches").filter(pl.col("nature") == "DED").sum().alias("ded"),
            pl.col("nb_fiches").filter(pl.col("nature").str.ends_with("individuelle")).sum().alias("indiv"),
            pl.col("udd").first(),
        )
        _ordre = {c: i for i, c in enumerate(CLASSES_2028)}
        _synthese = (
            _par_bat.group_by("classe_2028").agg(
                pl.len().alias("bâtiments"),
                pl.col("fiches").sum().alias("fiches"),
                pl.col("fiches").median().alias("fiches par bâtiment (médiane)"),
                (100 * pl.col("ded").sum() / pl.col("fiches").sum()).round(1).alias("% DED"),
                (100 * pl.col("indiv").sum() / pl.col("fiches").sum()).round(1).alias("% individuelles"),
                (100 * pl.col("udd").median()).round(1).alias("udd médian (%)"),
            ).sort(pl.col("classe_2028").replace_strict(_ordre, default=99))
        )
        _syn = {r["classe_2028"]: r for r in _synthese.iter_rows(named=True)}
        _classes = [c for c in CLASSES_2028 if c in _syn]
        _y = [f"{c}<br><sub>{_syn[c]['bâtiments']} bât. · {_milliers(_syn[c]['fiches'])} fiches</sub>"
              for c in _classes]
        _total_fiches = int(_synthese["fiches"].sum())

        _fig = go.Figure()
        for _nat, _coul in NATURES_FICHES.items():
            _p = dict(_parts.filter(pl.col("nature") == _nat).select("classe_2028", "part").iter_rows())
            if not _p:
                continue
            _v = [_p.get(c, 0.0) for c in _classes]
            _fig.add_trace(go.Bar(
                y=_y, x=_v, name=_nat, orientation="h",
                marker={"color": _coul, "line": {"color": "#ffffff", "width": 2}},
                text=[f"{v:.0f} %" if v >= _SEUIL_ETIQUETTE else "" for v in _v], textposition="inside",
                insidetextfont={"color": "#ffffff", "size": 12},
                hovertemplate=f"<b>%{{y}}</b><br>{_nat} : %{{x:.1f}} % des fiches<extra></extra>",
            ))
        _fig.update_layout(
            barmode="stack", height=max(340, 75 * len(_classes) + 190), width=None, template="plotly_white",
            title={"text": f"<b>{titre} — {_milliers(_total_fiches)} fiches au total</b><br><sup>{SOUS_TITRE_FILTRES}</sup>"},
            xaxis={"title": "% des fiches (en nombre)", "range": [0, 100], "gridcolor": "#ececec"},
            yaxis={"categoryorder": "array", "categoryarray": list(reversed(_y)), "automargin": True},
            legend={"orientation": "h", "x": 0, "y": -0.25, "traceorder": "normal"},
            margin={"l": 20, "r": 20, "t": 90, "b": 130},
        )
        _sortie = mo.vstack([
            mo.ui.plotly(_fig),
            mo.ui.table(_synthese.rename({"classe_2028": "classe"}), selection=None, pagination=False),
        ])
        return _sortie, _parts.sort("classe_2028", "nature"), _f

    return NATURES_FICHES, barres_fiches


@app.cell(hide_code=True)
def graphique_3d(DATA_fiches, barres_fiches, boutons_export, mo):
    # ============================================================================
    # CELLULE — Analyse3 : 3d. Nature des fiches environnementales, tous lots
    # ============================================================================
    _sortie, _parts, _ = barres_fiches(DATA_fiches, "Analyse3d — Nature des fiches, tous lots")
    mo.vstack([
        mo.md("### 3d. Nature des fiches environnementales, tous lots\n\n"
              "*Parts en **nombre** de fiches (la table composant ne donne pas l'impact par fiche).*"),
        _sortie,
        boutons_export(_parts, "analyse3d_fiches_tous_lots_par_classe") if _parts.height else mo.md(""),
    ])
    return


@app.cell(hide_code=True)
def graphique_3e(DATA_fiches, barres_fiches, boutons_export, mo, pl):
    # ============================================================================
    # CELLULE — Analyse3 : 3e. Nature des fiches du sous-lot 8.1
    #   - même graphique et même tableau que 3d, restreints au sous-lot 8.1
    #   - effet « donnée » : 8.1 médian selon la nature DOMINANTE des fiches 8.1
    #     de chaque bâtiment (PEP individuelles, collectives, DED…)
    # ============================================================================

    # ---- Variables -------------------------------------------------------------
    _N_MIN = 5

    _sortie, _parts, _f = barres_fiches(
        DATA_fiches.filter(pl.col("est_8_1") == 1), "Analyse3e — Nature des fiches du sous-lot 8.1"
    )
    if _f.height:
        _dominante = (
            _f.sort("nb_fiches", descending=True).group_by("ID", maintain_order=True)
            .agg(pl.col("nature").first().alias("nature dominante"),
                 pl.col("nb_fiches").sum().alias("fiches 8.1"),
                 pl.col("ic_composant_sous_lot_8_1").first(), pl.col("udd").first())
        )
        _tableau = (
            _dominante.group_by("nature dominante").agg(
                pl.len().alias("bâtiments"),
                pl.col("fiches 8.1").sum().alias("fiches 8.1"),
                pl.col("ic_composant_sous_lot_8_1").median().round(1).alias("8.1 médian (kg/m²)"),
                (pl.col("udd").median() * 100).round(1).alias("udd médian (%)"),
            ).sort("bâtiments", descending=True)
            .with_columns(pl.when(pl.col("bâtiments") < _N_MIN).then(pl.lit(f"< {_N_MIN} bâtiments"))
                          .otherwise(pl.lit("")).alias("remarque"))
        )
        _effet = [
            mo.md("**Effet « donnée » : 8.1 médian selon la nature dominante des fiches 8.1 du bâtiment**"),
            mo.ui.table(_tableau, selection=None, pagination=False),
            boutons_export(_dominante, "analyse3e_nature_dominante_par_batiment"),
        ]
    else:
        _effet = []

    mo.vstack([
        mo.md("### 3e. Nature des fiches du sous-lot 8.1\n\n"
              "*Parts en **nombre** de fiches (la table composant ne donne pas l'impact par fiche).*"),
        _sortie,
        *_effet,
        boutons_export(_parts, "analyse3e_fiches_8_1_par_classe") if _parts.height else mo.md(""),
    ])
    return


if __name__ == "__main__":
    app.run()
