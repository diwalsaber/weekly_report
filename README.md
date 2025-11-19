# Weekly Report Generator

Générateur automatique de rapports hebdomadaires professionnels au format PDF.

## 📋 Description

Ce projet implémente une solution complète de génération de rapports hebdomadaires automatisés. Les rapports sont générés en PDF à partir de données structurées (JSON) et peuvent être envoyés automatiquement par email.

**Format choisi** : PDF généré via Python (WeasyPrint + Jinja2)

## ✨ Caractéristiques

- ✅ **Professionnel** : Design épuré et moderne avec dégradés de couleurs
- ✅ **Automatisable** : Compatible Airflow, Cron, Cloud Run/Jobs
- ✅ **Modulaire** : Template HTML facilement personnalisable
- ✅ **Complet** : KPIs, graphiques, projets, points d'attention, prochaines étapes
- ✅ **Universel** : Format PDF lisible partout
- ✅ **Extensible** : Envoi email intégrable (SMTP, SendGrid)

## 🚀 Démarrage rapide

### Installation

```bash
# Installer les dépendances Python
pip install -r requirements.txt

# Vérifier la structure du projet
python3 test_structure.py
```

### Générer votre premier rapport

```bash
cd src
python generate_report.py data/example_data.json
```

Le PDF sera disponible dans le dossier `output/`.

## 📁 Structure du projet

```
weekly_report/
├── README.md                    # Ce fichier
├── USAGE.md                     # Guide d'utilisation détaillé
├── PROPOSITIONS_FORMATS.md      # Analyse comparative des formats
├── requirements.txt             # Dépendances Python
├── test_structure.py            # Script de validation
├── src/
│   ├── generate_report.py       # Script principal de génération
│   ├── templates/
│   │   └── weekly_report.html   # Template HTML du rapport
│   └── data/
│       └── example_data.json    # Exemple de données
└── output/                      # PDFs générés (gitignored)
```

## 📊 Aperçu du rapport

Le rapport généré comprend :

1. **Résumé exécutif** : Points clés de la semaine
2. **Indicateurs clés (KPIs)** : Cartes visuelles colorées avec évolutions
3. **Graphique d'évolution** : Visualisation des tendances
4. **Avancement des projets** : Tableau avec statuts et barres de progression
5. **Métriques détaillées** : Comparaison objectifs vs réalisé
6. **Points d'attention** : Alertes et problèmes à surveiller
7. **Prochaines étapes** : Actions planifiées avec échéances

## 🎨 Personnalisation

### Modifier le design

Éditez `src/templates/weekly_report.html` pour personnaliser :
- Couleurs et dégradés
- Sections affichées
- Mise en page
- Logo et branding

### Adapter les données

Créez votre fichier JSON basé sur `src/data/example_data.json` :

```json
{
  "week_start": "Date début",
  "week_end": "Date fin",
  "kpis": [...],
  "projects": [...],
  ...
}
```

## 🤖 Automatisation

### Avec Cron (Linux/macOS)

```bash
# Chaque lundi à 9h
0 9 * * 1 cd /path/to/weekly_report/src && python3 generate_report.py data/current_week.json
```

### Avec Airflow

Voir exemple de DAG dans `USAGE.md`.

### Avec Cloud Run

Dockerfile et instructions disponibles dans `USAGE.md`.

## 📧 Envoi par email

Le script supporte l'envoi automatique par email. Configuration à personnaliser dans `src/generate_report.py` (méthode `_send_email`).

Services supportables :
- SMTP standard
- SendGrid
- AWS SES
- Tout autre service compatible

## 📖 Documentation

- **[USAGE.md](USAGE.md)** : Guide complet d'utilisation, personnalisation et automatisation
- **[PROPOSITIONS_FORMATS.md](PROPOSITIONS_FORMATS.md)** : Analyse comparative de 5 formats de rapports

## 🛠️ Technologies utilisées

- **Python 3.8+**
- **WeasyPrint** : Conversion HTML → PDF
- **Jinja2** : Templating HTML
- **Matplotlib** : Génération de graphiques
- **Pandas** : Manipulation de données (optionnel)

## ✅ Validation

Exécutez le script de test pour vérifier l'intégrité du projet :

```bash
python3 test_structure.py
```

## 🎯 Avantages de cette solution

| Critère | Score |
|---------|-------|
| Simplicité d'utilisation | ⭐⭐⭐⭐⭐ |
| Professionnalisme | ⭐⭐⭐⭐⭐ |
| Automatisation | ⭐⭐⭐⭐⭐ |
| Coût de mise en place | ⭐⭐⭐⭐ (5-6 jours) |
| Maintenance | ⭐⭐⭐⭐⭐ |

## 📝 Prochaines améliorations

- [ ] Intégration email complète (SMTP/SendGrid)
- [ ] Interface web pour éditer les données
- [ ] Support multi-langues
- [ ] Thèmes multiples (dark mode, corporate, etc.)
- [ ] Export Excel complémentaire
- [ ] Collecte automatique depuis Google Analytics, bases de données, etc.

## 📄 Licence

Ce projet est un prototype destiné à un usage professionnel interne.
