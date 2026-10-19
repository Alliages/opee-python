# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "anywidget",
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
    #
    # À CHAQUE ÉDITION DU FICHIER :
    #   1. incrémenter VERSION de 0.01 (0.9 -> 0.91 -> 0.92 -> 0.93 ...)
    #   2. mettre à jour DATE_EDITION (date et heure de l'édition, heure de Paris)
    #   3. AJOUTER EN TÊTE de HISTORIQUE_VERSIONS une ligne ("version", "résumé")
    #      avec une phrase de synthèse des changements.
    # ============================================================================

    # ---- Variables (regroupées en début de cellule) -----------------------
    TITRE = "Analyse des projets RE2020"
    BASELINE_Y = 145          # ordonnée de la 1re ligne de la baseline (SVG 1000x500) : réduire pour la remonter
    SIGNATURE = "des prescripteurs bas carbone"
    VERSION = "0.99i"         # à ajuster : +0.01 à chaque édition du script
    DATE_EDITION = "18/10/2026 14:01"
    HISTORIQUE_VERSIONS = [
        # (version, synthèse des changements), la plus récente en premier
        (VERSION, "Tous les graphiques : encadré des filtres actifs placé SOUS le graphique (ordre filtres → graphique → filtres actifs). Impression : page de garde (visuel, version, encarts OPEE, liens vers le HUB, liste des graphiques), puis une page par graphique (graphique + filtres actifs) ; masqués en plus : historique des versions, jeton et tables, typologie, rappel du filtre de surface, intitulés d'export, aperçu des tables ; saut de page avant le graphique 1 ; page de garde tenue sur une page (visuel du HUB réduit à 540 px, marges des cellules masquées supprimées à l'impression)"),
        ("0.99h", "Graphique 10 (DH) : choix de l'unité « Zone du bâtiment » (comme avant) ou « Bâtiment » (dh_batiment, sans séparation traversant / non traversant) ; exports : tableau (en mode bâtiment, Q1 / médiane / Q3 par zone climatique) + export brut (une ligne par point tracé) ; filtres actifs sous le graphique"),
        ("0.99g", "Graphique 6 : filtre des seuils IC construction atteints (RE2022, RE2025, RE2028, RE2031) ; sous le graphique, en gros chiffres, part des FDES / PEP (individuelles, collectives, configurées…) face aux DED + forfaitaire pour le gros œuvre (lots 2-3, bleu), le second œuvre (lots 4-7, rouge) et les lots techniques (lots 8-13, vert), couleurs du graphique 3 ; encadré des filtres actifs placé sous le graphique"),
        ("0.99f", "Graphique 5 corrigé : empilement de tous les types de fiches du total (FDES, fiches configurées, PEP, PEP extrapolées, DED, autres ; nb_des exclu car hors total), valeurs écrites dans les segments, nouvelle palette (hachures pour les fiches configurées et les PEP extrapolées) ; colonne du milieu = total des fiches, point = médiane et barre = Q1 à Q3 (style du graphique 8)"),
        ("0.99e", "Nouveau graphique 6 : nombre de fiches par lot RE2020 (barres à 100 %) et par nature de fiche (FDES, FDES configurée, PEP, PEP extrapolée, DED, forfaitaire, autres), nombre moyen de fiches par bâtiment à droite ; fiches lues dans le Parquet DATA/composants_logements_collectifs_2026-10-16.parquet (logements collectifs), mêmes filtres que le graphique 5 (dont l'année de dépôt), petits et grands logements exclus par défaut ; anciens graphiques 6 à 10 renumérotés 7 à 11"),
        ("0.99d", "Impression : panneaux de filtres, titres « Paramètres du graphique », commandes (interrupteurs, curseurs, listes, boutons) et boutons « Télécharger en CSV / JSON » non imprimés (l'encadré des filtres actifs reste) ; en-tête réduit à la largeur de la page ; bouton « Download » des tableaux retiré (écran et impression)"),
        ("0.99c", "Graphique 10 : pourcentage affiché à côté de chaque part de 3 % ou plus (une décimale), nom de la catégorie ajouté au-dessus de 10 % (nom court, sans parenthèse) ; nouvelle palette du chauffage (chaudière aubergine, effet Joule ambre, réseau de chaleur lavande, poêle brun) pour la distinguer des 3 autres donuts"),
        ("0.99b", "Bouton « Imprimer / PDF » (anywidget) : sur molab le notebook est affiché dans un cadre et Ctrl+P n'imprimait que la 1re page ; le bouton imprime le notebook entier, réduit les graphiques à la largeur de la page (graphiques 3 et 10 coupés sinon) et masque la barre Plotly (dans le shadow DOM, hors de portée de la CSS de la page). Dépendance anywidget ajoutée"),
        ("0.99", "Impression en PDF depuis Chrome (Ctrl+P) : cellule `style_impression` (@media print : A4 portrait, couleurs conservées, barre Plotly masquée, graphiques non coupés) et cellules `saut_page_N` (nouvelle page avant chaque graphique 2 à 10)"),
        ("0.98", "Graphique 10 : bascule renommée « Masquer « Autre » / non renseigné » (désactivée par défaut) et placée dans un encadré visible sous « Valider… » ; Polars : explode(empty_as_null=True) explicite (fin de l'avertissement de dépréciation)"),
        ("0.97", "Nouveau graphique 10 : 4 donuts (matériau de structure, type de plancher, remplissage de façade, générateur de chauffage), bascule « bâtiments non renseignés », couleurs fixes par catégorie. Extraction de dc_type_plancher, dc_materiau_remplissage_facade et synthese_generateur_ch"),
        ("0.96", "Nouveau graphique 2 : répartition de l'impact carbone (composants, chantier, énergie, eau) par seuil RE2020 ; anciens graphiques 2 à 8 renumérotés 3 à 9 ; bouton « Download plot as JSON » ajouté à tous les graphiques (CONFIG_PLOTLY) ; extraction de ic_chantier et ic_eau"),
        ("0.95b", "Graphique 8 : slider « Zoom Axe Y » (350 à 2500, 1500 par défaut), zones à DH nul ou > 15000 écartées, DH max > 15000 ignoré, survol du « DHmax » (zone qui le porte)"),
        ("0.95", "Graphique 8 : dispersion du DH par zone climatique (zones traversantes / non traversantes). Nouvelles colonnes par zone : dh_zones, is_traversant_zones, dh_max_zones"),
        ("0.94", "Graphique 7 : inversion de l'ordre des graphiques « stock de carbone » et « IC composant lots 3 + 4 + 6 »"),
        ("0.93", "Graphique 7 (numérique) : groupe 1 scindé en 1a (dépôt 2022-2023) et 1b (dépôt 2024-2025)"),
        ("0.92b", "Correction mineure : graphique 7, « Masquer Autre » placé avec « Valider… » en haut des filtres"),
        ("0.92", "Amélioration visuelle"),
        ("0.91", "Graphique 7 : ajout de nb_ded, ic_ded et ic_composant_lot_8, et exclusion des « Petit logement coll. »"),
        ("0.9", "7 graphiques, version de base publique"),
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
    LIENS = [
        ("HUB des prescripteurs bas carbone", URL_HUB),
        ("Ressources du HUB", URL_RESSOURCES_HUB),
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

    # ---- Visuel d'en-tête : un seul SVG (viewBox 1000 x 500) qui s'adapte à la largeur ----
    # Largeur fixe en px + max-width:100% : fonctionne même si marimo place le HTML
    # dans un conteneur « shrink-to-fit » (c'est ce qui rendait le visuel invisible).
    _visuel = f"""
    <div class="visuel-hub" style="width:960px;max-width:100%;border-radius:14px;overflow:hidden;line-height:0;">
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


    # ---- Deux encarts numérotés (lisibles en thème clair comme sombre) ----
    def _carte(numero, texte):
        return f"""
        <div class="carte-hub" style="flex:1;min-width:260px;display:flex;gap:14px;align-items:flex-start;
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

    # Impression (page de garde) : visuel, version, encarts et liens vers le HUB.
    # Seul l'accordéon de l'historique (replié, donc vide sur papier) n'est pas
    # imprimé (classe « pas-imprime », cf. cellule style_impression).
    mo.vstack([
        mo.Html(_visuel + _version + _cartes + _rangee_liens),
        mo.Html('<div class="pas-imprime">' + _historique.text + '</div>'),
    ])
    return go, mo, pl, px


@app.cell(hide_code=True)
def style_impression(mo):
    # ============================================================================
    # IMPRESSION PDF : bouton « Imprimer / PDF » + règles @media print
    #
    # UTILISER LE BOUTON (pas Ctrl+P) sur molab : le notebook y est affiché dans
    # un cadre (iframe) sous le bandeau de molab ; Ctrl+P imprime la page molab,
    # où le cadre n'occupe qu'une hauteur d'écran (=> 1 seule page imprimée).
    # Le bouton appelle window.print() DEPUIS le cadre : tout le notebook sort.
    #
    # Ce que fait le bouton, juste avant d'ouvrir la boîte d'impression :
    #   1. réduit chaque graphique (zoom CSS) pour qu'il tienne dans la page
    #      (les graphiques 3 et 11 font 1180 et 1100 px de large, plus qu'une A4) ;
    #   2. masque la barre d'outils Plotly ;
    #   3. après l'impression (événement « afterprint »), rétablit l'affichage.
    # Les graphiques sont dans un « shadow DOM » (élément <marimo-plotly>) : la CSS
    # de la page ne les atteint pas, d'où ce passage par JavaScript.
    # Le bouton est un anywidget : marimo retire les `onclick` du HTML simple.
    #
    # Dans la boîte d'impression de Chrome (« Plus de paramètres ») :
    #   - cocher « Graphiques d'arrière-plan » (sinon les couleurs de fond disparaissent)
    #   - décocher « En-têtes et pieds de page » (URL et date sur chaque page)
    # Imprimés : page de garde (visuel, version, encarts OPEE / base fille, liens
    # vers le HUB, liste des graphiques), puis pour chaque graphique, sur sa page :
    # le graphique et l'encadré des filtres actifs (sous le graphique).
    # Non imprimés : panneaux de filtres et commandes (interrupteurs, curseurs, listes,
    # boutons), boutons « Télécharger en CSV / JSON » (et leurs liens) et leurs
    # intitulés, historique des versions, jeton et tables de la base, choix de la
    # typologie, rappel du filtre de surface, aperçu des tables.
    # Pour masquer le code : imprimer en mode application (mode « run » de molab).
    # Les sauts de page sont posés par les cellules `saut_page_N` (avant chaque graphique).
    # ============================================================================

    # --- Réglages -----------------------------------------------------------------
    _FORMAT_PAPIER = "A4 portrait"   # "A4 portrait" ou "A4 landscape" (paysage)
    _MARGE_PAGE = "12mm"             # marge de la feuille
    # Taille maximale d'un graphique imprimé, en pixels CSS (A4 portrait, marges
    # 12 mm : zone utile ≈ 700 x 1030 px ; on garde de la place pour les filtres).
    # En paysage : environ 1000 x 650.
    _LARGEUR_MAX_GRAPHIQUE_PX = 680
    _HAUTEUR_MAX_GRAPHIQUE_PX = 900
    # Largeur du visuel du HUB à l'impression : la page de garde (visuel, encarts,
    # liens, liste des graphiques) doit tenir sur UNE page A4
    _LARGEUR_VISUEL_IMPRIME_PX = 540
    _LIBELLE_BOUTON = "🖨 Imprimer / PDF"
    _AIDE_BOUTON = ("Imprime le notebook entier : attendre que tous les graphiques soient affichés, "
                    "puis choisir « Enregistrer au format PDF ». Dans « Plus de paramètres » : "
                    "cocher « Graphiques d'arrière-plan », décocher « En-têtes et pieds de page ».")

    # --- Règles CSS de la page (doubles accolades : f-string) ----------------------
    # Commandes (paramètres des graphiques) et boutons de téléchargement : masqués à
    # l'impression. Chaque élément marimo est un <marimo-ui-element> qui contient
    # une balise propre à son type (<marimo-switch>, <marimo-download>…).
    _COMMANDES_NON_IMPRIMEES = [
        "marimo-download", "marimo-switch", "marimo-slider", "marimo-dropdown",
        "marimo-multiselect", "marimo-radio", "marimo-button", "marimo-checkbox", "marimo-text",
    ]
    _SELECTEUR_COMMANDES = ",\n        ".join(
        f"marimo-ui-element:has({_balise})" for _balise in _COMMANDES_NON_IMPRIMEES
    )

    _CSS = f"""
    /* Écran : les textes « imprime-seul » (réglages écrits en clair) sont cachés */
    .imprime-seul {{ display: none; }}

    @media print {{
        /* Format de feuille et marges */
        @page {{ size: {_FORMAT_PAPIER}; margin: {_MARGE_PAGE}; }}

        /* Garder les couleurs des graphiques et des encadrés */
        * {{ -webkit-print-color-adjust: exact !important;
             print-color-adjust: exact !important; }}

        /* Page entière : pas de défilement ni de hauteur figée */
        html, body, #root, #app {{
            height: auto !important; overflow: visible !important;
        }}

        /* Un graphique (élément marimo qui contient le shadow DOM Plotly)
           ne doit pas être coupé entre deux pages */
        marimo-ui-element:has(marimo-plotly) {{
            display: block; break-inside: avoid; page-break-inside: avoid;
        }}

        /* Le bouton, son aide et les zones marquées « pas-imprime » (panneaux de
           filtres…) ne sont pas imprimés */
        .pas-imprime {{ display: none !important; }}

        /* Commandes et boutons de téléchargement (cf. _COMMANDES_NON_IMPRIMEES) */
        {_SELECTEUR_COMMANDES} {{ display: none !important; }}

        /* Réglages écrits en clair, à la place des commandes masquées */
        .imprime-seul {{ display: block !important; }}

        /* En-tête : visuel ramené à la largeur de la page, encarts sur une ligne */
        .visuel-hub {{ width: {_LARGEUR_VISUEL_IMPRIME_PX}px !important; max-width: 100% !important; }}
        .carte-hub {{ min-width: 0 !important; padding: 10px 12px !important; }}
        .carte-hub > div:last-child {{ font-size: 12px !important; }}

        /* Saut de page forcé (cellules `saut_page_N`) */
        .saut-page {{ break-before: page; page-break-before: always; height: 0; }}

        /* Pas de marge verticale autour des sorties de cellules : sinon les cellules
           dont tout le contenu est masqué laissent chacune ~30 px de blanc, ce qui
           fait déborder la page de garde (page blanche avant le graphique 1) */
        .marimo-cell .output {{ margin-top: 0 !important; margin-bottom: 0 !important; }}
        /* ... un peu d'air conservé entre un graphique et ses filtres actifs */
        .marimo-cell:has(marimo-plotly) {{ margin-bottom: 10px !important; }}
    }}
    """

    # --- Bouton « Imprimer / PDF » (anywidget : vrai JavaScript dans la page) -------
    import anywidget as _anywidget

    _JS_BOUTON = """
    const LARGEUR_MAX = __LARGEUR__;   // px CSS, cf. réglages Python
    const HAUTEUR_MAX = __HAUTEUR__;

    // Tous les graphiques Plotly, y compris dans les shadow DOM de marimo
    function graphiques(racine, liste = []) {
      racine.querySelectorAll(".js-plotly-plot").forEach(g => liste.push(g));
      racine.querySelectorAll("*").forEach(n => { if (n.shadowRoot) graphiques(n.shadowRoot, liste); });
      return liste;
    }

    function preparer() {
      const modifs = [];
      for (const g of graphiques(document)) {
        const racine = g.getRootNode();              // shadow root du graphique
        const hote = racine.host;                    // <marimo-plotly>
        const bloc = (hote && hote.closest("marimo-ui-element")) || g;
        // 1. masquer la barre Plotly (style injecté dans le shadow DOM)
        const style = document.createElement("style");
        style.textContent = ".modebar-container { display: none !important; }";
        (racine.host ? racine : document.head).appendChild(style);
        // 2. réduire le graphique pour qu'il tienne dans la page
        //    (taille réelle de la figure : _fullLayout ; le conteneur peut être plus étroit)
        const r = g.getBoundingClientRect();
        const largeur = (g._fullLayout && g._fullLayout.width) || r.width;
        const hauteur = (g._fullLayout && g._fullLayout.height) || r.height;
        const zoom = Math.min(1, LARGEUR_MAX / largeur, HAUTEUR_MAX / hauteur);
        modifs.push({ bloc, zoom: bloc.style.zoom, style });
        bloc.style.zoom = zoom;
      }
      return modifs;
    }

    function render({ el }) {
      const css = document.createElement("style");
      css.textContent = `
        button { padding: 6px 14px; font-size: 14px; cursor: pointer;
                 border: 1px solid #999; border-radius: 6px; background: #fff; }
        button:hover { background: #f2f2f2; }
        @media print { button { display: none; } }`;
      const bouton = document.createElement("button");
      bouton.textContent = "__LIBELLE__";
      bouton.onclick = () => {
        const modifs = preparer();
        // 3. après l'impression : rétablir l'affichage écran
        const retablir = () => {
          modifs.forEach(m => { m.bloc.style.zoom = m.zoom; m.style.remove(); });
          window.removeEventListener("afterprint", retablir);
        };
        window.addEventListener("afterprint", retablir);
        window.print();   // appelé DANS le cadre du notebook => notebook entier
      };
      el.append(css, bouton);
    }
    export default { render };
    """

    class _BoutonImprimer(_anywidget.AnyWidget):
        _esm = (_JS_BOUTON
                .replace("__LARGEUR__", str(_LARGEUR_MAX_GRAPHIQUE_PX))
                .replace("__HAUTEUR__", str(_HAUTEUR_MAX_GRAPHIQUE_PX))
                .replace("__LIBELLE__", _LIBELLE_BOUTON))

    # --- Affichage : style (invisible) + bouton et aide (non imprimés) ------------
    mo.vstack([
        mo.Html(f"<style>{_CSS}</style>"),
        mo.hstack(
            [mo.ui.anywidget(_BoutonImprimer()),
             mo.Html(f'<div class="pas-imprime" style="font-size:12px;color:#666">{_AIDE_BOUTON}</div>')],
            justify="start", align="center", gap=1,
        ),
    ])
    return


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
        2: "Répartition de l'impact carbone du bâtiment par seuil RE2020 (kgCO₂e/m² sur 50 ans)",
        3: "Impact carbone des matériaux : IC composant moyen par lot, par seuil RE2020",
        4: "Médiane IC Composant par matériau de structure et par seuil RE2020",
        5: "Nombre de fiches ACV par type (Q1 / total / Q3) par seuil RE2020",
        6: "Nature des fiches par lot RE2020 (% du nombre de fiches)",
        7: "Écart des bâtiments aux seuils réglementaires (%)",
        8: "Stock de carbone par type de matériau de structure et seuil RE2020",
        9: "Éloignement au seuil IC Construction 2028 : comparaison de deux groupes de bâtiments",
        10: "Dispersion du DH par zone climatique : par zone (traversante / non traversante) ou par bâtiment",
        11: "Répartition des bâtiments : structure, plancher, façade, générateur de chauffage",
    }

    # Configuration commune de TOUS les graphiques Plotly (barre d'outils au survol) :
    # ajoute le bouton « Download plot as JSON » (modeBarButtonsToAdd).
    CONFIG_PLOTLY = {"modeBarButtonsToAdd": ["downloadJson"]}

    # Imprimée : sommaire de la page de garde
    mo.md(
        "### Graphiques du dashboard\n\n"
        + "\n".join(f"- Graphique {_n} — {_titre}" for _n, _titre in GRAPHIQUES.items())
    )
    return CONFIG_PLOTLY, GRAPHIQUES


@app.cell(hide_code=True)
def saisie_jeton(mo):
    # ============================================================================
    # CELLULE — Jeton Turso. Il n'est JAMAIS écrit dans le code (dépôt GitHub) :
    #   1. variable d'environnement TURSO_TOKEN si elle existe (local / molab),
    #   2. sinon, champ de saisie masqué ci-dessous.
    # ============================================================================
    import os

    champ_jeton = mo.ui.text(kind="password", label="Jeton Turso", full_width=True)
    # (non imprimé : classe « pas-imprime »)
    mo.Html('<div class="pas-imprime">' + (
        mo.md("*Jeton Turso lu dans la variable d'environnement `TURSO_TOKEN`.*")
        if os.environ.get("TURSO_TOKEN")
        else mo.vstack([mo.md("### Connexion à la base OPEE"), champ_jeton])
    ).text + '</div>')
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

    _table = mo.ui.table(_df_comptages, show_download=False)
    _table
    """
    mo.Html('<div class="pas-imprime">' + _result.text + '</div>')   # (non imprimé)
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

    _table = mo.ui.table(_df, show_download=False)
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
    table = mo.ui.table(_df, show_download=False)
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

    # (non imprimé : l'usage figure dans le titre de chaque graphique)
    mo.Html('<div class="pas-imprime">' + mo.vstack([
        mo.md("### Pour quelle typologie ?"),
        dropdown_usage,
        mo.md(f"\n\n\n{button_lancer}"),
        mo.md("*🔽 cliquer pour lancer si rien ne s'affiche 🔽*")
    ]).text + '</div>')
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
    # TOUS les graphiques (1 à 11).
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
    # collectifs, cf. cellule `constantes_filtres`) ; ic_chantier et ic_eau complètent
    # ic_composant et ic_energie pour la répartition de l'impact carbone (graphique 2)
    _COLS_SUPPLEMENTAIRES = ["nb_total_fiche_acv", "stock_c", "surface_baies_rset", "surface_murs_rset",
                             "ic_chantier", "ic_eau"]
    # Choix constructifs et techniques (graphique 11) : plancher, remplissage de façade
    # (variables dc_*, peu fiables) et générateurs de chauffage (principal | appoint)
    _COLS_CHOIX_CONSTRUCTIFS = ["dc_type_plancher", "dc_materiau_remplissage_facade", "synthese_generateur_ch"]
    # Surfaces totales des zones (table zone_open_data, une ligne par zone)
    _COLS_ZONE = ["misurf_tot", "mbsurf_tot"]
    # Colonnes "une valeur PAR ZONE" : un bâtiment a 1 à n zones, on garde toutes
    # les valeurs sous forme de liste. {nom dans le DataFrame : (colonne de la table
    # zone_open_data, type SQL)}. Chaque liste est triée par numéro de zone (zone_index) ;
    # la valeur de rang n correspond donc à la même zone dans les trois listes.
    #   - dh_zones            : DH de chaque zone (le DH du bâtiment, dh_batiment, en est le max)
    #   - is_traversant_zones : la zone est-elle traversante (True / False) ?
    #   - dh_max_zones        : DH max réglementaire de chaque zone (graphique 10)
    _COLS_ZONE_LISTES = {
        "dh_zones": ("dh_zone", "REAL"),
        "is_traversant_zones": ("is_traversant", "INTEGER"),
        "dh_max_zones": ("dh_max", "REAL"),
    }
    _COL_ORDRE_ZONE = "zone_index"
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
        *[f"b.{col}" for col in _COLS_CHOIX_CONSTRUCTIFS],
        *[f"z.{col}" for col in _COLS_ZONE],
        *[f"z.{nom}_json" for nom in _COLS_ZONE_LISTES],   # listes par zone (JSON), décodées ensuite
        f"z.{_COL_ORDRE_ZONE}_json",                       # n° de zone, sert à trier les listes
        f"b.{_USAGE_COL} AS usage",
        "pf.annees_depot_pc_json",
        "pf.types_attestation_json",
    ]
    _select_sql = ",\n        ".join(_select)

    # Clé de rattachement bâtiment <-> zones (batiment_index NULL -> 0, comparé en texte)
    _CLE_BATIMENT_ZONE = "CAST(COALESCE(batiment_index, 0) AS TEXT)"
    _CLE_BATIMENT_B = "CAST(COALESCE(b.batiment_index, 0) AS TEXT)"
    _agg_zone = ",\n                ".join(f"MAX({col}) AS {col}" for col in _COLS_ZONE)
    # Listes par zone : json_group_array SANS DISTINCT (deux zones de même valeur
    # restent deux valeurs). CAST pour des types homogènes dans le JSON ; une valeur
    # absente (NULL) reste dans la liste (null) pour conserver le rang.
    _listes_zone = [
        *[(nom, col, _type) for nom, (col, _type) in _COLS_ZONE_LISTES.items()],
        (_COL_ORDRE_ZONE, _COL_ORDRE_ZONE, "INTEGER"),
    ]
    _agg_zone += ",\n                " + ",\n                ".join(
        f"json_group_array(CAST({col} AS {_type})) AS {nom}_json"
        for nom, col, _type in _listes_zone
    )

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
        -- Les valeurs PAR ZONE (DH, traversant, DH max) sont rassemblées en listes JSON ;
        -- leur tri par n° de zone est fait ensuite en polars (l'ordre d'un
        -- regroupement SQL n'est pas garanti).
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

    # Listes PAR ZONE (dh_zones, is_traversant_zones, dh_max_zones) :
    #   1. décodage JSON -> listes de nombres (is_traversant : 0/1 -> False/True) ;
    #   2. tri des trois listes par n° de zone (zone_index) : le rang n désigne la
    #      même zone dans chaque liste. Bâtiment sans zone -> listes NULL.
    _TYPES_LISTES_ZONE = {"dh_zones": pl.Float64, "is_traversant_zones": pl.Int64,
                          "dh_max_zones": pl.Float64}
    _df = _df.with_columns(
        *[pl.col(f"{_nom}_json").cast(pl.Utf8).str.json_decode(pl.List(_type)).alias(_nom)
          for _nom, _type in _TYPES_LISTES_ZONE.items()],
        pl.col(f"{_COL_ORDRE_ZONE}_json").cast(pl.Utf8).str.json_decode(pl.List(pl.Int64)).alias("_ordre_zone"),
    ).drop([f"{_nom}_json" for _nom in _TYPES_LISTES_ZONE] + [f"{_COL_ORDRE_ZONE}_json"])

    _a_trier = [*_TYPES_LISTES_ZONE, "_ordre_zone"]
    _lignes_zone = (
        _df.select("ID", *_a_trier)
        .filter(pl.col("_ordre_zone").is_not_null())
        .explode(_a_trier, empty_as_null=True)              # une ligne par zone (liste vide -> une ligne null, comportement actuel de Polars)
        .sort(["ID", "_ordre_zone"], nulls_last=True)       # tri par n° de zone
        .group_by("ID", maintain_order=True)
        .agg([pl.col(_nom) for _nom in _TYPES_LISTES_ZONE])  # on regroupe en listes
    )
    _df = _df.drop(list(_TYPES_LISTES_ZONE) + ["_ordre_zone"]).join(_lignes_zone, on="ID", how="left")
    _df = _df.with_columns(pl.col("is_traversant_zones").list.eval(pl.element().cast(pl.Boolean)))

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
    # (non imprimé : le filtre de surface figure dans l'encadré des filtres actifs)
    mo.Html('<div class="pas-imprime">' + mo.callout(mo.md(_texte), kind="info").text + '</div>')
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


    def panneau_filtres(parametres_graphique=None, *, avec_materiau=True, avec_inconnus=True, bascules_graphique=(), bascule_en_evidence=None):
        """Construit le panneau de filtres d'un graphique.

        - parametres_graphique : dict {libellé de l'accordéon: contenu} pour les paramètres
          propres au graphique (None = pas de 3e accordéon).
        - avec_materiau=False : graphique où le matériau est l'axe (pas de filtre matériau).
        - avec_inconnus=False : graphique qui n'applique pas « Masquer les inconnus ».
        - bascules_graphique : switchs propres au graphique, ajoutés dans la rangée du haut
          (à côté de « Valider… » et « Masquer les inconnus »).
        - bascule_en_evidence : un widget propre au graphique (switch, liste…), affiché dans un
          encadré SOUS la rangée du haut (plus visible que les bascules de la rangée).
        """
        # 1. Qualité des données : toujours visible, en haut
        _qualite = mo.hstack(
            [choix_valide_regles] + ([cacher_inconnu] if avec_inconnus else []) + list(bascules_graphique),
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

        _panneau = mo.vstack([
            _qualite,
            *([mo.callout(bascule_en_evidence, kind="info")] if bascule_en_evidence is not None else []),
            mo.hstack(_accordeons, justify="start", align="start", wrap=True, widths="equal"),
        ])
        # Non imprimé (classe « pas-imprime », cf. cellule style_impression) : les
        # filtres actifs restent lisibles dans l'encadré affiché sous le panneau
        return mo.Html(f'<div class="pas-imprime">{_panneau.text}</div>')

    return (panneau_filtres,)


@app.cell(hide_code=True)
def saut_page_1(mo):
    # Saut de page à l'impression avant le graphique 1 : la 1re page imprimée est la
    # page de garde (visuel, version, encarts, liens vers le HUB, liste des
    # graphiques). Aucun effet à l'écran.
    mo.Html('<div class="saut-page"></div>')
    return


@app.cell(hide_code=True)
def param_graphique_1(mo, panneau_filtres):
    # Paramètre propre au graphique 1
    seuil_bas_iccons = mo.ui.slider(start=400, stop=700, step=50, show_value=True, label="La tranche basse de l'ic_construction pour séparer les projets ?")

    mo.vstack([
        mo.Html('<div class="pas-imprime">' + mo.md("### Paramètres du graphique 1").text + '</div>'),
        panneau_filtres({
            "Graphique 1": mo.vstack([
                seuil_bas_iccons,
                mo.md("*400 pour le logement 500 pour le reste ?*\n"),
            ]),
        }),
    ])
    return (seuil_bas_iccons,)



@app.cell(hide_code=True)
def graphique_1(
    CONFIG_PLOTLY,
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

    _graphique = mo.ui.plotly(_fig, config=CONFIG_PLOTLY)

    # Export : les données TRACÉES (nombre de bâtiments par seuil x tranche d'IC)
    mo.vstack([_graphique, boutons_export(_agg.sort("seuil", "tranche_ic"), "graphique_1_batiments_par_tranche_ic")])
    return


@app.cell(hide_code=True)
def resume_filtres_graphique_1(resume_filtres):
    # Résumé des filtres actifs du graphique 1, placé SOUS le graphique (cellule
    # séparée : il lit les valeurs des widgets, alors que le panneau reste statique).
    resume_filtres()
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
    #                               des matériaux en 5 catégories (graphiques 4 et 8)
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
    # Regroupement des 15 matériaux de structure en 5 catégories (graphiques 4 et 8)
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
        TRANCHES_LOGEMENT_COLLECTIF,
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
    def resume_filtres(avec_materiau=True, avec_inconnus=True, parametres_graphique=None):
        """Encadré résumant les filtres actifs, rangés comme dans le panneau.
        - avec_materiau=False : graphique où le matériau est l'axe (filtre non appliqué).
        - avec_inconnus=False : graphique qui n'applique pas « Masquer les inconnus ».
        - parametres_graphique : dict {libellé : [textes]} des filtres propres au graphique,
          ajoutés en dernière ligne de l'encadré (ex. {"Graphique 6": ["seuils RE2022"]})."""
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
        # Filtres propres au graphique (optionnels), une ligne par libellé
        _lignes_graphique = "".join(
            f"  \n**{_libelle}** : {' · '.join(_textes)}"
            for _libelle, _textes in (parametres_graphique or {}).items()
        )
        return mo.callout(
            mo.md(
                "**Filtres actifs**  \n"
                f"**Qualité** : {' · '.join(_qualite)}  \n"
                f"**Période et lieu** : {' · '.join(_periode)}  \n"
                f"**Bâtiment** : {' · '.join(_batiment)}"
                f"{_lignes_graphique}"
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
def saut_page_2(mo):
    # Saut de page à l'impression avant le graphique 2 (aucun effet à l'écran ;
    # règle `.saut-page` dans la cellule `style_impression`).
    mo.Html('<div class="saut-page"></div>')
    return


@app.cell(hide_code=True)
def param_graphique_2(mo, panneau_filtres):
    # ============================================================================
    # CELLULE D'AFFICHAGE — paramètres (filtres) du graphique 2.
    # Pas de paramètre propre ; « Masquer les inconnus » n'y figure pas : seuls les
    # seuils RE2022 à RE2031 sont tracés (les bâtiments « Inconnu » sont ignorés).
    # ============================================================================

    mo.vstack([
        mo.Html('<div class="pas-imprime">' + mo.md("### Paramètres du graphique 2").text + '</div>'),
        panneau_filtres(avec_inconnus=False),
    ])
    return


@app.cell(hide_code=True)
def graphique_2(
    CONFIG_PLOTLY,
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
    # CELLULE — Graphique 2 : répartition de l'impact carbone du bâtiment par seuil
    # RE2020 (barres empilées : composants, chantier, énergie, eau).
    #
    # Part de DATA_brut (AUCUN appel réseau ici) ; filtres temps réel communs à tous
    # les graphiques (cellule `filtres_communs`), sauf « Masquer les inconnus ».
    #
    # Valeur d'une barre = MOYENNE par seuil, arrondie à l'unité ; le total « Bâtiment »
    # est la somme des quatre valeurs arrondies. Les pourcentages (bulles) sont
    # calculés sur composants + chantier + énergie (l'eau n'a pas de seuil).
    # ============================================================================

    # ============================================================================
    # PARAMÈTRES (toutes les variables au même endroit)
    # ============================================================================

    # --- Seuils tracés (un par barre, de gauche à droite) --------------------------
    _SEUILS = ["RE2022", "RE2025", "RE2028", "RE2031"]

    # --- Postes de l'impact carbone, DU BAS VERS LE HAUT de la pile ----------------
    # clé : (colonne de DATA_brut, libellé de la légende, couleur de la barre,
    #        couleur du chiffre dans la barre)
    _POSTES = {
        "Composants": ("ic_composant", "Composants", "#283246", "white"),
        "Chantier":   ("ic_chantier", "Chantier", "#B4BCCC", "black"),
        "Énergie":    ("ic_energie", "Énergie", "#FFDA7A", "black"),
        "Eau":        ("ic_eau", "Eau (sans seuil)", "#00B0F0", "black"),
    }
    # Poste dont le chiffre est écrit sur un petit fond de la couleur de la barre (le bloc,
    # très fin, est chevauché par les voisins : sans fond, le chiffre serait illisible)
    _POSTE_CHANTIER = "Chantier"
    # Postes avec bulle de pourcentage (l'eau n'en a pas) : couleur de la bulle
    _BULLES = {"Composants": "#283246", "Chantier": "#8892A6", "Énergie": "#FFC000"}

    # --- Dimensions et mise en page ------------------------------------------------
    _LARGEUR, _HAUTEUR = 1180, 640
    _MARGE_HAUT, _MARGE_BAS, _MARGE_GAUCHE, _MARGE_DROITE = 110, 90, 90, 30
    _LARGEUR_BARRE = 0.45               # largeur d'une barre (en unité d'axe x)
    _X_MIN = -0.75                      # bornes de l'axe x (la 1re barre est en x = 0)
    _MARGE_X_DROITE = 0.65              # espace à droite de la dernière barre (unité d'axe x)
    _COEF_Y_MAX = 1.35                  # axe y = total le plus haut x ce coefficient (place pour la légende)
    _POLICE = "Calibri, Carlito, Arial"

    # --- Bulles de pourcentage (ellipses dimensionnées en pixels) ------------------
    _BULLE_LARGEUR_PX, _BULLE_HAUTEUR_PX = 60, 34
    _BULLE_DECALAGE_PX = 8              # espace entre le bord de la barre et la bulle
    _BULLE_ECART_MIN_PX = 40            # distance verticale minimale entre deux bulles

    # --- Mot « construction » (composants + chantier, 1re barre seulement) ---------
    _COULEUR_CONSTRUCTION = "#8a8a8a"
    _ACCOLADE_DECALAGE_PX = 55          # distance entre le bord de la barre et le trait gris
    _TEXTE_CONSTRUCTION_DECALAGE_PX = 14  # distance entre le trait gris et le texte vertical

    # ============================================================================
    # 1. DONNÉES
    # ============================================================================

    _USAGE = dropdown_usage.value
    _cols = [_c[0] for _c in _POSTES.values()]

    _df = appliquer_filtres(DATA_brut, filtre_inconnu=False).filter(pl.col("seuil").is_in(_SEUILS))
    _nb_avant = _df.height
    # Les 4 postes doivent être renseignés, sinon la somme des barres serait faussée
    _df = _df.drop_nulls(_cols)
    _nb_exclus = _nb_avant - _df.height

    mo.stop(_df.height == 0, mo.md("**Aucun bâtiment (avec les 4 postes renseignés) ne correspond aux filtres choisis.**"))

    # Moyenne exacte par seuil, puis valeur arrondie à l'unité (celle qui est affichée)
    _stats = (
        _df.group_by("seuil")
        .agg(pl.len().alias("n"), *[pl.col(_c).mean().alias(_k) for _k, (_c, *_r) in _POSTES.items()])
        .with_columns(pl.col("seuil").replace_strict({_s: _i for _i, _s in enumerate(_SEUILS)}).alias("_ordre"))
        .sort("_ordre")
        .drop("_ordre")
    )
    _lignes = _stats.to_dicts()
    _seuils_presents = [_l["seuil"] for _l in _lignes]

    _valeurs = []        # une entrée par barre : {poste: valeur arrondie}, total, base des %
    for _l in _lignes:
        _v = {_k: round(_l[_k]) for _k in _POSTES}
        _valeurs.append({"v": _v, "total": sum(_v.values()), "base_pct": sum(_v[_k] for _k in _BULLES)})

    # ============================================================================
    # 2. ÉCHELLE (pixels par unité d'axe) : sert à placer bulles, accolade et libellés
    # ============================================================================

    _y_max = max(_b["total"] for _b in _valeurs) * _COEF_Y_MAX
    _x_max = len(_lignes) - 1 + _MARGE_X_DROITE
    _largeur_trace = _LARGEUR - _MARGE_GAUCHE - _MARGE_DROITE
    _px_par_unite_y = (_HAUTEUR - _MARGE_HAUT - _MARGE_BAS) / _y_max
    _demi_barre_px = _LARGEUR_BARRE / 2 * _largeur_trace / (_x_max - _X_MIN)

    # ============================================================================
    # 3. FIGURE
    # ============================================================================

    _fig = go.Figure()
    _formes, _annotations = [], []

    # --- Barres empilées (une trace par poste) ---------------------------------------
    for _k, (_col, _libelle, _couleur, _couleur_txt) in _POSTES.items():
        _fig.add_trace(go.Bar(
            x=_seuils_presents,
            y=[_b["v"][_k] for _b in _valeurs],
            name=_libelle,
            marker_color=_couleur,
            width=_LARGEUR_BARRE,
            # Chiffre au milieu de sa barre, MÊME quand le bloc est trop fin pour le contenir
            # (constraintext="none" : pas de réduction ni de déplacement ; textangle=0 : jamais
            # pivoté). Le chantier est écrit à part (annotation, cf. plus bas).
            text=[("" if _k == _POSTE_CHANTIER else _b["v"][_k]) for _b in _valeurs],
            textposition="inside",
            insidetextanchor="middle",
            textangle=0,
            constraintext="none",
            textfont=dict(color=_couleur_txt, size=14, family=_POLICE),
            customdata=[[_l[_k], _l["n"]] for _l in _lignes],
            hovertemplate=(
                f"<b>%{{x}}</b> — {_libelle}<br>"
                "Moyenne : %{customdata[0]:.1f} kgCO₂e/m²<br>"
                "Affiché (arrondi) : %{y}<br>"
                "n = %{customdata[1]} bâtiments<extra></extra>"
            ),
        ))

    # --- Annotations et formes, barre par barre -----------------------------------------
    for _i, (_l, _b) in enumerate(zip(_lignes, _valeurs)):
        _x = _l["seuil"]
        _v = _b["v"]

        # Total du bâtiment, au-dessus de la barre : « Bâtiment : » en petit, total en gras
        _annotations.append(dict(
            x=_x, y=_b["total"], yshift=30, showarrow=False,
            text="<span style='font-size:10px;color:#666'>Bâtiment :</span>",
        ))
        _annotations.append(dict(
            x=_x, y=_b["total"], yshift=13, showarrow=False,
            text=f"<b>{_b['total']}</b>", font=dict(size=20),
        ))

        # Chiffre du chantier : au milieu de son bloc, même style que les autres chiffres, sur
        # un fond de la couleur de la barre (il peut chevaucher un peu les blocs voisins)
        _annotations.append(dict(
            x=_x, y=_v["Composants"] + _v[_POSTE_CHANTIER] / 2, showarrow=False,
            text=str(_v[_POSTE_CHANTIER]), bgcolor=_POSTES[_POSTE_CHANTIER][2], borderpad=1,
            font=dict(color=_POSTES[_POSTE_CHANTIER][3], size=14, family=_POLICE),
        ))

        # Bulles de pourcentage : au centre de leur bloc, puis écartées de _BULLE_ECART_MIN_PX
        # (positions en pixels depuis l'axe x ; l'écart est réparti vers le haut et vers le bas)
        _centre, _cumul = {}, 0
        for _k in _POSTES:
            _centre[_k] = _cumul + _v[_k] / 2
            _cumul += _v[_k]
        _pos_px = {_k: _centre[_k] * _px_par_unite_y for _k in _BULLES}
        _cles = list(_BULLES)
        for _j in range(1, len(_cles)):
            _manque = _BULLE_ECART_MIN_PX - (_pos_px[_cles[_j]] - _pos_px[_cles[_j - 1]])
            if _manque > 0:
                _pos_px[_cles[_j]] += _manque / 2
                _pos_px[_cles[_j - 1]] -= _manque / 2
        _x0_bulle = _demi_barre_px + _BULLE_DECALAGE_PX
        for _k, _couleur_bulle in _BULLES.items():
            _y_bulle = _pos_px[_k] / _px_par_unite_y
            _pct = round(100 * _v[_k] / _b["base_pct"]) if _b["base_pct"] else 0
            _formes.append(dict(
                type="circle", xref="x", yref="y", xanchor=_x, yanchor=_y_bulle,
                xsizemode="pixel", ysizemode="pixel",
                x0=_x0_bulle, x1=_x0_bulle + _BULLE_LARGEUR_PX,
                y0=-_BULLE_HAUTEUR_PX / 2, y1=_BULLE_HAUTEUR_PX / 2,
                fillcolor=_couleur_bulle, line=dict(color="#9aa0a6", width=1),
            ))
            _annotations.append(dict(
                x=_x, y=_y_bulle, xshift=_x0_bulle + _BULLE_LARGEUR_PX / 2, showarrow=False,
                text=f"<b>{_pct} %</b>", font=dict(size=16, color="white"),
            ))

        # Bandeau noir sous la barre : seuil et nombre de bâtiments
        _annotations.append(dict(
            x=_x, y=0, yshift=-34, showarrow=False, width=170, bgcolor="black", borderpad=6,
            text=f"<b>{_x}</b>  <span style='font-size:11px'>n = {_l['n']}</span>",
            font=dict(color="white", size=17),
        ))

        # « construction » (composants + chantier) : 1re barre seulement, texte gris vertical
        # et trait gris de la hauteur composants + chantier
        if _i == 0:
            _haut = _v["Composants"] + _v["Chantier"]
            _x_trait = -(_demi_barre_px + _ACCOLADE_DECALAGE_PX)
            _formes.append(dict(
                type="line", xref="x", yref="y", xanchor=_x, xsizemode="pixel",
                x0=_x_trait, x1=_x_trait, y0=0, y1=_haut,
                line=dict(color="#9a9a9a", width=1.5),
            ))
            _annotations.append(dict(
                x=_x, y=_haut / 2, xshift=_x_trait - _TEXTE_CONSTRUCTION_DECALAGE_PX, showarrow=False,
                text="construction", textangle=-90, font=dict(size=15, color=_COULEUR_CONSTRUCTION),
            ))

    _fig.update_layout(
        barmode="stack",
        template="plotly_white",
        width=_LARGEUR,
        height=_HAUTEUR,
        shapes=_formes,
        annotations=_annotations,
        title=dict(
            text=f"<b>Graphique 2 — {GRAPHIQUES[2]} — {_USAGE}</b><br>"
                 f"<sup>{SOUS_TITRE_FILTRES} — moyenne par seuil, arrondie à l'unité</sup>",
            font=dict(size=18),
        ),
        font=dict(family=_POLICE),
        margin=dict(t=_MARGE_HAUT, b=_MARGE_BAS, l=_MARGE_GAUCHE, r=_MARGE_DROITE),
        yaxis=dict(
            title=dict(text="<i>kgCO₂e/m² sur 50 ans</i>", font=dict(size=15)),
            showgrid=False, range=[0, _y_max], tickfont=dict(size=13),
        ),
        xaxis=dict(
            showticklabels=False, showline=True, linecolor="black", linewidth=4,
            range=[_X_MIN, _x_max],
        ),
        # Légende en haut à droite, dans l'ordre de la pile (le dernier poste = le plus haut)
        legend=dict(traceorder="reversed", x=0.99, xanchor="right", y=0.99, yanchor="top", font=dict(size=15)),
    )

    _graphique = mo.ui.plotly(_fig, config=CONFIG_PLOTLY)

    # Export : les données TRACÉES (par seuil : n, moyennes exactes, valeurs arrondies, total, %)
    _export = _stats.rename({_k: f"moyenne_{_k}" for _k in _POSTES}).with_columns(
        *[pl.Series(f"arrondi_{_k}", [_b["v"][_k] for _b in _valeurs]) for _k in _POSTES],
        pl.Series("total_batiment", [_b["total"] for _b in _valeurs]),
        *[pl.Series(f"pct_{_k}", [round(100 * _b["v"][_k] / _b["base_pct"]) if _b["base_pct"] else 0 for _b in _valeurs])
          for _k in _BULLES],
    )

    _note_exclus = (
        mo.md(f"*{_nb_exclus} bâtiment(s) écarté(s) : au moins un des 4 postes "
              "(composants, chantier, énergie, eau) n'est pas renseigné.*")
        if _nb_exclus else mo.md("")
    )
    mo.vstack([_graphique, _note_exclus, boutons_export(_export, "graphique_2_repartition_impact_carbone")])
    return


@app.cell(hide_code=True)
def resume_filtres_graphique_2(resume_filtres):
    # Résumé des filtres actifs du graphique 2, placé SOUS le graphique (cellule
    # séparée : il lit les valeurs des widgets, alors que le panneau reste statique).
    resume_filtres(avec_inconnus=False)
    return


@app.cell(hide_code=True)
def saut_page_3(mo):
    # Saut de page à l'impression avant le graphique 3 (aucun effet à l'écran ;
    # règle `.saut-page` dans la cellule `style_impression`).
    mo.Html('<div class="saut-page"></div>')
    return


@app.cell(hide_code=True)
def param_graphique_3(mo, panneau_filtres):
    # Paramètre propre au graphique 3 (le seul qui utilise les 13 lots)
    valeur_exclusion_lots = mo.ui.range_slider(start=0, stop=500, step=10, value=[0, 300], label="Un lot est compris entre :", show_value=True)

    mo.vstack([
        mo.Html('<div class="pas-imprime">' + mo.md("### Paramètres du graphique 3").text + '</div>'),
        panneau_filtres({
            "Graphique 3": mo.vstack([
                valeur_exclusion_lots,
                mo.md("*pour exclure les valeurs anormales (un lot hors de cette plage est ignoré dans la moyenne)*"),
            ]),
        }),
    ])
    return (valeur_exclusion_lots,)



@app.cell(hide_code=True)
def graphique_3(
    CONFIG_PLOTLY,
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
    # CELLULE — Graphique 3 (lots)
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
                f"<b>Graphique 3 — {GRAPHIQUES[3]} — {dropdown_usage.value}</b><br>"
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

    _graphique = mo.ui.plotly(_fig, config=CONFIG_PLOTLY)

    # Export : les données TRACÉES (IC moyen de chaque lot, par seuil)
    mo.vstack([_graphique, boutons_export(
        _df_long.drop("_lot").with_columns(pl.col("composant").replace(_NOMS_LOTS).alias("lot")).drop("composant"),
        "graphique_3_ic_moyen_par_lot",
    )])
    return


@app.cell(hide_code=True)
def resume_filtres_graphique_3(resume_filtres):
    # Résumé des filtres actifs du graphique 3, placé SOUS le graphique (cellule
    # séparée : il lit les valeurs des widgets, alors que le panneau reste statique).
    resume_filtres()
    return


@app.cell(hide_code=True)
def saut_page_4(mo):
    # Saut de page à l'impression avant le graphique 4 (aucun effet à l'écran ;
    # règle `.saut-page` dans la cellule `style_impression`).
    mo.Html('<div class="saut-page"></div>')
    return


@app.cell(hide_code=True)
def param_graphique_4(mo, panneau_filtres):
    # ============================================================================
    # CELLULE D'AFFICHAGE — paramètres (filtres) du graphique 4.
    # Le matériau n'y figure pas : c'est l'axe du graphique.
    # ============================================================================

    mo.vstack([
        mo.Html('<div class="pas-imprime">' + mo.md("### Paramètres du graphique 4").text + '</div>'),
        panneau_filtres(avec_materiau=False),
    ])
    return



@app.cell(hide_code=True)
def graphique_4(
    CONFIG_PLOTLY,
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
    # GRAPHIQUE 4 — Médiane IC Composant par matériau de structure, par seuil
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
                f"<b>Graphique 4 — {GRAPHIQUES[4]} — {_USAGE}</b><br>"
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

    _graphique = mo.ui.plotly(_fig, config=CONFIG_PLOTLY)

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
    mo.vstack([_graphique, boutons_export(_export, "graphique_4_mediane_ic_par_materiau")])
    return


@app.cell(hide_code=True)
def resume_filtres_graphique_4(resume_filtres):
    # Résumé des filtres actifs du graphique 4, placé SOUS le graphique (cellule
    # séparée : il lit les valeurs des widgets, alors que le panneau reste statique).
    resume_filtres(avec_materiau=False)
    return


@app.cell(hide_code=True)
def saut_page_5(mo):
    # Saut de page à l'impression avant le graphique 5 (aucun effet à l'écran ;
    # règle `.saut-page` dans la cellule `style_impression`).
    mo.Html('<div class="saut-page"></div>')
    return


@app.cell(hide_code=True)
def param_graphique_5(mo, panneau_filtres):
    # ============================================================================
    # CELLULE D'AFFICHAGE — paramètres (filtres) du graphique 5.
    # ============================================================================

    mo.vstack([
        mo.Html('<div class="pas-imprime">' + mo.md("### Paramètres du graphique 5").text + '</div>'),
        panneau_filtres(),
    ])
    return



@app.cell(hide_code=True)
def graphique_5(
    CONFIG_PLOTLY,
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
    # GRAPHIQUE 5 — Nombre de fiches ACV par type, Q1 / total / Q3 par seuil RE2020
    #
    # Part de DATA_brut (cellule d'extraction partagée) : AUCUN appel
    # réseau ici. Tous les filtres sont appliqués en polars, en temps réel.
    #
    # Définition du total (vérifiée le 15/10/2026 sur tous les logements collectifs,
    # script de contrôle OPEE_Test_Fiches) :
    #     nb_total_fiche_acv = somme de TOUTES les colonnes nb_* SAUF nb_des
    # nb_des n'est donc pas tracé (il serait compté deux fois).
    #
    # Pour chaque seuil, 3 emplacements resserrés :
    #   - Q1 et Q3 : barres empilées par type de fiche ; hauteur de chaque segment =
    #     le quartile (25 % ou 75 %) de CE type. « Σ » au-dessus = somme de ces
    #     quartiles (ce n'est PAS le quartile du total).
    #   - Total (au milieu) : total des fiches calculé ci-dessus, style du graphique 8 :
    #     point = médiane, barre = de Q1 à Q3 (vrais quartiles du total).
    # ============================================================================


    # ============================================================================
    # PARAMÈTRES (toutes les variables au même endroit)
    # ============================================================================

    # --- Widgets : filtres temps réel -------------------------------------------
    _USAGE = dropdown_usage.value
    # (les autres filtres viennent de la cellule `filtres_communs`)


    # --- Segments empilés, de bas en haut : {nom affiché : colonnes additionnées} --
    # Les 6 segments couvrent exactement les colonnes du total (toutes sauf nb_des).
    _SEGMENTS = {
        "FDES": ["nb_fdes"],
        "Fiches configurées": ["nb_fiche_configuree"],
        "PEP": ["nb_pep"],
        "PEP extrapolées": ["nb_pep_extrapolee"],
        "DED": ["nb_ded"],
        "Autres": ["nb_conventionnelle", "nb_composant_reemploi", "nb_composant_vide"],
    }
    _COL_TOTAL = "_total_fiches"       # colonne de travail : total calculé par bâtiment

    # --- Couleurs (palette validée par Guigui le 15/10/2026) ----------------------
    # FDES / PEP : teinte des fiches individuelles (la table bâtiment ne distingue pas
    # individuelles et collectives).
    _COULEURS_SEGMENTS = {
        "FDES": "#55A868",                # vert
        "Fiches configurées": "#4C72B0",  # fond bleu (hachures vertes, cf. _HACHURES)
        "PEP": "#4C72B0",                 # bleu
        "PEP extrapolées": "#4C72B0",     # bleu hachuré (cf. _HACHURES)
        "DED": "#DD8452",                 # orange
        "Autres": "#CFCFCF",              # gris clair
    }
    # Segments hachurés : {segment : (motif, couleur des hachures, couleur du fond)}
    #   - Fiches configurées : une fiche configurée est une FDES ou une PEP
    #     -> hachures vertes (FDES) sur fond bleu (PEP)
    #   - PEP extrapolées : hachures bleues sur fond blanc
    _HACHURES = {
        "Fiches configurées": ("/", "#55A868", "#4C72B0"),
        "PEP extrapolées": ("/", "#4C72B0", "white"),
    }
    _TAILLE_HACHURES = 9
    _DENSITE_HACHURES = 0.5
    _COULEUR_TEXTE_SEGMENTS = {
        "FDES": "white", "Fiches configurées": "white", "PEP": "white",
        "PEP extrapolées": "#1F3A66", "DED": "white", "Autres": "#333333",
    }
    _COULEUR_TOTAL = "#333333"         # point et barre du total

    # --- Seuils (Inconnu inclus par défaut, sauf si la case "cacher" est cochée)
    _ORDRE_SEUILS = ["RE2022", "RE2025", "RE2028", "RE2031", "Inconnu"]

    # --- Mise en page -------------------------------------------------------------
    _LARGEUR_BARRE = 0.28      # largeur de chaque colonne Q1/Q3
    _ESPACE_ENTRE_SEUILS = 0.9  # espace entre deux groupes de seuil
    _TAILLE_TITRE_GRAPHIQUE = 20
    _TAILLE_MIN_TEXTE = 10     # px : valeur masquée si elle ne tient pas dans son segment (visible au survol)


    # ============================================================================
    # 1. FILTRAGE (polars, temps réel) -- même logique que les autres graphiques
    # ============================================================================

    _df = appliquer_filtres(DATA_brut)

    mo.stop(_df.height == 0, mo.md("**Aucun bâtiment ne correspond aux filtres choisis.**"))

    # Valeur de chaque segment (somme de ses colonnes) et total calculé.
    # ignore_nulls=False : une colonne NULL rend le segment NULL ; il est alors ignoré
    # par les quartiles (au lieu d'être compté comme 0).
    _df = _df.with_columns(
        [pl.sum_horizontal(_cols, ignore_nulls=False).alias(_seg) for _seg, _cols in _SEGMENTS.items()]
    ).with_columns(
        pl.sum_horizontal(list(_SEGMENTS), ignore_nulls=False).alias(_COL_TOTAL)
    )


    # ============================================================================
    # 2. AGRÉGATION : quartiles de chaque segment et du total, par seuil
    # ============================================================================

    _agg = _df.group_by("seuil").agg(
        pl.len().alias("nb_batiments"),
        *[pl.col(s).quantile(0.25).alias(f"{s}_q1") for s in _SEGMENTS],
        *[pl.col(s).quantile(0.75).alias(f"{s}_q3") for s in _SEGMENTS],
        pl.col(_COL_TOTAL).quantile(0.25).alias("total_q1"),
        pl.col(_COL_TOTAL).median().alias("total_mediane"),
        pl.col(_COL_TOTAL).quantile(0.75).alias("total_q3"),
    )

    _seuils = [s for s in _ORDRE_SEUILS if s in _agg["seuil"].to_list()]
    _par_seuil = {row["seuil"]: row for row in _agg.iter_rows(named=True)}


    # ============================================================================
    # 3. CONSTRUCTION DU GRAPHIQUE
    # ============================================================================

    _fig = go.Figure()

    # Positions x : Q1 et Q3 de part et d'autre du total (au milieu), gros espace
    # entre les groupes de seuils.
    _pas_groupe = 3 * _LARGEUR_BARRE + _ESPACE_ENTRE_SEUILS
    _centres = {s: i * _pas_groupe for i, s in enumerate(_seuils)}

    _tickvals, _ticktext = [], []
    _annotations = []

    for _seuil in _seuils:
        _ligne = _par_seuil[_seuil]
        _x_q1 = _centres[_seuil]
        _x_total = _x_q1 + _LARGEUR_BARRE
        _x_q3 = _x_q1 + 2 * _LARGEUR_BARRE

        # --- Colonnes Q1 et Q3 (empilées, valeur écrite dans chaque segment) ---
        for _quantile, _x in (("q1", _x_q1), ("q3", _x_q3)):
            _bas = 0
            for _seg in _SEGMENTS:
                _valeur = _ligne[f"{_seg}_{_quantile}"] or 0
                _hachure = _HACHURES.get(_seg)
                _fig.add_trace(go.Bar(
                    x=[_x], y=[_valeur], base=_bas, width=_LARGEUR_BARRE,
                    marker=dict(
                        color=_hachure[2] if _hachure else _COULEURS_SEGMENTS[_seg],
                        line=dict(color="white", width=0.6),
                        pattern=dict(shape=_hachure[0], fgcolor=_hachure[1], bgcolor=_hachure[2],
                                     size=_TAILLE_HACHURES, solidity=_DENSITE_HACHURES) if _hachure else None,
                    ),
                    text=[f"{_valeur:.0f}" if _valeur > 0 else ""],
                    textposition="inside", insidetextanchor="middle",
                    textfont=dict(color=_COULEUR_TEXTE_SEGMENTS[_seg], size=11,
                                  weight="bold" if _hachure else "normal"),
                    name=_seg,
                    legendgroup=_seg,
                    showlegend=(_seuil == _seuils[0] and _quantile == "q1"),
                    hovertemplate=f"{_seg}<br>{_seuil} ({_quantile.upper()}) : %{{y:.1f}}<extra></extra>",
                ))
                _bas += _valeur
            _annotations.append(dict(
                x=_x, y=_bas, text=f"<b>Σ {_bas:.0f}</b>", showarrow=False, yshift=10, font=dict(size=12),
            ))

        # --- Total (au milieu) : point = médiane, barre = Q1 à Q3 (style graphique 8)
        _q1_t, _med_t, _q3_t = _ligne["total_q1"], _ligne["total_mediane"], _ligne["total_q3"]
        if _med_t is not None:
            _fig.add_trace(go.Scatter(
                x=[_x_total], y=[_med_t], mode="markers",
                marker=dict(size=12, color=_COULEUR_TOTAL, line=dict(color="black", width=1)),
                error_y=dict(
                    type="data", symmetric=False, thickness=3, width=12, color=_COULEUR_TOTAL,
                    array=[_q3_t - _med_t], arrayminus=[_med_t - _q1_t],
                ),
                name="Total des fiches (point = médiane, barre = Q1 à Q3)",
                legendgroup="total",
                showlegend=(_seuil == _seuils[0]),
                hovertemplate=(
                    f"<b>Total des fiches — {_seuil}</b><br>Q1 = {_q1_t:.0f}<br>"
                    f"Médiane = {_med_t:.0f}<br>Q3 = {_q3_t:.0f}<extra></extra>"
                ),
            ))
            # Médiane écrite à gauche du point
            _annotations.append(dict(
                x=_x_total, y=_med_t, xshift=-12, xanchor="right", showarrow=False,
                text=f"<b>{_med_t:.0f}</b>", font=dict(size=12, color=_COULEUR_TOTAL),
            ))

        # --- Étiquettes Q1 / Total / Q3 sous les colonnes -----------------------
        _tickvals += [_x_q1, _x_total, _x_q3]
        _ticktext += ["Q1", "Total", "Q3"]

        # --- Nom du seuil, centré sous le groupe --------------------------------
        _annotations.append(dict(
            x=_x_total, y=0, yref="paper", yshift=-50, showarrow=False,
            text=f"<b>{_seuil}</b><br><span style='font-size:11px;color:gray'>n = {_ligne['nb_batiments']}</span>",
            font=dict(size=13),
        ))

    _fig.update_layout(
        barmode="overlay",  # les barres sont déjà positionnées par base=..., pas de superposition
        template="plotly_white",
        height=600,
        uniformtext=dict(minsize=_TAILLE_MIN_TEXTE, mode="hide"),
        title=dict(
            text=f"<b>Graphique 5 — {GRAPHIQUES[5]} — {_USAGE}</b><br>"
                 f"<sup>Q1 / Q3 : quartile de chaque type de fiche, empilés (Σ = somme des quartiles) ; "
                 f"Total : toutes les fiches sauf DES (point = médiane, barre = Q1 à Q3)</sup><br>"
                 f"<sup>{SOUS_TITRE_FILTRES}</sup>",
            font=dict(size=_TAILLE_TITRE_GRAPHIQUE),
        ),
        xaxis=dict(
            tickvals=_tickvals, ticktext=_ticktext, tickfont=dict(size=10, color="gray"),
            range=[-_LARGEUR_BARRE, max(_centres.values()) + 3 * _LARGEUR_BARRE],
        ),
        yaxis=dict(title="Nombre de fiches"),
        legend=dict(orientation="h", x=0.5, xanchor="center", y=-0.2, yanchor="top"),
        margin=dict(t=130, b=140, l=60, r=20),
        annotations=_annotations,
    )

    _graphique = mo.ui.plotly(_fig, config=CONFIG_PLOTLY)

    # Export : les données TRACÉES (Q1 / Q3 de chaque segment, Q1 / médiane / Q3 du total, par seuil)
    _export = _agg.sort(pl.col("seuil").replace_strict({s: i for i, s in enumerate(_ORDRE_SEUILS)}, default=99))
    mo.vstack([_graphique, boutons_export(_export, "graphique_5_quartiles_fiches_par_seuil")])
    return


@app.cell(hide_code=True)
def resume_filtres_graphique_5(resume_filtres):
    # Résumé des filtres actifs du graphique 5, placé SOUS le graphique (cellule
    # séparée : il lit les valeurs des widgets, alors que le panneau reste statique).
    resume_filtres()
    return


@app.cell(hide_code=True)
def saut_page_6(mo):
    # Saut de page à l'impression avant le graphique 6 (aucun effet à l'écran ;
    # règle `.saut-page` dans la cellule `style_impression`).
    mo.Html('<div class="saut-page"></div>')
    return


@app.cell(hide_code=True)
def param_graphique_6(mo, panneau_filtres):
    # ============================================================================
    # CELLULE WIDGETS — paramètres propres au graphique 6 (nature des fiches par lot).
    #
    # À placer AVANT la cellule graphique (marimo exige qu'un widget soit défini
    # dans une autre cellule que celle qui lit sa valeur).
    # Les filtres communs (dont l'année de dépôt, la zone, la surface…) viennent du
    # panneau partagé, comme pour le graphique 5.
    # ============================================================================

    # ---- Variables --------------------------------------------------------------
    SEUILS_6 = ["RE2022", "RE2025", "RE2028", "RE2031"]   # seuils IC construction atteints

    # Seuils : tout coché = pas de filtre (les « Inconnu » suivent alors « Masquer les inconnus ») ;
    # sélection partielle = seuls les seuils cochés sont gardés.
    choix_seuils_6 = mo.ui.multiselect(options=SEUILS_6, value=SEUILS_6, label="Seuil IC construction atteint")
    case_sous_lots_6 = mo.ui.switch(label="Détailler par sous-lot (8.1, 8.2…)", value=False)
    exclure_petits_6 = mo.ui.switch(label="Exclure les « Petit logement coll. » (baies RSET < 50 m²)", value=True)
    exclure_grands_6 = mo.ui.switch(label="Exclure les « Grand logement coll. » (baies RSET > 200 m²)", value=True)

    mo.vstack([
        mo.Html('<div class="pas-imprime">' + mo.md("### Paramètres du graphique 6").text + '</div>'),
        panneau_filtres(
            {"Graphique 6": mo.vstack([case_sous_lots_6, exclure_petits_6, exclure_grands_6])},
            bascule_en_evidence=choix_seuils_6,     # encadré visible sous la rangée du haut
        ),
    ])
    return case_sous_lots_6, choix_seuils_6, exclure_grands_6, exclure_petits_6


@app.cell(hide_code=True)
def composants_logements_collectifs(DATA_brut, USAGE_LOGEMENT_COLLECTIF, dropdown_usage, mo, pl):
    # ============================================================================
    # CELLULE — Lecture des COMPOSANTS (fiches) des logements collectifs, pour le
    # graphique 6. Source : fichier Parquet exporté de la base (script d'export,
    # une ligne par composant), publié dans le dépôt GitHub (dossier DATA).
    # Aucun appel à Turso : le fichier est lu une fois, puis réutilisé par le graphique.
    #
    # Pour changer de millésime d'export : modifier NOM_FICHIER ci-dessous.
    # ============================================================================

    # ---- Variables --------------------------------------------------------------
    NOM_FICHIER = "composants_logements_collectifs_2026-10-16.parquet"
    URL_DEPOT = f"https://raw.githubusercontent.com/Alliages/opee-python/main/DATA/{NOM_FICHIER}"
    CHEMIN_LOCAL = f"DATA/{NOM_FICHIER}"        # utilisé en priorité s'il existe (lancement local)

    mo.stop(
        dropdown_usage.value != USAGE_LOGEMENT_COLLECTIF,
        mo.md(f"**Graphique 6 : réservé aux logements collectifs** (l'usage choisi est « {dropdown_usage.value} »)."),
    )

    # ---- Lecture : fichier local s'il existe, sinon GitHub -----------------------
    from pathlib import Path as _Path
    _source = CHEMIN_LOCAL if _Path(CHEMIN_LOCAL).exists() else URL_DEPOT
    _composants = pl.read_parquet(_source, columns=[
        "projet_id", "batiment_index", "lot_ref", "sous_lot_ref", "type_donnees", "type_declaration",
    ])

    # ---- Réduction : une ligne par bâtiment x lot x sous-lot x type x déclaration --
    # (ID = même formule que la colonne "ID" de DATA_brut : projet_id_batiment_index,
    # batiment_index absent -> 0). Le classement en natures est fait dans le graphique.
    COMPOSANTS_LC = (
        _composants
        .with_columns(
            pl.concat_str(
                pl.col("projet_id").cast(pl.Utf8), pl.lit("_"),
                pl.col("batiment_index").fill_null(0).cast(pl.Utf8),
            ).alias("ID"),
        )
        .group_by("ID", "lot_ref", "sous_lot_ref", "type_donnees", "type_declaration")
        .agg(pl.len().alias("nb_fiches"))
    )
    print(f"Composants lus ({_source}) : {_composants.height} fiches, {COMPOSANTS_LC['ID'].n_unique()} bâtiments")
    return (COMPOSANTS_LC,)


@app.cell(hide_code=True)
def graphique_6(
    COMPOSANTS_LC,
    CONFIG_PLOTLY,
    DATA_brut,
    GRAPHIQUES,
    SOUS_TITRE_FILTRES,
    TRANCHES_LOGEMENT_COLLECTIF,
    appliquer_filtres,
    boutons_export,
    case_sous_lots_6,
    choix_seuils_6,
    dropdown_usage,
    exclure_grands_6,
    exclure_petits_6,
    go,
    mo,
    pl,
    valeurs_actives,
):
    # ============================================================================
    # GRAPHIQUE 6 — Nombre de fiches par lot RE2020 et par nature de fiche
    #
    # Barres horizontales empilées à 100 % : pour chaque lot (1 en haut, 13 en bas),
    # part de chaque nature de fiche dans le NOMBRE DE FICHES du lot. À droite de
    # chaque ligne : nombre moyen de fiches par bâtiment dans le lot.
    #
    # Fiches par bâtiment : on SOMME d'abord les fiches de chaque bâtiment dans le lot,
    # puis on fait la MOYENNE de ces sommes sur les bâtiments qui ont au moins une
    # fiche dans le lot. Le forfaitaire (conventionnelle) n'est PAS compté dans les DED.
    #
    # Sous le graphique, en gros chiffres, pour chaque macro-lot (gros œuvre, second
    # œuvre, lots techniques, mêmes groupes et couleurs que le graphique 3) : part des
    # FDES / PEP face aux DED + forfaitaire, en nombre de fiches.
    #
    # Bâtiments : ceux de DATA_brut passés par les filtres communs (comme le
    # graphique 5), puis par le filtre des seuils et sans les petits / grands
    # logements si les bascules sont actives.
    # Les fiches viennent du Parquet (cellule `composants_logements_collectifs`).
    # ============================================================================


    # ============================================================================
    # PARAMÈTRES (toutes les variables au même endroit)
    # ============================================================================

    _USAGE = dropdown_usage.value
    _PAR_SOUS_LOT = case_sous_lots_6.value
    _SEUILS_CHOISIS = valeurs_actives(choix_seuils_6)   # [] = tous cochés = pas de filtre
    _TEXTE_SEUILS = ", ".join(_SEUILS_CHOISIS) if _SEUILS_CHOISIS else "tous"
    _LOT_MIN, _LOT_MAX = 1, 13                  # lots conservés (les autres sont écartés)
    _LOT_MAX_FDES_CONFIGUREE = 7                # fiches configurées des lots 1 à 7 = FDES configurées
    _SEUIL_ETIQUETTE = 3                        # % : pas d'étiquette dans les segments plus fins
    _COULEUR_BORD = "rgba(137,135,129,0.5)"
    _COULEUR_TEXTE = "#898781"

    # Libellés des lots RE2020
    _LOTS = {
        1: "VRD, aménagements extérieurs",
        2: "Fondations, infrastructure",
        3: "Superstructure, maçonnerie",
        4: "Couverture, étanchéité, charpente",
        5: "Cloisonnement, plafonds suspendus",
        6: "Façades, menuiseries extérieures",
        7: "Revêtements, peintures",
        8: "Équipements de génie climatique (CVC)",
        9: "Installations sanitaires",
        10: "Réseaux d'énergie (courants forts)",
        11: "Réseaux de communication (courants faibles)",
        12: "Appareils élévateurs",
        13: "Production locale d'énergie",
    }

    # Natures de fiches, DANS L'ORDRE D'EMPILEMENT (gauche -> droite), avec leur couleur.
    # Familles : FDES (vert), PEP (bleu), DED (orange), forfaitaire et autres (gris).
    _NOM_FDES_CONFIGUREE = "FDES configurée"        # fiche configurée des lots 1 à 7
    _NOM_CONFIGUREE = "Fiche configurée"            # fiche configurée des lots 8 à 13
    _NOM_EXTRAPOLEE = "PEP extrapolée"
    _NOM_FORFAIT = "Forfaitaire (conventionnelle)"
    _NOM_AUTRES = "Autres (surtout réemploi et parfois vide)"
    _NATURES = {
        "FDES individuelle": "#55A868",
        _NOM_FDES_CONFIGUREE: "#55A868",            # hachuré vert / vert clair (cf. _MOTIFS)
        "FDES collective": "#A9D3B2",
        "FDES non précisée": "#DCEFE0",
        _NOM_CONFIGUREE: "#55A868",                 # hachuré vert / bleu (cf. _MOTIFS)
        "PEP individuelle": "#4C72B0",
        "PEP collective": "#A9BEDD",
        "PEP non précisée": "#DCE5F3",
        _NOM_EXTRAPOLEE: "#4C72B0",                 # hachuré bleu / blanc (cf. _MOTIFS)
        "DED": "#DD8452",
        _NOM_FORFAIT: "#8A8A8A",
        _NOM_AUTRES: "#CFCFCF",
    }
    # Natures tracées en hachures (motif Plotly : rayures fgcolor sur fond bgcolor)
    _MOTIFS = {
        _NOM_FDES_CONFIGUREE: {"shape": "/", "fgcolor": "#55A868", "bgcolor": "#A9D3B2", "size": 8, "solidity": 0.5},
        _NOM_CONFIGUREE: {"shape": "/", "fgcolor": "#55A868", "bgcolor": "#4C72B0", "size": 12, "solidity": 0.5},
        _NOM_EXTRAPOLEE: {"shape": "/", "fgcolor": "#4C72B0", "bgcolor": "white", "size": 6},
    }
    # Natures foncées : étiquette en blanc (les autres : étiquette sombre)
    _NATURES_TEXTE_BLANC = {"FDES individuelle", _NOM_CONFIGUREE, "PEP individuelle", "DED", _NOM_FORFAIT}
    _RANG_NATURE = {n: i for i, n in enumerate(_NATURES)}

    # --- Gros chiffres sous le graphique : macro-lots (groupes et couleurs du graphique 3)
    _MACRO_LOTS = {
        "Gros œuvre": {"lots": [2, 3], "texte_lots": "lots 2 et 3", "couleur": "#084594"},          # bleu
        "Second œuvre": {"lots": [4, 5, 6, 7], "texte_lots": "lots 4 à 7", "couleur": "#99000D"},   # rouge
        "Lots techniques": {"lots": list(range(8, 14)), "texte_lots": "lots 8 à 13", "couleur": "#0C562A"},  # vert
    }
    # Deux camps comparés (en nombre de fiches). Les « Autres » (réemploi, vide) ne sont
    # dans aucun des deux : ils sont retirés du dénominateur et signalés à part.
    _CAMP_FDES_PEP = [
        "FDES individuelle", "FDES collective", "FDES non précisée", _NOM_FDES_CONFIGUREE,
        _NOM_CONFIGUREE, "PEP individuelle", "PEP collective", "PEP non précisée", _NOM_EXTRAPOLEE,
    ]
    _CAMP_DED_FORFAIT = ["DED", _NOM_FORFAIT]
    _TAILLE_GROS_CHIFFRE = 46                   # px


    # ============================================================================
    # 1. BÂTIMENTS RETENUS : filtres communs, seuils, puis petits / grands logements
    # ============================================================================

    _df_bat = appliquer_filtres(DATA_brut)
    if _SEUILS_CHOISIS:                             # sélection partielle : seuils cochés seulement
        _df_bat = _df_bat.filter(pl.col("seuil").is_in(_SEUILS_CHOISIS))
        print(f"  après filtre seuils {_SEUILS_CHOISIS} : {_df_bat.height}")
    _tranches_exclues = (
        ([TRANCHES_LOGEMENT_COLLECTIF[0]] if exclure_petits_6.value else [])
        + ([TRANCHES_LOGEMENT_COLLECTIF[2]] if exclure_grands_6.value else [])
    )
    if _tranches_exclues:
        _avant = _df_bat.height
        _df_bat = _df_bat.filter(~pl.col("tranche_sref").is_in(_tranches_exclues))
        print(f"  {_tranches_exclues} exclus : {_avant - _df_bat.height}")
    _ids = _df_bat["ID"]

    # Fiches des bâtiments retenus, lots 1 à 13 uniquement
    _lot = pl.col("lot_ref").cast(pl.Int64, strict=False)
    _fiches = COMPOSANTS_LC.filter(pl.col("ID").is_in(_ids) & _lot.is_between(_LOT_MIN, _LOT_MAX))

    mo.stop(
        _fiches.height == 0,
        mo.md("**Aucune fiche ne correspond aux filtres choisis.**"),
    )


    # ============================================================================
    # 2. CLASSEMENT DE CHAQUE LIGNE DANS UNE NATURE
    #    (type_donnees normalisé : majuscules, espaces -> « _ »)
    # ============================================================================

    _type = (pl.col("type_donnees").cast(pl.Utf8).fill_null("")
             .str.strip_chars().str.to_uppercase().str.replace_all(" ", "_"))
    _decl = pl.col("type_declaration").cast(pl.Utf8).fill_null("").str.strip_chars().str.to_lowercase()
    _precision = (
        pl.when(_decl == "individuelle").then(pl.lit("individuelle"))
        .when(_decl == "collective").then(pl.lit("collective"))
        .otherwise(pl.lit("non précisée"))
    )
    _nature = (
        pl.when(_type.is_in(["FDES", "PEP"])).then(pl.concat_str(_type, pl.lit(" "), _precision))
        .when((_type == "FICHE_CONFIGUREE") & (_lot <= _LOT_MAX_FDES_CONFIGUREE)).then(pl.lit(_NOM_FDES_CONFIGUREE))
        .when(_type == "FICHE_CONFIGUREE").then(pl.lit(_NOM_CONFIGUREE))
        .when(_type == "PEP_EXTRAPOLEE").then(pl.lit(_NOM_EXTRAPOLEE))
        .when(_type == "DED").then(pl.lit("DED"))
        .when(_type == "CONVENTIONNELLE").then(pl.lit(_NOM_FORFAIT))
        .otherwise(pl.lit(_NOM_AUTRES))             # réemploi, composant vide, valeur inconnue
    )

    # Ligne du graphique : le lot, ou le sous-lot (« Sous-lot 8.1 ») ; `ordre` sert au tri
    if _PAR_SOUS_LOT:
        _groupe = pl.format("Sous-lot {}.{}", _lot, pl.col("sous_lot_ref").cast(pl.Utf8).fill_null("?"))
        _ordre = _lot * 100 + pl.col("sous_lot_ref").cast(pl.Int64, strict=False).fill_null(99)
    else:
        _groupe = _lot.replace_strict({k: f"Lot {k} – {v}" for k, v in _LOTS.items()}, return_dtype=pl.Utf8)
        _ordre = _lot * 100

    _f = _fiches.select(
        "ID", _lot.alias("lot"), pl.col("sous_lot_ref").cast(pl.Int64, strict=False).alias("sous_lot"),
        _nature.alias("nature"), _groupe.alias("groupe"), _ordre.alias("ordre"), "nb_fiches",
    )


    # ============================================================================
    # 3. AGRÉGATION
    # ============================================================================

    # Fiches par bâtiment et par ligne -> moyenne, médiane, nombre de bâtiments
    _par_batiment = _f.group_by("ID", "ordre", "groupe").agg(pl.col("nb_fiches").sum().alias("n"))
    _nb_batiments_total = _f["ID"].n_unique()       # bâtiments retenus ayant au moins une fiche
    _stats_groupe = _par_batiment.group_by("ordre", "groupe").agg(
        pl.col("n").mean().alias("moyenne_fiches_par_batiment"),
        pl.col("n").median().alias("mediane_fiches_par_batiment"),
        (pl.col("n").sum() / _nb_batiments_total).alias("moyenne_fiches_tous_batiments"),
        pl.len().alias("nb_batiments"),
    )

    # Grille complète ligne x nature (0 si aucune fiche), pour un export sans trou
    _grille = _stats_groupe.select("ordre", "groupe").join(pl.DataFrame({"nature": list(_NATURES)}), how="cross")
    _comptes = _f.group_by("ordre", "groupe", "nature").agg(pl.col("nb_fiches").sum())
    _valeurs = (
        _grille.join(_comptes, on=["ordre", "groupe", "nature"], how="left")
        .with_columns(pl.col("nb_fiches").fill_null(0))
        .with_columns(
            pl.col("nb_fiches").sum().over("ordre").alias("nb_fiches_groupe"),
            (pl.col("nb_fiches") / pl.col("nb_fiches").sum().over("ordre") * 100).alias("part_pct"),
        )
        # Part de DED strict (le forfaitaire n'y est pas compté), répétée sur chaque ligne
        .with_columns(
            pl.when(pl.col("nature") == "DED").then(pl.col("part_pct")).otherwise(0.0)
            .sum().over("ordre").alias("part_ded_pct")
        )
        .join(_stats_groupe.drop("groupe"), on="ordre")
        .with_columns(pl.col("nature").replace_strict(_RANG_NATURE, return_dtype=pl.Int64).alias("rang_nature"))
        .sort("ordre", "rang_nature")
        .select("groupe", "nature", "nb_fiches", "part_pct", "part_ded_pct",
                "nb_fiches_groupe", "nb_batiments", "moyenne_fiches_par_batiment",
                "mediane_fiches_par_batiment", "moyenne_fiches_tous_batiments")
    )

    # Détail par bâtiment (niveau sous-lot) : base d'analyses complémentaires
    _detail = (
        _f.group_by("ID", "lot", "sous_lot", "nature").agg(pl.col("nb_fiches").sum())
        .sort("ID", "lot", "sous_lot", "nature", nulls_last=True)
    )

    # Macro-lots : fiches FDES / PEP face aux DED + forfaitaire (en nombre de fiches).
    # Part = fiches du camp / (FDES-PEP + DED-forfait) ; les « Autres » sont hors calcul.
    _camp = (
        pl.when(pl.col("nature").is_in(_CAMP_FDES_PEP)).then(pl.lit("fdes_pep"))
        .when(pl.col("nature").is_in(_CAMP_DED_FORFAIT)).then(pl.lit("ded_forfait"))
        .otherwise(pl.lit("autres"))
    )
    def _part(valeur, base):
        """Part en % (None si la base est vide)."""
        return valeur / base * 100 if base else None

    _lignes_macro = []
    for _nom_macro, _macro in _MACRO_LOTS.items():
        _sous_total = (
            _f.filter(pl.col("lot").is_in(_macro["lots"]))
            .with_columns(_camp.alias("camp"))
        )
        _n = {
            "fdes_pep": int(_sous_total.filter(pl.col("camp") == "fdes_pep")["nb_fiches"].sum()),
            "ded": int(_sous_total.filter(pl.col("nature") == "DED")["nb_fiches"].sum()),
            "forfait": int(_sous_total.filter(pl.col("nature") == _NOM_FORFAIT)["nb_fiches"].sum()),
            "autres": int(_sous_total.filter(pl.col("camp") == "autres")["nb_fiches"].sum()),
        }
        _base = _n["fdes_pep"] + _n["ded"] + _n["forfait"]
        _lignes_macro.append({
            "macro_lot": _nom_macro, "lots": _macro["texte_lots"],
            "nb_fiches_fdes_pep": _n["fdes_pep"], "nb_fiches_ded": _n["ded"],
            "nb_fiches_forfaitaire": _n["forfait"], "nb_fiches_autres_hors_calcul": _n["autres"],
            "part_fdes_pep_pct": _part(_n["fdes_pep"], _base),
            "part_ded_forfait_pct": _part(_n["ded"] + _n["forfait"], _base),
            "part_ded_pct": _part(_n["ded"], _base), "part_forfait_pct": _part(_n["forfait"], _base),
            "nb_batiments": _sous_total["ID"].n_unique(),
        })
    _parts_macro = pl.DataFrame(_lignes_macro)


    # ============================================================================
    # 4. GRAPHIQUE
    # ============================================================================

    _lignes = _valeurs.select("groupe", "moyenne_fiches_par_batiment").unique(maintain_order=True)
    _fig = go.Figure()
    for _nom, _couleur in _NATURES.items():
        _d = _valeurs.filter(pl.col("nature") == _nom)
        if _d["nb_fiches"].sum() == 0:
            continue                                # nature absente : pas de légende vide
        _marque = {"color": _couleur, "line": {"color": _COULEUR_BORD, "width": 0.5}}
        if _nom in _MOTIFS:
            _marque["pattern"] = _MOTIFS[_nom]
        # Étiquette « x % » dans chaque segment d'au moins _SEUIL_ETIQUETTE %
        _textes = [f"{p:.0f} %" if p >= _SEUIL_ETIQUETTE else "" for p in _d["part_pct"]]
        _fig.add_trace(go.Bar(
            name=_nom, y=_d["groupe"], x=_d["part_pct"], orientation="h",
            marker=_marque, text=_textes, textposition="inside", insidetextanchor="middle",
            textfont={"color": "white" if _nom in _NATURES_TEXTE_BLANC else "#1f1f1f", "size": 12},
            customdata=_d["nb_fiches"],
            hovertemplate=f"<b>%{{y}}</b><br>{_nom} : %{{x:.1f}} % (%{{customdata}} fiches)<extra></extra>",
        ))

    # À droite de chaque ligne : nombre moyen de fiches par bâtiment
    for _g, _moy in _lignes.iter_rows():
        _fig.add_annotation(x=1, xref="paper", y=_g, yref="y", text=f"{_moy:.1f}".replace(".", ","),
                            showarrow=False, xanchor="left", xshift=12,
                            font={"size": 12, "color": _COULEUR_TEXTE})
    _fig.add_annotation(x=1, xref="paper", y=1, yref="paper", text="Fiches moy.<br>par bât.",
                        showarrow=False, xanchor="left", yanchor="bottom", xshift=4,
                        font={"size": 11, "color": _COULEUR_TEXTE})
    _fig.update_layout(
        template="plotly_white", barmode="stack", bargap=0.35, height=max(460, 34 * _lignes.height + 260),
        title=dict(
            text=f"<b>Graphique 6 — {GRAPHIQUES[6]} — {_USAGE}</b><br>"
                 f"<sup>{_nb_batiments_total} bâtiments ayant des fiches, {int(_f['nb_fiches'].sum())} fiches"
                 f" — Seuils IC construction : {_TEXTE_SEUILS}</sup><br>"
                 f"<sup>{SOUS_TITRE_FILTRES}</sup>",
            font=dict(size=20),
        ),
        margin={"l": 10, "r": 90, "t": 130, "b": 20},
        uniformtext={"minsize": 9, "mode": "show"},     # garde les petites étiquettes (>= 3 %)
        xaxis={"range": [0, 100], "title": "% du nombre de fiches"},
        yaxis={"autorange": "reversed", "categoryorder": "array", "categoryarray": _lignes["groupe"].to_list()},
        legend={"orientation": "h", "y": -0.12, "traceorder": "normal"},
    )

    _graphique = mo.ui.plotly(_fig, config=CONFIG_PLOTLY)


    # ============================================================================
    # 5. GROS CHIFFRES SOUS LE GRAPHIQUE : FDES / PEP face aux DED + forfaitaire
    # ============================================================================

    def _fr(valeur, decimales=0):
        """Nombre à la française (espace des milliers, virgule décimale)."""
        return f"{valeur:,.{decimales}f}".replace(",", " ").replace(".", ",")

    _cartes = []
    for _ligne in _parts_macro.iter_rows(named=True):
        _couleur = _MACRO_LOTS[_ligne["macro_lot"]]["couleur"]
        if _ligne["part_fdes_pep_pct"] is None:     # aucune fiche FDES / PEP / DED / forfait
            _corps = '<div style="color:#898781;margin-top:18px;">aucune fiche</div>'
        else:
            _corps = f"""
              <div style="font-size:{_TAILLE_GROS_CHIFFRE}px;font-weight:800;color:{_couleur};line-height:1.1;margin-top:6px;">
                {_fr(_ligne['part_fdes_pep_pct'])} %</div>
              <div style="font-size:13px;color:{_couleur};font-weight:600;">FDES / PEP</div>
              <div style="font-size:22px;font-weight:700;color:#555;margin-top:8px;">
                vs {_fr(_ligne['part_ded_forfait_pct'])} %</div>
              <div style="font-size:13px;color:#555;">DED + forfaitaire</div>
              <div style="font-size:12px;color:#898781;margin-top:6px;">
                DED {_fr(_ligne['part_ded_pct'])} % · forfaitaire {_fr(_ligne['part_forfait_pct'])} %</div>"""
        _cartes.append(f"""
            <div style="flex:1 1 180px;border:1px solid #e3e3e3;border-top:5px solid {_couleur};
                        border-radius:8px;padding:12px 14px;text-align:center;">
              <div style="font-size:17px;font-weight:700;color:{_couleur};">{_ligne['macro_lot']}</div>
              <div style="font-size:12px;color:#898781;">{_ligne['lots']}</div>
              {_corps}
              <div style="font-size:11px;color:#898781;margin-top:8px;">
                {_fr(_ligne['nb_fiches_fdes_pep'] + _ligne['nb_fiches_ded'] + _ligne['nb_fiches_forfaitaire'])} fiches ·
                {_fr(_ligne['nb_batiments'])} bâtiments</div>
            </div>""")
    _gros_chiffres = mo.Html(f"""
        <div style="margin:4px 0 8px 0;">
          <div style="font-size:15px;font-weight:700;margin-bottom:8px;">
            Part des FDES / PEP face aux DED et au forfaitaire, par macro-lot (en nombre de fiches)</div>
          <div style="display:flex;gap:14px;flex-wrap:wrap;">{''.join(_cartes)}</div>
          <div style="font-size:11px;color:#898781;margin-top:6px;">
            FDES / PEP : individuelles, collectives, non précisées, configurées et PEP extrapolées.
            Lot 1 (VRD) non compté, comme au graphique 3 ; réemploi et composants vides hors calcul.</div>
        </div>""")

    mo.vstack([
        _graphique,
        _gros_chiffres,
        mo.Html('<div class="pas-imprime">' + mo.md("**Valeurs du graphique**").text + '</div>'),
        boutons_export(_valeurs, "graphique_6_nature_fiches_par_lot"),
        mo.Html('<div class="pas-imprime">' + mo.md("**Parts FDES / PEP et DED + forfaitaire par macro-lot**").text + '</div>'),
        boutons_export(_parts_macro, "graphique_6_parts_par_macro_lot"),
        mo.Html('<div class="pas-imprime">' + mo.md("**Détail par bâtiment, lot, sous-lot et nature**").text + '</div>'),
        boutons_export(_detail, "graphique_6_detail_par_batiment"),
    ])
    return


@app.cell(hide_code=True)
def resume_filtres_graphique_6(
    choix_seuils_6,
    exclure_grands_6,
    exclure_petits_6,
    resume_filtres,
    valeurs_actives,
):
    # Résumé des filtres actifs du graphique 6, placé SOUS le graphique (cellule
    # séparée : il lit les valeurs des widgets, alors que le panneau reste statique).
    # Dernière ligne : filtres propres au graphique 6 (seuils, petits / grands logements).
    _SEUILS = valeurs_actives(choix_seuils_6)
    _EXCLUS = (["petits"] if exclure_petits_6.value else []) + (["grands"] if exclure_grands_6.value else [])

    resume_filtres(parametres_graphique={"Graphique 6": [
        f"seuils {', '.join(_SEUILS) if _SEUILS else 'tous'}",
        f"logements {' et '.join(_EXCLUS)} exclus" if _EXCLUS else "tous logements (petits et grands inclus)",
    ]})
    return


@app.cell(hide_code=True)
def saut_page_7(mo):
    # Saut de page à l'impression avant le graphique 7 (aucun effet à l'écran ;
    # règle `.saut-page` dans la cellule `style_impression`).
    mo.Html('<div class="saut-page"></div>')
    return


@app.cell(hide_code=True)
def param_graphique_7(mo, panneau_filtres):
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
        mo.Html('<div class="pas-imprime">' + mo.md("### Paramètres du graphique 7").text + '</div>'),
        panneau_filtres({"Graphique 7": choix_seuil}),
    ])
    return (choix_seuil,)



@app.cell(hide_code=True)
def graphique_7(
    CONFIG_PLOTLY,
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
    # GRAPHIQUE 6 — Écart des bâtiments aux différents seuils (en %)
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
                f"<span style='font-size:16px'>Graphique 7 — {GRAPHIQUES[7]} — {_USAGE}</span><br>"
                f"<sup>{SOUS_TITRE_FILTRES}</sup>"
            ),
        ),
        margin=dict(t=140, b=40, l=60, r=20),
    )

    _graphique = mo.ui.plotly(_fig, config=CONFIG_PLOTLY)

    # Export : les données TRACÉES (un point par bâtiment et par indicateur :
    # écart au seuil en %, avec l'ID du bâtiment)
    mo.vstack([_graphique, boutons_export(pl.concat(_points_export), "graphique_7_ecarts_aux_seuils")])
    return


@app.cell(hide_code=True)
def resume_filtres_graphique_7(resume_filtres):
    # Résumé des filtres actifs du graphique 7, placé SOUS le graphique (cellule
    # séparée : il lit les valeurs des widgets, alors que le panneau reste statique).
    resume_filtres()
    return


@app.cell(hide_code=True)
def saut_page_8(mo):
    # Saut de page à l'impression avant le graphique 8 (aucun effet à l'écran ;
    # règle `.saut-page` dans la cellule `style_impression`).
    mo.Html('<div class="saut-page"></div>')
    return


@app.cell(hide_code=True)
def param_graphique_8(mo, panneau_filtres):
    # ============================================================================
    # CELLULE WIDGET — paramètres propres au graphique 8 (stock C) :
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
        mo.Html('<div class="pas-imprime">' + mo.md("### Paramètres du graphique 8").text + '</div>'),
        panneau_filtres(
            {"Graphique 8": mo.vstack([choix_seuil_stock_c, choix_y_max_stock_c])},
            avec_materiau=False,
        ),
    ])
    return choix_seuil_stock_c, choix_y_max_stock_c



@app.cell(hide_code=True)
def graphique_8(
    CONFIG_PLOTLY,
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
    # GRAPHIQUE 7 — Stock de carbone (stock_c) par type de matériau de structure
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
    # Sous-titre expliquant le regroupement « Bas Carbone » (cf. MAPPING_MATERIAU)
    _SOUS_TITRE_BAS_CARBONE = "Les bâtiments dont la structure est en bois, pierre ou terre crue sont « bas carbone »"

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
                f"<b>Graphique 8 — {GRAPHIQUES[8]} — {_USAGE}</b><br>"
                f"<sup>{_SOUS_TITRE_BAS_CARBONE}</sup><br>"
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
        margin=dict(t=195, b=100, l=60, r=20),
    )

    _graphique = mo.ui.plotly(_fig, config=CONFIG_PLOTLY)

    # Export : statistiques de chaque boîte (toutes les combinaisons, avec un
    # indicateur `boite_affichee` pour celles masquées faute d'effectif)
    mo.vstack([_graphique, boutons_export(_agg, "graphique_8_stock_c_par_materiau_et_seuil")])
    return


@app.cell(hide_code=True)
def resume_filtres_graphique_8(resume_filtres):
    # Résumé des filtres actifs du graphique 8, placé SOUS le graphique (cellule
    # séparée : il lit les valeurs des widgets, alors que le panneau reste statique).
    resume_filtres(avec_materiau=False)
    return


@app.cell(hide_code=True)
def saut_page_9(mo):
    # Saut de page à l'impression avant le graphique 9 (aucun effet à l'écran ;
    # règle `.saut-page` dans la cellule `style_impression`).
    mo.Html('<div class="saut-page"></div>')
    return


@app.cell(hide_code=True)
def param_graphique_9(mo, panneau_filtres):
    # ============================================================================
    # CELLULE WIDGET — paramètres propres au graphique 9 (éloignement au seuil
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
        mo.Html('<div class="pas-imprime">' + mo.md("### Paramètres du graphique 9").text + '</div>'),
        panneau_filtres(
            {"Graphique 9": mo.vstack([choix_ecart_max_2028, choix_variable_categorielle_7])},
            avec_materiau=False, avec_inconnus=False,
            bascules_graphique=[cacher_autre_7],       # rangée du haut, avec « Valider… »
        ),
    ])
    return cacher_autre_7, choix_ecart_max_2028, choix_variable_categorielle_7



