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
def les_imports():
    import marimo as mo
    import plotly.express as px
    import plotly.graph_objects as go
    import polars as pl

    return go, mo, pl, px


@app.cell(hide_code=True)
def liste_graphiques(mo):
    # ============================================================================
    # CELLULE — Liste des graphiques du dashboard (numéro + titre).
    #
    # SOURCE UNIQUE des numéros et titres : chaque cellule graphique lit son titre
    # dans GRAPHIQUES, et ce résumé est affiché tel quel en début de notebook.
    # Pour renommer ou renuméroter un graphique, c'est ICI qu'il faut modifier.
    # ============================================================================

    GRAPHIQUES = {
        1: "Nombre de bâtiments par seuil IC Construction et par tranche d'IC Construction",
        2: "Impact carbone des matériaux : IC composant moyen par lot, par seuil RE2020",
        3: "Médiane IC Composant par matériau de structure et par seuil RE2020",
        4: "Q1 / Médiane / Q3 du nombre de fiches (FDES + PEP + DED) par seuil RE2020",
        5: "Écart des bâtiments aux seuils réglementaires (%)",
        6: "Stock de carbone par type de matériau de structure et seuil RE2020",
        7: "Éloignement au seuil IC Construction 2028 : comparaison de deux groupes de bâtiments",
    }

    mo.md(
        "### Graphiques du dashboard\n\n"
        + "\n".join(f"- Graphique {_n} — {_titre}" for _n, _titre in GRAPHIQUES.items())
    )
    return (GRAPHIQUES,)


@app.cell(hide_code=True)
def saisie_jeton(mo):
    # ============================================================================
    # CELLULE — Jeton Turso. Il n'est JAMAIS écrit dans le code (dépôt GitHub) :
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
    #creation de turso_conn
    import os as _os
    import libsql_experimental as libsql

    turso_token = _os.environ.get("TURSO_TOKEN") or champ_jeton.value
    mo.stop(not turso_token, mo.md("*Saisir le jeton Turso ci-dessus pour lancer le notebook.*"))

    turso_conn = libsql.connect(
        "libsql://opee-alliages.aws-eu-west-1.turso.io",
        auth_token=turso_token
    )
    # --- 1. Liste des tables (1er appel) ---------------------------------------
    _tables = turso_conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table'"
    ).fetchall()
    _result = (
        mo.md(
            "### Tables disponibles\n"
            + "\n".join(f"- {t[0]}" for t in _tables)
        ) if _tables else mo.md("""Aucune table trouvée""")
    )
    noms_tables = [t[0] for t in _tables]

    # --- 2. Comptage de toutes les tables en UN SEUL appel (2e et dernier) -----
    # Plutôt qu'un COUNT(*) par table (un appel réseau par table), on combine
    # tous les comptages en une seule requête via UNION ALL, exécutée en un
    # unique aller-retour vers la base.
    """
    _requete = " UNION ALL ".join(
        f"SELECT '{_nom}' AS table_name, COUNT(*) AS nb_lignes FROM \"{_nom}\""
        for _nom in noms_tables
    )
    _comptages = turso_conn.execute(_requete).fetchall()

    _df_comptages = pl.DataFrame(
        _comptages, schema=["table", "nb_lignes"], orient="row"
    ).sort("nb_lignes", descending=True)

    _table = mo.ui.table(_df_comptages)
    _table
    """
    _result
    return noms_tables, turso_conn


@app.cell(disabled=True, hide_code=True)
def _(mo, pl, turso_conn):


    # Sélectionne un projet_id qui a plusieurs bâtiments (celui qui en a le
    # plus, pour être sûr d'avoir un exemple), puis affiche jusqu'à 10 de ses
    # bâtiments -- un seul appel à Turso (sous-requête imbriquée).
    _requete = """
        SELECT projet_id, batiment_index, usage_principal_txt
        FROM batiment_open_data
        WHERE projet_id = (
            SELECT projet_id
            FROM batiment_open_data
            GROUP BY projet_id
            HAVING COUNT(*) > 1
            ORDER BY COUNT(*) DESC
            LIMIT 1
        )
        LIMIT 10
    """
    _cursor = turso_conn.execute(_requete)
    _col_names = [desc[0] for desc in _cursor.description]
    _lignes = _cursor.fetchall()

    _df = pl.DataFrame(_lignes, schema=_col_names, orient="row")

    _table = mo.ui.table(_df)
    _table
    return


@app.cell(disabled=True, hide_code=True)
def _(mo, noms_tables):
    dropdown_table = mo.ui.dropdown(
        options=noms_tables,
        value='batiment_open_data',
        label="Table à afficher"
    )
    limit_extract = mo.ui.slider(start=10, stop=150, step=10, show_value=True,label="Combien de ligne afficher ?")
    button_run_table = mo.ui.run_button(label="---> lancer le calcul <----")
    juste_quelques_colonnes = mo.ui.checkbox()

    mo.vstack([
        mo.md("### TABLEAU AVEC UN EXTRAIT D'UNE TABLE"),
        dropdown_table,
        limit_extract,
        mo.md(f"Seulement les colonnes les plus importantes des bâtiments ? {juste_quelques_colonnes} (oui = coché)"),
        #juste_quelques_colonnes,
        mo.md(f"\n\n\n{button_run_table}"),
        mo.md("*🔽 cliquer pour lancer si rien ne s'affiche 🔽*")
    ])
    return (
        button_run_table,
        dropdown_table,
        juste_quelques_colonnes,
        limit_extract,
    )


@app.cell(disabled=True, hide_code=True)
def affiche_table(
    button_run_table,
    dropdown_table,
    juste_quelques_colonnes,
    limit_extract,
    mo,
    pl,
    turso_conn,
):
    mo.stop(not button_run_table.value)
    # ============================================================================
    # Affiche l'intégralité de la table batiment_open_data sous forme de
    # DataFrame (un seul appel à la base Turso).
    # ============================================================================
    _TABLE_NAME = dropdown_table.value
    # Récupérer les noms de colonnes
    _cursor = turso_conn.execute(f"PRAGMA table_info({_TABLE_NAME})")
    _columns = [row[1] for row in _cursor.fetchall()]

    if (_TABLE_NAME == "batiment_open_data" and juste_quelques_colonnes.value == True):
        # Colonnes nommées explicitement, dans l'ordre voulu à l'affichage
        _colonnes_prioritaires = [
            "projet_id",
            "usage_principal_txt",
            "shab",
            "sref",
            "seuil_ic_construction_atteint",
            "ic_energie",
            "ic_construction",
        ]
        # Puis les colonnes qui matchent un motif, dans l'ordre où elles
        # apparaissent dans la table (pas d'ordre particulier à préciser)
        _colonnes_batiment = [col for col in _columns if "batiment" in col.lower()]
        _colonnes_ic_composant = [col for col in _columns if col.startswith("ic_composant")]

        # Assemblage dans l'ordre : prioritaires -> batiment -> ic_composant,
        # en ne gardant que les colonnes qui existent réellement dans la table
        # et sans doublon (garde la première occurrence rencontrée).
        _selected_columns = []
        for col in _colonnes_prioritaires + _colonnes_batiment + _colonnes_ic_composant:
            if col in _columns and col not in _selected_columns:
                _selected_columns.append(col)

        # Construire et exécuter la requête
        _query = f"""
            SELECT {", ".join(f'"{col}"' for col in _selected_columns)}
            FROM {_TABLE_NAME}
            LIMIT {limit_extract.value}
        """
    else:
        _query = f"""
            SELECT *
            FROM {_TABLE_NAME}
            LIMIT {limit_extract.value}
        """
    _cursor = turso_conn.execute(_query)

    _col_names = [desc[0] for desc in _cursor.description]
    _lignes = _cursor.fetchall()


    """
    _TABLE_NAME = "batiment_open_data"

    _cursor = turso_conn.execute(f"SELECT * FROM {_TABLE_NAME} LIMIT 100")
    _col_names = [desc[0] for desc in _cursor.description]
    _lignes = _cursor.fetchall()
    """
    # Construction à partir de dicts (colonne par colonne) pour éviter les
    # erreurs de dépassement de capacité lors de l'inférence de type de polars
    # (orient="row" peut inférer Int32 sur les premières lignes puis planter
    # sur une valeur plus grande).
    # infer_schema_length=None force polars à scanner TOUTES les lignes avant
    # de décider du type de chaque colonne, évitant qu'il infère Int32 sur un
    # sous-ensemble puis plante sur une valeur plus grande.
    _data_dicts = [dict(zip(_col_names, row)) for row in _lignes]
    _df = pl.DataFrame(_data_dicts, infer_schema_length=None)

    DATA_tab1 = _df

    print(f"{_df.height} lignes, {_df.width} colonnes")

    # Affichage interactif (tri, filtre, pagination) dans marimo
    table = mo.ui.table(_df)
    table
    return (DATA_tab1,)


@app.cell(disabled=True, hide_code=True)
def _(DATA_tab1, mo):
    _df_long = DATA_tab1
    _csv_download = mo.download(
        data=_df_long.write_csv().encode("utf-8-sig"),
        filename="data.csv",
        mimetype="text/csv",
        label="Download CSV",
    )
    # JSON download data=json.dumps(_df_long).encode("utf-8"),
    _json_download = mo.download(
        data=_df_long.write_json().encode("utf-8"),
        filename="data.json",
        mimetype="application/json",
        label="Download JSON",
    )

    mo.vstack([_csv_download, _json_download])
    return


@app.cell(hide_code=True)
def exports(mo, pl):
    # ============================================================================
    # CELLULE — Export CSV / JSON, COMMUN à tous les graphiques
    #
    # boutons_export(df, nom) -> deux boutons de téléchargement (CSV + JSON).
    # Chaque graphique l'appelle avec SES données (celles qui sont tracées), pas
    # avec le DataFrame complet : `nom` donne le nom des fichiers téléchargés.
    # ============================================================================

    def boutons_export(df, nom):
        # Le CSV ne supporte pas les colonnes "liste" : converties en texte
        # (valeurs séparées par des virgules) pour le CSV uniquement. Le JSON,
        # lui, garde les vraies listes.
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
def choisir_typo(mo):
    typologies = ['Bureau', 'Enseignement primaire', 'Enseignement secondaire (partie jour)', 'Logement collectif', 'Maison individuelle ou accolée']
    dropdown_usage = mo.ui.dropdown(
        options=typologies,
        value='Logement collectif',
        label="Usage à afficher"
    )
    button_lancer = mo.ui.run_button(label="---> lancer la calcul <----")

    mo.vstack([
        mo.md("### Pour quelle typologie ?"),
        dropdown_usage,
        mo.md(f"\n\n\n{button_lancer}"),
        mo.md("*🔽 cliquer pour lancer si rien ne s'affiche 🔽*")
    ])
    return button_lancer, dropdown_usage


@app.cell(hide_code=True)
def fonction_retrouver_sref(pl):
    # ============================================================================
    # CELLULE — Fonction "retrouver sref" : reconstitue la surface de référence
    # (colonne `sref` du DataFrame) des LOGEMENTS COLLECTIFS à partir de
    # misurf_tot et mbsurf_tot (table zone_open_data).
    #
    # Retourne une EXPRESSION polars, évaluée ligne par ligne sur DATA_brut.
    # (Version vectorisée de `retrouver_sref.py`.)
    #
    # Fonctions directes (sref -> misurf_tot) :
    #     sref <= 1300        : misurf_tot = -0.104  + 0.00008  * sref
    #     1300 < sref < 4000  : misurf_tot =  0.0455 - 0.000035 * sref
    #     sref >= 4000        : misurf_tot = -0.0945
    # mbsurf_tot sert à lever l'ambiguïté : > 0 si sref < 1300, = 0 si sref >= 1300.
    #
    # Une ligne incohérente (ou avec un NULL) reçoit sref = NULL.
    # ============================================================================


    # ============================================================================
    # PARAMÈTRES (toutes les variables au même endroit)
    # ============================================================================

    # Tranche 2 : misurf_tot = A2 - B2 * sref
    A2, B2 = 0.0455, 0.000035
    # Tranche 3 (plateau) : valeur constante de misurf_tot
    PLATEAU = -0.0945
    SREF_PLATEAU = 5000       # m² : valeur de sref renvoyée sur le plateau (sref >= 4000)

    # Tranche 1 : rétro-ingénierie grâce à mbsurf_tot (qui semble fonctionner)
    #   sref = ((misurf_tot + RETRO_A) * 10000) / RETRO_K
    # (ancienne formule, inverse exacte de misurf_tot = -0.104 + 0.00008 * sref :
    #   sref = (misurf_tot + 0.104) / 0.00008)
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

    return (retrouver_sref,)


