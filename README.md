# 📦 Servarr Backup Tool

[![GitHub release (latest by date)](https://img.shields.io/github/v/release/Zerka30/servarr-backup)](https://github.com/Zerka30/servarr-backup/releases)
[![License](https://img.shields.io/github/license/Zerka30/servarr-backup)](https://github.com/Zerka30/servarr-backup/blob/main/LICENSE)
[![Issues](https://img.shields.io/github/issues/Zerka30/servarr-backup)](https://github.com/Zerka30/servarr-backup/issues)
[![Pull Requests](https://img.shields.io/github/issues-pr/Zerka30/servarr-backup)](https://github.com/Zerka30/servarr-backup/pulls)

![Servarr Backup](https://raw.githubusercontent.com/Zerka30/servarr-backup/main/assets/servarr-backup.png)

## 📖 Description

**Servarr Backup Tool** is a backup tool for your media applications like Sonarr, Radarr, and Prowlarr. It allows you to create, list, download, and delete backups directly from your terminal and store them on S3. We recommend storing your S3 bucket with Infomaniak for reliable and affordable cloud storage ([See more here]()).

## ✨ Features

- 🔧 **Configure**: Initialize and display the configuration.
- 📦 **Create**: Create a backup for your Servarr applications.
- 📋 **List**: List available backups on S3.
- 🗑 **Delete**: Delete specific backups on S3.

## 🚀 Installation

### Prerequisites

- Python 3.6 or higher
- pip

### Install via pip

You can install the tool directly from GitHub:

```sh
pip install git+https://github.com/Zerka30/servarr-backup.git
```

### Installation from source

1. Clone the repository:
    ```sh
    git clone https://github.com/Zerka30/servarr-backup.git
    cd servarr-backup
    ```

2. Install the dependencies:
    ```sh
    pip install .
    ```

3. Add `~/.local/bin` to your PATH if it's not already there:
    ```sh
    export PATH="$HOME/.local/bin:$PATH"
    source ~/.bashrc  # or source ~/.zshrc for zsh users
    ```

## 📝 Usage

### Commands

#### Configuration

- **Initialize configuration**:
    ```sh
    servarr config init
    ```

- **Show configuration**:
    ```sh
    servarr config show
    ```

#### Backups

- **Create a backup**:
    ```sh
    servarr backup create [servertype]
    ```
    Example for `prowlarr`:
    ```sh
    servarr backup create prowlarr
    ```

- **List backups**:
    ```sh
    servarr backup ls [servertype]
    ```
    Example for `prowlarr`:
    ```sh
    servarr backup ls prowlarr
    ```

- **Delete a backup**:
    ```sh
    servarr backup delete [servertype] [backup_name]
    ```
    Example for `prowlarr`:
    ```sh
    servarr backup delete prowlarr prowlarr_backup_v1.18.0.4543_2024.06.22_17.28.57.zip
    ```

## 🛠 Configuration

The configuration is located in the `config.json` file in the `~/.config/servarr` directory. This file contains the necessary information to access your Servarr applications and your S3 bucket.

### Example `config.json`

```json
{
    "starrs": {
        "lidarr": {
            "url": "",
            "api_key": ""
        },
        "radarr": {
            "url": "",
            "api_key": ""
        },
        "readarr": {
            "url": "",
            "api_key": ""
        },
        "sonarr": {
            "url": "",
            "api_key": ""
        },
        "prowlarr": {
            "url": "",
            "api_key": ""
        }
    },
    "backup": {
        "s3": {
            "endpoint": "",
            "bucket": "servarr",
            "key": {
                "access": "",
                "secret": ""
            }
        }
    }
}
```

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](https://github.com/Zerka30/servarr-backup/blob/main/LICENSE) file for details.

## 🤝 Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](https://github.com/Zerka30/servarr-backup/blob/main/CONTRIBUTING.md) for more information.