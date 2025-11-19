#!/usr/bin/env python3
"""
Weekly Report Generator
Génère un rapport hebdomadaire au format PDF à partir de données JSON
"""

import json
import os
from datetime import datetime
from pathlib import Path
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML, CSS
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from io import BytesIO
import base64


class WeeklyReportGenerator:
    """Générateur de rapports hebdomadaires en PDF"""

    def __init__(self, template_dir="templates", output_dir="../output"):
        """
        Initialise le générateur

        Args:
            template_dir: Répertoire contenant les templates HTML
            output_dir: Répertoire de sortie pour les PDFs
        """
        self.base_dir = Path(__file__).parent
        self.template_dir = self.base_dir / template_dir
        self.output_dir = self.base_dir / output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Configure Jinja2
        self.env = Environment(loader=FileSystemLoader(str(self.template_dir)))

    def create_chart(self, data):
        """
        Crée un graphique d'évolution

        Args:
            data: Données pour le graphique (dict avec dates et valeurs)

        Returns:
            Chemin vers l'image du graphique encodée en base64
        """
        if not data or 'dates' not in data or 'values' not in data:
            return None

        fig, ax = plt.subplots(figsize=(10, 4))

        dates = [datetime.strptime(d, '%Y-%m-%d') for d in data['dates']]
        values = data['values']

        ax.plot(dates, values, marker='o', linewidth=2, markersize=8, color='#3498db')
        ax.fill_between(dates, values, alpha=0.3, color='#3498db')

        ax.set_xlabel('Date', fontsize=12)
        ax.set_ylabel(data.get('label', 'Valeur'), fontsize=12)
        ax.set_title(data.get('title', 'Évolution'), fontsize=14, fontweight='bold')

        ax.grid(True, alpha=0.3)
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m'))

        plt.tight_layout()

        # Convertir en base64 pour inclusion dans HTML
        buffer = BytesIO()
        plt.savefig(buffer, format='png', dpi=150, bbox_inches='tight')
        plt.close(fig)
        buffer.seek(0)

        image_base64 = base64.b64encode(buffer.read()).decode()
        return f"data:image/png;base64,{image_base64}"

    def load_data(self, data_path):
        """
        Charge les données depuis un fichier JSON

        Args:
            data_path: Chemin vers le fichier de données

        Returns:
            Dictionnaire contenant les données
        """
        with open(data_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def generate_pdf(self, data_path, output_filename=None):
        """
        Génère le rapport PDF

        Args:
            data_path: Chemin vers le fichier de données JSON
            output_filename: Nom du fichier PDF de sortie (optionnel)

        Returns:
            Chemin vers le fichier PDF généré
        """
        # Charger les données
        data = self.load_data(data_path)

        # Ajouter la date de génération
        data['generation_date'] = datetime.now().strftime('%d/%m/%Y à %H:%M')

        # Créer le graphique si des données sont présentes
        if 'chart_data' in data:
            data['chart_path'] = self.create_chart(data['chart_data'])

        # Charger et rendre le template
        template = self.env.get_template('weekly_report.html')
        html_content = template.render(**data)

        # Générer le nom du fichier de sortie
        if output_filename is None:
            week_start = data.get('week_start', datetime.now().strftime('%Y-%m-%d'))
            output_filename = f"weekly_report_{week_start}.pdf"

        output_path = self.output_dir / output_filename

        # Générer le PDF
        HTML(string=html_content, base_url=str(self.template_dir)).write_pdf(
            output_path,
            stylesheets=None,
            presentational_hints=True
        )

        print(f"✅ Rapport généré avec succès : {output_path}")
        return str(output_path)

    def generate_and_send(self, data_path, recipients, smtp_config=None):
        """
        Génère le rapport et l'envoie par email

        Args:
            data_path: Chemin vers le fichier de données
            recipients: Liste des destinataires
            smtp_config: Configuration SMTP (optionnel)

        Returns:
            Chemin vers le fichier PDF généré
        """
        # Générer le PDF
        pdf_path = self.generate_pdf(data_path)

        # Envoyer par email (à implémenter selon le service utilisé)
        if smtp_config:
            self._send_email(pdf_path, recipients, smtp_config)
        else:
            print(f"ℹ️  Email non configuré. PDF disponible à : {pdf_path}")

        return pdf_path

    def _send_email(self, pdf_path, recipients, smtp_config):
        """
        Envoie le rapport par email

        Args:
            pdf_path: Chemin vers le PDF
            recipients: Liste des destinataires
            smtp_config: Configuration SMTP
        """
        # TODO: Implémenter l'envoi d'email
        # Exemple avec SendGrid, SMTP, etc.
        print(f"📧 Envoi du rapport à {', '.join(recipients)}...")
        print("⚠️  Fonction d'envoi à implémenter selon votre service email")


def main():
    """Point d'entrée principal"""
    import argparse

    parser = argparse.ArgumentParser(description='Génère un rapport hebdomadaire en PDF')
    parser.add_argument('data', help='Chemin vers le fichier de données JSON')
    parser.add_argument('-o', '--output', help='Nom du fichier de sortie (optionnel)')
    parser.add_argument('--send', nargs='+', help='Envoyer par email aux destinataires spécifiés')

    args = parser.parse_args()

    # Créer le générateur
    generator = WeeklyReportGenerator()

    # Générer le rapport
    if args.send:
        generator.generate_and_send(args.data, args.send)
    else:
        generator.generate_pdf(args.data, args.output)


if __name__ == '__main__':
    main()