@app.cell(hide_code=True)
def extraction_unique(
    boutons_export,
    button_lancer,
    USAGE_LOGEMENT_COLLECTIF,
    dropdown_usage,
    mo,
    pl,
    retrouver_sref,
    turso_conn,
):
    mo.stop(not button_lancer.value)
    # ============================================================================
    # CELLULE D'EXTRACTION UNIQUE — un seul appel réseau à Turso, partagé par
    # TOUS les graphiques (1 à 6).
    #
    # Ne dépend QUE de dropdown_usage (et du bouton). Tous les autres filtres
    # (règles de validation, min/max, surface, années, attestation, zone
    # climatique, matériau...) sont appliqués plus tard, en polars, dans les
    # cellules graphiques : aucun appel réseau supplémentaire.
    #
    # Une ligne par BÂTIMENT (identifiant "ID" = projet_id_batiment_index), avec
    # des valeurs brutes (pas de AVG, pas d'exclusion).
    # Résultat : DATA_brut (variable globale, partagée).
    # ============================================================================


    # ============================================================================
    # PARAMÈTRES (toutes les variables au même endroit)
    # ============================================================================

    # --- Widget : seul filtre appliqué côté SQL ---------------------------------
    _USAGE_FILTRE = dropdown_usage.value

    # --- Tables et colonnes de base ---------------------------------------------
    _TABLE_BATIMENT = "batiment_open_data"
    _TABLE_PROJET = "projet_open_data"
    _TABLE_ZONE = "zone_open_data"
    _PID_COL = "projet_id"
    _USAGE_COL = "usage_principal_txt"
    _SEUIL_COL = "seuil_ic_construction_atteint"
    _SREF_COL = "sref"      # colonne de la base ; devient `sref_approx` dans le DataFrame

    # --- Colonnes ramenées brutes -------------------------------------------------
    # Lots du graphique "lots"
    _COLS_LOTS = [f"ic_composant_lot_{i}" for i in range(1, 14)]
    # Paramètres du graphique "boîtes à moustaches"
    _COLS_BOXPLOT = [
        "nb_fdes", "nb_pep", "nb_ded", "nb_des", "nb_conventionnelle",
        "nb_composant_reemploi", "nb_composant_vide", "nb_fiche_configuree",
        "nb_pep_extrapolee", "ic_ded",
    ]
    # Colonnes supplémentaires : fiches ACV, stock carbone, surface de baies
    # (surface_baies_rset sert à définir les tranches de taille des logements
    # collectifs, cf. cellule `constantes_filtres`)
    _COLS_SUPPLEMENTAIRES = ["nb_total_fiche_acv", "stock_c", "surface_baies_rset", "surface_murs_rset"]
    # Surfaces totales des zones (table zone_open_data, une ligne par zone)
    _COLS_ZONE = ["misurf_tot", "mbsurf_tot"]
    # Indicateurs et seuils du graphique "écarts aux seuils"
    # NB : il n'existe pas de colonne ic_energie_max_2031 dans la base -- le
    # seuil IC Énergie n'est donc défini que pour 2022/2025/2028.
    _COLS_ECARTS = [
        "bbio_batiment", "bbio_max",
        "cep_batiment", "cep_max",
        "cep_nr_batiment", "cep_nr_max",
        "dh_batiment", "dh_max",
        "ic_construction", "ic_energie",
        "ic_construction_max_2022", "ic_construction_max_2025",
        "ic_construction_max_2028", "ic_construction_max_2031",
        "ic_energie_max_2022", "ic_energie_max_2025",
        "ic_energie_max_2028",
    ]

    # --- Affichage des seuils ----------------------------------------------------
    _RENOMMAGE_SEUILS = {"2022": "RE2022", "2025": "RE2025", "2028": "RE2028", "2031": "RE2031"}


    # ============================================================================
    # 1. REQUÊTE SQL
    # ============================================================================

    # Identifiant unique par bâtiment (un même projet_id peut avoir plusieurs
    # bâtiments) ; COALESCE évite qu'un batiment_index NULL fasse disparaître le
    # bâtiment du comptage.
    _ID_SQL = f"(b.{_PID_COL} || '_' || COALESCE(b.batiment_index, '0'))"

    # Colonnes du SELECT, dans l'ordre d'affichage ("ID" en premier)
    _select = [
        f'{_ID_SQL} AS "ID"',
        f"b.{_PID_COL} AS projet_id",
        "b.batiment_index",
        f"COALESCE(CAST(b.{_SEUIL_COL} AS TEXT), 'Inconnu') AS seuil",
        f"b.{_SREF_COL} AS sref_approx",   # sref de la base = valeur APPROCHÉE
        "CAST(NULL AS REAL) AS sref",       # remplie ensuite en polars (retrouver_sref)
        "b.zone_climatique",
        "b.dc_materiau_structure",
        "b.dc_type_structure_principale",
        "b.regle_validation_globale",
        "b.ic_composant",
        *[f"b.{col}" for col in _COLS_LOTS],
        *[f"b.{col}" for col in _COLS_BOXPLOT],
        *[f"b.{col}" for col in _COLS_ECARTS],
        *[f"b.{col}" for col in _COLS_SUPPLEMENTAIRES],
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

    # La CTE regroupe, par projet, toutes les années et attestations (sous forme
    # de listes JSON, non filtrées) : elles sont filtrées ensuite en polars.
    # LEFT JOIN : un bâtiment dont le projet n'a aucune ligne dans
    # projet_open_data reste dans le résultat.
    _requete = f"""
        WITH projets_info AS (
            SELECT
                {_PID_COL},
                json_group_array(DISTINCT annee_depot_pc) AS annees_depot_pc_json,
                json_group_array(DISTINCT type_attestation) AS types_attestation_json
            FROM {_TABLE_PROJET}
            GROUP BY {_PID_COL}
        ),
        -- zone_open_data : plusieurs lignes (zones) par bâtiment, qui portent la même
        -- valeur de misurf_tot / mbsurf_tot -> une seule valeur par bâtiment (MAX ignore
        -- les NULL et donne la valeur commune). Clé = projet_id + batiment_index (NULL -> 0,
        -- comme pour l'identifiant "ID"), comparée en texte pour éviter tout écart de type.
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
        WHERE b.{_USAGE_COL} = '{_USAGE_FILTRE}'
    """

    _cursor = turso_conn.execute(_requete)
    _col_names = [desc[0] for desc in _cursor.description]
    _lignes = _cursor.fetchall()


    # ============================================================================
    # 2. MISE EN FORME (polars, aucun appel réseau)
    # ============================================================================

    _df = pl.DataFrame(_lignes, schema=_col_names, orient="row")

    # Seuils affichés RE2022, RE2025, ... (fait ici une fois pour toutes)
    _df = _df.with_columns(pl.col("seuil").replace(_RENOMMAGE_SEUILS).alias("seuil"))

    # Matériau de structure : certaines valeurs contiennent des espaces
    # parasites ("Béton "). Nettoyé UNE FOIS ICI pour que filtres, mappings et
    # regroupements en aval fonctionnent partout de la même façon.
    _df = _df.with_columns(
        pl.col("dc_materiau_structure").cast(pl.Utf8).str.strip_chars(),
        pl.col("dc_type_structure_principale").cast(pl.Utf8).str.strip_chars(),
    )

    # Colonne `sref` : renseignée uniquement pour les LOGEMENTS COLLECTIFS (fonction
    # `retrouver_sref`) ; NULL pour les autres usages. Remplace la colonne vide créée
    # par la requête, à la même place.
    _df = _df.with_columns(
        pl.when(pl.col("usage") == USAGE_LOGEMENT_COLLECTIF)
        .then(retrouver_sref())
        .otherwise(pl.lit(None, dtype=pl.Float64))
        .cast(pl.Float64)
        .alias("sref")
    )
    if _USAGE_FILTRE == USAGE_LOGEMENT_COLLECTIF:
        print(f"  sref retrouvé : {_df.height - _df['sref'].null_count()} / {_df.height} bâtiments "
              f"(NULL = misurf_tot / mbsurf_tot absents ou incohérents)")

    # Listes JSON -> vraies listes polars (filtrage propre ensuite)
    _df = _df.with_columns(
        pl.col("annees_depot_pc_json").cast(pl.Utf8).str.json_decode(pl.List(pl.Int64)).alias("annees_depot_pc"),
        pl.col("types_attestation_json").cast(pl.Utf8).str.json_decode(pl.List(pl.Utf8)).alias("types_attestation"),
    ).drop(["annees_depot_pc_json", "types_attestation_json"])

    # Variable globale (pas de préfixe _) : lue par les cellules graphiques.
    DATA_brut = _df

    print(f"Bâtiments extraits pour l'usage '{_USAGE_FILTRE}' : {_df.height}")


    # ============================================================================
    # 3. EXPORT CSV / JSON (toutes les données extraites, une ligne par bâtiment)
    # ============================================================================

    boutons_export(_df, "batiments_bruts")
    return (DATA_brut,)


@app.cell(hide_code=True)
def widgets_filtres(
    MATERIAUX_OPTIONS,
    MODE_SURFACE_SREF,
    MODE_SURFACE_SREF_APPROX,
    SREF_MAX_SLIDER,
    SREF_PAS_SLIDER,
    mo,
):
    # ============================================================================
    # CELLULE — Définition des widgets de filtres COMMUNS à tous les graphiques
    #
    # Définis ici UNE fois (aucun affichage) ; chaque cellule de paramètres les
    # affiche là où elle en a besoin. (Le widget "surface", qui dépend de l'usage,
    # est dans sa propre cellule : changer d'usage ne réinitialise que lui.)
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

    # Surface : DEUX filtres possibles, un seul appliqué à la fois (le choix ci-dessous).
    # Par défaut : sref_approx (tranches), comme avant.
    choix_mode_surface = mo.ui.radio(
        options=[MODE_SURFACE_SREF_APPROX, MODE_SURFACE_SREF],
        value=MODE_SURFACE_SREF_APPROX,
        label="Filtre de surface APPLIQUÉ",
    )
    choix_sref = mo.ui.range_slider(
        start=0, stop=SREF_MAX_SLIDER, step=SREF_PAS_SLIDER, value=[0, SREF_MAX_SLIDER],
        show_value=True, label="sref (m²) entre :",
    )

    return (
        cacher_inconnu,
        choix_de_attestation,
        choix_de_la_date,
        choix_materiau_structure,
        choix_mode_surface,
        choix_sref,
        choix_valide_regles,
        choix_zone_climatique,
    )


@app.cell(hide_code=True)
def widget_surface(dropdown_usage, mo, options_surface):
    # Options du filtre surface : dépendent de l'usage choisi (tranches de sref, ou
    # tranches de taille de logement collectif) -- cf. cellule `constantes_filtres`.
    _options_surface = options_surface(dropdown_usage.value)
    choix_de_surface = mo.ui.multiselect(
        options=_options_surface, value=_options_surface, label="Surface"
    )
    return (choix_de_surface,)


@app.cell(hide_code=True)
def bloc_surface(choix_de_surface, choix_mode_surface, choix_sref, mo):
    # ============================================================================
    # CELLULE D'AFFICHAGE — bloc "surface" réutilisé dans toutes les cellules de
    # paramètres : le choix du filtre appliqué + les DEUX filtres (tranches de
    # sref_approx, plage de sref). Mise en page statique (ne lit aucune valeur) :
    # changer de filtre ne réinitialise donc pas les autres paramètres.
    # ============================================================================

    bloc_filtre_surface = mo.vstack([
        choix_mode_surface,
        mo.hstack([choix_de_surface, choix_sref], justify="start", align="end", wrap=True),
    ])
    return (bloc_filtre_surface,)


@app.cell(hide_code=True)
def rappel_filtre_surface(MODE_SURFACE_SREF, choix_mode_surface, choix_sref, mo):
    # Rappel (affiché une fois) du filtre de surface réellement appliqué.
    if choix_mode_surface.value == MODE_SURFACE_SREF:
        _texte = f"**Filtre de surface appliqué : `sref`** — entre {choix_sref.value[0]} et {choix_sref.value[1]} m². Les tranches `sref_approx` sont ignorées."
    else:
        _texte = "**Filtre de surface appliqué : `sref_approx`** (tranches). Le curseur `sref` est ignoré."
    mo.callout(mo.md(_texte), kind="info")
    return


@app.cell(hide_code=True)
def panneau_filtres_def(
    bloc_filtre_surface,
    cacher_inconnu,
    choix_de_attestation,
    choix_de_la_date,
    choix_materiau_structure,
    choix_valide_regles,
    choix_zone_climatique,
    mo,
):
    # ============================================================================
    # CELLULE — Panneau de filtres, construit UNE fois, répété avant chaque graphique
    #
    # Disposition :
    #   1. Qualité des données (toujours visible, en haut) : règles de validation,
    #      masquer les inconnus
    #   2. Trois accordéons FERMÉS côte à côte :
    #        - Période et lieu : années de dépôt, type d'attestation, zone climatique
    #        - Bâtiment        : filtre de surface, matériau de structure
    #        - Graphique N     : paramètres propres au graphique (optionnel)
    #
    # Cette cellule ne lit AUCUNE valeur de widget : sa mise en page est statique,
    # donc modifier un filtre ne referme pas les accordéons ni ne réinitialise les
    # autres paramètres. Le résumé des filtres actifs (qui, lui, lit les valeurs)
    # est affiché à part : cf. `resume_filtres` (cellule `filtres_communs`).
    # ============================================================================


    # ============================================================================
    # PARAMÈTRES
    # ============================================================================

    _LIBELLE_PERIODE = "Période et lieu"
    _LIBELLE_BATIMENT = "Bâtiment"


    def panneau_filtres(parametres_graphique=None, *, avec_materiau=True, avec_inconnus=True):
        """Construit le panneau de filtres d'un graphique.

        - parametres_graphique : dict {libellé de l'accordéon: contenu} pour les paramètres
          propres au graphique (None = pas de 3e accordéon).
        - avec_materiau=False : graphique où le matériau est l'axe (pas de filtre matériau).
        - avec_inconnus=False : graphique qui n'applique pas « Masquer les inconnus ».
        """
        # 1. Qualité des données : toujours visible, en haut
        _qualite = mo.hstack(
            [choix_valide_regles] + ([cacher_inconnu] if avec_inconnus else []),
            justify="start", gap=2,
        )

        # 2. Contenu des accordéons
        _bloc_periode = mo.vstack([
            mo.hstack([choix_de_la_date, choix_de_attestation], justify="start", wrap=True),
            choix_zone_climatique,
        ])
        _bloc_batiment = mo.vstack(
            [bloc_filtre_surface] + ([choix_materiau_structure] if avec_materiau else [])
        )

        # Accordéons fermés par défaut, côte à côte
        _accordeons = [
            mo.accordion({_LIBELLE_PERIODE: _bloc_periode}),
            mo.accordion({_LIBELLE_BATIMENT: _bloc_batiment}),
        ]
        if parametres_graphique:
            _accordeons.append(mo.accordion(parametres_graphique))

        return mo.vstack([
            _qualite,
            mo.hstack(_accordeons, justify="start", align="start", wrap=True, widths="equal"),
        ])

    return (panneau_filtres,)


@app.cell(hide_code=True)
def param_graphique_1(mo, panneau_filtres):
    # Paramètre propre au graphique 1
    seuil_bas_iccons = mo.ui.slider(start=400, stop=700, step=50, show_value=True, label="La tranche basse de l'ic_construction pour séparer les projets ?")

    mo.vstack([
        mo.md("### Paramètres du graphique 1"),
        panneau_filtres({
            "Graphique 1": mo.vstack([
                seuil_bas_iccons,
                mo.md("*400 pour le logement 500 pour le reste ?*\n"),
            ]),
        }),
    ])
    return (seuil_bas_iccons,)



@app.cell(hide_code=True)
def resume_filtres_graphique_1(resume_filtres):
    # Résumé des filtres actifs du graphique 1 (cellule séparée : il lit les valeurs
    # des widgets, alors que le panneau ci-dessus reste statique).
    resume_filtres()
    return


@app.cell(hide_code=True)
def graphique_1(
    GRAPHIQUES,
    DATA_brut,
    SOUS_TITRE_FILTRES,
    appliquer_filtres,
    boutons_export,
    dropdown_usage,
    mo,
    pl,
    px,
    seuil_bas_iccons,
):
    # ============================================================================
    # CELLULE — Graphique 1 : nombre de bâtiments par seuil RE2020 et par tranche
    # d'IC Construction (barres empilées).
    #
    # Part de DATA_brut (AUCUN appel réseau ici) ; filtres temps réel communs à
    # tous les graphiques : cellule `filtres_communs`.
    # ============================================================================

    # --- Paramètre des tranches d'IC Construction -------------------------------
    _SEUIL_TRANCHE_BASE = seuil_bas_iccons.value
    _LARGEUR_TRANCHE = 100
    _NB_TRANCHES_INTERMEDIAIRES = 4

    # --- 1. Filtres communs (règles, années, attestation, surface, zone,
    #        matériau, masquage des inconnus) ----------------------------------
    _df = appliquer_filtres(DATA_brut)

    mo.stop(_df.height == 0, mo.md("**Aucun bâtiment ne correspond aux filtres choisis.**"))

    # --- 2. Découpage en tranches d'IC Construction (paramétrable) -------------
    # Equivalent polars du CASE WHEN qu'on avait en SQL : change uniquement
    # _SEUIL_TRANCHE_BASE (ex. 400 -> 500) pour tout mettre à jour.
    _bornes = [_SEUIL_TRANCHE_BASE + i * _LARGEUR_TRANCHE for i in range(_NB_TRANCHES_INTERMEDIAIRES + 1)]

    _ORDRE_TRANCHES = [f"< {_bornes[0]}"]
    _expr_tranche = pl.when(pl.col("ic_construction") < _bornes[0]).then(pl.lit(f"< {_bornes[0]}"))
    for _i in range(_NB_TRANCHES_INTERMEDIAIRES):
        _bas, _haut = _bornes[_i] + 1, _bornes[_i + 1]
        _label = f"{_bas}-{_haut}"
        _ORDRE_TRANCHES.append(_label)
        # Conditions ENCHAÎNÉES (<= borne haute) plutôt que BETWEEN(bas, haut) :
        # une valeur décimale (ex. 400.5) ne tombe plus entre deux tranches.
        _expr_tranche = _expr_tranche.when(
            pl.col("ic_construction") <= _haut
        ).then(pl.lit(_label))
    _ORDRE_TRANCHES.append(f"> {_bornes[-1]}")
    _expr_tranche = _expr_tranche.when(pl.col("ic_construction") > _bornes[-1]).then(
        pl.lit(f"> {_bornes[-1]}")
    ).otherwise(pl.lit("Inconnu"))

    _df = _df.with_columns(_expr_tranche.alias("tranche_ic"))

    print(f"Bâtiments après filtres (avant retrait Inconnu) : {_df.height}")

    # Retire les bâtiments sans ic_construction connu (tranche "Inconnu") : pas
    # affichés dans le graphique.
    _df_graph = _df.filter(pl.col("tranche_ic") != "Inconnu")
    print(f"Bâtiments utilisés pour le graphique : {_df_graph.height}")

    # --- 3. Agrégation pour le graphique (toujours en polars) -------------------
    _agg = (
        _df_graph
        .group_by(["seuil", "tranche_ic"])
        .agg(pl.len().alias("nb_batiments"))
    )

    _tranches_presentes = [t for t in _ORDRE_TRANCHES if t in _agg["tranche_ic"].unique().to_list()]

    _valeurs_seuils = _agg["seuil"].unique().to_list()
    _ordre_seuils = sorted(v for v in _valeurs_seuils if v != "Inconnu")
    if "Inconnu" in _valeurs_seuils:
        _ordre_seuils.append("Inconnu")


    def _degrade_couleurs(n, debut, fin):
        def _hex_vers_rgb(h):
            h = h.lstrip("#")
            return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))

        r1, g1, b1 = _hex_vers_rgb(debut)
        r2, g2, b2 = _hex_vers_rgb(fin)
        if n == 1:
            return [debut]
        return [
            "#{:02x}{:02x}{:02x}".format(
                round(r1 + (r2 - r1) * i / (n - 1)),
                round(g1 + (g2 - g1) * i / (n - 1)),
                round(b1 + (b2 - b1) * i / (n - 1)),
            )
            for i in range(n)
        ]


    _couleurs = _degrade_couleurs(len(_tranches_presentes), "E2ADF2", "574AE2")
    _couleur_par_tranche = dict(zip(_tranches_presentes, _couleurs))

    _fig = px.bar(
        _agg,
        x="seuil",
        y="nb_batiments",
        color="tranche_ic",
        barmode="stack",
        category_orders={"seuil": _ordre_seuils, "tranche_ic": _tranches_presentes},
        color_discrete_map=_couleur_par_tranche,
        labels={
            "seuil": "Seuil IC Construction",
            "nb_batiments": "Nombre de bâtiments",
            "tranche_ic": "Tranche IC Construction",
        },
        title=f"<b>Graphique 1 — {GRAPHIQUES[1]} — {dropdown_usage.value}</b><br>"
              f"<sup>{SOUS_TITRE_FILTRES}</sup>",
    )
    _fig.update_layout(
        xaxis_type="category",
        xaxis=dict(title="Seuil IC Construction", categoryorder="array", categoryarray=_ordre_seuils),
        yaxis=dict(title="Nombre de bâtiments"),
        bargap=0.4,
        bargroupgap=0.0,
        width=900,
        height=550,
        margin=dict(t=100),
    )
    _fig.update_traces(width=0.7)

    _totaux_par_seuil = _agg.group_by("seuil").agg(pl.col("nb_batiments").sum().alias("total"))
    for _seuil, _total in zip(_totaux_par_seuil["seuil"], _totaux_par_seuil["total"]):
        _fig.add_annotation(
            x=str(_seuil), y=_total, text=str(_total), showarrow=False, yshift=10,
            font=dict(size=13, color="black"),
        )

    _graphique = mo.ui.plotly(_fig)

    # Export : les données TRACÉES (nombre de bâtiments par seuil x tranche d'IC)
    mo.vstack([_graphique, boutons_export(_agg.sort("seuil", "tranche_ic"), "graphique_1_batiments_par_tranche_ic")])
    return