@app.cell(hide_code=True)
def groupes_graphique_9(
    DATA_brut,
    SREF_MAX_SLIDER,
    TRANCHES_LOGEMENT_COLLECTIF,
    USAGE_LOGEMENT_COLLECTIF,
    appliquer_filtres,
    choix_ecart_max_2028,
    dropdown_usage,
    mo,
    pl,
):
    # ============================================================================
    # CELLULE — Constitution des 2 groupes du graphique 9 (aucun appel réseau)
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
    _TRANCHE_EXCLUE = TRANCHES_LOGEMENT_COLLECTIF[0]        # "Petit logement coll." : retiré des 2 groupes

    NOMS_GROUPES_7 = [
        f"Groupe 1 : conforme ou ≤ {_ECART_MAX} au-dessus du seuil 2028",
        f"Groupe 2 : > {_ECART_MAX} au-dessus du seuil 2028",
    ]

    # Indicateurs numériques comparés : colonne -> (libellé, unité)
    INDICATEURS_NUM_7 = {
        "nb_total_fiche_acv": ("Nombre total de fiches ACV", "fiches"),
        "nb_fdes": ("Nombre de FDES", "fiches"),
        "nb_ded": ("Nombre de DED", "fiches"),
        "ic_lots_3_4_6": ("IC composant lots 3 + 4 + 6", "kgeq.CO2/m²"),
        "ic_ded": ("IC DED (DED + valeurs forfaitaires)", "kgeq.CO2/m²"),
        "ic_composant_lot_8": ("IC composant lot 8 (CVC)", "kgeq.CO2/m²"),
        "ratio_baies_sref": ("Surface de baies / sref", "m²/m²"),
        "ratio_baies_murs_sref": ("(Baies + murs) / sref", "m²/m²"),
        "stock_c": ("Stock de carbone", "kg C/m²"),
    }


    # ============================================================================
    # 1. LOGEMENTS COLLECTIFS UNIQUEMENT
    # ============================================================================

    mo.stop(
        _USAGE != USAGE_LOGEMENT_COLLECTIF,
        mo.md(f"**Graphique 9 : réservé aux logements collectifs** (l'usage choisi est « {_USAGE} »)."),
    )


    # ============================================================================
    # 2. FILTRAGE (le matériau est comparé, donc non filtré ; « Inconnu » concerne le
    #    seuil atteint, sans rapport avec l'écart au seuil 2028)
    # ============================================================================

    _df = appliquer_filtres(DATA_brut, filtre_materiau=False, filtre_inconnu=False)

    # Les « Petit logement coll. » (surface_baies_rset < 50 m², cf. `tranche_sref`) sont
    # exclus des deux groupes, quel que soit le filtre de surface choisi.
    _avant_tranche = _df.height
    _df = _df.filter(pl.col("tranche_sref") != _TRANCHE_EXCLUE)
    print(f"  « {_TRANCHE_EXCLUE} » exclus : {_avant_tranche - _df.height}")

    # Colonnes numériques lues en flottants (valeurs absentes -> NULL)
    _cols_num = [
        _COL_IC, _COL_SEUIL_2028, "sref", "surface_baies_rset", "surface_murs_rset",
        "nb_total_fiche_acv", "nb_fdes", "nb_ded", "stock_c", "ic_ded", "ic_composant_lot_8",
        *_LOTS_SOMMES,
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
def graphique_9_numerique(
    DATA_groupes_7,
    CONFIG_PLOTLY,
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
    # GRAPHIQUE 9 (partie numérique) — Q1 / médiane / Q3 de chaque indicateur, pour
    # les groupes 1a, 1b et 2, un panneau par indicateur (échelles indépendantes).
    # Le groupe 1 est scindé selon l'année de dépôt du permis (la plus ancienne du projet,
    # comme au graphique 7) : 1a = 2022-2023, 1b = 2024-2025. Les bâtiments du groupe 1
    # déposés une autre année n'apparaissent dans aucun des deux sous-groupes.
    # Point = médiane ; barre d'erreur = de Q1 à Q3 (même lecture que le graphique 5).
    # ============================================================================

    from plotly.subplots import make_subplots as _make_subplots


    # ============================================================================
    # PARAMÈTRES
    # ============================================================================

    _USAGE = dropdown_usage.value
    _ANNEES_1A = [2022, 2023]                      # groupe 1a : années de dépôt du permis
    _ANNEES_1B = [2024, 2025]                      # groupe 1b
    # (libellé court de l'axe, libellé complet de la légende, couleur) : 1a, 1b, puis 2
    _GROUPES = [
        ("Groupe 1a", f"{NOMS_GROUPES_7[0]} — dépôt {_ANNEES_1A[0]}-{_ANNEES_1A[-1]}", "#79A757"),   # vert
        ("Groupe 1b", f"{NOMS_GROUPES_7[0]} — dépôt {_ANNEES_1B[0]}-{_ANNEES_1B[-1]}", "#B5D69C"),   # vert clair
        ("Groupe 2", NOMS_GROUPES_7[1], "#A26E2E"),                                                 # brun
    ]
    _NB_COLONNES = 3
    _NB_MIN_PAR_GROUPE = 5          # en dessous, le groupe n'est pas tracé pour cet indicateur
    _HAUTEUR_PAR_LIGNE = 330
    _TAILLE_TITRE_GRAPHIQUE = 20


    # ============================================================================
    # 0. SOUS-GROUPES 1a / 1b (année de dépôt la plus ancienne du projet)
    # ============================================================================

    _annee = pl.col("annees_depot_pc").list.min()
    _df = DATA_groupes_7.with_columns(
        pl.when(pl.col("groupe") == NOMS_GROUPES_7[1]).then(pl.lit(_GROUPES[2][1]))
        .when((pl.col("groupe") == NOMS_GROUPES_7[0]) & _annee.is_in(_ANNEES_1A)).then(pl.lit(_GROUPES[0][1]))
        .when((pl.col("groupe") == NOMS_GROUPES_7[0]) & _annee.is_in(_ANNEES_1B)).then(pl.lit(_GROUPES[1][1]))
        .alias("sous_groupe")      # NULL = groupe 1 déposé une autre année : écarté ici
    )
    _nb_ecartes = _df.filter(pl.col("sous_groupe").is_null()).height
    _df = _df.filter(pl.col("sous_groupe").is_not_null())
    print(f"  groupe 1 hors {_ANNEES_1A + _ANNEES_1B} (écartés du graphique) : {_nb_ecartes}")


    # ============================================================================
    # 1. STATISTIQUES PAR (indicateur, groupe)
    # ============================================================================

    _lignes_stats = []
    for _col, (_libelle, _unite) in INDICATEURS_NUM_7.items():
        for _court, _groupe, _couleur in _GROUPES:
            _v = _df.filter(pl.col("sous_groupe") == _groupe)[_col].drop_nulls()
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
        for _court, _groupe, _couleur in _GROUPES:
            _s = _stats.filter((pl.col("indicateur") == _col) & (pl.col("groupe") == _groupe)).row(0, named=True)
            if not _s["trace"]:
                continue
            _fig.add_trace(
                go.Scatter(
                    x=[f"{_court}<br>n = {_s['n']}"],
                    y=[_s["mediane"]],
                    mode="markers",
                    marker=dict(size=12, color=_couleur, line=dict(color="black", width=1)),
                    error_y=dict(
                        type="data", symmetric=False, thickness=3, width=12, color=_couleur,
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
                f"<b>Graphique 9 — {GRAPHIQUES[9]} — {_USAGE}</b><br>"
                f"<sup>Point = médiane ; barre = de Q1 à Q3 ; groupe 1 scindé par année de dépôt du permis (1a : {_ANNEES_1A[0]}-{_ANNEES_1A[-1]}, 1b : {_ANNEES_1B[0]}-{_ANNEES_1B[-1]})</sup><br>"
                f"<sup>{SOUS_TITRE_SANS_MATERIAU}</sup>"
            ),
            font=dict(size=_TAILLE_TITRE_GRAPHIQUE),
        ),
        legend=dict(orientation="h", x=0.5, xanchor="center", y=-0.08, yanchor="top"),
        margin=dict(t=170, b=100, l=60, r=20),
    )

    _graphique = mo.ui.plotly(_fig, config=CONFIG_PLOTLY)

    # Export : statistiques de chaque (indicateur, groupe), avec l'indicateur `trace`
    mo.vstack([_graphique, boutons_export(_stats, "graphique_9_stats_par_groupe")])
    return


@app.cell(hide_code=True)
def graphique_9_categoriel(
    DATA_groupes_7,
    CONFIG_PLOTLY,
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
    # GRAPHIQUE 9 (partie catégorielle) — Répartition (%) d'une variable catégorielle
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
                f"<b>Graphique 9 — {GRAPHIQUES[9]} — {_USAGE}</b><br>"
                f"<sup>Répartition : {_LIBELLE_VARIABLE}{_note_masque}</sup><br>"
                f"<sup>{SOUS_TITRE_SANS_MATERIAU}</sup>"
            ),
            font=dict(size=_TAILLE_TITRE_GRAPHIQUE),
        ),
        yaxis=dict(title="Part du groupe (%)", range=[0, 100]),
        legend=dict(title=_LIBELLE_VARIABLE, orientation="v"),
        margin=dict(t=170, b=80, l=60, r=20),
    )

    _graphique = mo.ui.plotly(_fig, config=CONFIG_PLOTLY)

    # Export : effectif et part de chaque modalité dans chaque groupe
    mo.vstack([_graphique, boutons_export(_agg.sort("groupe", "n", descending=[False, True]), "graphique_9_repartition_categorielle")])
    return


