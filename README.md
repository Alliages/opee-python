# OPEE by GM

Notebook [marimo](https://marimo.io) d'analyse de la base open data OPEE (RE2020) :
IC Construction, impact carbone par lot, matériaux de structure, fiches FDES/PEP/DED,
écarts aux seuils réglementaires, stock de carbone.

Les données sont lues dans la base Turso `opee-alliages`.

## Lancer en local

```bash
uvx marimo edit --sandbox OPEE_by_GM.py
```

Jeton Turso : définir la variable d'environnement `TURSO_TOKEN`, ou le saisir dans le
champ prévu en haut du notebook. **Ne jamais l'écrire dans le code.**

## molab

Notebook synchronisé depuis GitHub : chaque `git push` met à jour la version molab.