@app.cell(hide_code=True)
def constantes_filtres(pl):
    # ============================================================================
    # CELLULE — Constantes des filtres (surface, matériau), définies en UN seul endroit
    #
    #   - Cas général : tranches de sref_approx (surface de référence approchée, en m²).
    #   - Logement collectif : tranches basées sur surface_baies_rset (taille des
    #     logements), qui remplacent celles de sref pour cet usage.
    #
    # Matériau : "None" est le libellé affiché pour les matériaux NON RENSEIGNÉS
    # (valeur NULL dans la base) -- cf. `appliquer_filtres`.
    #
    # Fournit :
    #   - options_surface(usage)  : options du widget "surface" pour un usage
    #   - LIBELLE_MATERIAU_NUL / MATERIAUX_OPTIONS : options du filtre matériau
    #   - MODE_SURFACE_SREF_APPROX / MODE_SURFACE_SREF : libellés du choix "quel filtre de
    #                               surface s'applique ?" ; SREF_MAX_SLIDER / SREF_PAS_SLIDER :
    #                               bornes du curseur de sref
    #   - CATEGORIES_MATERIAU / MAPPING_MATERIAU / COULEURS_CATEGORIES : regroupement
    #                               des matériaux en 5 catégories (graphiques 3 et 6)
    #   - expr_tranche_surface()  : expression polars donnant la tranche de chaque
    #                               bâtiment (colonne `tranche_sref`)
    # ============================================================================

    # --- Paramètres ---------------------------------------------------------------
    USAGE_LOGEMENT_COLLECTIF = "Logement collectif"
    TRANCHES_SREF = ["< 75 m²", "Entre 75 et 99 m²", "Entre 100 et 149 m²", ">= 150 m²"]
    TRANCHES_LOGEMENT_COLLECTIF = ["Petit logement coll.", "Logement coll. moyen", "Grand logement coll."]
    # Deux filtres de surface possibles (un seul appliqué à la fois, au choix) :
    #   - sref_approx : tranches (colonne `sref_approx` = ancienne colonne sref de la base ;
    #                   surface_baies_rset pour les logements collectifs)
    #   - sref        : plage en m² sur la colonne `sref` (renseignée pour les logements
    #                   collectifs, via la fonction `retrouver_sref`)
    MODE_SURFACE_SREF_APPROX = "sref_approx (tranches de surface)"
    MODE_SURFACE_SREF = "sref (plage en m²)"
    SREF_MAX_SLIDER = 5000          # = SREF_PLATEAU (fonction retrouver_sref) : les bâtiments "plateau" restent inclus
    SREF_PAS_SLIDER = 10
    LIBELLE_MATERIAU_NUL = "None"      # libellé de l'option "matériau non renseigné" (NULL)
    MATERIAUX_OPTIONS = [
        LIBELLE_MATERIAU_NUL,
        "Acier", "Autre", "Béton", "Béton cellulaire", "Béton de bois", "Béton de chanvre",
        "Béton fibré", "Béton haute performance", "Mixte: bois-béton", "Mixte: béton-acier",
        "Pierre", "Terre crue", "Terre cuite", "Bois massif", "Bois massif reconstitué",
    ]
    # Regroupement des 15 matériaux de structure en 5 catégories (graphiques 3 et 6)
    CATEGORIES_MATERIAU = ["Sans info", "Béton", "Terre cuite", "Acier", "Bas Carbone"]
    MAPPING_MATERIAU = {
        "Autre": "Sans info",
        "Béton": "Béton", "Béton cellulaire": "Béton", "Béton de bois": "Béton",
        "Béton fibré": "Béton", "Béton haute performance": "Béton",
        "Béton de chanvre": "Béton", "Mixte: béton-acier": "Béton",
        "Terre cuite": "Terre cuite",
        "Acier": "Acier",
        "Mixte: bois-béton": "Bas Carbone", "Pierre": "Bas Carbone", "Terre crue": "Bas Carbone",
        "Bois massif": "Bas Carbone", "Bois massif reconstitué": "Bas Carbone",
    }
    COULEURS_CATEGORIES = {
        "Sans info": "#EDEDED", "Béton": "#B0A99F", "Terre cuite": "#A26E2E",
        "Acier": "#475F8F", "Bas Carbone": "#79A757",
    }

    _SEUIL_PETIT = 50      # surface_baies_rset <  50 -> petit
    _SEUIL_GRAND = 200     # surface_baies_rset > 200 -> grand (50 à 200 inclus -> moyen)


    def options_surface(usage):
        """Options du filtre surface selon l'usage choisi."""
        return TRANCHES_LOGEMENT_COLLECTIF if usage == USAGE_LOGEMENT_COLLECTIF else TRANCHES_SREF


    def expr_tranche_surface():
        """Tranche de surface de chaque bâtiment. Le choix se fait ligne par ligne
        sur la colonne `usage` : logement collectif -> tranches de
        surface_baies_rset ; sinon -> tranches de sref_approx. Valeur absente -> "Inconnu"."""
        _baies = pl.col("surface_baies_rset").cast(pl.Float64, strict=False)
        _tranche_logement_collectif = (
            pl.when(_baies < _SEUIL_PETIT).then(pl.lit(TRANCHES_LOGEMENT_COLLECTIF[0]))
            .when(_baies.is_between(_SEUIL_PETIT, _SEUIL_GRAND)).then(pl.lit(TRANCHES_LOGEMENT_COLLECTIF[1]))
            .when(_baies > _SEUIL_GRAND).then(pl.lit(TRANCHES_LOGEMENT_COLLECTIF[2]))
            .otherwise(pl.lit("Inconnu"))
        )
        # Bornes SUPÉRIEURES exclusives, enchaînées : aucune valeur décimale (ex. 99.5)
        # ne tombe entre deux tranches.
        _tranche_sref = (
            pl.when(pl.col("sref_approx") < 75).then(pl.lit(TRANCHES_SREF[0]))
            .when(pl.col("sref_approx") < 100).then(pl.lit(TRANCHES_SREF[1]))
            .when(pl.col("sref_approx") < 150).then(pl.lit(TRANCHES_SREF[2]))
            .when(pl.col("sref_approx") >= 150).then(pl.lit(TRANCHES_SREF[3]))
            .otherwise(pl.lit("Inconnu"))
        )
        return (
            pl.when(pl.col("usage") == USAGE_LOGEMENT_COLLECTIF)
            .then(_tranche_logement_collectif)
            .otherwise(_tranche_sref)
        )

    return (
        CATEGORIES_MATERIAU,
        COULEURS_CATEGORIES,
        LIBELLE_MATERIAU_NUL,
        MAPPING_MATERIAU,
        MATERIAUX_OPTIONS,
        MODE_SURFACE_SREF,
        MODE_SURFACE_SREF_APPROX,
        SREF_MAX_SLIDER,
        SREF_PAS_SLIDER,
        USAGE_LOGEMENT_COLLECTIF,
        expr_tranche_surface,
        options_surface,
    )


@app.cell(hide_code=True)
def filtres_communs(
    LIBELLE_MATERIAU_NUL,
    MODE_SURFACE_SREF,
    SREF_MAX_SLIDER,
    cacher_inconnu,
    choix_de_attestation,
    choix_de_la_date,
    choix_de_surface,
    choix_materiau_structure,
    choix_mode_surface,
    choix_sref,
    choix_valide_regles,
    choix_zone_climatique,
    expr_tranche_surface,
    mo,
    pl,
):
    # ============================================================================
    # CELLULE — Filtres temps réel COMMUNS à tous les graphiques
    #
    # Une seule définition de la logique de filtrage (au lieu d'une copie par
    # graphique). Fournit :
    #   - FILTRES            : dict des sélections actives
    #   - SOUS_TITRE_FILTRES : texte résumant les filtres (sous-titre de TOUS les graphiques)
    #   - SOUS_TITRE_SANS_MATERIAU : idem sans le matériau (graphique où il est l'axe)
    #   - appliquer_filtres  : fonction (DataFrame -> DataFrame filtré)
    #   - valeurs_actives    : "tout sélectionné = pas de filtre" (réutilisable)
    #   - resume_filtres     : résumé lisible des filtres actifs (affiché sous le panneau
    #                          de filtres de chaque graphique)
    #
    # Toute modification d'un widget relance cette cellule, donc tous les
    # graphiques qui en dépendent.
    # ============================================================================

    # ============================================================================
    # PARAMÈTRES (toutes les variables au même endroit)
    # ============================================================================
    _VALID_REGLES = choix_valide_regles.value
    _CACHER_INCONNU = cacher_inconnu.value


    def valeurs_actives(widget):
        """Sélection d'un widget sous forme de liste, remplacée par [] si
        TOUTES les options sont sélectionnées (= pas de filtre réel).
        Les options sont lues dynamiquement sur le widget : aucune liste codée
        en dur à maintenir."""
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
        # Surface : UN SEUL des deux filtres est appliqué, selon `mode_surface`
        "mode_surface": "sref" if choix_mode_surface.value == MODE_SURFACE_SREF else "sref_approx",
        "sref_approx": valeurs_actives(choix_de_surface),           # tranches
        "sref_plage": [int(v) for v in choix_sref.value],           # [min, max] en m²
        "zones": valeurs_actives(choix_zone_climatique),
        "materiaux": valeurs_actives(choix_materiau_structure),
        "cacher_inconnu": _CACHER_INCONNU,
    }


    # --- Sous-titre commun à tous les graphiques (résumé des filtres actifs) ------
    def _resume(valeurs, si_vide="toutes"):
        return ", ".join(str(v) for v in valeurs) if valeurs else si_vide

    # Plage de sref "pleine" (0 -> max du curseur) = pas de filtre réel
    _SREF_PLAGE_ACTIVE = FILTRES["sref_plage"] != [0, SREF_MAX_SLIDER]
    if FILTRES["mode_surface"] == "sref":
        _texte_surface = (
            f"sref : {FILTRES['sref_plage'][0]}-{FILTRES['sref_plage'][1]} m²" if _SREF_PLAGE_ACTIVE else "sref : toutes"
        )
    else:
        _texte_surface = f"sref_approx : {_resume(FILTRES['sref_approx'])}"

    _sous_titre_sans_materiau = (
        f"Surface ({_texte_surface}) — "
        f"Années de dépôt PC : {_resume(FILTRES['annees'])} — "
        f"Types d'attestation : {_resume(FILTRES['attestations'])} — "
        f"Zone climatique : {_resume(FILTRES['zones'])}"
    )
    SOUS_TITRE_FILTRES = f"{_sous_titre_sans_materiau} — Matériau structure : {_resume(FILTRES['materiaux'], 'tous')}"
    # Variante pour les graphiques où le matériau est l'AXE (donc non filtré)
    SOUS_TITRE_SANS_MATERIAU = _sous_titre_sans_materiau


    # --- Résumé des filtres actifs, par catégorie (même découpage que le panneau) --
    def resume_filtres(avec_materiau=True, avec_inconnus=True):
        """Encadré résumant les filtres actifs, rangés comme dans le panneau.
        - avec_materiau=False : graphique où le matériau est l'axe (filtre non appliqué).
        - avec_inconnus=False : graphique qui n'applique pas « Masquer les inconnus »."""
        _qualite = [
            "bâtiments validés seulement" if _VALID_REGLES else "tous les bâtiments (non validés inclus)"
        ]
        if avec_inconnus:
            _qualite.append("« Inconnu » masqués" if _CACHER_INCONNU else "« Inconnu » inclus")
        _periode = [
            f"années {_resume(FILTRES['annees'])}",
            f"attestations {_resume(FILTRES['attestations'])}",
            f"zones {_resume(FILTRES['zones'])}",
        ]
        _batiment = [f"surface ({_texte_surface})"]
        if avec_materiau:
            _batiment.append(f"matériaux {_resume(FILTRES['materiaux'], 'tous')}")
        return mo.callout(
            mo.md(
                "**Filtres actifs**  \n"
                f"**Qualité** : {' · '.join(_qualite)}  \n"
                f"**Période et lieu** : {' · '.join(_periode)}  \n"
                f"**Bâtiment** : {' · '.join(_batiment)}"
            ),
            kind="neutral",
        )


    # --- Filtre matériau : l'option "None" correspond aux matériaux NON renseignés
    # (NULL dans la base ; on accepte aussi un éventuel texte "None").
    def _expr_materiau(selection):
        _materiau = pl.col("dc_materiau_structure")
        _valeurs = [m for m in selection if m != LIBELLE_MATERIAU_NUL]
        _expr = _materiau.is_in(_valeurs).fill_null(False)
        if LIBELLE_MATERIAU_NUL in selection:
            _expr = _expr | _materiau.is_null() | (_materiau == LIBELLE_MATERIAU_NUL)
        return _expr


    def appliquer_filtres(df, *, filtre_materiau=True, filtre_inconnu=True, verbeux=True):
        """Applique les filtres temps réel (polars, aucun appel réseau).

        - filtre_materiau=False : ne filtre pas sur le matériau (graphiques où
          le matériau est l'axe du graphique).
        - filtre_inconnu=True : respecte l'option "Masquer les inconnus".
        Ajoute aussi la colonne `tranche_sref`.
        """
        # --- Tranche de surface (sref_approx, ou surface_baies_rset pour les logements
        #     collectifs) : cf. cellule `constantes_filtres` ---------------------
        df = df.with_columns(expr_tranche_surface().alias("tranche_sref"))

        if (FILTRES["mode_surface"] == "sref" and _SREF_PLAGE_ACTIVE and df.height > 0
                and df["sref"].null_count() == df.height):
            print("  ATTENTION : la colonne `sref` est vide (renseignée seulement pour les "
                  "logements collectifs, via `retrouver_sref`) : le filtre sref exclut tout.")

        # --- Liste des filtres : (libellé, actif ?, expression polars) ---------
        _filtres = [
            ("règles de validation", FILTRES["regles_validation"],
             pl.col("regle_validation_globale") == True),
            ("années de dépôt", bool(FILTRES["annees"]),
             pl.col("annees_depot_pc").list.eval(pl.element().is_in(FILTRES["annees"])).list.any().fill_null(False)),
            ("type d'attestation", bool(FILTRES["attestations"]),
             pl.col("types_attestation").list.eval(pl.element().is_in(FILTRES["attestations"])).list.any().fill_null(False)),
            ("surface (sref_approx : tranches)", FILTRES["mode_surface"] == "sref_approx" and bool(FILTRES["sref_approx"]),
             pl.col("tranche_sref").is_in(FILTRES["sref_approx"])),
            ("surface (sref : plage en m²)", FILTRES["mode_surface"] == "sref" and _SREF_PLAGE_ACTIVE,
             pl.col("sref").is_between(FILTRES["sref_plage"][0], FILTRES["sref_plage"][1]).fill_null(False)),
            ("zone climatique", bool(FILTRES["zones"]),
             pl.col("zone_climatique").is_in(FILTRES["zones"])),
            ("matériau de structure", filtre_materiau and bool(FILTRES["materiaux"]),
             _expr_materiau(FILTRES["materiaux"])),
            ("cacher « Inconnu »", filtre_inconnu and FILTRES["cacher_inconnu"],
             pl.col("seuil") != "Inconnu"),
        ]

        if verbeux:
            print(f"Bâtiments au départ : {df.height}")
        for _libelle, _actif, _expression in _filtres:
            if _actif:
                df = df.filter(_expression)
                if verbeux:
                    print(f"  après filtre {_libelle} : {df.height}")
        return df

    return FILTRES, SOUS_TITRE_FILTRES, SOUS_TITRE_SANS_MATERIAU, appliquer_filtres, resume_filtres, valeurs_actives


