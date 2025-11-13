# Installation Guide

**Ultimate CLI Wallet GUI v2.0**

**Created by: Magnafic0 unchained & Gistgard Reventlov**

## Quick Start

### Linux

```bash
# 1. Extract the zip file
unzip ultimate-cli-wallet-gui.zip
cd ultimate-cli-wallet-gui

# 2. Install dependencies (if needed)
# Ubuntu/Debian:
sudo apt-get install python3 python3-tk

# Fedora:
sudo dnf install python3 python3-tkinter

# 3. Make launcher executable
chmod +x launch_wallet.sh

# 4. Run the GUI
./launch_wallet.sh
```

### macOS

```bash
# 1. Extract the zip file
unzip ultimate-cli-wallet-gui.zip
cd ultimate-cli-wallet-gui

# 2. Install Python (if needed)
# Download from python.org or use Homebrew:
brew install python3

# 3. Make launcher executable
chmod +x launch_wallet.sh

# 4. Run the GUI
./launch_wallet.sh
```

### Windows

```cmd
1. Extract the zip file
2. Install Python from python.org (if not installed)
3. Double-click launch_wallet.bat
   OR
   Double-click wallet_gui.py
```

## Detailed Installation

### System Requirements

- **Operating System**: Linux, macOS, or Windows
- **Python**: Version 3.6 or higher
- **Tkinter**: Python GUI library (usually included)
- **Coin Daemons**: Install the daemon/CLI for coins you want to use

### Installing Python

#### Ubuntu/Debian Linux

```bash
sudo apt-get update
sudo apt-get install python3 python3-tk python3-pip
```

#### Fedora Linux

```bash
sudo dnf install python3 python3-tkinter python3-pip
```

#### Arch Linux

```bash
sudo pacman -S python python-pip tk
```

#### macOS

