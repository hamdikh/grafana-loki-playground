# Utilisation d'une image officielle Python légère
FROM python:3.9-slim

# Définition du répertoire de travail
WORKDIR /app

# Copier le fichier source dans le conteneur
COPY log_generator_app.py app.py 

# Exécuter l'application
CMD ["python", "app.py"]