@app.cell(hide_code=True)
def param_graphique_2(mo, panneau_filtres):
    # Paramètre propre au graphique 2 (le seul qui utilise les 13 lots)
    valeur_exclusion_lots = mo.ui.range_slider(start=0, stop=500, step=10, value=[0, 300], label="Un lot est compris entre :", show_value=True)

    mo.vstack([
        mo.md("### Paramètres du graphique 2"),
        panneau_filtres({
            "Graphique 2": mo.vstack([
                valeur_exclusion_lots,
                mo.md("*pour exclure les valeurs anormales (un lot hors de cette plage est ignoré dans la moyenne)*"),
            ]),
        }),
    ])
    return (valeur_exclusion_lots,)



@app.cell(hide_code=True)
def resume_filtres_graphique_2(resume_filtres):
    # Résumé des filtres actifs du graphique 2 (cellule séparée : il lit les valeurs
    # des widgets, alors que le panneau ci-dessus reste statique).
    resume_filtres()
    return


@app.cell(hide_code=True)
def graphique_2(
    GRAPHIQUES,
    DATA_brut,
    SOUS_TITRE_FILTRES,
    appliquer_filtres,
    boutons_export,
    dropdown_usage,
    mo,
    pl,
    px,
    valeur_exclusion_lots,
):
    # ============================================================================
    # CELLULE — Graphique 2 (lots)
    #
    # Part de DATA_brut (variable globale, cellule d'extraction),
    # AUCUN appel réseau ici. Applique tous les filtres temps réel en polars :
    # règles de validation, exclusion MIN/MAX des lots, surface, années,
    # attestation, zone climatique, matériau de structure, et l'option pour
    # cacher la colonne "Inconnu" -- tous gérés par la cellule `filtres_communs`.
    # ============================================================================

    _IC_COLS = [f"ic_composant_lot_{i}" for i in range(1, 14)]

    _NOMS_LOTS = {
        "ic_composant_lot_1": "1. VRD",
        "ic_composant_lot_2": "2. Fondations",
        "ic_composant_lot_3": "3. Superstructure",
        "ic_composant_lot_4": "4. Couverture",
        "ic_composant_lot_5": "5. Cloisonnement",
        "ic_composant_lot_6": "6. Façades",
        "ic_composant_lot_7": "7. Revêtements intérieurs",
        "ic_composant_lot_8": "8. CVC",
        "ic_composant_lot_9": "9. Installations sanitaires",
        "ic_composant_lot_10": "10. Courant fort",
        "ic_composant_lot_11": "11. Courant faible",
        "ic_composant_lot_12": "12. Appareils élévateurs",
        "ic_composant_lot_13": "13. Photovoltaique",
    }

    _couleurs = {
        "ic_composant_lot_1": "#808080",
        "ic_composant_lot_2": "#9ECAE1", "ic_composant_lot_3": "#2171B5",
        "ic_composant_lot_4": "#FCBBA1", "ic_composant_lot_5": "#FC9272",
        "ic_composant_lot_6": "#EF3B2C", "ic_composant_lot_7": "#99000D",
        "ic_composant_lot_8": "#BAE4B3", "ic_composant_lot_9": "#74C476",
        "ic_composant_lot_10": "#41AB5D", "ic_composant_lot_11": "#238B45",
        "ic_composant_lot_12": "#006D2C", "ic_composant_lot_13": "#00441B",
    }

    # --- 1. Filtres communs (cellule `filtres_communs`) --------------------------
    _df = appliquer_filtres(DATA_brut)

    mo.stop(_df.height == 0, mo.md("**Aucun bâtiment ne correspond aux filtres choisis.**"))

    # --- 2. Exclusion MIN/MAX des valeurs de lots (propre à ce graphique) --------
    # Équivalent polars de l'ancien AVG(CASE WHEN lot BETWEEN min AND max ...) :
    # un lot hors plage est mis à null, donc ignoré par .mean() ; le bâtiment
    # reste compté et ses autres lots restent utilisés.
    _MIN_EXCLUSION, _MAX_EXCLUSION = valeur_exclusion_lots.value
    for _lot in _IC_COLS:
        _df = _df.with_columns(
            pl.when(pl.col(_lot).is_between(_MIN_EXCLUSION, _MAX_EXCLUSION))
            .then(pl.col(_lot))
            .otherwise(None)
            .alias(_lot)
        )
    print(f"Bâtiments après filtres : {_df.height}")

    # --- 3. Agrégation par seuil (comptage + moyennes), en polars --------------
    _agg = _df.group_by("seuil").agg(
        pl.len().alias("nb_batiments"),
        pl.col("ic_composant").mean().alias("moyenne_ic_composant"),
        *[pl.col(_lot).mean().alias(_lot) for _lot in _IC_COLS],
    )

    # (l'option "Masquer les inconnus" est gérée dans appliquer_filtres)

    _ordre_seuils_disponibles = ["RE2022", "RE2025", "RE2028", "RE2031", "Inconnu"]
    _ordre_seuils_plot = [s for s in _ordre_seuils_disponibles if s in _agg["seuil"].to_list()]

    _nb_batiments_par_seuil = dict(zip(_agg["seuil"], _agg["nb_batiments"]))

    # --- 4. Passage en format long (unpivot) pour le graphique empilé ----------
    _df_long = _agg.unpivot(
        index=["seuil", "moyenne_ic_composant", "nb_batiments"],
        on=_IC_COLS,
        variable_name="composant",
        value_name="ic_moyen",
    )
    _df_long = (
        _df_long
        .with_columns(pl.col("composant").str.extract(r"(\d+)$").cast(pl.Int64).alias("_lot"))
        .sort(["seuil", "_lot"])
    )

    # --- 5. Graphique en barres empilées ---------------------------------------
    _fig = px.bar(
        _df_long,
        x="seuil",
        y="ic_moyen",
        color="composant",
        barmode="stack",
        category_orders={"seuil": _ordre_seuils_plot, "composant": _IC_COLS},
        color_discrete_map=_couleurs,
        labels={"seuil": "Seuil IC construction atteint", "ic_moyen": "IC moyen", "composant": "Lot"},
    )

    for _trace in _fig.data:
        if _trace.name in _NOMS_LOTS:
            _trace.name = _NOMS_LOTS[_trace.name]

    _fig.add_scatter(
        # UN point par seuil (et non un par lot : la moyenne est répétée sur les 13 lignes)
        x=_agg["seuil"].to_list(),
        y=_agg["moyenne_ic_composant"].to_list(),
        mode="markers+text",
        name="Moyenne IC composant",
        marker={"size": 10, "color": "black", "symbol": "circle"},
        text=[
            f"{v:.0f}" if v is not None else ""
            for v in _agg["moyenne_ic_composant"].to_list()
        ],
        textposition="top center",
        textfont={
            "size": 12,
            "color": "black",
            "family": "Arial Black",
        },
        hovertemplate="<b>%{x}</b><br>Moyenne IC composant : %{y:.2f}<extra></extra>",
    )

    # --- 6. Proportions par groupe de lots (2-3 ; 4-7 ; 8-13) -----------------
    # Calculées sur les lots 2 à 13 uniquement (lot 1 exclu du dénominateur).
    _groupes = {
        "Lots 2–3": ["ic_composant_lot_2", "ic_composant_lot_3"],
        "Lots 4–7": ["ic_composant_lot_4", "ic_composant_lot_5", "ic_composant_lot_6", "ic_composant_lot_7"],
        "Lots 8–13": [f"ic_composant_lot_{i}" for i in range(8, 14)],
    }

    for _seuil in _ordre_seuils_plot:
        if _seuil == "Inconnu":
            continue

        _df_seuil = _df_long.filter(pl.col("seuil") == _seuil)
        _valeurs_lots = {
            _ligne["composant"]: (_ligne["ic_moyen"] if _ligne["ic_moyen"] is not None else 0)
            for _ligne in _df_seuil.iter_rows(named=True)
        }

        _total_lots_2_13 = sum(_valeurs_lots.get(_lot, 0) for _lot in _IC_COLS[1:])
        if _total_lots_2_13 == 0:
            continue

        _position = _valeurs_lots.get("ic_composant_lot_1", 0)

        for _nom_groupe, _lots in _groupes.items():
            _valeur_groupe = sum(_valeurs_lots.get(_lot, 0) for _lot in _lots)
            _proportion = _valeur_groupe / _total_lots_2_13 * 100
            _position_centre = _position + (_valeur_groupe / 2)

            if _nom_groupe == "Lots 2–3":
                _couleur_texte = "#084594"
            elif _nom_groupe == "Lots 4–7":
                _couleur_texte = "#99000D"
            else:
                _couleur_texte = "#0C562A"

            _fig.add_annotation(
                x=_seuil, y=_position_centre, text=f"{_proportion:.0f} %",
                showarrow=False,
                font={"size": 13, "color": _couleur_texte, "family": "Arial Black"},
                xanchor="center", yanchor="middle",
            )
            _position += _valeur_groupe

        # --- Comptage de bâtiments au sommet de la barre ------------------------
        _fig.add_annotation(
            x=_seuil, y=_position, text=f"nb = {_nb_batiments_par_seuil.get(_seuil, 0)}",
            showarrow=False, yshift=40,
            font={"size": 10, "color": "grey"},
            xanchor="center",
        )

    # --- 7. Mise en forme -------------------------------------------------------
    _titre_axe_x = f"Impact carbone des matériaux selon le seuil RE2020 - {dropdown_usage.value}"

    _fig.update_layout(
        height=500,
        width=None,
        template="plotly_white",
        title={
            "text": (
                f"<b>Graphique 2 — {GRAPHIQUES[2]} — {dropdown_usage.value}</b><br>"
                f"<sup>{SOUS_TITRE_FILTRES}</sup>"
            ),
        },
        xaxis={
            "title": _titre_axe_x, "type": "category",
            "categoryorder": "array", "categoryarray": _ordre_seuils_plot,
        },
        yaxis={"title": "kgCO₂e/m².50ans", "rangemode": "tozero"},
        legend_title="Lot",
        legend={"traceorder": "reversed"},
        margin={"l": 60, "r": 20, "t": 90, "b": 60},
    )

    _graphique = mo.ui.plotly(_fig)

    # Export : les données TRACÉES (IC moyen de chaque lot, par seuil)
    mo.vstack([_graphique, boutons_export(
        _df_long.drop("_lot").with_columns(pl.col("composant").replace(_NOMS_LOTS).alias("lot")).drop("composant"),
        "graphique_2_ic_moyen_par_lot",
    )])
    return


@app.cell(hide_code=True)
def param_graphique_3(mo, panneau_filtres):
    # ============================================================================
    # CELLULE D'AFFICHAGE — paramètres (filtres) du graphique 3.
    # Le matériau n'y figure pas : c'est l'axe du graphique.
    # ============================================================================

    mo.vstack([
        mo.md("### Paramètres du graphique 3"),
        panneau_filtres(avec_materiau=False),
    ])
    return



@app.cell(hide_code=True)
def resume_filtres_graphique_3(resume_filtres):
    # Résumé des filtres actifs du graphique 3 (cellule séparée : il lit les valeurs
    # des widgets, alors que le panneau ci-dessus reste statique).
    resume_filtres(avec_materiau=False)
    return


