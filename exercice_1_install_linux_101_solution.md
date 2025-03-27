# Documentation Technique – Procédure Complète d’Installation : Loki, Grafana Alloy et Grafana (Sans Docker, avec services systemd)

## Introduction

Ce guide présente les instructions pour installer et configurer Loki, Alloy et Grafana. Il inclut également la mise en place de services `systemd` pour assurer le démarrage automatique des composants après chaque redémarrage système, et une gestion centralisée par le système d’init.

Les composants concernés sont :

- **Loki** – moteur de journalisation.
- **Alloy** – agent collecteur de logs, métriques et traces.
- **Grafana** – interface de visualisation des données.

---

## Pré-requis

- Distribution Linux compatible avec `systemd` (Debian 10+, Ubuntu 18.04+).
- Accès administrateur (sudo/root).
- Connexion Internet.
- Paquets essentiels installés : `wget` et `unzip`.

---

## Étape 1 – Installation et configuration de **Loki**

### 1.1 Téléchargement et préparation

```bash
cd /opt
sudo mkdir loki && cd loki
sudo wget https://github.com/grafana/loki/releases/download/v2.9.0/loki-linux-amd64.zip
sudo unzip loki-linux-amd64.zip
sudo mv loki-linux-amd64 loki
sudo chmod +x loki
```

### 1.2 Fichier de configuration
Créez les dossiers et fichiers nécessaires :

```bash
sudo mkdir -p /etc/loki /var/lib/loki /var/log/loki
sudo nano /etc/loki/config.yaml
```
Copiez cette configuration de base :
```yaml
auth_enabled: false

server:
  http_listen_port: 3100

common:
  ring:
    instance_addr: 127.0.0.1
    kvstore:
      store: inmemory
  replication_factor: 1
  path_prefix: /tmp/loki

schema_config:
  configs:
  - from: 2020-05-15
    store: tsdb
    object_store: filesystem
    schema: v13
    index:
      prefix: index_
      period: 24h

storage_config:
  filesystem:
    directory: /tmp/loki/chunks
```

### 1.3 Service systemd pour Loki

```bash
sudo nano /etc/systemd/system/loki.service
```

```ini
[Unit]
Description=Loki Log Aggregator
After=network.target

[Service]
ExecStart=/opt/loki/loki -config.file=/etc/loki/config.yaml
Restart=on-failure
User=root
WorkingDirectory=/var/lib/loki

[Install]
WantedBy=multi-user.target
```

### 1.4 Activation du service
Activez et démarrez le service :

```bash
sudo systemctl daemon-reexec
sudo systemctl daemon-reload
sudo systemctl enable --now loki.service
sudo systemctl start loki.service
```

---

## Étape 2 – Installation et configuration de **Grafana Alloy**

### 2.1 Téléchargement et installation

```bash
cd /opt
sudo mkdir alloy && cd alloy
sudo wget https://github.com/grafana/alloy/releases/latest/download/alloy-linux-amd64.zip
sudo unzip alloy-linux-amd64.zip
sudo mv alloy-linux-amd64 alloy
sudo chmod +x alloy
sudo mv alloy /usr/local/bin/alloy
```

### 2.2 Configuration d’Alloy
Créez les répertoires et le fichier de configuration :
```bash
sudo mkdir -p /etc/alloy /var/lib/alloy /var/log/alloy
sudo nano /etc/alloy/config.alloy
```
Configuration de base :
```
local.file_match "local_files" {
    path_targets = [{"__path__" = "/var/log/*.log"}]
    sync_period = "5s"
}

loki.source.file "log_scrape" {
  targets    = local.file_match.local_files.targets
  forward_to = [loki.write.grafana_loki.receiver]
} 

loki.write "grafana_loki" {
  endpoint {
    url = "http://localhost:3100/loki/api/v1/push"
  }
}
```

### 2.3 Service systemd pour Alloy

```bash
sudo nano /etc/systemd/system/alloy.service
```

```ini
[Unit]
Description=Vendor-neutral programmable observability pipelines.
Documentation=https://grafana.com/docs/alloy/
Wants=network-online.target
After=network-online.target

[Service]
Restart=always
Environment=HOSTNAME=%H
WorkingDirectory=/var/lib/alloy
ExecStart=/usr/local/bin/alloy run --storage.path=/var/lib/alloy /etc/alloy/config.alloy
ExecReload=/usr/bin/env kill -HUP $MAINPID
TimeoutStopSec=20s
SendSIGKILL=no

[Install]
WantedBy=multi-user.target
```

### 2.4 Activation du service
Activez et démarrez Alloy :
```bash
sudo systemctl daemon-reload
sudo systemctl enable --now alloy.service
sudo systemctl start alloy.service
```

---

## Étape 3 – Installation de **Grafana**

### 3.1 Téléchargement et installation

```bash
cd /opt
sudo mkdir grafana && cd grafana
wget https://dl.grafana.com/oss/release/grafana-10.3.1.linux-amd64.tar.gz
tar -zxvf grafana-10.3.1.linux-amd64.tar.gz
sudo mv grafana-v10.3.1 /usr/local/grafana
```

### 3.2 Service systemd pour Grafana
```bash
sudo nano /etc/systemd/system/grafana.service
```

```
[Unit]
Description=Grafana Dashboard
After=network.target

[Service]
ExecStart=/usr/local/grafana/bin/grafana-server \
  --homepath=/usr/local/grafana \
  --config=/usr/local/grafana/conf/defaults.ini
WorkingDirectory=/usr/local/grafana
Restart=always
LimitNOFILE=10000

[Install]
WantedBy=multi-user.target

```

### 3.3 Activation du service Grafana
Activez Grafana :
```bash
sudo systemctl daemon-reload
sudo systemctl enable --now grafana.service
sudo systemctl start grafana.service
```

---

## Étape 4 – Vérification de l’état des services

```bash
systemctl status loki
systemctl status alloy
systemctl status grafana
```

---

## Étape 5 – Configuration finale

1. Accédez à Grafana via [http://localhost:3000](http://localhost:3000)
2. Identifiants par défaut : `admin / admin`, à changer à la première connexion
3. Ajoutez **Loki** comme source de données (URL : `http://localhost:3100`)
4. Créez un tableau de bord avec LOKI comme source de données
5. En utilisant le filtre à base de `label`, selectionner filename = /var/log/auth.log
---

## Conclusion

Les trois outils sont désormais installés, configurés, et gérés de manière autonome par `systemd`. Ce mode de gestion permet une plus grande stabilité, une meilleure traçabilité et une intégration directe dans l’écosystème d’administration des systèmes Linux.

---

## Ressources

- [Loki Documentation](https://grafana.com/docs/loki/latest/)
- [Alloy Documentation](https://grafana.com/docs/alloy/latest/)
- [Grafana Documentation](https://grafana.com/docs/grafana/latest/)

