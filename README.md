# pygandi

CLI pour gérer les enregistrements DNS sur [Gandi.net](https://gandi.net/)

J'utilise le gestionnaire de paquets [uv](https://docs.astral.sh/uv/) pour gérer l'environnement Python et les dépendances.

## Installation et Construction

Les commandes suivantes sont disponibles via `make` :

| Commande | Description |
|----------|-------------|
| `help` | Affiche l'aide pour cette commande (par défaut) |
| `install-uv` | Installe le gestionnaire de paquets uv s'il n'est pas déjà installé |
| `clean` | Nettoie les artefacts de construction et l'environnement virtuel |
| `venv` | Crée l'environnement virtuel et installe les dépendances |
| `build` | Construit le paquet Python |
| `tests` | Lance la suite de tests |
| `image` | Crée l'image Docker locale |
| `image-test` | Lance les tests de l'image Docker |
| `image-push` | Pousse l'image locale vers Docker Hub |

## Guide d'Installation

1. **Installer le gestionnaire de paquets uv** :
   ```bash
   make install-uv
   ```

2. **Lancer le linter et la suite de tests** :
   ```bash
   make tests
   ```

3. **Construire le paquet Python** (tgz et whl) :
   ```bash
   make build
   ```

4. **Installer le paquet wheel** sur votre système :
   ```bash
   uv pip install dist/pygandi-<version>-py3-none-any.whl
   ```
   ou avec pipx :
   ```bash
   pipx install dist/pygandi-<version>-py3-none-any.whl
   ```

5. **Construire l'image Docker** :
   ```bash
   make image
   ```

## Développement

Pour installer l'environnement Python :
```bash
make venv
```

Cette commande installe les bibliothèques de dépendances et active un environnement virtuel.

Pour lancer le script :
```bash
API_TOKEN=xxxxx uv run pygandi --help
```

## Utilisation

```
usage: pygandi [-h] [--ttl TTL] [--noipv4] [--noipv6] [--dry-run] [--log LOG] zone record [record ...]
```

### Description

Utilitaire pour maintenir à jour vos enregistrements DNS avec votre IP actuelle.
Fonctionne avec les services API de Gandi.net.

### Authentication

Pour s'authentifier avec l'API Gandi, passez votre token comme variable d'environnement :
```bash
API_TOKEN=xxxxxxxxxx
```

Version actuelle : 0.1.6

### Arguments

| Argument | Description |
|----------|-------------|
| `zone` | Zone à mettre à jour |
| `record` | Enregistrements à mettre à jour |

### Options

| Option | Description |
|--------|-------------|
| `-h, --help` | Affiche l'aide et quitte |
| `--ttl TTL` | Définit un TTL personnalisé (en secondes) |
| `--noipv4` | Ne pas définir les enregistrements 'A' avec l'IPv4 actuelle |
| `--noipv6` | Ne pas définir les enregistrements 'AAAA' avec l'IPv6 actuelle |
| `--dry-run` | Effectue une simulation sans rien modifier |
| `--log LOG` | Niveaux disponibles : CRITICAL (3), ERROR (2), WARNING (1), INFO (0), DEBUG (-1) |

## Installation comme Tâche CRON

Ajoutez un fichier dans votre dossier `/etc/cron.d`

Exemple (`gandi-dns-update`) :
```bash
5 * * * * root test -x pygandi && API_TOKEN=xxxxxxxxxx ; pygandi example.com www subdomain1 subdomain2
```

## Image Docker

Vous pouvez utiliser une image docker pour lancer dans kubernetes comme cronjob :
[DockerHub](https://hub.docker.com/repository/docker/freuds2k/pygandi)
