# OPEE by GM

Deux notebooks [marimo](https://marimo.io) d'analyse de la base open data OPEE (RE2020),
réalisés pour le HUB des prescripteurs bas carbone. Les données sont lues dans la base
Turso `opee-alliages`.

| Notebook | Contenu |
|---|---|
| `OPEE_by_GM.py` | Dashboard général : IC Construction, impact carbone par lot, matériaux de structure, fiches FDES/PEP/DED, écarts aux seuils réglementaires, stock de carbone. |
| `OPEE_Analyse_RE2028.py` | Analyse RE2028 : facilité d'atteindre le seuil 2028 de l'IC construction (via l'IC composant) en logement collectif, et leviers associés (Analyse1 à Analyse6). |

Les deux scripts sont indépendants (pas de module commun) : le code partagé est recopié
d'un notebook à l'autre, avec un commentaire « COPIE DE OPEE_by_GM vX.XX ».

## Données Parquet (dossier `DATA/`)

Le graphique 6 de `OPEE_by_GM.py` lit les fiches (composants) des logements collectifs dans
`DATA/composants_logements_collectifs_AAAA-MM-JJ.parquet`, produit par le script d'export
(base Turso) puis publié ici. Pour changer de millésime : modifier `NOM_FICHIER` dans la cellule
`composants_logements_collectifs`.

## Lancer en local

```bash
uvx marimo edit --sandbox OPEE_by_GM.py
uvx marimo edit --sandbox OPEE_Analyse_RE2028.py
```

Jeton Turso : définir la variable d'environnement `TURSO_TOKEN`, ou le saisir dans le
champ prévu en haut du notebook. **Ne jamais l'écrire dans le code.**

## molab

Chaque notebook est synchronisé depuis GitHub (un notebook molab par fichier) :
chaque `git push` met à jour la version molab.
