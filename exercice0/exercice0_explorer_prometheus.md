# ⚔️ Mission : *L'Œil de Prometheus* - Édition Kind 🐳

> 🕵️ Votre mission, si vous l’acceptez, est d’installer et de configurer **Prometheus**, le gardien des métriques, sur un cluster Kubernetes local propulsé par **Kind**, sans utiliser de solutions managées ou simplificatrices comme Minikube.  
> Préparez-vous à entrer dans le monde brut et réel du monitoring Kubernetes. 🛡️

## 🛠️ Les outils du héros

- 🐳 **Kind** : votre forge pour créer un cluster Kubernetes local.
- 📡 **Prometheus** : votre sentinelle des métriques.
- 🧠 **Kubectl** et **Helm** : vos baguettes magiques pour parler au cluster.


## 🎖️ Objectifs à atteindre

### 🔨 Étape 1 : Forgez votre royaume

- 🧱 Installez et configurez Kind sur votre machine.
- 🏰 Créez un cluster Kubernetes nommé `prometheus-cluster`.

### 🗂️ Étape 2 : Le sanctuaire des métriques

- 🌀 Créez un namespace dédié : `monitoring`.
- 📦 Ajoutez le dépôt Helm de Prometheus.
- 🧙‍♂️ Déployez Prometheus via Helm dans ce namespace.

### 🔧 Étape 3 : Le portail mystique

- 🚪 Configurez un **port-forwarding** pour accéder à l’interface web de Prometheus depuis votre navigateur.
- 🌐 Accédez à Prometheus via [http://localhost:9090](http://localhost:9090).

### 🧪 Étape 4 : Les runes de PromQL

- 🔍 Interrogez la métrique `up` dans Prometheus.
- 🔮 Explorez quelques métriques disponibles et identifiez celles liées aux pods ou aux nodes.

## 🛡️ Contrôles finaux

- ✅ Tous les pods du namespace `monitoring` doivent être en état `Running`.
- ✅ L’interface web de Prometheus doit être accessible et afficher les métriques.
- ✅ Votre cluster doit apparaître dans l’onglet "Targets" de Prometheus.

## 🗺️ Ressources à disposition

📘 [Documentation officielle de Prometheus](https://prometheus.io/docs/introduction/overview/)  
📘 [Helm Charts Prometheus Community](https://github.com/prometheus-community/helm-charts)  
📘 [Kind - Kubernetes in Docker](https://kind.sigs.k8s.io/)

Bonne chance, opérateur. Que l’œil de Prometheus veille sur votre royaume. 👁️🔥
