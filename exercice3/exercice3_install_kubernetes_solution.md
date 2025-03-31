# Exercice 🚀 : Mise en place d'un environnement Kubernetes de monitoring avec Docker, Minikube, Helm, Loki, Alloy et Grafana

## Objectifs 🎯

Déployer un environnement local complet de monitoring Kubernetes en utilisant Docker 🐳, Minikube 🖥️, Helm ⛵, Grafana Loki 📜, Alloy ⚙️ et Grafana 📊. À la fin de cet exercice, vous disposerez d'une plateforme de monitoring prête à l'emploi 👍.

## Étape 1 🔧 : Installer les pré-requis

```bash
sudo apt update
sudo apt-get install ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
```

## Étape 2 🐳 : Installer Docker

- **Docker** : plateforme de conteneurisation

```bash
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu $(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}") stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update
sudo apt-get install docker-ce
sudo systemctl status docker
```

## Étape 3 🚀 : Installer Minikube

- **Minikube** : outil pour lancer un cluster Kubernetes local

```bash
sudo curl -LO https://github.com/kubernetes/minikube/releases/latest/download/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube && rm minikube-linux-amd64
```

## Étape 4 🛠️ : Installer kubectl

- **kubectl** : outil en ligne de commande pour interagir avec Kubernetes

```bash
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl
```

## Étape 5 ⛵ : Installer Helm

- **Helm** : gestionnaire de paquets pour Kubernetes

```bash
curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3
chmod 700 get_helm.sh
./get_helm.sh
```

## Étape 6 🖥️ : Démarrer Minikube et créer un namespace

```bash
minikube start --force
kubectl get nodes
kubectl create namespace monitoring
```

## Étape 7 📦 : Ajouter le repository Helm de Grafana

```bash
helm repo add grafana https://grafana.github.io/helm-charts
```

## Étape 8 📜 : Installer Loki (agrégateur de logs)

Créer un fichier `loki-values.yaml` avec la configuration fournie dans l'exercice original.

```yaml
loki:
  auth_enabled: false
  schemaConfig:
    configs:
      - from: "2024-04-01"
        store: tsdb
        object_store: s3
        schema: v13
        index:
          prefix: loki_index_
          period: 24h
  ingester:
    chunk_encoding: snappy
  querier:
    max_concurrent: 4
  pattern_ingester:
    enabled: true
  limits_config:
    allow_structured_metadata: true
    volume_enabled: true
  commonConfig:
    replication_factor: 1

deploymentMode: SimpleScalable

backend:
  replicas: 1
read:
  replicas: 1
write:
  replicas: 1

minio:
  enabled: true
```

```bash
helm install --namespace monitoring --values loki-values.yaml loki grafana/loki
```

## Étape 9 🛠️ : Installer Alloy (outil de collecte et transmission de données)

Créer un fichier `alloy-values.yaml` avec la configuration suivante :

```yaml
alloy:
  configMap:
    content: |-
      discovery.kubernetes "pods" {
        role = "pod"
      }

      discovery.relabel "pods" {
        targets = discovery.kubernetes.pods.targets
        rule {
          action        = "replace"
          source_labels = ["__meta_kubernetes_namespace"]
          target_label  = "namespace"
        }
        rule {
          action        = "replace"
          source_labels = ["__meta_kubernetes_pod_name"]
          target_label  = "pod_name"
        }
        rule {
          action        = "replace"
          source_labels = ["__meta_kubernetes_pod_container_name"]
          target_label  = "container_name"
        }
      }

      loki.source.kubernetes "pods" {
        targets    = discovery.relabel.pods.output
        forward_to = [loki.write.local.receiver]
      }

      loki.write "local" {
        endpoint {
          url       = "http://loki-gateway.monitoring.svc.cluster.local/loki/api/v1/push"
        }
      }
```

```bash
helm install --namespace monitoring --values=alloy-values.yaml alloy grafana/alloy
```

## Étape 10 📊 : Installer Grafana

```bash
helm install grafana --namespace monitoring grafana/grafana
```

## Étape 11 🔑 : Accéder au dashboard Grafana

Récupérer le mot de passe administrateur :

```bash
kubectl get secret --namespace monitoring grafana -o jsonpath="{.data.admin-password}" | base64 --decode ; echo
```

Exposer Grafana sur le port 3000 :

```bash
export POD_NAME=$(kubectl get pods --namespace monitoring -l "app.kubernetes.io/name=grafana,app.kubernetes.io/instance=grafana" -o jsonpath="{.items[0].metadata.name}")
kubectl --namespace monitoring port-forward $POD_NAME 3000 --address 0.0.0.0
```

Vous pouvez accéder à Grafana via : `http://<adresse_ip_machine_locale>:3000` 🌐

## Étape 12 🔗 : Ajouter une datasource Loki

Depuis l'interface de Grafana, ajouter une datasource de type **Loki** ayant l'URL suivante :

```text
http://loki-gateway.monitoring.svc.cluster.local
```

## Étape 13 🔍 : Explorer les données fournies par Loki

```text
https://grafana.com/grafana/dashboards/
```