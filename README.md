# Golden Therapie — site vitrine (démo)

Site en production : https://goldentherapie.lu (GitHub Pages, domaine EuroDNS)

- `index.html` : export Claude Design (runtime `support.js`, React chargé depuis unpkg)
- `assets/golden-therapie-flyer.pdf` : version web compressée du triptyque (l'original d'impression de 165 Mo reste hors dépôt)
- Langues : FR (racine, source) · EN (`/en/`) · PT (`/pt/`). Après toute modif du FR : `python3 tools/i18n.py` (échoue si un texte FR traduit a changé → mettre à jour `TEXTS`)
- Mise à jour : push sur `main` → redéploiement automatique Pages
