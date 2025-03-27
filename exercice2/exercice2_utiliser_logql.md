# 🛰️ Exercice Pratique : LogQL & Loki avec Grafana

Bienvenue dans cet exercice gamifié qui te fera découvrir et pratiquer LogQL en utilisant Loki pour analyser des logs d'une flotte spatiale imaginaire. 🚀

## 🚧 Prérequis

- Grafana
- Loki
- Grafana Alloy
- Python

## 🛠️ Installation et configuration

1. **Clone ce dépôt**.

2. **Génère des logs** en exécutant l'application Python :

    ```bash
    python log_generator_app.py
    ```

3. **Configure Grafana Alloy** avec la configuration fournie (`grafana_alloy_config`).

4. Lance Alloy et Grafana.

## 🎯 Objectifs des défis

- **Défi 1 :** Trouver les logs du vaisseau `StarSeeker`.
- **Défi 2 :** Identifier tous les logs contenant "ERROR".
- **Défi 3 :** Compter les erreurs toutes les 5 minutes.
- **Défi 4 :** Vérifier les messages envoyés par le pilote `Zara`.

Bonne exploration ! 🌌🚀
