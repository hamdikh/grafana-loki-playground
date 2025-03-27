# 🗝️ Solutions Complètes : À la Conquête de LogQL avec Loki 🌌

Voici toutes les solutions aux défis proposés dans l'exercice gamifié de LogQL avec Loki.

## 🎯 Solutions des Défis

### ✅ Solution Défi 1 : Retrouve le vaisseau perdu 🛰️

```logql
{vaisseau="StarSeeker"}
```

### ✅ Solution Défi 2 : Chasse au bug 🐛

```logql
{job="flotte-interstellaire"} |= "ERROR"
```

### ✅ Solution Défi 3 : La fréquence mystérieuse 📡

```logql
count_over_time({job="flotte-interstellaire"} |= "ERROR" [5m])
```

*Conseil : Affiche le résultat sous forme graphique pour mieux visualiser les périodes critiques.*

### ✅ Solution Défi 4 : Localise le pilote intrépide 👩‍🚀

```logql
count_over_time({pilote="Zara"} |= "mission accomplie" [24h])
```

Tu devrais obtenir exactement "3".

Bravo pour ton parcours ! Tu maîtrises désormais les bases de LogQL. Continue de pratiquer pour devenir un expert des journaux d'événements spatiaux ! 🌟🚀