@app.cell(hide_code=True)
def graphique_3(
    GRAPHIQUES,
    CATEGORIES_MATERIAU,
    COULEURS_CATEGORIES,
    DATA_brut,
    MAPPING_MATERIAU,
    SOUS_TITRE_SANS_MATERIAU,
    appliquer_filtres,
    boutons_export,
    dropdown_usage,
    go,
    mo,
    pl,
):
    # ============================================================================
    # GRAPHIQUE 3 — Médiane IC Composant par matériau de structure, par seuil
    # Variante : la LARGEUR de chaque barre est proportionnelle au pourcentage
    # de bâtiments de cette catégorie (façon "Marimekko") -- les barres d'un
    # même seuil se touchent et couvrent ensemble toute la largeur du groupe.
    # ============================================================================


    # ============================================================================
    # PARAMÈTRES
    # ============================================================================

    _USAGE = dropdown_usage.value
    # (les filtres viennent de la cellule `filtres_communs`)


    # (catégories de matériau, mapping et couleurs : cf. cellule `constantes_filtres`)
    _ORDRE_SEUILS = ["RE2022", "RE2025", "RE2028", "RE2031", "Inconnu"]

    # --- Mise en page -------------------------------------------------------------
    _LARGEUR_GROUPE = 1.0          # largeur totale allouée à un seuil (= 100 % de ses bâtiments)
    _ESPACE_ENTRE_SEUILS = 0.5
    _LARGEUR_MIN_BARRE = 0.02       # évite une barre invisible pour une part infime
    _FACTEUR_PROPORTIONNALITE = 0.5  # 0 = toutes les barres égales ; 1 = pleinement
                                     # proportionnel (trop marqué, cf. retour) ; 0.4 =
                                     # un peu plus large/étroit qu'une largeur standard
    _TAILLE_TITRE_GRAPHIQUE = 20


    # ============================================================================
    # 1. FILTRAGE
    # ============================================================================

    _df = appliquer_filtres(DATA_brut, filtre_materiau=False)

    mo.stop(_df.height == 0, mo.md("**Aucun bâtiment ne correspond aux filtres choisis.**"))

    _df = _df.filter(pl.col("ic_composant").is_not_null())
    print(f"  avec ic_composant renseigné : {_df.height}")


    # ============================================================================
    # 2. CATÉGORIE DE MATÉRIAU
    # ============================================================================

    _df = _df.with_columns(
        pl.col("dc_materiau_structure").fill_null("Autre")
        .replace_strict(MAPPING_MATERIAU, default="Sans info", return_dtype=pl.Utf8)
        .alias("categorie_materiau")
    )


    # ============================================================================
    # 3. AGRÉGATION
    # ============================================================================

    _agg = _df.group_by(["seuil", "categorie_materiau"]).agg(
        pl.col("ic_composant").median().alias("mediane_ic"),
        pl.len().alias("nb_batiments"),
    )

    _seuils = [s for s in _ORDRE_SEUILS if s in _agg["seuil"].to_list()]
    _total_par_seuil = {s: _agg.filter(pl.col("seuil") == s)["nb_batiments"].sum() for s in _seuils}
    _valeurs = {
        (row["seuil"], row["categorie_materiau"]): (row["mediane_ic"], row["nb_batiments"])
        for row in _agg.iter_rows(named=True)
    }


    # ============================================================================
    # 4. GRAPHIQUE -- largeur de barre proportionnelle au pourcentage
    # ============================================================================

    _fig = go.Figure()

    _centres_gauche = {}
    _x_courant = 0.0
    for _seuil in _seuils:
        _centres_gauche[_seuil] = _x_courant
        _x_courant += _LARGEUR_GROUPE + _ESPACE_ENTRE_SEUILS

    _tickvals, _ticktext = [], []
    _categories_deja_dans_legende = set()

    for _seuil in _seuils:
        _total_seuil = _total_par_seuil[_seuil]
        _x_debut_barre = _centres_gauche[_seuil]

        # 1ère passe : catégories réellement présentes (n > 0) pour ce seuil,
        # nécessaire pour répartir la "base uniforme" entre elles uniquement.
        _categories_presentes = [
            (cat, *_valeurs[(_seuil, cat)])
            for cat in CATEGORIES_MATERIAU
            if _valeurs.get((_seuil, cat), (0, 0))[1] > 0
        ]
        _largeur_uniforme = _LARGEUR_GROUPE / len(_categories_presentes)

        for _categorie, _mediane, _n in _categories_presentes:
            _pourcentage = _n / _total_seuil * 100
            # Mélange entre une largeur standard (uniforme) et la part
            # proportionnelle réelle -- _FACTEUR_PROPORTIONNALITE règle le dosage.
            _largeur_proportionnelle = _LARGEUR_GROUPE * (_pourcentage / 100)
            _largeur = (
                (1 - _FACTEUR_PROPORTIONNALITE) * _largeur_uniforme
                + _FACTEUR_PROPORTIONNALITE * _largeur_proportionnelle
            )
            _largeur = max(_largeur, _LARGEUR_MIN_BARRE)
            _x_centre = _x_debut_barre + _largeur / 2

            _fig.add_trace(go.Bar(
                x=[_x_centre], y=[_mediane], width=_largeur,
                marker=dict(color=COULEURS_CATEGORIES[_categorie], line=dict(color="#888888", width=0.6)),
                name=_categorie, legendgroup=_categorie,
                showlegend=(_categorie not in _categories_deja_dans_legende),
                hovertemplate=f"{_categorie}<br>{_seuil}<br>Médiane IC : %{{y:.0f}}<br>"
                              f"n = {_n} ({_pourcentage:.0f}%)<extra></extra>",
            ))
            _categories_deja_dans_legende.add(_categorie)

            _fig.add_annotation(
                x=_x_centre, y=_mediane, text=f"nb = {_n}", showarrow=False, yshift=40,
                font={"size": 10, "color": "grey"}, xanchor="center", textangle=-90,
            )
            # La barre étant maintenant assez large pour les grosses catégories,
            # le pourcentage reste simplement centré verticalement.
            _fig.add_annotation(
                x=_x_centre, y=_mediane / 2, text=f"<b>{_pourcentage:.0f}%</b>", showarrow=False,
                font={"size": 11, "color": "black"}, xanchor="center",
            )

            _x_debut_barre += _largeur

        _tickvals.append(_centres_gauche[_seuil] + _LARGEUR_GROUPE / 2)
        _ticktext.append(f"<b>{_seuil}</b><br><span style='font-size:11px;color:gray'>nb total = {_total_seuil}</span>")

    _fig.update_layout(
        template="plotly_white",
        height=560,
        title=dict(
            text=(
                f"<b>Graphique 3 — {GRAPHIQUES[3]} — {_USAGE}</b><br>"
                f"<sup>Largeur des barres proportionnelle à la part de bâtiments</sup><br>"
                f"<sup>{SOUS_TITRE_SANS_MATERIAU}</sup>"
            ),
            font=dict(size=_TAILLE_TITRE_GRAPHIQUE),
        ),
        xaxis=dict(
            tickvals=_tickvals, ticktext=_ticktext, tickfont=dict(size=13),
            range=[-_ESPACE_ENTRE_SEUILS / 2, _x_courant],
        ),
        yaxis=dict(title="Médiane IC Composant (kgCO₂e/m².50ans)"),
        legend=dict(title="Matériau", orientation="h", x=0.5, xanchor="center", y=-0.15, yanchor="top"),
        margin=dict(t=120, b=90, l=60, r=20),
    )

    _graphique = mo.ui.plotly(_fig)

    # Export : les données TRACÉES (médiane d'IC composant, effectif et part
    # de chaque catégorie de matériau, par seuil)
    _export = (
        _agg
        .with_columns(
            (pl.col("nb_batiments") / pl.col("nb_batiments").sum().over("seuil") * 100)
            .round(1).alias("part_pct")
        )
        .sort(pl.col("seuil").replace_strict({s: i for i, s in enumerate(_ORDRE_SEUILS)}, default=99),
              pl.col("categorie_materiau").replace_strict({c: i for i, c in enumerate(CATEGORIES_MATERIAU)}, default=99))
    )
    mo.vstack([_graphique, boutons_export(_export, "graphique_3_mediane_ic_par_materiau")])
    return


@app.cell(hide_code=True)
def param_graphique_4(mo, panneau_filtres):
    # ============================================================================
    # CELLULE D'AFFICHAGE — paramètres (filtres) du graphique 4.
    # ============================================================================

    mo.vstack([
        mo.md("### Paramètres du graphique 4"),
        panneau_filtres(),
    ])
    return



@app.cell(hide_code=True)
def resume_filtres_graphique_4(resume_filtres):
    # Résumé des filtres actifs du graphique 4 (cellule séparée : il lit les valeurs
    # des widgets, alors que le panneau ci-dessus reste statique).
    resume_filtres()
    return


@app.cell(hide_code=True)
def graphique_4(
    GRAPHIQUES,
    DATA_brut,
    SOUS_TITRE_FILTRES,
    appliquer_filtres,
    boutons_export,
    dropdown_usage,
    go,
    mo,
    pl,
):
    # ============================================================================
    # GRAPHIQUE 4 — Q1 / Médiane / Q3 par seuil RE2020, empilé FDES + PEP + DED
    #
    # Part de DATA_brut (cellule d'extraction partagée) : AUCUN appel
    # réseau ici. Tous les filtres sont appliqués en polars, en temps réel.
    #
    # Pour chaque seuil, 3 emplacements resserrés (Q1, Médiane, Q3) :
    #   - Q1 et Q3 : barres empilées (nb_fdes, nb_pep, nb_ded), hauteur de
    #     chaque segment = le quartile (25% ou 75%) de CETTE variable.
    #   - Médiane : 3 points noirs, aux mêmes hauteurs cumulées qu'aurait une
    #     barre empilée des médianes (donc Q1/Médiane/Q3 sont juste les 3
    #     quartiles de chaque variable, empilés de façon cohérente).
    # ============================================================================


    # ============================================================================
    # PARAMÈTRES (toutes les variables au même endroit)
    # ============================================================================

    # --- Widgets : filtres temps réel -------------------------------------------
    _USAGE = dropdown_usage.value
    # (les autres filtres viennent de la cellule `filtres_communs`)


    # --- Les 3 variables empilées, et leurs noms d'affichage --------------------
    _VARIABLES = ["nb_fdes", "nb_pep", "nb_ded"]
    _NOMS_AFFICHES = {"nb_fdes": "Nombre de FDES", "nb_pep": "Nombre de PEP", "nb_ded": "Nombre de DED"}
    _COULEURS_VARIABLES = {"nb_fdes": "#4C72B0", "nb_pep": "#DD8452", "nb_ded": "#55A868"}

    # --- Seuils (Inconnu inclus par défaut, sauf si la case "cacher" est cochée)
    _ORDRE_SEUILS = ["RE2022", "RE2025", "RE2028", "RE2031", "Inconnu"]

    # --- Mise en page -------------------------------------------------------------
    _LARGEUR_BARRE = 0.28      # largeur de chaque colonne Q1/Q3
    _ESPACE_ENTRE_SEUILS = 0.9  # espace entre deux groupes de seuil
    _TAILLE_TITRE_GRAPHIQUE = 20


    # ============================================================================
    # 1. FILTRAGE (polars, temps réel) -- même logique que les autres graphiques
    # ============================================================================

    _df = appliquer_filtres(DATA_brut)

    mo.stop(_df.height == 0, mo.md("**Aucun bâtiment ne correspond aux filtres choisis.**"))


    # ============================================================================
    # 2. AGRÉGATION : quartiles (25/50/75 %) de chaque variable, par seuil
    # ============================================================================

    _agg = _df.group_by("seuil").agg(
        pl.len().alias("nb_batiments"),
        *[pl.col(v).quantile(0.25).alias(f"{v}_q1") for v in _VARIABLES],
        *[pl.col(v).quantile(0.5).alias(f"{v}_median") for v in _VARIABLES],
        *[pl.col(v).quantile(0.75).alias(f"{v}_q3") for v in _VARIABLES],
    )

    _seuils = [s for s in _ORDRE_SEUILS if s in _agg["seuil"].to_list()]
    _par_seuil = {row["seuil"]: row for row in _agg.iter_rows(named=True)}


    # ============================================================================
    # 3. CONSTRUCTION DU GRAPHIQUE
    # ============================================================================

    _fig = go.Figure()

    # Positions x : Q1 et Q3 collés à la Médiane (au milieu), gros espace entre
    # les groupes de seuils.
    _pas_groupe = 3 * _LARGEUR_BARRE + _ESPACE_ENTRE_SEUILS
    _centres = {s: i * _pas_groupe for i, s in enumerate(_seuils)}

    _tickvals, _ticktext = [], []
    _annotations = []

    for _seuil in _seuils:
        _ligne = _par_seuil[_seuil]
        _x_q1 = _centres[_seuil]
        _x_median = _x_q1 + _LARGEUR_BARRE
        _x_q3 = _x_q1 + 2 * _LARGEUR_BARRE

        # --- Colonnes Q1 et Q3 (empilées) --------------------------------------
        for _quantile, _x in (("q1", _x_q1), ("q3", _x_q3)):
            _bas = 0
            for _var in _VARIABLES:
                _valeur = _ligne[f"{_var}_{_quantile}"] or 0
                _fig.add_trace(go.Bar(
                    x=[_x], y=[_valeur], base=_bas, width=_LARGEUR_BARRE,
                    marker_color=_COULEURS_VARIABLES[_var],
                    name=_NOMS_AFFICHES[_var],
                    legendgroup=_var,
                    showlegend=(_seuil == _seuils[0] and _quantile == "q1"),
                    hovertemplate=f"{_NOMS_AFFICHES[_var]}<br>{_seuil} ({_quantile.upper()}) : %{{y:.1f}}<extra></extra>",
                ))
                _bas += _valeur
            _annotations.append(dict(
                x=_x, y=_bas, text=f"<b>{_bas:.0f}</b>", showarrow=False, yshift=10, font=dict(size=12),
            ))

        # --- 3 points noirs de la médiane, aux hauteurs cumulées ----------------
        _bas = 0
        _y_points = []
        for _var in _VARIABLES:
            _bas += _ligne[f"{_var}_median"] or 0
            _y_points.append(_bas)
        _fig.add_trace(go.Scatter(
            x=[_x_median] * 3, y=_y_points, mode="markers",
            marker=dict(color="black", size=9, symbol="circle"),
            name="Médiane", legendgroup="mediane",
            showlegend=(_seuil == _seuils[0]),
            hovertemplate="Médiane cumulée : %{y:.1f}<extra></extra>",
        ))
        _annotations.append(dict(
            x=_x_median, y=_bas, text=f"<b>{_bas:.0f}</b>", showarrow=False, yshift=10, font=dict(size=12),
        ))

        # --- Étiquettes Q1 / Q3 sous les barres ---------------------------------
        _tickvals += [_x_q1, _x_q3]
        _ticktext += ["Q1", "Q3"]

        # --- Nom du seuil, centré sous le groupe --------------------------------
        _annotations.append(dict(
            x=_x_median, y=0, yref="paper", yshift=-42, showarrow=False,
            text=f"<b>{_seuil}</b><br><span style='font-size:11px;color:gray'>n = {_ligne['nb_batiments']}</span>",
            font=dict(size=13),
        ))

    _fig.update_layout(
        barmode="overlay",  # les barres sont déjà positionnées par base=..., pas de superposition
        template="plotly_white",
        height=560,
        title=dict(
            text=f"<b>Graphique 4 — {GRAPHIQUES[4]} — {_USAGE}</b><br>"
                 f"<sup>Empilement Nombre de FDES + Nombre de PEP + Nombre de DED</sup><br>"
                 f"<sup>{SOUS_TITRE_FILTRES}</sup>",
            font=dict(size=_TAILLE_TITRE_GRAPHIQUE),
        ),
        xaxis=dict(
            tickvals=_tickvals, ticktext=_ticktext, tickfont=dict(size=10, color="gray"),
            range=[-_LARGEUR_BARRE, max(_centres.values()) + 2 * _LARGEUR_BARRE + _LARGEUR_BARRE],
        ),
        yaxis=dict(title="Nombre de fiches"),
        legend=dict(orientation="h", x=0.5, xanchor="center", y=-0.22, yanchor="top"),
        margin=dict(t=130, b=110, l=60, r=20),
        annotations=_annotations,
    )

    _graphique = mo.ui.plotly(_fig)

    # Export : les données TRACÉES (Q1 / médiane / Q3 de chaque variable, par seuil)
    _export = _agg.sort(pl.col("seuil").replace_strict({s: i for i, s in enumerate(_ORDRE_SEUILS)}, default=99))
    mo.vstack([_graphique, boutons_export(_export, "graphique_4_quartiles_fiches_par_seuil")])
    return


@app.cell(hide_code=True)
def param_graphique_5(mo, panneau_filtres):
    # ============================================================================
    # CELLULE WIDGET — filtre "seuil RE2020" pour le graphique des écarts
    #
    # À placer AVANT la cellule graphique (marimo exige qu'un widget soit défini
    # dans une autre cellule que celle qui lit sa valeur).
    # Tout coché par défaut = "Tous" (pas de filtre réel).
    # ============================================================================

    choix_seuil = mo.ui.multiselect(
        options=["RE2022", "RE2025", "RE2028", "RE2031"],
        value=["RE2022", "RE2025", "RE2028", "RE2031"],
        label="Seuil RE2020",
    )

    mo.vstack([
        mo.md("### Paramètres du graphique 5"),
        panneau_filtres({"Graphique 5": choix_seuil}),
    ])
    return (choix_seuil,)



@app.cell(hide_code=True)
def resume_filtres_graphique_5(resume_filtres):
    # Résumé des filtres actifs du graphique 5 (cellule séparée : il lit les valeurs
    # des widgets, alors que le panneau ci-dessus reste statique).
    resume_filtres()
    return


