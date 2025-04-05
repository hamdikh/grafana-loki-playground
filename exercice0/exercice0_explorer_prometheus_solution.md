# 📈 Installer Prometheus et Alertmanager sur Minikube

## 🧰 Prérequis

Avant de commencer, assure-toi d’avoir installé :

- [Minikube](https://minikube.sigs.k8s.io/docs/start/)
- [kubectl](https://kubernetes.io/docs/tasks/tools/)
- [Helm](https://helm.sh/docs/intro/install/)

Et d’avoir démarré ton cluster Minikube :

```bash
minikube start
```

## 🚀 Étape 1 : Créer un namespace

```bash
kubectl create namespace monitoring
```

## 📦 Étape 2 : Installer Prometheus avec Alertmanager via Helm

```bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update

helm install prometheus prometheus-community/prometheus \
  --namespace monitoring
```

✅ Ce chart installe automatiquement :

- Prometheus
- Alertmanager
- Node Exporter
- Pushgateway (optionnel)

## 🌐 Étape 3 : Accéder à l’interface web de Prometheus

```bash
kubectl port-forward -n monitoring deploy/prometheus-server 9090
```

👉 Ensuite, ouvre ton navigateur à l'adresse suivante :  
http://localhost:9090

## 🧹 Étape 4 : Nettoyer l’installation (optionnel)

```bash
helm uninstall prometheus -n monitoring
kubectl delete namespace monitoring
```