@app.cell(hide_code=True)
def resume_filtres_graphique_9(resume_filtres):
    # Résumé des filtres actifs du graphique 9, placé SOUS le graphique (cellule
    # séparée : il lit les valeurs des widgets, alors que le panneau reste statique).
    resume_filtres(avec_materiau=False, avec_inconnus=False)
    return


@app.cell(hide_code=True)
def saut_page_10(mo):
    # Saut de page à l'impression avant le graphique 10 (aucun effet à l'écran ;
    # règle `.saut-page` dans la cellule `style_impression`).
    mo.Html('<div class="saut-page"></div>')
    return


@app.cell(hide_code=True)
def param_graphique_10(mo, panneau_filtres):
    # ============================================================================
    # CELLULE WIDGET — paramètres propres au graphique 10 :
    #   - unité du graphique : la ZONE du bâtiment (une valeur par zone, comme en
    #     base) ou le BÂTIMENT (dh_batiment = DH de sa zone la plus défavorable) ;
    #   - zoom sur l'axe Y (borne haute, en °C·h). Valeurs proposées : 350, puis de
    #     100 en 100 de 400 à 2500 (une grille 350, 450, ... ne contiendrait pas 1500).
    # Affichés sous le panneau de filtres, hors accordéon (donc toujours visibles).
    # ============================================================================

    # ---- Variables ----------------------------------------------------------
    UNITES_DH = ["Zone du bâtiment", "Bâtiment"]
    UNITE_DH_DEFAUT = "Zone du bâtiment"
    Y_MAX_DH_MIN = 350
    Y_MAX_DH_MAX = 2500
    Y_MAX_DH_PAS = 100
    Y_MAX_DH_DEFAUT = 1500

    choix_unite_dh = mo.ui.radio(
        options=UNITES_DH, value=UNITE_DH_DEFAUT, inline=True,
        label="**Unité du graphique**",
    )
    choix_y_max_dh = mo.ui.slider(
        steps=[Y_MAX_DH_MIN] + list(range(400, Y_MAX_DH_MAX + 1, Y_MAX_DH_PAS)),
        value=Y_MAX_DH_DEFAUT, show_value=True, full_width=True,
        label="Zoom Axe Y : maximum du DH affiché (graphique 10)",
    )

    mo.vstack([
        mo.Html('<div class="pas-imprime">' + mo.md("### Paramètres du graphique 10").text + '</div>'),
        panneau_filtres(),
        choix_unite_dh,
        choix_y_max_dh,
    ])
    return choix_unite_dh, choix_y_max_dh


