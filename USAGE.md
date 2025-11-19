# Guide d'Utilisation - Weekly Report Generator

## 📋 Table des matières

1. [Installation](#installation)
2. [Utilisation de base](#utilisation-de-base)
3. [Structure des données](#structure-des-données)
4. [Personnalisation](#personnalisation)
5. [Automatisation](#automatisation)
6. [Intégration email](#intégration-email)

---

## Installation

### Prérequis

- Python 3.8 ou supérieur
- pip (gestionnaire de paquets Python)

### Installation des dépendances

```bash
# Cloner ou naviguer vers le répertoire du projet
cd weekly_report

# Installer les dépendances
pip install -r requirements.txt
```

### Dépendances système pour WeasyPrint

WeasyPrint nécessite certaines bibliothèques système :

**Ubuntu/Debian :**
```bash
sudo apt-get install python3-dev python3-pip python3-setuptools python3-wheel python3-cffi libcairo2 libpango-1.0-0 libpangocairo-1.0-0 libgdk-pixbuf2.0-0 libffi-dev shared-mime-info
```

**macOS :**
```bash
brew install python3 cairo pango gdk-pixbuf libffi
```

**Windows :**
Télécharger et installer GTK+ depuis : https://github.com/tschoonj/GTK-for-Windows-Runtime-Environment-Installer/releases

---

## Utilisation de base

### 1. Génération d'un rapport avec les données d'exemple

```bash
cd src
python generate_report.py data/example_data.json
```

Le PDF sera généré dans le dossier `output/`.

### 2. Génération avec un nom de fichier personnalisé

```bash
python generate_report.py data/example_data.json -o mon_rapport_hebdo.pdf
```

### 3. Tester avec vos propres données

Créez un fichier JSON basé sur `src/data/example_data.json` :

```bash
cp src/data/example_data.json src/data/ma_semaine.json
# Éditer ma_semaine.json avec vos données
python generate_report.py data/ma_semaine.json
```

---

## Structure des données

### Format JSON requis

Votre fichier JSON doit contenir les clés suivantes :

```json
{
  "week_start": "Date de début (texte libre)",
  "week_end": "Date de fin (texte libre)",
  "executive_summary": [
    "Point clé 1",
    "Point clé 2",
    "..."
  ],
  "kpis": [
    {
      "label": "Nom du KPI",
      "value": "Valeur affichée",
      "change": "Évolution (optionnel)",
      "type": "success|info|warning"
    }
  ],
  "chart_data": {
    "title": "Titre du graphique",
    "label": "Label axe Y",
    "dates": ["2024-11-11", "2024-11-12", "..."],
    "values": [1000, 1200, ...]
  },
  "projects": [
    {
      "name": "Nom du projet",
      "status": "completed|in-progress|planned|blocked",
      "status_label": "Label affiché",
      "progress": 75,
      "owner": "Responsable"
    }
  ],
  "detailed_metrics": [
    {
      "name": "Nom métrique",
      "current": "Valeur actuelle",
      "target": "Objectif",
      "evolution": "Évolution"
    }
  ],
  "attention_points": [
    {
      "title": "Titre du point",
      "description": "Description détaillée"
    }
  ],
  "next_steps": [
    {
      "action": "Action à réaliser",
      "deadline": "Date limite (optionnel)",
      "owner": "Responsable (optionnel)"
    }
  ]
}
```

### Champs optionnels

- `chart_data` : Si absent, aucun graphique ne sera généré
- `detailed_metrics` : Section optionnelle
- `change` dans les KPIs
- `deadline` et `owner` dans next_steps

### Types de KPI disponibles

- `success` : Carte verte (indicateur positif)
- `info` : Carte bleue (indicateur neutre)
- `warning` : Carte rose/rouge (indicateur d'attention)

---

## Personnalisation

### Modifier le template HTML

Le template se trouve dans `src/templates/weekly_report.html`.

**Exemple : Modifier les couleurs**

```html
<!-- Dans la section <style> -->
.kpi-card.success {
    background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
}
```

**Exemple : Ajouter une nouvelle section**

```html
<div class="section">
    <h2>Ma Nouvelle Section</h2>
    <p>{{ ma_nouvelle_donnee }}</p>
</div>
```

N'oubliez pas d'ajouter `ma_nouvelle_donnee` dans votre fichier JSON.

### Ajouter votre logo

1. Placez votre logo dans `src/templates/`
2. Modifiez le template :

```html
<div class="header">
    <img src="logo.png" alt="Logo" style="height: 50px;">
    <h1>Weekly Report</h1>
    <!-- ... -->
</div>
```

### Personnaliser le graphique

Dans `src/generate_report.py`, méthode `create_chart()` :

```python
# Changer la couleur
ax.plot(dates, values, marker='o', linewidth=2, color='#e74c3c')

# Ajouter des annotations
ax.annotate('Pic', xy=(dates[3], values[3]),
            xytext=(10, 10), textcoords='offset points')
```

---

## Automatisation

### Avec Cron (Linux/macOS)

Exécuter chaque lundi à 9h :

```bash
# Éditer la crontab
crontab -e

# Ajouter cette ligne
0 9 * * 1 cd /chemin/vers/weekly_report/src && /usr/bin/python3 generate_report.py data/ma_semaine.json
```

### Avec Airflow

Créer un DAG `weekly_report_dag.py` :

```python
from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'data-team',
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'weekly_report_generation',
    default_args=default_args,
    description='Génère le rapport hebdomadaire',
    schedule_interval='0 9 * * 1',  # Lundi 9h
    start_date=datetime(2024, 11, 1),
    catchup=False,
)

generate_report = BashOperator(
    task_id='generate_weekly_report',
    bash_command='cd /path/to/weekly_report/src && python generate_report.py data/current_week.json',
    dag=dag,
)
```

### Avec Google Cloud Run Jobs

1. Créer un `Dockerfile` :

```dockerfile
FROM python:3.10-slim

# Installer dépendances système pour WeasyPrint
RUN apt-get update && apt-get install -y \
    python3-dev \
    libcairo2 \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libgdk-pixbuf2.0-0 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ ./src/
WORKDIR /app/src

CMD ["python", "generate_report.py", "data/example_data.json"]
```

2. Déployer :

```bash
# Build et push
gcloud builds submit --tag gcr.io/PROJECT_ID/weekly-report

# Créer le job
gcloud run jobs create weekly-report \
  --image gcr.io/PROJECT_ID/weekly-report \
  --region europe-west1

# Planifier avec Cloud Scheduler
gcloud scheduler jobs create http weekly-report-trigger \
  --schedule="0 9 * * 1" \
  --uri="https://REGION-run.googleapis.com/apis/run.googleapis.com/v1/namespaces/PROJECT_ID/jobs/weekly-report:run" \
  --http-method POST
```

---

## Intégration email

### Option 1 : SMTP Simple

Modifier `src/generate_report.py`, méthode `_send_email()` :

```python
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

def _send_email(self, pdf_path, recipients, smtp_config):
    msg = MIMEMultipart()
    msg['From'] = smtp_config['from']
    msg['To'] = ', '.join(recipients)
    msg['Subject'] = f"Weekly Report - {datetime.now().strftime('%d/%m/%Y')}"

    # Corps du message
    body = "Bonjour,\n\nVeuillez trouver ci-joint le rapport hebdomadaire.\n\nCordialement"
    msg.attach(MIMEText(body, 'plain'))

    # Pièce jointe PDF
    with open(pdf_path, 'rb') as f:
        pdf = MIMEApplication(f.read(), _subtype='pdf')
        pdf.add_header('Content-Disposition', 'attachment',
                      filename=os.path.basename(pdf_path))
        msg.attach(pdf)

    # Envoi
    with smtplib.SMTP(smtp_config['host'], smtp_config['port']) as server:
        server.starttls()
        server.login(smtp_config['username'], smtp_config['password'])
        server.send_message(msg)
```

Utilisation :

```python
smtp_config = {
    'host': 'smtp.gmail.com',
    'port': 587,
    'username': 'your-email@gmail.com',
    'password': 'your-app-password',
    'from': 'your-email@gmail.com'
}

generator.generate_and_send(
    'data/example_data.json',
    ['client@example.com', 'manager@example.com'],
    smtp_config
)
```

### Option 2 : SendGrid

```bash
pip install sendgrid
```

```python
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Attachment
import base64

def _send_email(self, pdf_path, recipients, smtp_config):
    with open(pdf_path, 'rb') as f:
        data = f.read()

    encoded = base64.b64encode(data).decode()

    message = Mail(
        from_email=smtp_config['from'],
        to_emails=recipients,
        subject=f"Weekly Report - {datetime.now().strftime('%d/%m/%Y')}",
        html_content='<p>Veuillez trouver ci-joint le rapport hebdomadaire.</p>'
    )

    attachment = Attachment()
    attachment.file_content = encoded
    attachment.file_type = 'application/pdf'
    attachment.file_name = os.path.basename(pdf_path)
    attachment.disposition = 'attachment'
    message.attachment = attachment

    sg = SendGridAPIClient(smtp_config['api_key'])
    response = sg.send(message)
```

---

## Collecte automatique des données

### Exemple : Récupération depuis une base de données

```python
import psycopg2
import json

def collect_weekly_data():
    conn = psycopg2.connect("dbname=mydb user=user password=pass")
    cur = conn.cursor()

    # Récupérer les KPIs
    cur.execute("""
        SELECT metric_name, metric_value, change_percent
        FROM weekly_kpis
        WHERE week = CURRENT_WEEK
    """)

    kpis = []
    for row in cur.fetchall():
        kpis.append({
            "label": row[0],
            "value": str(row[1]),
            "change": f"+{row[2]}%",
            "type": "success" if row[2] > 0 else "warning"
        })

    # Construire le JSON
    data = {
        "week_start": "...",
        "week_end": "...",
        "kpis": kpis,
        # ... autres données
    }

    # Sauvegarder
    with open('data/current_week.json', 'w') as f:
        json.dump(data, f, indent=2)

    conn.close()

# Exécuter avant la génération du rapport
collect_weekly_data()
```

### Exemple : Récupération depuis une API

```python
import requests
import json

def collect_from_api():
    response = requests.get('https://api.example.com/metrics/weekly')
    api_data = response.json()

    # Transformer au format requis
    report_data = {
        "week_start": api_data['period']['start'],
        "week_end": api_data['period']['end'],
        "kpis": [
            {
                "label": "Utilisateurs",
                "value": str(api_data['users']['total']),
                "change": f"+{api_data['users']['growth']}%",
                "type": "success"
            },
            # ... autres KPIs
        ],
        # ... autres sections
    }

    with open('data/current_week.json', 'w') as f:
        json.dump(report_data, f, indent=2)
```

---

## Dépannage

### Erreur : "OSError: cannot load library"

WeasyPrint nécessite des dépendances système. Voir [Installation](#installation).

### Le graphique ne s'affiche pas

Vérifiez que `chart_data` contient bien des dates au format `YYYY-MM-DD` et des valeurs numériques.

### Le PDF est vide ou mal formaté

Vérifiez la structure de votre JSON avec :

```bash
python -m json.tool data/ma_semaine.json
```

### Problème d'encodage des caractères

Assurez-vous que vos fichiers JSON sont en UTF-8 :

```python
with open('data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
```

---

## Prochaines améliorations possibles

- [ ] Envoi automatique par email (intégration SendGrid/SMTP)
- [ ] Support de graphiques multiples
- [ ] Export vers d'autres formats (Excel, PowerPoint)
- [ ] Interface web pour éditer les données
- [ ] Génération de rapports comparatifs (semaine N vs N-1)
- [ ] Intégration avec Google Analytics, Mixpanel, etc.
- [ ] Templates multiples (différents clients/projets)

---

## Support

Pour toute question ou problème, consultez :
- Documentation WeasyPrint : https://weasyprint.org/
- Documentation Jinja2 : https://jinja.palletsprojects.com/
- Les données d'exemple dans `src/data/example_data.json`
