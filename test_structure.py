#!/usr/bin/env python3
"""
Script de validation de la structure du projet
Vérifie que tous les fichiers nécessaires sont présents et valides
"""

import os
import json
from pathlib import Path


def test_project_structure():
    """Vérifie la structure du projet"""
    print("🔍 Vérification de la structure du projet...")

    required_files = [
        'requirements.txt',
        'src/generate_report.py',
        'src/templates/weekly_report.html',
        'src/data/example_data.json',
        'USAGE.md',
        'PROPOSITIONS_FORMATS.md'
    ]

    required_dirs = [
        'src',
        'src/templates',
        'src/data',
        'output'
    ]

    # Vérifier les répertoires
    all_ok = True
    for directory in required_dirs:
        if os.path.isdir(directory):
            print(f"  ✅ Répertoire '{directory}' présent")
        else:
            print(f"  ❌ Répertoire '{directory}' manquant")
            all_ok = False

    # Vérifier les fichiers
    for file_path in required_files:
        if os.path.isfile(file_path):
            print(f"  ✅ Fichier '{file_path}' présent")
        else:
            print(f"  ❌ Fichier '{file_path}' manquant")
            all_ok = False

    return all_ok


def test_json_validity():
    """Vérifie la validité du JSON d'exemple"""
    print("\n🔍 Vérification du fichier de données d'exemple...")

    try:
        with open('src/data/example_data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)

        required_keys = [
            'week_start', 'week_end', 'executive_summary',
            'kpis', 'projects', 'attention_points', 'next_steps'
        ]

        all_ok = True
        for key in required_keys:
            if key in data:
                print(f"  ✅ Clé '{key}' présente")
            else:
                print(f"  ❌ Clé '{key}' manquante")
                all_ok = False

        # Vérifications spécifiques
        if 'kpis' in data and len(data['kpis']) > 0:
            kpi = data['kpis'][0]
            if 'label' in kpi and 'value' in kpi:
                print(f"  ✅ Structure des KPIs valide")
            else:
                print(f"  ❌ Structure des KPIs invalide")
                all_ok = False

        return all_ok

    except json.JSONDecodeError as e:
        print(f"  ❌ Erreur de parsing JSON : {e}")
        return False
    except FileNotFoundError:
        print(f"  ❌ Fichier example_data.json non trouvé")
        return False


def test_template():
    """Vérifie que le template HTML contient les sections essentielles"""
    print("\n🔍 Vérification du template HTML...")

    try:
        with open('src/templates/weekly_report.html', 'r', encoding='utf-8') as f:
            content = f.read()

        required_sections = [
            'executive_summary',
            'kpis',
            'projects',
            'attention_points',
            'next_steps'
        ]

        all_ok = True
        for section in required_sections:
            if section in content:
                print(f"  ✅ Section '{section}' présente dans le template")
            else:
                print(f"  ❌ Section '{section}' manquante dans le template")
                all_ok = False

        return all_ok

    except FileNotFoundError:
        print(f"  ❌ Template HTML non trouvé")
        return False


def main():
    """Point d'entrée principal"""
    print("=" * 60)
    print("  VALIDATION DU PROJET WEEKLY REPORT GENERATOR")
    print("=" * 60)

    results = []

    results.append(("Structure du projet", test_project_structure()))
    results.append(("Données JSON", test_json_validity()))
    results.append(("Template HTML", test_template()))

    print("\n" + "=" * 60)
    print("  RÉSUMÉ")
    print("=" * 60)

    all_passed = True
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
        if not result:
            all_passed = False

    print("=" * 60)

    if all_passed:
        print("\n🎉 Tous les tests sont passés avec succès !")
        print("\nProchaines étapes :")
        print("  1. Installer les dépendances : pip install -r requirements.txt")
        print("  2. Générer un rapport test : cd src && python generate_report.py data/example_data.json")
        print("  3. Consulter USAGE.md pour plus d'informations")
        return 0
    else:
        print("\n⚠️  Certains tests ont échoué. Veuillez corriger les erreurs.")
        return 1


if __name__ == '__main__':
    exit(main())