Option 1 - Official installer:
1. Download from [python.org](https://www.python.org/downloads/)
2. Run the installer
3. Tkinter is included

Option 2 - Homebrew:
```bash
brew install python3
```

#### Windows

1. Download from [python.org](https://www.python.org/downloads/)
2. Run the installer
3. **Important**: Check "Add Python to PATH"
4. Tkinter is included

### Installing Coin Daemons

You need to install the daemon/CLI for each coin you want to use.

#### Bitcoin

**Linux:**
```bash
# Download from bitcoin.org
wget https://bitcoin.org/bin/bitcoin-core-XX.X/bitcoin-XX.X-x86_64-linux-gnu.tar.gz
tar -xzf bitcoin-XX.X-x86_64-linux-gnu.tar.gz
sudo install -m 0755 -o root -g root -t /usr/local/bin bitcoin-XX.X/bin/*
```

**macOS:**
```bash
brew install bitcoin
```

**Windows:**
Download installer from [bitcoin.org](https://bitcoin.org/en/download)

#### Litecoin

**Linux:**
```bash
# Download from litecoin.org
wget https://download.litecoin.org/litecoin-X.XX.X/linux/litecoin-X.XX.X-x86_64-linux-gnu.tar.gz
tar -xzf litecoin-X.XX.X-x86_64-linux-gnu.tar.gz
sudo install -m 0755 -o root -g root -t /usr/local/bin litecoin-X.XX.X/bin/*
```

**macOS:**
```bash
brew install litecoin
```

**Windows:**
Download installer from [litecoin.org](https://litecoin.org/)

#### Dogecoin

**Linux:**
```bash
# Download from dogecoin.com
wget https://github.com/dogecoin/dogecoin/releases/download/vX.XX.X/dogecoin-X.XX.X-x86_64-linux-gnu.tar.gz
tar -xzf dogecoin-X.XX.X-x86_64-linux-gnu.tar.gz
sudo install -m 0755 -o root -g root -t /usr/local/bin dogecoin-X.XX.X/bin/*
```

**Windows:**
Download from [dogecoin.com](https://dogecoin.com/)

#### Aleo

**Linux:**
```bash
# Download from aleo.org
wget https://github.com/AleoHQ/snarkOS/releases/latest/download/snarkos-linux
chmod +x snarkos-linux
sudo mv snarkos-linux /usr/local/bin/snarkos
```

**Windows:**
Download from [aleo.org](https://aleo.org/)

#### Cardano

**Linux:**
```bash
# Using official installation script
curl -sSf https://get.cardano.org | sh
```

**Windows:**
Download Daedalus wallet from [cardano.org](https://cardano.org/)

#### Solana

**Linux/macOS:**
```bash
sh -c "$(curl -sSfL https://release.solana.com/stable/install)"
```

**Windows:**
Download from [solana.com](https://solana.com/)

#### Other Coins

For Polkadot, Avalanche, Cosmos, Algorand, Tezos, Stellar, Kaspa, and Ergo:

Visit the official website for each coin and download the appropriate daemon/CLI for your operating system.

### Optional Dependencies

#### QR Code Generation

```bash
pip3 install qrcode[pil]
```

This enables QR code generation for addresses.

## Configuration

### First Run

On first run, the application will create a configuration file at:

- **Linux/macOS**: `~/.wallet_gui_config.json`
- **Windows**: `C:\Users\YourName\.wallet_gui_config.json`

### Configuring Coin Paths

If your coin daemons are not in the system PATH, you can configure custom paths:

1. Open the GUI
2. Go to **Tools** → **Add Custom Coin**
3. Enter the full path to the CLI command

Example:
```
CLI Command: /usr/local/bin/bitcoin-cli
Daemon Command: /usr/local/bin/bitcoind
Data Directory: /home/user/.bitcoin
```

### Manual Configuration

Edit `~/.wallet_gui_config.json`:

```json
{
  "coins": {
    "Bitcoin": {
      "cli": "/usr/local/bin/bitcoin-cli",
      "daemon": "/usr/local/bin/bitcoind",
      "datadir": "/home/user/.bitcoin",
      "port": 8332
    }
  },
  "current_coin": "Bitcoin",
  "auto_backup": true,
  "backup_dir": "/home/user/wallet_backups"
}
```

## Starting Coin Daemons

Before using the wallet GUI, you need to start the daemon for your coin.

### Bitcoin Example

```bash
# Start daemon
bitcoind -daemon

# Check if running
bitcoin-cli getinfo

# Stop daemon (when done)
bitcoin-cli stop
```

### Litecoin Example

```bash
# Start daemon
litecoind -daemon

# Check if running
litecoin-cli getinfo

# Stop daemon
litecoin-cli stop
```

### Dogecoin Example

```bash
# Start daemon
dogecoind -daemon

# Check if running
dogecoin-cli getinfo

# Stop daemon
dogecoin-cli stop
```

## Creating Desktop Shortcut

### Linux

```bash
# Copy desktop file
cp wallet_gui.desktop ~/.local/share/applications/

# Edit the file and replace %INSTALL_DIR% with actual path
nano ~/.local/share/applications/wallet_gui.desktop

# Make executable
chmod +x ~/.local/share/applications/wallet_gui.desktop
```

### macOS

Create an Automator application:

1. Open Automator
2. Create new "Application"
3. Add "Run Shell Script" action
4. Enter: `cd /path/to/ultimate-cli-wallet-gui && ./launch_wallet.sh`
5. Save as "Wallet GUI.app"

### Windows

Create a shortcut:

1. Right-click on `launch_wallet.bat`
2. Select "Create shortcut"
3. Move shortcut to Desktop
4. (Optional) Change icon

## Troubleshooting Installation

### Python not found

**Linux/macOS:**
```bash
# Check Python installation
which python3
python3 --version

# If not found, install Python
```

**Windows:**
```cmd
# Check Python installation
python --version

# If not found, reinstall Python and check "Add to PATH"
```

### Tkinter not found

**Linux:**
```bash
# Test Tkinter
python3 -c "import tkinter"

# If error, install:
# Ubuntu/Debian:
sudo apt-get install python3-tk

# Fedora:
sudo dnf install python3-tkinter
```

**macOS/Windows:**
Tkinter should be included with Python. Reinstall Python if missing.

### Permission denied

**Linux/macOS:**
```bash
# Make launcher executable
chmod +x launch_wallet.sh

# If still denied, check file ownership
ls -l launch_wallet.sh
```

### Daemon connection failed

1. **Check daemon is running:**
   ```bash
   ps aux | grep bitcoind
   ```

2. **Check RPC configuration:**
   - Verify `~/.bitcoin/bitcoin.conf` exists
   - Check RPC username/password
   - Verify RPC port

3. **Check datadir path:**
   - Verify path in configuration
   - Check permissions

### GUI doesn't start

1. **Check Python version:**
   ```bash
   python3 --version  # Should be 3.6+
   ```

2. **Check Tkinter:**
   ```bash
   python3 -c "import tkinter; print('OK')"
   ```

3. **Run with error output:**
   ```bash
   python3 wallet_gui.py
   ```

4. **Check logs:**
   - Look for error messages in terminal
   - Check system logs

## Updating

To update to a new version:

1. **Backup your configuration:**
   ```bash
   cp ~/.wallet_gui_config.json ~/.wallet_gui_config.json.backup
   ```

2. **Extract new version:**
   ```bash
   unzip ultimate-cli-wallet-gui-new.zip
   ```

3. **Copy configuration:**
   ```bash
   # Your config will be preserved automatically
   # Or manually restore if needed:
   cp ~/.wallet_gui_config.json.backup ~/.wallet_gui_config.json
   ```

## Uninstallation

To remove the application:

```bash
# Remove application files
rm -rf /path/to/ultimate-cli-wallet-gui

# Remove configuration (optional)
rm ~/.wallet_gui_config.json

# Remove desktop shortcut (optional)
rm ~/.local/share/applications/wallet_gui.desktop
```

**Note:** This does NOT remove your wallet data or coin daemons!

## Next Steps

After installation:

1. **Start a coin daemon** (e.g., `bitcoind -daemon`)
2. **Launch the GUI** (`./launch_wallet.sh`)
3. **Select your coin** from the dropdown
4. **Test with "Get Balance"** button
5. **Read the README.md** for usage instructions

## Getting Help

If you encounter issues:

1. Check the **Troubleshooting** section in README.md
2. Verify coin daemon is running
3. Check configuration file
4. Review daemon logs
5. Test CLI commands manually

## Security Notes

- **Never share your private keys**
- **Backup your wallets regularly**
- **Use strong passphrases**
- **Keep software updated**
- **Test with small amounts first**

---

**Installation complete! Ready to manage your wallets! 💰**
