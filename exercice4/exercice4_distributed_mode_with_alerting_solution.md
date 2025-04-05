# 🚀 Installation complète d'une Stack d'observabilité sur Kubernetes avec Helmfile et Kind

Ce document décrit étape par étape l'installation d'une stack complète comprenant **Prometheus**, **Grafana**, **Loki**, **Alertmanager**, **Mailhog**, **Alloy** et une application Python personnalisée dans un cluster Kubernetes local (Kind).

## 📋 Prérequis

Avant de commencer, assurez-vous que ces outils sont installés sur votre machine :

- [Docker](https://docs.docker.com/get-docker/) 🐳
- [Kind](https://kind.sigs.k8s.io/docs/user/quick-start/) 📦
- [Kubectl](https://kubernetes.io/docs/tasks/tools/) 🔧
- [Helm](https://helm.sh/docs/intro/install/) 🎩
- [Helmfile](https://github.com/helmfile/helmfile#installation) 📄

## 🛠️ Installation

### 1️⃣ Création du cluster Kind

Créez un fichier nommé `kind-cluster.yaml` avec ce contenu :

```yaml
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
name: local
nodes:
- role: control-plane
- role: worker
- role: worker
- role: worker
```

Puis lancez la création du cluster :

```bash
kind create cluster --config kind-cluster.yaml
```

### 2️⃣ Chargement de l'image Docker locale dans Kind

Construisez votre image Docker pour l'application Python :

```bash
docker build -t flotte-interstellaire:latest .
kind load docker-image flotte-interstellaire:latest --name local
```

### 3️⃣ Configuration des fichiers Helmfile

Créez un fichier `helmfile.yaml` avec la configuration donnée initialement, en spécifiant ces configurations spécifiques :

**🔧 Alloy configuration (`alloy-values.yaml`) :** (voir configuration fournie précédemment)

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

**🔧 Loki configuration (`loki-values.yaml`) :**

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
  rulerConfig:
    enable_api: true
    enable_alertmanager_v2: true
    external_url: "http://prometheus-alertmanager:9093"
    alertmanager_url: "http://prometheus-alertmanager:9093"
    rule_path: /tmp/loki/rules/
    storage:
      type: local
      local:
        directory: /etc/loki/rules

deploymentMode: Distributed

ingester:
  replicas: 3  # To ensure data durability with replication
  zoneAwareReplication:
    enabled: false
querier:
  replicas: 3  # Improve query performance via parallelism
  maxUnavailable: 2
queryFrontend:
  replicas: 2
  maxUnavailable: 1
queryScheduler:
  replicas: 2
distributor:
  replicas: 3
  maxUnavailable: 2
compactor:
  replicas: 1
indexGateway:
  replicas: 2
  maxUnavailable: 1

bloomPlanner:
  replicas: 0
bloomBuilder:
  replicas: 0
bloomGateway:
  replicas: 0

# Zero out replica counts of other deployment modes
backend:
  replicas: 0
read:
  replicas: 0
write:
  replicas: 0

singleBinary:
  replicas: 0

# Expose the Loki gateway externally via a LoadBalancer.
gateway:
  service:
    type: ClusterIP

# Enable Minio for object storage.
minio:
  enabled: true

# Ruler configuration for alerting.
ruler:
  replicas: 1
  enabled: true
  extraVolumes:
    - name: fake
      emptyDir: {}
  extraVolumeMounts:
    - name: fake
      mountPath: /tmp/loki/rules/
  persistence:
    enabled: true
    size: 1Gi
  directories:
    fake:
      rules.txt: |
        groups:
        - name: FlotteInterstellaireAlerts
          rules:
          - alert: ErrorLogDetected
            expr: sum(count_over_time({pod_name=~"flotte-interstellaire.*"} |= "ERROR" [5m])) by (pod_name) > 0
            for: 1m
            labels:
              severity: critical
            annotations:
              summary: "Erreur détectée dans les logs"
              description: "Des erreurs ont été détectées dans les logs de l'application flotte-interstellaire durant la dernière minute."
```

**🔧 Prometheus Alertmanager configuration (`prometheus-values.yaml`) :**

```yaml
alertmanager:
  config:
    global:
      resolve_timeout: 1m
      smtp_smarthost: 'mailhog:1025'
      smtp_from: 'alertmanager@loki.local'
      smtp_require_tls: false
    route:
      group_by: ['alertname']
      group_wait: 30s
      group_interval: 1m
      repeat_interval: 5m
      receiver: 'email'
    receivers:
    - name: 'email'
      email_configs:
      - to: 'hamdi@loki.local'
```

### 4️⃣ Installation avec Helmfile

Exécutez cette commande pour installer toute la stack :

```bash
helmfile sync
```

✅ Votre stack est installée !

## 🔍 Vérifications

Vérifiez que tout fonctionne bien :

```bash
kubectl get pods -n monitoring
kubectl get pods -n app
```

## 🌐 Accès aux interfaces

- Grafana : utilisez `kubectl port-forward` pour accéder à Grafana :

```bash
kubectl port-forward svc/grafana -n monitoring 3000:80
```

Puis ouvrez [http://localhost:3000](http://localhost:3000). Identifiant : `admin`, Mot de passe : `admin`

- Mailhog (pour tester les emails) :

```bash
kubectl port-forward svc/mailhog -n monitoring 8025:8025
```

Accès via [http://localhost:8025](http://localhost:8025).

## 📜 Logs de l'application Python

L'application génère des logs visibles avec :

```bash
kubectl logs -f <pod-app-python> -n app
```

## 🛑 Désinstallation

Pour tout nettoyer facilement :

```bash
helmfile destroy
kind delete cluster --name local
```

🎉 Voilà ! Votre environnement Kubernetes local avec stack complète d'observabilité est prêt à l'emploi ! 🚀✨
