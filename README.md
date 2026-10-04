# Golden Therapie — site vitrine (démo)

Démo pour revue client, hébergée sur GitHub Pages : https://iooikos-yann.github.io/golden-therapie-site/

- `index.html` : export Claude Design (runtime `support.js`, React chargé depuis unpkg)
- `assets/golden-therapie-flyer.pdf` : version web compressée du triptyque (l'original d'impression de 165 Mo reste hors dépôt)
- Langues : FR (racine, source) · EN (`/en/`) · PT (`/pt/`). Après toute modif du FR : `python3 tools/i18n.py` (échoue si un texte FR traduit a changé → mettre à jour `TEXTS`)
- Mise à jour : push sur `main` → redéploiement automatique Pages