@app.cell(hide_code=True)
def graphique_5(
    GRAPHIQUES,
    DATA_brut,
    SOUS_TITRE_FILTRES,
    appliquer_filtres,
    boutons_export,
    choix_seuil,
    dropdown_usage,
    go,
    mo,
    pl,
    valeurs_actives,
):
    import math
    import statistics
    from plotly.subplots import make_subplots
    # ============================================================================
    # GRAPHIQUE 5 — Écart des bâtiments aux différents seuils (en %)
    #
    # Part de DATA_brut (cellule d'extraction partagée) : AUCUN appel
    # réseau ici. Tous les filtres sont appliqués en polars, en temps réel.
    #
    # écart (%) = (valeur_bâtiment - seuil_max) / seuil_max * 100
    #   -> positif = le bâtiment DÉPASSE le seuil (non conforme)
    #   -> négatif = le bâtiment est SOUS le seuil (conforme)
    #
    # Pour ic_construction et ic_energie, le seuil applicable (_max_2022/2025/
    # 2028/2031) dépend de la date de dépôt PC la plus ancienne du bâtiment,
    # et ce choix est fait séparément pour les deux indicateurs.
    # ============================================================================


    # ============================================================================
    # PARAMÈTRES (toutes les variables au même endroit)
    # ============================================================================

    # --- Widgets : filtres temps réel -------------------------------------------
    _USAGE = dropdown_usage.value
    # (les filtres viennent de la cellule `filtres_communs`)

    # Nouveau filtre : seuil RE2020 (RE2022/25/28/31/Tous). "Tous" = toutes les
    # options cochées dans le multiselect -> reset à [] comme les autres filtres.
    _SEUIL_FILTRE = valeurs_actives(choix_seuil)


    # --- Les 6 indicateurs : (nom affiché, colonne bâtiment, colonne(s) seuil) --
    # Pour bbio/cep/cep_nr/dh : une seule colonne de seuil, fixe.
    # Pour ic_construction/ic_energie : 4 colonnes de seuil (selon la date de
    # dépôt la plus ancienne), sélectionnées via _expr_seuil_applicable ci-dessous.
    _INDICATEURS_SIMPLES = [
        ("Bbio", "bbio_batiment", "bbio_max"),
        ("Cep", "cep_batiment", "cep_max"),
        ("Cep non renouvelable", "cep_nr_batiment", "cep_nr_max"),
        ("DH", "dh_batiment", "dh_max"),
    ]
    _INDICATEURS_DATES = [
        ("IC Construction", "ic_construction", "ic_construction_max"),
        ("IC Énergie", "ic_energie", "ic_energie_max"),
    ]

    _COULEURS_INDICATEURS = {
        "Bbio": "#4C72B0", "Cep": "#DD8452", "Cep non renouvelable": "#C44E52",
        "DH": "#8172B2", "IC Construction": "#55A868", "IC Énergie": "#CCB974",
    }

    _NB_COLONNES_GRILLE = 3
    _TAILLE_TITRE_PRINCIPAL = 24   # le choix du filtre "seuil", en grand
    _TAILLE_TITRE_INDICATEUR = 15


    # ============================================================================
    # 1. FILTRAGE (polars, temps réel) -- filtres communs aux autres graphiques
    # ============================================================================

    _df = appliquer_filtres(DATA_brut)
    if _SEUIL_FILTRE:
        _df = _df.filter(pl.col("seuil").is_in(_SEUIL_FILTRE))
        print(f"  après filtre seuil RE2020 : {_df.height}")

    mo.stop(_df.height == 0, mo.md("**Aucun bâtiment ne correspond aux filtres choisis.**"))


    # ============================================================================
    # 2. SEUIL APPLICABLE POUR IC CONSTRUCTION / IC ÉNERGIE
    #    (selon la date de dépôt PC la plus ancienne du bâtiment)
    # ============================================================================

    _date_la_plus_ancienne = pl.col("annees_depot_pc").list.min()


    def _expr_seuil_applicable(prefixe_colonne):
        """Choisit la bonne colonne _max_20XX selon la date de dépôt la plus
        ancienne (calcul indépendant pour chaque indicateur, comme demandé).

        Ignore silencieusement un palier dont la colonne _max_20XX n'existe pas
        dans DATA_brut (ex. ic_energie_max_2031, absente de la base) :
        les bâtiments concernés par ce palier auront alors un écart non calculé
        (None) pour cet indicateur, plutôt que de faire planter la requête.
        """
        paliers = [
            (_date_la_plus_ancienne < 2025, f"{prefixe_colonne}_2022"),
            (_date_la_plus_ancienne.is_between(2025, 2027), f"{prefixe_colonne}_2025"),
            (_date_la_plus_ancienne.is_between(2028, 2030), f"{prefixe_colonne}_2028"),
            (_date_la_plus_ancienne >= 2031, f"{prefixe_colonne}_2031"),
        ]
        paliers_disponibles = [(condition, colonne) for condition, colonne in paliers if colonne in _df.columns]

        if not paliers_disponibles:
            return pl.lit(None)

        expression = pl.when(paliers_disponibles[0][0]).then(pl.col(paliers_disponibles[0][1]))
        for condition, colonne in paliers_disponibles[1:]:
            expression = expression.when(condition).then(pl.col(colonne))
        return expression.otherwise(None)


    for _nom, _col_valeur, _prefixe_seuil in _INDICATEURS_DATES:
        _df = _df.with_columns(_expr_seuil_applicable(_prefixe_seuil).alias(f"_seuil_applicable__{_col_valeur}"))


    # ============================================================================
    # 3. CALCUL DE L'ÉCART (%) POUR CHAQUE INDICATEUR
    # ============================================================================

    _indicateurs = []  # liste de (nom, colonne_écart)

    for _nom, _col_valeur, _col_seuil in _INDICATEURS_SIMPLES:
        _col_ecart = f"_ecart__{_col_valeur}"
        _df = _df.with_columns(
            pl.when(pl.col(_col_seuil).is_not_null() & (pl.col(_col_seuil) != 0))
            .then((pl.col(_col_valeur) - pl.col(_col_seuil)) / pl.col(_col_seuil) * 100)
            .otherwise(None)
            .alias(_col_ecart)
        )
        _indicateurs.append((_nom, _col_ecart))

    for _nom, _col_valeur, _prefixe_seuil in _INDICATEURS_DATES:
        _col_seuil_applicable = f"_seuil_applicable__{_col_valeur}"
        _col_ecart = f"_ecart__{_col_valeur}"
        _df = _df.with_columns(
            pl.when(pl.col(_col_seuil_applicable).is_not_null() & (pl.col(_col_seuil_applicable) != 0))
            .then((pl.col(_col_valeur) - pl.col(_col_seuil_applicable)) / pl.col(_col_seuil_applicable) * 100)
            .otherwise(None)
            .alias(_col_ecart)
        )
        _indicateurs.append((_nom, _col_ecart))


    # ============================================================================
    # 4. GRAPHIQUE : une boîte (avec tous les points) par indicateur
    # ============================================================================

    _points_export = []  # un DataFrame par indicateur (rempli dans la boucle)
    _nb_lignes = math.ceil(len(_indicateurs) / _NB_COLONNES_GRILLE)

    _fig = make_subplots(
        rows=_nb_lignes, cols=_NB_COLONNES_GRILLE,
        subplot_titles=[f"<b>{nom}</b>" for nom, _ in _indicateurs],
        vertical_spacing=0.18, horizontal_spacing=0.06,
    )
    _fig.update_annotations(font_size=_TAILLE_TITRE_INDICATEUR)

    for _i, (_nom, _col_ecart) in enumerate(_indicateurs):
        _ligne, _colonne = _i // _NB_COLONNES_GRILLE + 1, _i % _NB_COLONNES_GRILLE + 1

        _df_points = _df.select(["ID", "seuil", _col_ecart]).filter(
            pl.col(_col_ecart).is_not_null()
        )
        # Points tracés de cet indicateur, pour l'export (format long)
        _points_export.append(
            _df_points.rename({_col_ecart: "ecart_pct"}).with_columns(pl.lit(_nom).alias("indicateur"))
            .select(["indicateur", "ID", "seuil", "ecart_pct"])
        )

        _valeurs = _df_points[_col_ecart].to_list()
        _ids = _df_points["ID"].to_list()

        # Un boxplot demande au moins 2 points. Un indicateur peut être vide (ex. seuil
        # non défini pour cet usage ou ces dates) : on l'indique au lieu de planter.
        if len(_valeurs) < 2:
            _fig.add_annotation(
                text="Pas assez de données", showarrow=False, font=dict(size=13, color="gray"),
                xref=f"x{_i + 1 if _i > 0 else ''} domain", yref=f"y{_i + 1 if _i > 0 else ''} domain",
                x=0.5, y=0.5,
            )
            continue

        # ------------------------------------------------------------------------
        # Statistiques du boxplot
        # ------------------------------------------------------------------------
        _q1 = statistics.quantiles(_valeurs, n=4, method="inclusive")[0]
        _mediane = statistics.median(_valeurs)
        _q3 = statistics.quantiles(_valeurs, n=4, method="inclusive")[2]

        # -----------------------------------------------------------------------
        # 1. BOX : forme visuelle du boxplot
        # ------------------------------------------------------------------------
        # La boîte reste étroite (width) et CENTRÉE ; les points sont décalés sur
        # le côté (pointpos) avec un jitter limité à leur propre zone -- boîte et
        # points ne se recouvrent plus, donc leurs hovers respectifs ne se
        # concurrencent plus (cf. explication ci-dessus : Plotly choisit le point
        # de donnée le plus proche du curseur, toutes traces confondues, pas la
        # trace la plus "au-dessus").
        _fig.add_trace(
            go.Box(
                y=_valeurs,
                name=_nom,
                marker_color=_COULEURS_INDICATEURS[_nom],
                boxpoints=False,
                line=dict(width=1.4),
                width=0.5,
                showlegend=False,
                hoverinfo="skip",
            ),
            row=_ligne,
            col=_colonne,
        )

        # ------------------------------------------------------------------------
        # 2. POINTS : décalés à droite de la boîte (pointpos), jitter restreint à
        #    leur propre zone pour ne pas revenir chevaucher la boîte
        # ------------------------------------------------------------------------
        _fig.add_trace(
            go.Box(
                y=_valeurs,
                name=_nom,
                marker_color=_COULEURS_INDICATEURS[_nom],
                boxpoints="all",
                jitter=0.3,
                pointpos=1.5,  # décale le nuage de points à droite, hors de la boîte
                marker=dict(size=3, opacity=0.4),

                # La boîte de cette trace est rendue invisible (seuls les points
                # de CETTE trace sont visibles)
                line=dict(width=0),
                fillcolor="rgba(0,0,0,0)",

                showlegend=False,

                hoveron="points",

                customdata=_ids,
                hovertemplate=(
                    f"<b>{_nom}</b><br>"
                    "Valeur : %{y:.0f} %<br>"
                    "ID : %{customdata}"
                    "<extra></extra>"
                ),
            ),
            row=_ligne,
            col=_colonne,
        )

        # ------------------------------------------------------------------------
        # 3. ZONE DE SURVOL DU BOXPLOT -- uniquement sur la largeur de la boîte
        #    elle-même (pas celle des points), donc plus aucune compétition de
        #    proximité avec les points du nuage.
        # ------------------------------------------------------------------------
        _n_points_hover = 25
        if _q3 != _q1:
            _y_hover = [
                _q1 + (_q3 - _q1) * _j / (_n_points_hover - 1)
                for _j in range(_n_points_hover)
            ]
        else:
            _y_hover = [_q1]

        _fig.add_trace(
            go.Scatter(
                x=[_nom] * len(_y_hover),
                y=_y_hover,
                mode="markers",
                marker=dict(size=28, color="rgba(0,0,0,0.001)"),
                showlegend=False,
                hovertemplate=(
                    f"<b>{_nom}</b><br>"
                    f"Min : {min(_valeurs):.0f} %<br>"
                    f"Q1 : {_q1:.0f} %<br>"
                    f"Médiane : {_mediane:.0f} %<br>"
                    f"Q3 : {_q3:.0f} %<br>"
                    f"Max : {max(_valeurs):.0f} %"
                    "<extra></extra>"
                ),
            ),
            row=_ligne,
            col=_colonne,
        )

        # Ligne de référence à 0 % (seuil atteint pile)
        _fig.add_hline(
            y=0,
            line_dash="dash",
            line_color="gray",
            line_width=1,
            row=_ligne,
            col=_colonne,
        )

        if _valeurs:
            _fig.add_annotation(
                text=f"médiane = {_mediane:.1f} %",
                xref=f"x{_i + 1 if _i > 0 else ''} domain",
                yref=f"y{_i + 1 if _i > 0 else ''} domain",
                x=0.5,
                y=1.0,
                yshift=2,
                showarrow=False,
                font=dict(size=11, color="black"),
            )

    _fig.update_yaxes(title_text="Écart au seuil (%)", col=1)
    _fig.update_xaxes(showticklabels=False)

    # --- Titre : le filtre "seuil" est affiché en grand, comme demandé --------
    _libelle_seuil = ", ".join(_SEUIL_FILTRE) if _SEUIL_FILTRE else "Tous"


    _fig.update_layout(
        template="plotly_white",
        height=_nb_lignes * 380 + 170,
        title=dict(
            text=(
                f"<span style='font-size:{_TAILLE_TITRE_PRINCIPAL}px'><b>Seuil RE2020 : {_libelle_seuil}</b></span><br>"
                f"<span style='font-size:16px'>Graphique 5 — {GRAPHIQUES[5]} — {_USAGE}</span><br>"
                f"<sup>{SOUS_TITRE_FILTRES}</sup>"
            ),
        ),
        margin=dict(t=140, b=40, l=60, r=20),
    )

    _graphique = mo.ui.plotly(_fig)

    # Export : les données TRACÉES (un point par bâtiment et par indicateur :
    # écart au seuil en %, avec l'ID du bâtiment)
    mo.vstack([_graphique, boutons_export(pl.concat(_points_export), "graphique_5_ecarts_aux_seuils")])
    return


@app.cell(hide_code=True)
def param_graphique_6(mo, panneau_filtres):
    # ============================================================================
    # CELLULE WIDGET — paramètres propres au graphique 6 (stock C) :
    #   - filtre "seuil RE2020" (tout coché par défaut = tous les seuils)
    #   - zoom sur l'axe Y (borne haute, en kg C/m²)
    # Le matériau n'y figure pas : c'est l'axe du graphique.
    # ============================================================================

    choix_seuil_stock_c = mo.ui.multiselect(
        options=["RE2022", "RE2025", "RE2028", "RE2031"],
        value=["RE2022", "RE2025", "RE2028", "RE2031"],
        label="Seuil RE2020",
    )

    choix_y_max_stock_c = mo.ui.slider(
        start=50, stop=300, step=10, value=150, show_value=True,
        label="Zoom Axe Y du maximum de stockC",
    )

    mo.vstack([
        mo.md("### Paramètres du graphique 6"),
        panneau_filtres(
            {"Graphique 6": mo.vstack([choix_seuil_stock_c, choix_y_max_stock_c])},
            avec_materiau=False,
        ),
    ])
    return choix_seuil_stock_c, choix_y_max_stock_c



@app.cell(hide_code=True)
def resume_filtres_graphique_6(resume_filtres):
    # Résumé des filtres actifs du graphique 6 (cellule séparée : il lit les valeurs
    # des widgets, alors que le panneau ci-dessus reste statique).
    resume_filtres(avec_materiau=False)
    return