@app.cell(hide_code=True)
def graphique_10(
    CONFIG_PLOTLY,
    DATA_brut,
    SOUS_TITRE_FILTRES,
    appliquer_filtres,
    boutons_export,
    choix_unite_dh,
    choix_y_max_dh,
    dropdown_usage,
    go,
    mo,
    pl,
):
    # ============================================================================
    # GRAPHIQUE 10 — Dispersion du DH (degrés-heures) par zone climatique.
    # Une boîte à moustaches et les points individuels par zone climatique.
    #
    # Deux unités au choix (paramètre « Unité du graphique ») :
    #   - « Zone du bâtiment » : une valeur par ZONE (un bâtiment a 1 à n zones,
    #     listes `dh_zones`, `is_traversant_zones`, `dh_max_zones`, triées par n° de
    #     zone), séparée en zones traversantes / non traversantes ;
    #   - « Bâtiment » : une valeur par BÂTIMENT, `dh_batiment` (= le plus grand des
    #     DH de ses zones, celui comparé à `dh_max`), sans séparation traversant /
    #     non traversant (un bâtiment peut mélanger les deux).
    #
    # Exports :
    #   - zone : statistiques par (zone climatique, traversante ou non) ;
    #   - bâtiment : Q1 / médiane / Q3 par zone climatique (8 zones x 3 valeurs) ;
    #   - dans les deux cas, export brut : une ligne par point tracé.
    # ============================================================================


    # ============================================================================
    # PARAMÈTRES
    # ============================================================================

    _USAGE = dropdown_usage.value
    _PAR_BATIMENT = choix_unite_dh.value == "Bâtiment"
    _Y_MAX = choix_y_max_dh.value   # borne haute de l'axe Y (°C·h) ; les valeurs au-delà sont coupées

    # Valeurs écartées (données aberrantes) :
    #   - DH nul (0) : zone non utilisée ;
    #   - DH ou DH max supérieur à _DH_ABERRANT : un DH au-delà écarte le point, un DH max
    #     au-delà est ignoré (le point reste tracé, sans compter pour l'affichage « DHmax »)
    _DH_NUL = 0
    _DH_ABERRANT = 15000

    # Ordre d'affichage des zones climatiques (les autres valeurs, s'il y en a,
    # sont ajoutées à la fin par ordre alphabétique)
    _ORDRE_ZONES_CLIMATIQUES = ["H1a", "H1b", "H1c", "H2a", "H2b", "H2c", "H2d", "H3"]

    # Groupes tracés : libellé -> (couleur, décalage en x)
    _GROUPES_ZONE = {
        "Traversante": ("#2A7F62", -0.2),
        "Non traversante": ("#D9822B", 0.2),
    }
    _GROUPES_BATIMENT = {
        "Bâtiment": ("#3D5A80", 0.0),
    }
    _LARGEUR_BOITE_ZONE = 0.32      # largeur d'une boîte (unités de l'axe x : 1 = écart entre zones climatiques)
    _LARGEUR_BOITE_BATIMENT = 0.5
    _NB_MIN_PAR_BOITE = 5           # une boîte de moins de 5 points n'est pas tracée (les points le sont)

    # Repères réglementaires (DH)
    _DH_MAX_REGLEMENTAIRE = 1250
    _COULEUR_DH_MAX = "#C0392B"
    _DH_SEUIL_BAS = 350
    _COULEUR_SEUIL_BAS = "#888888"

    _TAILLE_TITRE_GRAPHIQUE = 20

    # Textes et réglages qui dépendent de l'unité choisie
    _GROUPES = _GROUPES_BATIMENT if _PAR_BATIMENT else _GROUPES_ZONE
    _LARGEUR_BOITE = _LARGEUR_BOITE_BATIMENT if _PAR_BATIMENT else _LARGEUR_BOITE_ZONE
    _UNITE = "bâtiment" if _PAR_BATIMENT else "zone"
    _UNITES = "bâtiments" if _PAR_BATIMENT else "zones"
    _ECARTES = "écartés" if _PAR_BATIMENT else "écartées"
    _TITRE = ("Dispersion du DH par zone climatique, par bâtiment" if _PAR_BATIMENT
              else "Dispersion du DH par zone climatique, zones traversantes et non traversantes")


    # ============================================================================
    # 1. FILTRAGE (filtres communs, sur les bâtiments) PUIS UNE LIGNE PAR POINT
    #    Colonnes communes aux deux unités : ID, zone_climatique, groupe,
    #    n_zone (zone seulement), dh, dh_max (limite réglementaire)
    # ============================================================================

    _df = appliquer_filtres(DATA_brut)

    mo.stop(_df.height == 0, mo.md("**Aucun bâtiment ne correspond aux filtres choisis.**"))

    if _PAR_BATIMENT:
        # --- Une ligne par bâtiment : dh_batiment et dh_max du bâtiment ------------
        _points = (
            _df.filter(pl.col("zone_climatique").is_not_null())
            .select(
                "ID", "zone_climatique",
                pl.lit("Bâtiment").alias("groupe"),
                pl.lit(None, dtype=pl.UInt32).alias("n_zone"),
                pl.col("dh_batiment").alias("dh"),
                pl.col("dh_max").alias("dh_max"),
            )
        )
    else:
        # --- Une ligne par zone : les trois listes ont la même longueur et le même
        #     ordre (par n° de zone) ; `explode` les déplie ensemble ----------------
        _points = (
            _df.filter(pl.col("dh_zones").is_not_null() & pl.col("zone_climatique").is_not_null())
            .select("ID", "zone_climatique", "dh_zones", "is_traversant_zones", "dh_max_zones")
            .explode("dh_zones", "is_traversant_zones", "dh_max_zones", empty_as_null=True)
            .with_row_index("rang_global")
            .with_columns(
                # n° de la zone dans son bâtiment (1, 2, ...), pour l'infobulle et l'export
                pl.col("rang_global").rank("ordinal").over("ID").alias("n_zone"),
                pl.when(pl.col("is_traversant_zones")).then(pl.lit("Traversante"))
                .when(pl.col("is_traversant_zones").not_()).then(pl.lit("Non traversante"))
                .otherwise(None).alias("groupe"),
            )
            .select(
                "ID", "zone_climatique", "groupe", "n_zone",
                pl.col("dh_zones").alias("dh"),
                pl.col("dh_max_zones").alias("dh_max"),
            )
        )
    _nb_total = _points.height

    # DH absent, nul ou aberrant : point écarté. DH max aberrant : valeur ignorée (NULL).
    # (en mode zone, une zone sans information « traversant » est aussi écartée)
    _dh_valide = pl.col("dh").is_not_null() & (pl.col("dh") != _DH_NUL) & (pl.col("dh") <= _DH_ABERRANT)
    _sans_dh = _points.filter(pl.col("dh").is_null()).height
    _dh_ecartes = _points.filter(pl.col("dh").is_not_null() & ~_dh_valide).height   # DH à 0 ou aberrant
    _sans_trav = _points.filter(_dh_valide & pl.col("groupe").is_null()).height       # toujours 0 en mode bâtiment
    _points = _points.filter(_dh_valide & pl.col("groupe").is_not_null()).with_columns(
        pl.when(pl.col("dh_max") > _DH_ABERRANT).then(None).otherwise(pl.col("dh_max")).alias("dh_max")
    )
    print(f"  {_UNITES} : {_nb_total} ; sans DH : {_sans_dh} ; DH à 0 ou > {_DH_ABERRANT} : {_dh_ecartes}"
          + ("" if _PAR_BATIMENT else f" ; sans information « traversant » : {_sans_trav}"))

    mo.stop(_points.height == 0, mo.md(f"**Aucun{'' if _PAR_BATIMENT else 'e'} {_UNITE} avec un DH exploitable pour ces filtres.**"))


    # ============================================================================
    # 2. STATISTIQUES PAR (zone climatique, groupe)
    # ============================================================================

    _agg = (
        _points.group_by(["zone_climatique", "groupe"]).agg(
            pl.len().alias("nb"),
            pl.col("dh").min().alias("min"),
            pl.col("dh").quantile(0.25).alias("q1"),
            pl.col("dh").median().alias("mediane"),
            pl.col("dh").quantile(0.75).alias("q3"),
            pl.col("dh").max().alias("max"),
            pl.col("dh_max").max().alias("dh_max_maximum"),   # plus grand DH max réglementaire du groupe
            # point qui porte ce plus grand DH max (affiché au survol du « DHmax »)
            pl.col("ID").sort_by("dh_max", descending=True, nulls_last=True).first().alias("id_dh_max"),
            pl.col("dh").sort_by("dh_max", descending=True, nulls_last=True).first().alias("dh_de_id_dh_max"),
            (pl.col("dh") > _Y_MAX).sum().alias("nb_au_dela_axe"),
        )
        .with_columns((pl.col("nb") >= _NB_MIN_PAR_BOITE).alias("boite_affichee"))
    )

    # Zones climatiques présentes, dans l'ordre voulu
    _presentes = _agg["zone_climatique"].unique().to_list()
    _zones_climatiques = (
        [z for z in _ORDRE_ZONES_CLIMATIQUES if z in _presentes]
        + sorted(z for z in _presentes if z not in _ORDRE_ZONES_CLIMATIQUES)
    )
    _position = {z: i for i, z in enumerate(_zones_climatiques)}   # abscisse de chaque zone climatique
    _nb_masquees = _agg.filter(~pl.col("boite_affichee")).height


    # ============================================================================
    # 3. GRAPHIQUE
    # ============================================================================

    _fig = go.Figure()
    _annotations_dh_max = []
    _n_par_groupe = {}    # {(zone climatique, groupe): nombre de points}, pour les étiquettes de l'axe

    for _libelle, (_couleur, _decalage) in _GROUPES.items():
        _z = _points.filter(pl.col("groupe") == _libelle).with_columns(
            (pl.col("zone_climatique").replace_strict(_position, default=None, return_dtype=pl.Int64) + _decalage).alias("x")
        )
        if _z.height == 0:
            continue
        _infobulle = [
            f"{_id}" + ("" if _n is None else f" — zone {_n}") + (f"<br>DH max : {_m:.0f}" if _m is not None else "")
            for _id, _n, _m in zip(_z["ID"], _z["n_zone"], _z["dh_max"])
        ]

        # Boîte (sans points), uniquement pour les groupes d'au moins _NB_MIN_PAR_BOITE points
        _gros = _agg.filter((pl.col("groupe") == _libelle) & pl.col("boite_affichee"))["zone_climatique"].to_list()
        _zb = _z.filter(pl.col("zone_climatique").is_in(_gros))
        if _zb.height:
            _fig.add_trace(go.Box(
                x=_zb["x"].to_list(), y=_zb["dh"].to_list(),
                name=_libelle, legendgroup=_libelle, marker_color=_couleur,
                boxpoints=False, line=dict(width=1.4), width=_LARGEUR_BOITE,
                hoverinfo="skip",
            ))

        # Points individuels de TOUS les groupes (même ceux sans boîte)
        _fig.add_trace(go.Box(
            x=_z["x"].to_list(), y=_z["dh"].to_list(),
            name=_libelle, legendgroup=_libelle, showlegend=not _zb.height,
            marker=dict(color=_couleur, size=4, opacity=0.5),
            boxpoints="all", jitter=0.4, pointpos=0, width=_LARGEUR_BOITE,
            line=dict(width=0), fillcolor="rgba(0,0,0,0)",
            hoveron="points", customdata=_infobulle,
            hovertemplate=f"<b>{_libelle}</b><br>DH : %{{y:.0f}}<br>%{{customdata}}<extra></extra>",
        ))

        for _r in _agg.filter(pl.col("groupe") == _libelle).iter_rows(named=True):
            _x = _position[_r["zone_climatique"]] + _decalage
            _n_par_groupe[(_r["zone_climatique"], _libelle)] = _r["nb"]

            # Valeur de la médiane, lisible en permanence, à droite de la boîte
            if _r["boite_affichee"]:
                _fig.add_trace(go.Scatter(
                    x=[_x + _LARGEUR_BOITE / 2], y=[_r["mediane"]],
                    mode="text", text=[f"<b>{_r['mediane']:.0f}</b>"], textposition="middle right",
                    textfont=dict(color=_couleur, size=12),
                    showlegend=False, hoverinfo="skip", cliponaxis=False,
                ))

            # DH max réglementaire du groupe, UNIQUEMENT s'il dépasse 1250 : petit
            # chiffre en haut de la colonne, dans la couleur du groupe
            if _r["dh_max_maximum"] is not None and _r["dh_max_maximum"] > _DH_MAX_REGLEMENTAIRE:
                # Ce chiffre est la LIMITE réglementaire (dh_max) et non un DH mesuré : aucun
                # point n'est donc situé à cette hauteur. Au survol : le point qui la porte.
                _annotations_dh_max.append(dict(
                    x=_x, y=1.0, xref="x", yref="paper", yanchor="bottom", showarrow=False,
                    text=f"DHmax<br>{_r['dh_max_maximum']:.0f}", font=dict(size=11, color=_couleur),
                    captureevents=True,
                    hovertext=(f"DH max réglementaire le plus élevé du groupe : {_r['dh_max_maximum']:.0f}<br>"
                               f"porté par {_r['id_dh_max']} (DH de ce{'' if _PAR_BATIMENT else 'tte'} "
                               f"{_UNITE} : {_r['dh_de_id_dh_max']:.0f})"),
                ))

    # Repères horizontaux
    _fig.add_hline(
        y=_DH_MAX_REGLEMENTAIRE, line=dict(color=_COULEUR_DH_MAX, width=1.5, dash="dash"),
        annotation_text=f"DH max réglementaire ({_DH_MAX_REGLEMENTAIRE})", annotation_position="top left",
        annotation_font=dict(size=11, color=_COULEUR_DH_MAX),
    )
    _fig.add_hline(
        y=_DH_SEUIL_BAS, line=dict(color=_COULEUR_SEUIL_BAS, width=1, dash="dot"),
        annotation_text=f"Seuil bas ({_DH_SEUIL_BAS})", annotation_position="bottom left",
        annotation_font=dict(size=11, color=_COULEUR_SEUIL_BAS),
    )

    # Notes du sous-titre et textes des axes
    _note_masquees = (
        f" — {_nb_masquees} boîte(s) de moins de {_NB_MIN_PAR_BOITE} {_UNITES} non tracée(s) (points conservés)"
        if _nb_masquees else ""
    )
    _note_exclues = (
        f" — {_UNITES} {_ECARTES} : {_sans_dh} sans DH, {_dh_ecartes} DH à 0 ou > {_DH_ABERRANT}"
        + ("" if _PAR_BATIMENT else f", {_sans_trav} sans information « traversant »")
        if (_sans_dh or _dh_ecartes or _sans_trav) else ""
    )
    _nb_au_dela = int(_agg["nb_au_dela_axe"].sum())
    _note_axe = f" — {_nb_au_dela} {_UNITE}(s) au-dessus de {_Y_MAX} non visible(s) (axe coupé)" if _nb_au_dela else ""
    _effectif = (f"{_points.height} bâtiments" if _PAR_BATIMENT
                 else f"{_points.height} zones de {_points['ID'].n_unique()} bâtiments")
    if _PAR_BATIMENT:
        _titre_axe_x = "Zone climatique  (n bâtiments)"
        _sous_ticks = {_zc: f"n = {_n_par_groupe.get((_zc, 'Bâtiment'), 0)}" for _zc in _zones_climatiques}
    else:
        _titre_axe_x = "Zone climatique  (n zones traversantes / n zones non traversantes)"
        _sous_ticks = {
            _zc: f"n = {_n_par_groupe.get((_zc, 'Traversante'), 0)} / {_n_par_groupe.get((_zc, 'Non traversante'), 0)}"
            for _zc in _zones_climatiques
        }

    _fig.update_layout(
        template="plotly_white",
        height=620,
        title=dict(
            text=(
                f"<b>Graphique 10 — {_TITRE} — {_USAGE}</b><br>"
                f"<sup>Unité : {choix_unite_dh.value.lower()} — {_effectif}{_note_masquees}</sup><br>"
                + (f"<sup>{(_note_exclues + _note_axe).lstrip(' —')}</sup><br>" if (_note_exclues or _note_axe) else "")
                + f"<sup>{SOUS_TITRE_FILTRES}</sup>"
            ),
            font=dict(size=_TAILLE_TITRE_GRAPHIQUE),
        ),
        xaxis=dict(
            title=_titre_axe_x,
            tickmode="array", tickvals=list(range(len(_zones_climatiques))),
            ticktext=[
                f"<b>{_zc}</b><br><span style='font-size:11px;color:gray'>{_sous_ticks[_zc]}</span>"
                for _zc in _zones_climatiques
            ],
            range=[-0.6, len(_zones_climatiques) - 0.4],
        ),
        yaxis=dict(title=f"DH {'du bâtiment' if _PAR_BATIMENT else 'de la zone'} (°C·h)", range=[0, _Y_MAX]),
        legend=dict(orientation="h", x=0.5, xanchor="center", y=-0.2, yanchor="top"),
        margin=dict(t=210, b=110, l=60, r=20),
    )

    # add_annotation (et non update_layout(annotations=...)) : ajoute aux annotations
    # des repères horizontaux au lieu de les écraser
    for _annotation in _annotations_dh_max:
        _fig.add_annotation(**_annotation)

    _graphique = mo.ui.plotly(_fig, config=CONFIG_PLOTLY)


    # ============================================================================
    # 4. EXPORTS (tableau des statistiques + export brut des points tracés)
    # ============================================================================

    _ordre = pl.col("zone_climatique").replace_strict(
        {z: i for i, z in enumerate(_zones_climatiques)}, default=len(_zones_climatiques), return_dtype=pl.Int64
    )
    if _PAR_BATIMENT:
        # Tableau : une ligne par zone climatique, Q1 / médiane / Q3 (8 zones x 3 valeurs)
        _export_tableau = (
            _agg.sort(_ordre)
            .select("zone_climatique", pl.col("q1").round(0), pl.col("mediane").round(0), pl.col("q3").round(0))
        )
        # Brut : une ligne par bâtiment tracé
        _export_brut = _points.sort(_ordre, "ID").select(
            "ID", "zone_climatique", pl.col("dh").alias("dh_batiment"), "dh_max"
        )
        _nom = "graphique_10_dh_par_batiment"
    else:
        # Tableau : statistiques de chaque (zone climatique, traversante ou non)
        _export_tableau = (
            _agg.sort(_ordre, pl.col("groupe") == "Non traversante")
            .rename({"groupe": "traversante", "nb": "nb_zones"})
        )
        # Brut : une ligne par zone tracée
        _export_brut = _points.sort(_ordre, "ID", "n_zone").select(
            "ID", "zone_climatique", "n_zone", pl.col("groupe").alias("traversante"),
            pl.col("dh").alias("dh_zone"), pl.col("dh_max").alias("dh_max_zone"),
        )
        _nom = "graphique_10_dh_par_zone"

    mo.vstack([
        _graphique,
        mo.Html('<div class="pas-imprime">' + mo.md(f"**Tableau ({'Q1 / médiane / Q3 par zone climatique' if _PAR_BATIMENT else 'statistiques par zone climatique et type de zone'})**").text + '</div>'),
        boutons_export(_export_tableau, f"{_nom}_tableau"),
        mo.Html('<div class="pas-imprime">' + mo.md(f"**Export brut (une ligne par {_UNITE} tracé{'' if _PAR_BATIMENT else 'e'})**").text + '</div>'),
        boutons_export(_export_brut, f"{_nom}_brut"),
    ])
    return


