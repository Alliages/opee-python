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
    VERSION = "0.51"          # à ajuster : +0.01 à chaque édition du script
    DATE_EDITION = "08/10/2026 23:15"
    HISTORIQUE_VERSIONS = [
        # (version, synthèse des changements), la plus récente en premier
        (VERSION, "Analyse1 : classes d'écart au budget composant 2028, nombre et part des projets "
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
        3: "Macro-lots par classe, puis focus sur le lot 8 et le sous-lot 8.1",
        4: "Évolution par année de dépôt",
        5: "Simulateur de leviers",
        6: "Effet propre de chaque levier (régression)",
    }
    ANALYSES_PRETES = {1}       # analyses déjà construites

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


if __name__ == "__main__":
    app.run()
