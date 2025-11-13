#!/bin/bash
# Ultimate CLI Wallet GUI Launcher

echo "🚀 Launching Ultimate CLI Wallet GUI..."
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed!"
    echo "Please install Python 3 to run this application."
    exit 1
fi

echo "✅ Python 3 found"

# Check tkinter
if ! python3 -c "import tkinter" 2>/dev/null; then
    echo "❌ Tkinter is not installed!"
    echo ""
    echo "Install with:"
    echo "  Ubuntu/Debian: sudo apt-get install python3-tk"
    echo "  Fedora: sudo dnf install python3-tkinter"
    echo "  macOS: (included with Python)"
    exit 1
fi

echo "✅ Tkinter found"
echo ""

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Launch GUI
cd "$SCRIPT_DIR"
python3 wallet_gui.py

echo ""
echo "👋 Wallet GUI closed"