@app.cell(hide_code=True)
def resume_filtres_graphique_10(choix_unite_dh, choix_y_max_dh, resume_filtres):
    # Résumé des filtres actifs du graphique 10, placé SOUS le graphique (cellule
    # séparée : il lit les valeurs des widgets, alors que le panneau reste statique).
    # Dernière ligne : paramètres propres au graphique 10 (unité, zoom Y).
    resume_filtres(parametres_graphique={"Graphique 10": [
        f"unité : {choix_unite_dh.value.lower()}",
        f"axe Y jusqu'à {choix_y_max_dh.value} °C·h",
    ]})
    return


@app.cell(hide_code=True)
def saut_page_11(mo):
    # Saut de page à l'impression avant le graphique 11 (aucun effet à l'écran ;
    # règle `.saut-page` dans la cellule `style_impression`).
    mo.Html('<div class="saut-page"></div>')
    return


@app.cell(hide_code=True)
def param_graphique_11(mo, panneau_filtres):
    # ============================================================================
    # CELLULE WIDGET — paramètres propres au graphique 11 (4 donuts : matériau de
    # structure, type de plancher, remplissage de façade, générateur de chauffage).
    #   - bascule « Masquer « Autre » / non renseigné » (encadré visible sous « Valider… ») :
    #     masque « Autre » et les valeurs vides, les pourcentages sont recalculés ;
    #     les couleurs des autres catégories ne changent pas
    #   - nombre maximal de catégories par donut (le reste est regroupé)
    # « Masquer les inconnus » n'est pas appliqué : tous les seuils sont comptés.
    # ============================================================================

    masquer_non_renseignes_10 = mo.ui.switch(
        value=False, label="**Masquer « Autre » / non renseigné**",
    )

    choix_nb_categories_10 = mo.ui.slider(
        start=2, stop=10, step=1, value=5, show_value=True,
        label="Nombre maximal de catégories par donut (le reste : « Autres catégories »)",
    )

    mo.vstack([
        mo.Html('<div class="pas-imprime">' + mo.md("### Paramètres du graphique 11").text + '</div>'),
        panneau_filtres(
            {"Graphique 11": choix_nb_categories_10},
            avec_inconnus=False,
            bascule_en_evidence=masquer_non_renseignes_10,     # encadré sous « Valider… », bien visible
        ),
    ])
    return choix_nb_categories_10, masquer_non_renseignes_10