@app.cell(hide_code=True)
def graphique_6(
    GRAPHIQUES,
    DATA_brut,
    MAPPING_MATERIAU,
    SOUS_TITRE_SANS_MATERIAU,
    appliquer_filtres,
    boutons_export,
    choix_seuil_stock_c,
    choix_y_max_stock_c,
    dropdown_usage,
    go,
    mo,
    pl,
):
    # ============================================================================
    # GRAPHIQUE 6 — Stock de carbone (stock_c) par type de matériau de structure
    # ("Bas Carbone" / "Tout le reste") et par
    # seuil RE2020 : une boîte à moustaches par (catégorie, seuil), avec en
    # pointillés les seuils du label "bâtiment biosourcé" (arrêté du 2 juillet 2024).
    #
    # Hypothèse d'unité : stock_c en kg C / m² de surface de plancher, comme les
    # seuils du label (15 / 25 / 45).
    # ============================================================================


    # ============================================================================
    # PARAMÈTRES
    # ============================================================================

    _USAGE = dropdown_usage.value
    _SEUILS_CHOISIS = choix_seuil_stock_c.value
    _Y_MAX = choix_y_max_stock_c.value   # borne haute de l'axe Y (kg C/m²) ; valeurs au-delà coupées
    # (les autres filtres viennent de la cellule `filtres_communs` ; le matériau
    #  n'est pas filtré : c'est l'axe du graphique)

    # Deux types de matériaux seulement : "Bas Carbone" (cf. MAPPING_MATERIAU) et tout le reste
    # (y compris les matériaux non renseignés)
    _CATEGORIE_BAS_CARBONE = "Bas Carbone"
    _CATEGORIE_RESTE = "Tout le reste"
    _CATEGORIES = [_CATEGORIE_BAS_CARBONE, _CATEGORIE_RESTE]

    _ORDRE_SEUILS = ["RE2022", "RE2025", "RE2028", "RE2031"]
    _COULEURS_SEUIL = {"RE2022": "#E2ADF2", "RE2025": "#B58BEA", "RE2028": "#8A6BE6", "RE2031": "#574AE2"}

    # Seuils du label bâtiment biosourcé 2024 (kg C / m²), identiques pour tous les usages
    _SEUILS_LABEL_BIOSOURCE = [(15, "niveau 1"), (25, "niveau 2"), (45, "niveau 3")]
    _COULEUR_LABEL = "#2E7D32"

    _NB_MIN_PAR_BOITE = 5     # une boîte de moins de 5 bâtiments n'est pas tracée
    _TAILLE_TITRE_GRAPHIQUE = 20


    # ============================================================================
    # 1. FILTRAGE
    # ============================================================================

    _df = appliquer_filtres(DATA_brut, filtre_materiau=False)

    mo.stop(_df.height == 0, mo.md("**Aucun bâtiment ne correspond aux filtres choisis.**"))

    # stock_c renseigné (les 0 sont conservés : bâtiment sans matériau biosourcé) et seuils choisis
    _df = _df.with_columns(pl.col("stock_c").cast(pl.Float64, strict=False)).filter(
        pl.col("stock_c").is_not_null() & pl.col("seuil").is_in(_SEUILS_CHOISIS)
    )
    print(f"  avec stock_c renseigné (seuils choisis) : {_df.height}")

    mo.stop(_df.height == 0, mo.md("**Aucun bâtiment avec un stock_c renseigné pour ces filtres.**"))


    # ============================================================================
    # 2. TYPE DE MATÉRIAU + STATISTIQUES PAR (type, seuil)
    # ============================================================================

    _df = _df.with_columns(
        pl.when(
            pl.col("dc_materiau_structure").fill_null("Autre")
            .replace_strict(MAPPING_MATERIAU, default="Sans info", return_dtype=pl.Utf8)
            == _CATEGORIE_BAS_CARBONE
        )
        .then(pl.lit(_CATEGORIE_BAS_CARBONE))
        .otherwise(pl.lit(_CATEGORIE_RESTE))
        .alias("categorie_materiau")
    )

    # Médiane GLOBALE : tous les bâtiments filtrés avec un stock_c, tous seuils
    # et types de matériaux confondus
    _mediane_globale = _df["stock_c"].median()
    _n_global = _df.height

    _agg = (
        _df.group_by(["categorie_materiau", "seuil"]).agg(
            pl.len().alias("nb_batiments"),
            pl.col("stock_c").min().alias("min"),
            pl.col("stock_c").quantile(0.25).alias("q1"),
            pl.col("stock_c").median().alias("mediane"),
            pl.col("stock_c").mean().alias("moyenne"),
            pl.col("stock_c").quantile(0.75).alias("q3"),
            pl.col("stock_c").max().alias("max"),
        )
        .with_columns((pl.col("nb_batiments") >= _NB_MIN_PAR_BOITE).alias("boite_affichee"))
        .sort(
            pl.col("categorie_materiau").replace_strict({c: i for i, c in enumerate(_CATEGORIES)}, default=99),
            pl.col("seuil").replace_strict({s: i for i, s in enumerate(_ORDRE_SEUILS)}, default=99),
        )
    )
    _nb_masquees = _agg.filter(~pl.col("boite_affichee")).height
    _agg_tracee = _agg.filter(pl.col("boite_affichee"))

    mo.stop(_agg_tracee.height == 0, mo.md(f"**Aucune boîte à tracer : toutes les combinaisons matériau × seuil ont moins de {_NB_MIN_PAR_BOITE} bâtiments.**"))

    # Données individuelles des seules boîtes tracées
    _df_trace = _df.join(
        _agg_tracee.select("categorie_materiau", "seuil"), on=["categorie_materiau", "seuil"], how="inner"
    )

    # Catégories et seuils réellement tracés, dans l'ordre voulu
    _categories = [c for c in _CATEGORIES if c in _agg_tracee["categorie_materiau"].to_list()]
    _seuils = [s for s in _ORDRE_SEUILS if s in _agg_tracee["seuil"].to_list()]
    _n_par_categorie = {
        r["categorie_materiau"]: r["n"]
        for r in _agg_tracee.group_by("categorie_materiau").agg(pl.col("nb_batiments").sum().alias("n")).iter_rows(named=True)
    }
    _n_par_seuil = {
        r["seuil"]: r["n"]
        for r in _agg_tracee.group_by("seuil").agg(pl.col("nb_batiments").sum().alias("n")).iter_rows(named=True)
    }


    # ============================================================================
    # 3. GRAPHIQUE
    # ============================================================================

    _fig = go.Figure()

    for _seuil in _seuils:
        _d = _df_trace.filter(pl.col("seuil") == _seuil)
        _fig.add_trace(go.Box(
            x=_d["categorie_materiau"].to_list(),
            y=_d["stock_c"].to_list(),
            name=f"{_seuil} (n = {_n_par_seuil[_seuil]})",
            marker_color=_COULEURS_SEUIL[_seuil],
            boxmean=True,          # losange = moyenne
            boxpoints=False,       # pas de points individuels (lisibilité)
        ))

    # Seuils du label bâtiment biosourcé
    for _valeur, _niveau in _SEUILS_LABEL_BIOSOURCE:
        _fig.add_hline(
            y=_valeur,
            line=dict(color=_COULEUR_LABEL, width=1.5, dash="dot"),
            annotation_text=f"Label biosourcé {_niveau} ({_valeur})",
            annotation_position="top left",
            annotation_font=dict(size=11, color=_COULEUR_LABEL),
        )

    # Médiane globale, affichée en haut et au milieu du graphique
    _fig.add_annotation(
        text=f"<b>Médiane globale : {_mediane_globale:.1f} kg C/m²</b> (n = {_n_global})",
        xref="paper", yref="paper", x=0.5, y=1.0, yanchor="bottom",
        showarrow=False, font=dict(size=14),
        bgcolor="rgba(255,255,255,0.9)", bordercolor="#888888", borderwidth=1, borderpad=4,
    )

    _note_masquees = (
        f" — {_nb_masquees} boîte(s) de moins de {_NB_MIN_PAR_BOITE} bâtiments non tracée(s)" if _nb_masquees else ""
    )
    _fig.update_layout(
        template="plotly_white",
        boxmode="group",
        height=620,
        title=dict(
            text=(
                f"<b>Graphique 6 — {GRAPHIQUES[6]} — {_USAGE}</b><br>"
                f"<sup>Pointillés : seuils du label bâtiment biosourcé 2024{_note_masquees}</sup><br>"
                f"<sup>{SOUS_TITRE_SANS_MATERIAU}</sup>"
            ),
            font=dict(size=_TAILLE_TITRE_GRAPHIQUE),
        ),
        xaxis=dict(
            categoryorder="array", categoryarray=_categories,
            tickvals=_categories,
            ticktext=[
                f"<b>{_c}</b><br><span style='font-size:11px;color:gray'>n = {_n_par_categorie[_c]}</span>"
                for _c in _categories
            ],
            tickfont=dict(size=13),
        ),
        yaxis=dict(title="Stock carbone (kg C/m² SDP)", range=[0, _Y_MAX]),
        legend=dict(title="Seuil RE2020", orientation="h", x=0.5, xanchor="center", y=-0.15, yanchor="top"),
        margin=dict(t=170, b=100, l=60, r=20),
    )

    _graphique = mo.ui.plotly(_fig)

    # Export : statistiques de chaque boîte (toutes les combinaisons, avec un
    # indicateur `boite_affichee` pour celles masquées faute d'effectif)
    mo.vstack([_graphique, boutons_export(_agg, "graphique_6_stock_c_par_materiau_et_seuil")])
    return


@app.cell(hide_code=True)
def param_graphique_7(mo, panneau_filtres):
    # ============================================================================
    # CELLULE WIDGET — paramètres propres au graphique 7 (éloignement au seuil
    # IC Construction 2028, logements collectifs).
    #   - écart maximal au-dessus du seuil 2028 qui reste dans le groupe 1
    #   - variable catégorielle comparée (barres 100 % empilées)
    #   - option pour masquer « Autre » / non renseigné
    # Le matériau de structure n'est pas un filtre ici : c'est une variable comparée.
    # « Masquer les inconnus » n'est pas appliqué non plus (cf. cellule des groupes).
    # ============================================================================

    choix_ecart_max_2028 = mo.ui.slider(
        start=0, stop=100, step=5, value=20, show_value=True,
        label="Groupe 1 : écart maximal AU-DESSUS du seuil 2028 (kgeq.CO2/m²)",
    )

    choix_variable_categorielle_7 = mo.ui.dropdown(
        options={
            "Zone climatique": "zone_climatique",
            "Type de structure principale": "dc_type_structure_principale",
            "Matériau de structure": "dc_materiau_structure",
        },
        value="Zone climatique",
        label="Variable catégorielle comparée",
    )

    cacher_autre_7 = mo.ui.switch(
        value=True, label="Masquer « Autre » / non renseigné (variables dc_*, peu fiables)",
    )

    mo.vstack([
        mo.md("### Paramètres du graphique 7"),
        panneau_filtres(
            {"Graphique 7": mo.vstack([choix_ecart_max_2028, choix_variable_categorielle_7, cacher_autre_7])},
            avec_materiau=False, avec_inconnus=False,
        ),
    ])
    return cacher_autre_7, choix_ecart_max_2028, choix_variable_categorielle_7



@app.cell(hide_code=True)
def resume_filtres_graphique_7(resume_filtres):
    # Résumé des filtres actifs du graphique 7 (cellule séparée : il lit les valeurs
    # des widgets, alors que le panneau ci-dessus reste statique).
    resume_filtres(avec_materiau=False, avec_inconnus=False)
    return


@app.cell(hide_code=True)
def groupes_graphique_7(
    DATA_brut,
    SREF_MAX_SLIDER,
    USAGE_LOGEMENT_COLLECTIF,
    appliquer_filtres,
    choix_ecart_max_2028,
    dropdown_usage,
    mo,
    pl,
):
    # ============================================================================
    # CELLULE — Constitution des 2 groupes du graphique 7 (aucun appel réseau)
    #
    # Éloignement au seuil 2028, propre à CHAQUE bâtiment :
    #     ecart_2028 = ic_construction - ic_construction_max_2028
    #   (négatif ou nul = seuil 2028 respecté ; positif = au-dessus du seuil)
    #
    #   Groupe 1 : ecart_2028 <= ECART_MAX  -> bâtiments conformes 2028 / 2031
    #              + bâtiments au-dessus du seuil 2028 d'au plus ECART_MAX
    #   Groupe 2 : ecart_2028 >  ECART_MAX  -> tous les autres
    #
    # Les conformes 2031 sont inclus d'office : le seuil 2031 est plus strict que 2028.
    # Fournit DATA_groupes_7 (une ligne par bâtiment, indicateurs calculés inclus),
    # INDICATEURS_NUM_7 (indicateurs numériques comparés) et NOMS_GROUPES_7.
    # ============================================================================


    # ============================================================================
    # PARAMÈTRES (toutes les variables au même endroit)
    # ============================================================================

    _USAGE = dropdown_usage.value
    _ECART_MAX = choix_ecart_max_2028.value                 # kgeq.CO2/m², au-dessus du seuil 2028
    _SREF_PLATEAU = SREF_MAX_SLIDER                         # sref >= 4000 est renvoyé = 5000 par
                                                            # `retrouver_sref` : valeur-plafond, pas une surface réelle
    _COL_IC = "ic_construction"
    _COL_SEUIL_2028 = "ic_construction_max_2028"
    _LOTS_SOMMES = ["ic_composant_lot_3", "ic_composant_lot_4", "ic_composant_lot_6"]

    NOMS_GROUPES_7 = [
        f"Groupe 1 : conforme ou ≤ {_ECART_MAX} au-dessus du seuil 2028",
        f"Groupe 2 : > {_ECART_MAX} au-dessus du seuil 2028",
    ]

    # Indicateurs numériques comparés : colonne -> (libellé, unité)
    INDICATEURS_NUM_7 = {
        "nb_total_fiche_acv": ("Nombre total de fiches ACV", "fiches"),
        "nb_fdes": ("Nombre de FDES", "fiches"),
        "stock_c": ("Stock de carbone", "kg C/m²"),
        "ratio_baies_sref": ("Surface de baies / sref", "m²/m²"),
        "ratio_baies_murs_sref": ("(Baies + murs) / sref", "m²/m²"),
        "ic_lots_3_4_6": ("IC composant lots 3 + 4 + 6", "kgeq.CO2/m²"),
    }


    # ============================================================================
    # 1. LOGEMENTS COLLECTIFS UNIQUEMENT
    # ============================================================================

    mo.stop(
        _USAGE != USAGE_LOGEMENT_COLLECTIF,
        mo.md(f"**Graphique 7 : réservé aux logements collectifs** (l'usage choisi est « {_USAGE} »)."),
    )


    # ============================================================================
    # 2. FILTRAGE (le matériau est comparé, donc non filtré ; « Inconnu » concerne le
    #    seuil atteint, sans rapport avec l'écart au seuil 2028)
    # ============================================================================

    _df = appliquer_filtres(DATA_brut, filtre_materiau=False, filtre_inconnu=False)

    # Colonnes numériques lues en flottants (valeurs absentes -> NULL)
    _cols_num = [
        _COL_IC, _COL_SEUIL_2028, "sref", "surface_baies_rset", "surface_murs_rset",
        "nb_total_fiche_acv", "nb_fdes", "stock_c", *_LOTS_SOMMES,
    ]
    _df = _df.with_columns([pl.col(_c).cast(pl.Float64, strict=False) for _c in _cols_num])

    # Il faut l'IC construction ET un seuil 2028 strictement positif
    _avant = _df.height
    _df = _df.filter(
        pl.col(_COL_IC).is_not_null()
        & pl.col(_COL_SEUIL_2028).is_not_null()
        & (pl.col(_COL_SEUIL_2028) > 0)
    )
    print(f"  avec ic_construction et seuil 2028 renseignés : {_df.height} / {_avant}")

    mo.stop(_df.height == 0, mo.md("**Aucun bâtiment avec ic_construction et seuil 2028 pour ces filtres.**"))


    # ============================================================================
    # 3. ÉCART AU SEUIL 2028, GROUPES ET INDICATEURS CALCULÉS
    # ============================================================================

    # sref exploitable : renseigné, > 0 et différent de la valeur-plafond
    _sref_ok = pl.col("sref").is_not_null() & (pl.col("sref") > 0) & (pl.col("sref") < _SREF_PLATEAU)
    _baies = pl.col("surface_baies_rset")
    _murs = pl.col("surface_murs_rset")

    DATA_groupes_7 = _df.with_columns(
        (pl.col(_COL_IC) - pl.col(_COL_SEUIL_2028)).alias("ecart_2028"),
    ).with_columns(
        pl.when(pl.col("ecart_2028") <= _ECART_MAX)
        .then(pl.lit(NOMS_GROUPES_7[0]))
        .otherwise(pl.lit(NOMS_GROUPES_7[1]))
        .alias("groupe"),
        # Ratios : NULL si sref inexploitable ou si une surface manque (jamais 0 par défaut)
        pl.when(_sref_ok & _baies.is_not_null()).then(_baies / pl.col("sref")).alias("ratio_baies_sref"),
        pl.when(_sref_ok & _baies.is_not_null() & _murs.is_not_null())
        .then((_baies + _murs) / pl.col("sref")).alias("ratio_baies_murs_sref"),
        # Somme des 3 lots : NULL si UN des lots manque (sum_horizontal ignorerait les NULL)
        pl.when(pl.all_horizontal([pl.col(_c).is_not_null() for _c in _LOTS_SOMMES]))
        .then(pl.sum_horizontal(_LOTS_SOMMES)).alias("ic_lots_3_4_6"),
    )

    _effectifs = DATA_groupes_7.group_by("groupe").len().sort("groupe")
    print("  effectifs :", {r["groupe"]: r["len"] for r in _effectifs.iter_rows(named=True)})
    print(f"  sref exploitable (ratios) : {DATA_groupes_7.select(_sref_ok.sum()).item()} / {DATA_groupes_7.height}")

    return DATA_groupes_7, INDICATEURS_NUM_7, NOMS_GROUPES_7


