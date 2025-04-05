import logging
import random
import time

# Configuration du logger
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("fleet_logs.log"),
        logging.StreamHandler()
    ]
)

vaisseaux = ["StarSeeker", "GalaxyRunner", "NebulaX", "CosmosCruiser"]
pilotes = ["Zara", "Kane", "Luna", "Orion"]
messages = [
    "mission accomplie",
    "navigation stable",
    "ERROR: problème moteur",
    "réserve carburant faible",
    "ERROR: système navigation indisponible",
    "entrée atmosphérique réussie",
    "scan planète terminé"
]

logger = logging.getLogger("flotte-interstellaire")


def generer_log():
    vaisseau = random.choice(vaisseaux)
    pilote = random.choice(pilotes)
    message = random.choice(messages)

    log_message = f"vaisseau={vaisseau} pilote={pilote} message='{message}'"

    if "ERROR" in message:
        logger.error(log_message)
    else:
        logger.info(log_message)


if __name__ == "__main__":
    try:
        while True:
            generer_log()
            time.sleep(random.uniform(0.5, 2))
    except KeyboardInterrupt:
        print("Génération des logs interrompue.")