@app.cell(hide_code=True)
def graphique_11(
    CONFIG_PLOTLY,
    GRAPHIQUES,
    DATA_brut,
    SOUS_TITRE_FILTRES,
    appliquer_filtres,
    boutons_export,
    choix_nb_categories_10,
    dropdown_usage,
    go,
    masquer_non_renseignes_10,
    mo,
    pl,
):
    # ============================================================================
    # CELLULE — Graphique 11 : 4 donuts, répartition (%) des bâtiments par matériau
    # de structure, type de plancher, matériau de remplissage de façade et
    # générateur de chauffage.
    #
    # Part de DATA_brut (AUCUN appel réseau ici) ; filtres temps réel communs à tous
    # les graphiques (cellule `filtres_communs`), sauf « Masquer les inconnus ».
    # Variables dc_* : fiabilité « mauvaise » (valeur « Autre » surreprésentée).
    # ============================================================================

    # ============================================================================
    # PARAMÈTRES (toutes les variables au même endroit)
    # ============================================================================

    _USAGE = dropdown_usage.value
    _AFFICHER_NON_RENSEIGNES = not masquer_non_renseignes_10.value
    _NB_MAX_CATEGORIES = choix_nb_categories_10.value

    # --- Libellés spéciaux -------------------------------------------------------------
    _LIBELLE_AUTRE = "Autre"                     # valeur saisie « Autre » (dc_*)
    _LIBELLE_NON_RENSEIGNE = "Non renseigné"     # valeur absente (NULL / vide)
    _LIBELLE_REGROUPE = "Autres catégories"      # catégories au-delà de _NB_MAX_CATEGORIES
    _NON_RENSEIGNES = [_LIBELLE_AUTRE, _LIBELLE_NON_RENSEIGNE]

    # --- Les 4 donuts, dans l'ordre d'affichage (haut-gauche, haut-droite, bas-gauche,
    #     bas-droite) : clé -> (titre, colonne de DATA_brut, position (colonne, ligne))
    _DONUTS = {
        "structure":  ("matériau de structure principal", "dc_materiau_structure", (0, 1)),
        "plancher":   ("type de plancher", "dc_type_plancher", (1, 1)),
        "facade":     ("matériau de remplissage de façade", "dc_materiau_remplissage_facade", (0, 0)),
        "generateur": ("générateur de chauffage", "synthese_generateur_ch", (1, 0)),
    }
    _SEPARATEUR_GENERATEURS = "|"     # synthese_generateur_ch : « principal | appoint » -> on garde le principal

    # --- Couleurs : FIXES par catégorie (une couleur ne change pas quand on masque
    #     « Autre » ou qu'on change le filtre). Règles testées dans l'ordre sur le libellé
    #     en minuscules : (mots-clés, couleur) ; sinon couleur de repli (cycle).
    _GRIS_AUTRE, _GRIS_VIDE, _GRIS_REGROUPE = "#A6A6A6", "#D9D9D9", "#C9CED8"
    _REGLES_COULEUR_MATERIAUX = [
        (["chanvre", "paille", "terre crue"], "#7FB069"),            # biosourcés : vert
        (["bois"], "#A9D18E"),                                       # bois : vert pâle
        (["mixte"], "#5E8C6A"),                                      # mixtes : vert-gris
        (["terre cuite", "brique"], "#C8553D"),                      # terre cuite : terracotta
        (["parpaing", "bloc", "hourdis", "poutrelle"], "#4A6FA5"),   # béton préfabriqué : bleu moyen
        (["béton", "beton", "dalle"], "#283246"),                    # béton : bleu nuit
        (["acier", "métal", "metal"], "#6F86A8"),                    # acier : bleu-gris
        (["pierre"], "#D8C3A5"),                                     # pierre : sable
    ]
    _REGLES_COULEUR_GENERATEURS = [                                  # palette distincte des 3 autres donuts
        (["air / eau"], "#0E7C86"),                                  # PAC air / eau : turquoise
        (["air / air"], "#7CCFC8"),                                  # PAC air / air : turquoise clair
        (["poêle", "poele", "insert"], "#9A6B3F"),                   # poêle, insert : brun
        (["gaz", "chaudière", "chaudiere"], "#4A1F3D"),              # chaudière gaz : aubergine foncé
        (["joule"], "#E3A72F"),                                      # effet Joule : ambre
        (["réseau", "reseau", "urbain"], "#9B8AC4"),                 # réseau de chaleur : lavande
        (["pac"], "#3A9CA6"),                                        # autres PAC : turquoise moyen
    ]
    _COULEURS_REPLI = ["#B5838D", "#E9C46A", "#9C89B8", "#F4A261", "#2A9D8F"]

    # --- Mise en page (pixels) ------------------------------------------------------------
    _LARGEUR, _HAUTEUR = 1100, 1100
    _MARGE_HAUT, _MARGE_BAS, _MARGE_GAUCHE, _MARGE_DROITE = 100, 20, 30, 30
    _COLONNES_X = {0: (0.05, 0.45), 1: (0.55, 0.95)}              # emprise horizontale d'un donut (0-1)
    _LIGNES_PX = {                                                 # positions (px depuis le haut de la figure)
        1: dict(titre=125, donut=(185, 425), legende=445),         # ligne du haut
        0: dict(titre=640, donut=(700, 940), legende=960),         # ligne du bas
    }
    _TROU = 0.55                      # taille du trou central (0 = camembert plein)
    _SEUIL_PCT = 3                    # à partir de ce pourcentage, le % est affiché à côté de la part
    _SEUIL_NOM_PCT = 10               # au-dessus de ce pourcentage, le nom de la catégorie s'ajoute au %
    _LARGEUR_NOM_ETIQUETTE = 16       # nombre de caractères par ligne du nom (retour à la ligne au-delà)
    _LONGUEUR_MAX_LIBELLE = 34        # libellés de légende tronqués (le survol donne le texte complet)
    _POLICE = "Calibri, Carlito, Arial"

    # ============================================================================
    # 1. DONNÉES : filtres communs, puis une colonne « libellé propre » par donut
    # ============================================================================

    _df = appliquer_filtres(DATA_brut, filtre_inconnu=False)
    mo.stop(_df.height == 0, mo.md("**Aucun bâtiment ne correspond aux filtres choisis.**"))

    def _nettoyer(colonne):
        """Texte propre : espaces retirés, 1re lettre en majuscule, vide -> « Non renseigné »,
        « autre » (toute casse) -> « Autre »."""
        _texte = pl.col(colonne).cast(pl.Utf8).str.strip_chars()
        _texte = _texte.str.slice(0, 1).str.to_uppercase() + _texte.str.slice(1)
        return (
            pl.when(_texte.is_null() | (_texte == ""))
            .then(pl.lit(_LIBELLE_NON_RENSEIGNE))
            .when(_texte.str.to_lowercase() == _LIBELLE_AUTRE.lower())
            .then(pl.lit(_LIBELLE_AUTRE))
            .otherwise(_texte)
        )

    _df = _df.with_columns(
        _nettoyer("dc_materiau_structure").alias("structure"),
        _nettoyer("dc_type_plancher").alias("plancher"),
        _nettoyer("dc_materiau_remplissage_facade").alias("facade"),
        # générateur : on ne garde que le principal (avant le séparateur), espaces autour de « / » normalisés
        pl.col("synthese_generateur_ch").cast(pl.Utf8).str.split(_SEPARATEUR_GENERATEURS).list.first()
        .str.replace_all(r"\s*/\s*", " / ").alias("_generateur_principal"),
    ).with_columns(_nettoyer("_generateur_principal").alias("generateur"))

    # ============================================================================
    # 2. COULEUR D'UNE CATÉGORIE
    # ============================================================================

    def _couleur(libelle, regles, repli):
        if libelle == _LIBELLE_AUTRE:
            return _GRIS_AUTRE
        if libelle == _LIBELLE_NON_RENSEIGNE:
            return _GRIS_VIDE
        if libelle == _LIBELLE_REGROUPE:
            return _GRIS_REGROUPE
        _minuscules = libelle.lower()
        for _mots, _couleur_regle in regles:
            if any(_mot in _minuscules for _mot in _mots):
                return _couleur_regle
        return repli.setdefault(libelle, _COULEURS_REPLI[len(repli) % len(_COULEURS_REPLI)])

    def _tronque(libelle):
        if len(libelle) <= _LONGUEUR_MAX_LIBELLE:
            return libelle
        return libelle[: _LONGUEUR_MAX_LIBELLE - 1] + "…"

    def _etiquette(libelle, pourcentage):
        """Texte posé à côté d'une part du donut :
        - sous _SEUIL_PCT : rien (la légende et le survol donnent la valeur) ;
        - de _SEUIL_PCT à _SEUIL_NOM_PCT : le pourcentage seul ;
        - au-dessus de _SEUIL_NOM_PCT : le nom court (parenthèse retirée, sur plusieurs
          lignes) puis le pourcentage."""
        if pourcentage < _SEUIL_PCT:
            return ""
        _pct_txt = f"{pourcentage:.1f}".replace(".", ",") + " %"
        if pourcentage <= _SEUIL_NOM_PCT:
            return _pct_txt
        _nom = libelle.split("(")[0].strip()          # « Bloc de béton (parpaing...) » -> « Bloc de béton »
        _lignes, _ligne = [], ""
        for _mot in _nom.split():
            if _ligne and len(_ligne) + 1 + len(_mot) > _LARGEUR_NOM_ETIQUETTE:
                _lignes.append(_ligne)
                _ligne = _mot
            else:
                _ligne = f"{_ligne} {_mot}".strip()
        _lignes.append(_ligne)
        return "<br>".join(_lignes + [_pct_txt])

    # ============================================================================
    # 3. FIGURE : un donut (go.Pie) par variable
    # ============================================================================

    _hauteur_trace = _HAUTEUR - _MARGE_HAUT - _MARGE_BAS
    _y_paper = lambda px: 1 - (px - _MARGE_HAUT) / _hauteur_trace     # px depuis le haut -> coordonnée « paper »

    _fig = go.Figure()
    _annotations = []
    _legendes = {}
    _export = []

    for _rang, (_cle, (_titre, _colonne_source, (_cx, _cy))) in enumerate(_DONUTS.items()):
        _x0, _x1 = _COLONNES_X[_cx]
        _ligne = _LIGNES_PX[_cy]
        _y_bas, _y_haut = _y_paper(_ligne["donut"][1]), _y_paper(_ligne["donut"][0])
        _x_centre = (_x0 + _x1) / 2
        _nom_legende = "legend" if _rang == 0 else f"legend{_rang + 1}"
        _regles = _REGLES_COULEUR_GENERATEURS if _cle == "generateur" else _REGLES_COULEUR_MATERIAUX

        # Comptage par catégorie ; masquage éventuel de « Autre » / « Non renseigné »
        _comptes = (
            _df.group_by(_cle).len().rename({_cle: "categorie", "len": "n"})
            .sort(["n", "categorie"], descending=[True, False])
        )
        if not _AFFICHER_NON_RENSEIGNES:
            _comptes = _comptes.filter(~pl.col("categorie").is_in(_NON_RENSEIGNES))

        # Catégories renseignées (les plus fréquentes), regroupement du reste, puis
        # « Autre » et « Non renseigné » en fin de donut
        _renseignees = _comptes.filter(~pl.col("categorie").is_in(_NON_RENSEIGNES))
        _gardees = _renseignees.head(_NB_MAX_CATEGORIES)
        _reste = _renseignees.tail(max(_renseignees.height - _NB_MAX_CATEGORIES, 0))
        _parts = [(_l["categorie"], _l["n"]) for _l in _gardees.iter_rows(named=True)]
        if _reste.height:
            _parts.append((_LIBELLE_REGROUPE, _reste["n"].sum()))
        for _l in _comptes.filter(pl.col("categorie").is_in(_NON_RENSEIGNES)).iter_rows(named=True):
            _parts.append((_l["categorie"], _l["n"]))

        # Titre du donut
        _annotations.append(dict(
            x=_x_centre, y=_y_paper(_ligne["titre"]), xref="paper", yref="paper",
            xanchor="center", yanchor="top", showarrow=False, font=dict(size=15),
            text=f"<b>Répartition par {_titre}</b><br>"
                 "<i><span style='font-size:12px'>en pourcentage du nombre de bâtiments total</span></i>",
        ))

        if not _parts:
            _annotations.append(dict(
                x=_x_centre, y=(_y_bas + _y_haut) / 2, xref="paper", yref="paper",
                xanchor="center", yanchor="middle", showarrow=False, font=dict(size=14, color="#888"),
                text="Aucun bâtiment renseigné",
            ))
            continue

        _total = sum(_n for _, _n in _parts)
        _repli = {}
        _couleurs = [_couleur(_c, _regles, _repli) for _c, _ in _parts]

        _fig.add_trace(go.Pie(
            # Plotly confond les parts de même libellé entre deux donuts (légende) : un
            # suffixe invisible (espaces de largeur nulle) les distingue ; le vrai libellé
            # est dans customdata (survol).
            labels=[_tronque(_c) + "​" * _rang for _c, _ in _parts],
            values=[_n for _, _n in _parts],
            customdata=[[_c] for _c, _ in _parts],
            hole=_TROU, sort=False, direction="clockwise", rotation=0,
            marker=dict(colors=_couleurs, line=dict(color="white", width=2)),
            text=[_etiquette(_c, 100 * _n / _total) for _c, _n in _parts],
            textinfo="text", textposition="outside", textfont=dict(size=14),
            domain=dict(x=[_x0, _x1], y=[_y_bas, _y_haut]),
            legend=_nom_legende,
            hovertemplate="<b>%{customdata[0]}</b><br>%{value} bâtiments (%{percent})<extra></extra>",
        ))
        # Total au centre du donut
        _annotations.append(dict(
            x=_x_centre, y=(_y_bas + _y_haut) / 2, xref="paper", yref="paper",
            xanchor="center", yanchor="middle", showarrow=False, font=dict(size=16),
            text=f"<b>n = {_total}</b><br><span style='font-size:11px'>bâtiments</span>",
        ))
        _legendes[_nom_legende] = dict(
            orientation="v", x=_x_centre, xanchor="center", y=_y_paper(_ligne["legende"]), yanchor="top",
            font=dict(size=12), tracegroupgap=0,
        )
        _export.append(pl.DataFrame({
            "donut": [_titre] * len(_parts),
            "categorie": [_c for _c, _ in _parts],
            "nb_batiments": [_n for _, _n in _parts],
            "pourcentage": [round(100 * _n / _total, 1) for _, _n in _parts],
            "couleur": _couleurs,
        }))

    mo.stop(not _fig.data, mo.md("**Aucun bâtiment renseigné pour ces variables.**"))

    _non_renseignes_txt = "bâtiments non renseignés inclus" if _AFFICHER_NON_RENSEIGNES else "bâtiments non renseignés exclus"
    _fig.update_layout(
        template="plotly_white",
        width=_LARGEUR,
        height=_HAUTEUR,
        annotations=_annotations,
        margin=dict(t=_MARGE_HAUT, b=_MARGE_BAS, l=_MARGE_GAUCHE, r=_MARGE_DROITE),
        font=dict(family=_POLICE),
        title=dict(
            text=f"<b>Graphique 11 — {GRAPHIQUES[11]} — {_USAGE}</b><br>"
                 f"<sup>{SOUS_TITRE_FILTRES} — {_non_renseignes_txt}</sup>",
            font=dict(size=18),
        ),
        **_legendes,
    )

    _graphique = mo.ui.plotly(_fig, config=CONFIG_PLOTLY)

    # Export : les données TRACÉES (donut, catégorie, nombre de bâtiments, %, couleur)
    mo.vstack([_graphique, boutons_export(pl.concat(_export), "graphique_11_repartition_choix_constructifs")])
    return


