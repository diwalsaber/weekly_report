#!/usr/bin/env python3
"""
Exemple de script de collecte automatique de données
Ce script montre comment récupérer des données depuis diverses sources
et les formater pour le générateur de rapport
"""

import json
from datetime import datetime, timedelta


def collect_from_database():
    """
    Exemple : Collecte depuis une base de données
    À adapter selon votre système (PostgreSQL, MySQL, MongoDB, etc.)
    """
    # Exemple avec psycopg2 (PostgreSQL)
    # import psycopg2
    #
    # conn = psycopg2.connect(
    #     host="localhost",
    #     database="mydb",
    #     user="user",
    #     password="password"
    # )
    # cur = conn.cursor()
    #
    # cur.execute("""
    #     SELECT metric_name, metric_value, change_percent
    #     FROM weekly_metrics
    #     WHERE week_start = %s
    # """, (week_start,))
    #
    # return cur.fetchall()

    # Données simulées
    return {
        'active_users': {'current': 12450, 'change': 15},
        'response_time': {'current': 340, 'change': -40},
        'conversion_rate': {'current': 3.8, 'change': 0.5}
    }


def collect_from_api():
    """
    Exemple : Collecte depuis une API externe
    (Google Analytics, Mixpanel, API interne, etc.)
    """
    # Exemple avec requests
    # import requests
    #
    # response = requests.get(
    #     'https://api.example.com/metrics/weekly',
    #     headers={'Authorization': f'Bearer {API_KEY}'}
    # )
    # return response.json()

    # Données simulées
    return {
        'new_users': 1240,
        'retention_rate': 68,
        'revenue': 45200
    }


def collect_project_status():
    """
    Exemple : Collecte du statut des projets
    (depuis Jira, GitHub, Asana, etc.)
    """
    # Exemple avec Jira
    # from jira import JIRA
    #
    # jira = JIRA(server='https://your-domain.atlassian.net',
    #             basic_auth=('email', 'api_token'))
    #
    # issues = jira.search_issues('project=PROJ AND sprint in openSprints()')
    #
    # projects = []
    # for issue in issues:
    #     projects.append({
    #         'name': issue.fields.summary,
    #         'status': issue.fields.status.name,
    #         'progress': calculate_progress(issue)
    #     })
    # return projects

    # Données simulées
    return [
        {
            'name': 'Module d\'Authentification SSO',
            'status': 'completed',
            'status_label': 'Terminé',
            'progress': 100,
            'owner': 'Équipe Backend'
        },
        {
            'name': 'Refonte Dashboard Analytique',
            'status': 'in-progress',
            'status_label': 'En cours',
            'progress': 75,
            'owner': 'Équipe Frontend'
        }
    ]


def collect_time_series_data():
    """
    Exemple : Collecte de données temporelles pour les graphiques
    """
    # Simuler 7 jours de données
    today = datetime.now()
    dates = [(today - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(6, -1, -1)]

    # Données simulées (à remplacer par vraies requêtes)
    values = [10500, 11200, 10800, 12100, 12450, 11900, 12300]

    return {
        'title': 'Évolution des Utilisateurs Actifs Quotidiens',
        'label': 'Utilisateurs',
        'dates': dates,
        'values': values
    }


def generate_weekly_data():
    """
    Fonction principale : agrège toutes les sources de données
    et génère le fichier JSON final
    """
    # Calculer les dates de la semaine
    today = datetime.now()
    week_start = (today - timedelta(days=today.weekday())).strftime('%d %B %Y')
    week_end = (today - timedelta(days=today.weekday() - 6)).strftime('%d %B %Y')

    # Collecter les données depuis différentes sources
    db_metrics = collect_from_database()
    api_metrics = collect_from_api()
    projects = collect_project_status()
    chart_data = collect_time_series_data()

    # Construire la structure de données pour le rapport
    report_data = {
        'week_start': week_start,
        'week_end': week_end,

        'executive_summary': [
            'Point clé automatiquement identifié basé sur les données',
            f"Croissance de {db_metrics['active_users']['change']}% des utilisateurs actifs",
            f"Amélioration de {abs(db_metrics['response_time']['change'])}% du temps de réponse",
            f"{len([p for p in projects if p['status'] == 'completed'])} projets complétés cette semaine"
        ],

        'kpis': [
            {
                'label': 'Utilisateurs Actifs',
                'value': f"{db_metrics['active_users']['current']:,}",
                'change': f"+{db_metrics['active_users']['change']}% vs semaine précédente",
                'type': 'success'
            },
            {
                'label': 'Temps de Réponse Moyen',
                'value': f"{db_metrics['response_time']['current']}ms",
                'change': f"{db_metrics['response_time']['change']}% (amélioration)",
                'type': 'success'
            },
            {
                'label': 'Taux de Conversion',
                'value': f"{db_metrics['conversion_rate']['current']}%",
                'change': f"+{db_metrics['conversion_rate']['change']} points",
                'type': 'info'
            },
            {
                'label': 'Nouveaux Utilisateurs',
                'value': f"{api_metrics['new_users']:,}",
                'change': 'Cette semaine',
                'type': 'info'
            },
            {
                'label': 'Taux de Rétention',
                'value': f"{api_metrics['retention_rate']}%",
                'change': 'Objectif atteint',
                'type': 'success'
            },
            {
                'label': 'Revenus',
                'value': f"€{api_metrics['revenue']:,}",
                'change': '+7.6% vs semaine précédente',
                'type': 'success'
            }
        ],

        'chart_data': chart_data,

        'projects': projects,

        'detailed_metrics': [
            {
                'name': 'Nouveaux Utilisateurs',
                'current': f"{api_metrics['new_users']:,}",
                'target': '1,000',
                'evolution': f"+{((api_metrics['new_users'] - 1000) / 1000 * 100):.1f}%"
            },
            {
                'name': 'Taux de Rétention (J+7)',
                'current': f"{api_metrics['retention_rate']}%",
                'target': '65%',
                'evolution': f"+{api_metrics['retention_rate'] - 65} points"
            },
            {
                'name': 'Revenus Hebdomadaires',
                'current': f"€{api_metrics['revenue']:,}",
                'target': '€42,000',
                'evolution': f"+{((api_metrics['revenue'] - 42000) / 42000 * 100):.1f}%"
            }
        ],

        'attention_points': [
            {
                'title': 'Point d\'attention automatique',
                'description': 'Ce point pourrait être généré automatiquement basé sur des seuils ou anomalies détectées dans les données.'
            }
        ],

        'next_steps': [
            {
                'action': 'Action générée automatiquement basée sur les données',
                'deadline': (datetime.now() + timedelta(days=7)).strftime('%d %B %Y'),
                'owner': 'Équipe concernée'
            }
        ]
    }

    return report_data


def main():
    """Point d'entrée principal"""
    print("🔄 Collecte des données en cours...")

    # Générer les données
    data = generate_weekly_data()

    # Sauvegarder dans un fichier JSON
    output_file = 'data/current_week.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"✅ Données collectées et sauvegardées dans {output_file}")
    print(f"\nVous pouvez maintenant générer le rapport avec :")
    print(f"  python generate_report.py {output_file}")

    return data


if __name__ == '__main__':
    main()