@app.cell(hide_code=True)
def graphique_7_numerique(
    DATA_groupes_7,
    GRAPHIQUES,
    INDICATEURS_NUM_7,
    NOMS_GROUPES_7,
    SOUS_TITRE_SANS_MATERIAU,
    boutons_export,
    dropdown_usage,
    go,
    mo,
    pl,
):
    # ============================================================================
    # GRAPHIQUE 7 (partie numérique) — Q1 / médiane / Q3 de chaque indicateur, pour
    # les deux groupes, un panneau par indicateur (échelles indépendantes).
    # Point = médiane ; barre d'erreur = de Q1 à Q3 (même lecture que le graphique 4).
    # ============================================================================

    from plotly.subplots import make_subplots as _make_subplots


    # ============================================================================
    # PARAMÈTRES
    # ============================================================================

    _USAGE = dropdown_usage.value
    _COULEURS_GROUPES = ["#79A757", "#A26E2E"]    # groupe 1 (vert), groupe 2 (brun)
    _NB_COLONNES = 3
    _NB_MIN_PAR_GROUPE = 5          # en dessous, le groupe n'est pas tracé pour cet indicateur
    _HAUTEUR_PAR_LIGNE = 330
    _TAILLE_TITRE_GRAPHIQUE = 20


    # ============================================================================
    # 1. STATISTIQUES PAR (indicateur, groupe)
    # ============================================================================

    _lignes_stats = []
    for _col, (_libelle, _unite) in INDICATEURS_NUM_7.items():
        for _groupe in NOMS_GROUPES_7:
            _v = DATA_groupes_7.filter(pl.col("groupe") == _groupe)[_col].drop_nulls()
            _n = _v.len()
            _lignes_stats.append({
                "indicateur": _col, "libelle": _libelle, "unite": _unite, "groupe": _groupe, "n": _n,
                "q1": _v.quantile(0.25) if _n else None,
                "mediane": _v.median() if _n else None,
                "moyenne": _v.mean() if _n else None,
                "q3": _v.quantile(0.75) if _n else None,
                "trace": _n >= _NB_MIN_PAR_GROUPE,
            })
    _stats = pl.DataFrame(_lignes_stats, infer_schema_length=None)

    mo.stop(_stats.filter(pl.col("trace")).height == 0,
            mo.md(f"**Aucun groupe n'a au moins {_NB_MIN_PAR_GROUPE} bâtiments pour un indicateur.**"))


    # ============================================================================
    # 2. GRAPHIQUE
    # ============================================================================

    _nb_ind = len(INDICATEURS_NUM_7)
    _nb_lignes = -(-_nb_ind // _NB_COLONNES)      # division entière par excès
    _fig = _make_subplots(
        rows=_nb_lignes, cols=_NB_COLONNES,
        subplot_titles=[f"{_l} ({_u})" for _l, _u in INDICATEURS_NUM_7.values()],
        vertical_spacing=0.2, horizontal_spacing=0.08,
    )

    _legende_deja_vue = set()
    for _i, _col in enumerate(INDICATEURS_NUM_7):
        _r, _c = divmod(_i, _NB_COLONNES)
        for _k, _groupe in enumerate(NOMS_GROUPES_7):
            _s = _stats.filter((pl.col("indicateur") == _col) & (pl.col("groupe") == _groupe)).row(0, named=True)
            if not _s["trace"]:
                continue
            _fig.add_trace(
                go.Scatter(
                    x=[f"Groupe {_k + 1}<br>n = {_s['n']}"],
                    y=[_s["mediane"]],
                    mode="markers",
                    marker=dict(size=12, color=_COULEURS_GROUPES[_k], line=dict(color="black", width=1)),
                    error_y=dict(
                        type="data", symmetric=False, thickness=3, width=12, color=_COULEURS_GROUPES[_k],
                        array=[_s["q3"] - _s["mediane"]], arrayminus=[_s["mediane"] - _s["q1"]],
                    ),
                    name=_groupe, legendgroup=_groupe, showlegend=_groupe not in _legende_deja_vue,
                    hovertemplate=(
                        f"<b>{_groupe}</b><br>n = {_s['n']}<br>Q1 = {_s['q1']:.3g}<br>"
                        f"Médiane = {_s['mediane']:.3g}<br>Q3 = {_s['q3']:.3g}<br>"
                        f"Moyenne = {_s['moyenne']:.3g}<extra></extra>"
                    ),
                ),
                row=_r + 1, col=_c + 1,
            )
            _legende_deja_vue.add(_groupe)

    _fig.update_layout(
        template="plotly_white",
        height=_HAUTEUR_PAR_LIGNE * _nb_lignes + 200,
        title=dict(
            text=(
                f"<b>Graphique 7 — {GRAPHIQUES[7]} — {_USAGE}</b><br>"
                f"<sup>Point = médiane ; barre = de Q1 à Q3 (écart au seuil : ic_construction − ic_construction_max_2028)</sup><br>"
                f"<sup>{SOUS_TITRE_SANS_MATERIAU}</sup>"
            ),
            font=dict(size=_TAILLE_TITRE_GRAPHIQUE),
        ),
        legend=dict(orientation="h", x=0.5, xanchor="center", y=-0.08, yanchor="top"),
        margin=dict(t=170, b=100, l=60, r=20),
    )

    _graphique = mo.ui.plotly(_fig)

    # Export : statistiques de chaque (indicateur, groupe), avec l'indicateur `trace`
    mo.vstack([_graphique, boutons_export(_stats, "graphique_7_stats_par_groupe")])
    return


@app.cell(hide_code=True)
def graphique_7_categoriel(
    DATA_groupes_7,
    GRAPHIQUES,
    NOMS_GROUPES_7,
    SOUS_TITRE_SANS_MATERIAU,
    boutons_export,
    cacher_autre_7,
    choix_variable_categorielle_7,
    dropdown_usage,
    go,
    mo,
    pl,
):
    # ============================================================================
    # GRAPHIQUE 7 (partie catégorielle) — Répartition (%) d'une variable catégorielle
    # dans chaque groupe : barres 100 % empilées, une barre par groupe.
    # Variables : zone climatique, type de structure principale, matériau de structure.
    # ============================================================================


    # ============================================================================
    # PARAMÈTRES
    # ============================================================================

    _USAGE = dropdown_usage.value
    _VARIABLE = choix_variable_categorielle_7.value
    _LIBELLE_VARIABLE = choix_variable_categorielle_7.selected_key
    _CACHER_AUTRE = cacher_autre_7.value
    _LIBELLE_NON_RENSEIGNE = "Non renseigné"
    _MODALITES_MASQUEES = ["Autre", _LIBELLE_NON_RENSEIGNE, "None", ""]
    _SEUIL_TEXTE_PCT = 4            # sous ce pourcentage, pas d'étiquette dans le segment
    _COULEURS = [
        "#79A757", "#B0A99F", "#A26E2E", "#475F8F", "#E2ADF2",
        "#B58BEA", "#574AE2", "#E8C66A", "#C0504D", "#4BACC6",
    ]
    _TAILLE_TITRE_GRAPHIQUE = 20


    # ============================================================================
    # 1. MODALITÉS (valeurs absentes -> « Non renseigné »), PUIS % PAR GROUPE
    # ============================================================================

    _df = DATA_groupes_7.with_columns(
        pl.col(_VARIABLE).cast(pl.Utf8).str.strip_chars().fill_null(_LIBELLE_NON_RENSEIGNE).alias("modalite")
    )
    if _CACHER_AUTRE:
        _df = _df.filter(~pl.col("modalite").is_in(_MODALITES_MASQUEES))

    mo.stop(_df.height == 0, mo.md("**Aucun bâtiment avec une valeur renseignée pour cette variable.**"))

    _n_par_groupe = _df.group_by("groupe").len().rename({"len": "n_groupe"})
    _agg = (
        _df.group_by(["groupe", "modalite"]).len().rename({"len": "n"})
        .join(_n_par_groupe, on="groupe")
        .with_columns((100 * pl.col("n") / pl.col("n_groupe")).alias("part_pct"))
    )

    # Modalités triées par effectif total décroissant (les plus fréquentes en bas)
    _ordre = (
        _df.group_by("modalite").len().sort("len", descending=True)["modalite"].to_list()
    )


    # ============================================================================
    # 2. GRAPHIQUE
    # ============================================================================

    _fig = go.Figure()
    _x_groupes = [
        f"Groupe {_k + 1}<br>n = {_n_par_groupe.filter(pl.col('groupe') == _g)['n_groupe'].item()}"
        for _k, _g in enumerate(NOMS_GROUPES_7)
        if _g in _n_par_groupe["groupe"].to_list()
    ]
    _groupes_presents = [_g for _g in NOMS_GROUPES_7 if _g in _n_par_groupe["groupe"].to_list()]

    for _j, _modalite in enumerate(_ordre):
        _parts, _ns = [], []
        for _g in _groupes_presents:
            _ligne = _agg.filter((pl.col("groupe") == _g) & (pl.col("modalite") == _modalite))
            _parts.append(_ligne["part_pct"].item() if _ligne.height else 0.0)
            _ns.append(_ligne["n"].item() if _ligne.height else 0)
        _fig.add_trace(go.Bar(
            x=_x_groupes, y=_parts, name=_modalite,
            marker_color=_COULEURS[_j % len(_COULEURS)],
            text=[f"{_p:.0f} %" if _p >= _SEUIL_TEXTE_PCT else "" for _p in _parts],
            textposition="inside",
            customdata=_ns,
            hovertemplate=f"<b>{_modalite}</b><br>%{{y:.1f}} % (n = %{{customdata}})<extra></extra>",
        ))

    _note_masque = " — « Autre » / non renseigné masqués" if _CACHER_AUTRE else ""
    _fig.update_layout(
        template="plotly_white",
        barmode="stack",
        height=560,
        title=dict(
            text=(
                f"<b>Graphique 7 — {GRAPHIQUES[7]} — {_USAGE}</b><br>"
                f"<sup>Répartition : {_LIBELLE_VARIABLE}{_note_masque}</sup><br>"
                f"<sup>{SOUS_TITRE_SANS_MATERIAU}</sup>"
            ),
            font=dict(size=_TAILLE_TITRE_GRAPHIQUE),
        ),
        yaxis=dict(title="Part du groupe (%)", range=[0, 100]),
        legend=dict(title=_LIBELLE_VARIABLE, orientation="v"),
        margin=dict(t=170, b=80, l=60, r=20),
    )

    _graphique = mo.ui.plotly(_fig)

    # Export : effectif et part de chaque modalité dans chaque groupe
    mo.vstack([_graphique, boutons_export(_agg.sort("groupe", "n", descending=[False, True]), "graphique_7_repartition_categorielle")])
    return


@app.cell(hide_code=True)
def param_apercu_tables(mo):
    # ============================================================================
    # CELLULE WIDGET — bouton de l'export "aperçu des tables"
    # (défini dans une autre cellule que celle qui lit sa valeur, cf. règle marimo)
    # ============================================================================

    bouton_apercu_tables = mo.ui.run_button(label="Exporter l'aperçu des tables (10 premières lignes)")

    mo.vstack([
        mo.md("### Aperçu des tables de la base"),
        bouton_apercu_tables,
    ])
    return (bouton_apercu_tables,)


@app.cell(hide_code=True)
def apercu_tables(bouton_apercu_tables, mo, noms_tables, pl, turso_conn):
    # ============================================================================
    # EXPORT — les 10 premières lignes de chaque table, un CSV par table,
    # téléchargeables un par un ou dans une seule archive ZIP.
    # ============================================================================


    import io
    import zipfile


    # ============================================================================
    # PARAMÈTRES
    # ============================================================================

    _TABLES = [
        "composant_open_data",
        "groupe_open_data",
        "metadonnees_batiment",
        "metadonnees_composant",
        "metadonnees_groupe",
        "metadonnees_projet",
        "metadonnees_zone",
        "projet_open_data",
        "zone_open_data",
    ]
    _NB_LIGNES = 10
    _NOM_ARCHIVE = "apercu_tables.zip"


    # ============================================================================
    # 1. LECTURE (uniquement après un clic sur le bouton)
    # ============================================================================

    mo.stop(not bouton_apercu_tables.value, mo.md("*Clique sur le bouton pour lancer l'export.*"))

    _apercus = {}      # nom de table -> DataFrame (10 premières lignes)
    _absentes = []     # tables demandées mais introuvables dans la base
    for _table in _TABLES:
        if _table not in noms_tables:
            _absentes.append(_table)
            continue
        _curseur = turso_conn.execute(f'SELECT * FROM "{_table}" LIMIT {_NB_LIGNES}')
        _colonnes = [d[0] for d in _curseur.description]
        # Construction par dicts + infer_schema_length=None : évite les erreurs
        # d'inférence de type de polars (cf. cellule d'aperçu des tables)
        _lignes = _curseur.fetchall()
        if _lignes:
            _apercus[_table] = pl.DataFrame(
                [dict(zip(_colonnes, ligne)) for ligne in _lignes], infer_schema_length=None
            )
        else:   # table vide : on garde au moins les en-têtes
            _apercus[_table] = pl.DataFrame({c: [] for c in _colonnes})


    # ============================================================================
    # 2. TÉLÉCHARGEMENTS
    # ============================================================================

    def _csv(df):
        return df.write_csv().encode("utf-8-sig")   # même format que les autres exports

    _tampon = io.BytesIO()
    with zipfile.ZipFile(_tampon, "w", zipfile.ZIP_DEFLATED) as _zip:
        for _table, _df in _apercus.items():
            _zip.writestr(f"{_table}.csv", _csv(_df))

    _bouton_zip = mo.download(
        data=_tampon.getvalue(), filename=_NOM_ARCHIVE, mimetype="application/zip",
        label=f"Télécharger les {len(_apercus)} CSV (ZIP)",
    )
    _boutons_csv = [
        mo.download(data=_csv(_df), filename=f"{_table}.csv", mimetype="text/csv", label=_table)
        for _table, _df in _apercus.items()
    ]
    _resume = pl.DataFrame({
        "table": list(_apercus),
        "lignes_exportees": [_df.height for _df in _apercus.values()],
        "colonnes": [_df.width for _df in _apercus.values()],
    })

    mo.vstack([
        mo.md(f"**{len(_apercus)} table(s) lues** — {_NB_LIGNES} premières lignes de chacune."),
        mo.md(f"⚠️ Tables introuvables dans la base : {', '.join(_absentes)}") if _absentes else mo.md(""),
        mo.ui.table(_resume, selection=None),
        _bouton_zip,
        mo.md("Ou table par table :"),
        mo.hstack(_boutons_csv, justify="start", wrap=True),
    ])
    return


# Cellule désactivée : button_run_analyse_comp et table_a_afficher ne sont plus définis nulle part.
@app.cell(disabled=True, hide_code=True)
def _(button_run_analyse_comp, mo, pl, table_a_afficher, turso_conn):
    #resultat du click to run qui affiche le tableau
    # if the button hasn't been clicked, don't run.
    mo.stop(not button_run_analyse_comp.value)

    _table_name = table_a_afficher.value

    _cursor = turso_conn.execute(f"SELECT * FROM {_table_name}")
    _col_names = [desc[0] for desc in _cursor.description]
    _data = _cursor.fetchall()

    _columns_summary = []
    for _i, col_name in enumerate(_col_names):
        col_values = [row[_i] for row in _data]
        non_null_count = sum(1 for v in col_values if v is not None)
        premiere_valeur_non_nulle = next((v for v in col_values if v is not None), None)
        col_type = type(premiere_valeur_non_nulle).__name__ if premiere_valeur_non_nulle is not None else "unknown"
        first_2 = col_values[:2]
        _columns_summary.append({
            "Colonne": col_name,
            "Type": col_type,
            "Nombre d'éléments": non_null_count,
            "1ère valeur": str(first_2[0]) if len(first_2) > 0 else "",
            "2ème valeur": str(first_2[1]) if len(first_2) > 1 else "",
        })

    _summary_df = pl.DataFrame(_columns_summary)
    mo.ui.table(_summary_df)
    return


if __name__ == "__main__":
    app.run()