@app.cell(hide_code=True)
def resume_filtres_graphique_11(resume_filtres):
    # Résumé des filtres actifs du graphique 11, placé SOUS le graphique (cellule
    # séparée : il lit les valeurs des widgets, alors que le panneau reste statique).
    resume_filtres(avec_inconnus=False)
    return


@app.cell(hide_code=True)
def param_apercu_tables(mo):
    # ============================================================================
    # CELLULE WIDGET — bouton de l'export "aperçu des tables"
    # (défini dans une autre cellule que celle qui lit sa valeur, cf. règle marimo)
    # ============================================================================

    bouton_apercu_tables = mo.ui.run_button(label="Exporter l'aperçu des tables (10 premières lignes)")

    # (non imprimé : classe « pas-imprime »)
    mo.Html('<div class="pas-imprime">' + mo.vstack([
        mo.md("### Aperçu des tables de la base"),
        bouton_apercu_tables,
    ]).text + '</div>')
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

    mo.stop(not bouton_apercu_tables.value,
            mo.Html('<div class="pas-imprime">' + mo.md("*Clique sur le bouton pour lancer l'export.*").text + '</div>'))

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

    # (non imprimé : classe « pas-imprime »)
    mo.Html('<div class="pas-imprime">' + mo.vstack([
        mo.md(f"**{len(_apercus)} table(s) lues** — {_NB_LIGNES} premières lignes de chacune."),
        mo.md(f"⚠️ Tables introuvables dans la base : {', '.join(_absentes)}") if _absentes else mo.md(""),
        mo.ui.table(_resume, selection=None, show_download=False),
        _bouton_zip,
        mo.md("Ou table par table :"),
        mo.hstack(_boutons_csv, justify="start", wrap=True),
    ]).text + '</div>')
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
    mo.ui.table(_summary_df, show_download=False)
    return


if __name__ == "__main__":
    app.run()