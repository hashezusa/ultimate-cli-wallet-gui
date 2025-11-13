#!/usr/bin/env python3
"""
Ultimate CLI Wallet GUI
A comprehensive multi-coin wallet manager with programmable buttons

Created by: Magnafic0 unchained & Gistgard Reventlov
Version: 2.0
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import subprocess
import json
import os
from pathlib import Path
import threading
import queue

class WalletGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Ultimate CLI Wallet GUI 💰 - by Magnafic0 unchained & Gistgard Reventlov")
        self.root.geometry("1200x800")
        
        # Light blue theme colors
        self.colors = {
            'bg': '#E3F2FD',           # Light blue background
            'fg': '#0D47A1',           # Dark blue text
            'accent': '#2196F3',       # Medium blue accent
            'button_bg': '#BBDEFB',    # Light blue for buttons
            'button_active': '#90CAF9', # Active button color
            'frame_bg': '#FFFFFF',     # White for frames
            'highlight': '#64B5F6'     # Highlight color
        }
        
        # Apply theme
        self.root.configure(bg=self.colors['bg'])
        
        # Configure ttk style
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure styles
        style.configure('TFrame', background=self.colors['bg'])
        style.configure('TLabel', background=self.colors['bg'], foreground=self.colors['fg'])
        style.configure('TButton', background=self.colors['button_bg'], foreground=self.colors['fg'])
        style.map('TButton', background=[('active', self.colors['button_active'])])
        style.configure('TNotebook', background=self.colors['bg'])
        style.configure('TNotebook.Tab', background=self.colors['button_bg'], foreground=self.colors['fg'])
        style.map('TNotebook.Tab', background=[('selected', self.colors['accent'])], foreground=[('selected', 'white')])
        style.configure('TLabelframe', background=self.colors['bg'], foreground=self.colors['fg'])
        style.configure('TLabelframe.Label', background=self.colors['bg'], foreground=self.colors['fg'], font=('Arial', 10, 'bold'))
        style.configure('TCombobox', fieldbackground='white', background=self.colors['button_bg'])
        
        # Set window icon if logo exists
        logo_path = Path(__file__).parent / "logo.png"
        if logo_path.exists():
            try:
                from PIL import Image, ImageTk
                icon = Image.open(logo_path)
                icon = icon.resize((64, 64), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(icon)
                self.root.iconphoto(True, photo)
            except:
                pass
        
        # Store coin logo reference
        self.current_coin_logo = None
        
        # Configuration
        self.config_file = Path.home() / ".wallet_gui_config.json"
        self.load_config()
        
        # Command queue for async operations
        self.command_queue = queue.Queue()
        
        # Create main interface
        self.create_menu()
        self.create_main_interface()
        
        # Start command processor
        self.process_queue()
        
    def load_config(self):
        """Load or create default configuration"""
        default_config = {
            "coins": {
                "Bitcoin": {
                    "cli": "bitcoin-cli",
                    "daemon": "bitcoind",
                    "datadir": str(Path.home() / ".bitcoin"),
                    "port": 8332
                },
                "Litecoin": {
                    "cli": "litecoin-cli",
                    "daemon": "litecoind",
                    "datadir": str(Path.home() / ".litecoin"),
                    "port": 9332
                },
                "Dogecoin": {
                    "cli": "dogecoin-cli",
                    "daemon": "dogecoind",
                    "datadir": str(Path.home() / ".dogecoin"),
                    "port": 22555
                },
                "Ethereum": {
                    "cli": "geth",
                    "daemon": "geth",
                    "datadir": str(Path.home() / ".ethereum"),
                    "port": 8545
                },
                "Monero": {
                    "cli": "monero-wallet-cli",
                    "daemon": "monerod",
                    "datadir": str(Path.home() / ".monero"),
                    "port": 18081
                },
                "Zcash": {
                    "cli": "zcash-cli",
                    "daemon": "zcashd",
                    "datadir": str(Path.home() / ".zcash"),
                    "port": 8232
                },
                "Dash": {
                    "cli": "dash-cli",
                    "daemon": "dashd",
                    "datadir": str(Path.home() / ".dash"),
                    "port": 9998
                },
                "Bitcoin Cash": {
                    "cli": "bitcoin-cash-cli",
                    "daemon": "bitcoin-cashd",
                    "datadir": str(Path.home() / ".bitcoincash"),
                    "port": 8332
                },
                "Ravencoin": {
                    "cli": "raven-cli",
                    "daemon": "ravend",
                    "datadir": str(Path.home() / ".raven"),
                    "port": 8766
                },
                "Vertcoin": {
                    "cli": "vertcoin-cli",
                    "daemon": "vertcoind",
                    "datadir": str(Path.home() / ".vertcoin"),
                    "port": 5888
                },
                "Groestlcoin": {
                    "cli": "groestlcoin-cli",
                    "daemon": "groestlcoind",
                    "datadir": str(Path.home() / ".groestlcoin"),
                    "port": 1441
                },
                "Digibyte": {
                    "cli": "digibyte-cli",
                    "daemon": "digibyted",
                    "datadir": str(Path.home() / ".digibyte"),
                    "port": 14022
                },
                "Aleo": {
                    "cli": "aleo",
                    "daemon": "snarkos",
                    "datadir": str(Path.home() / ".aleo"),
                    "port": 3032
                },
                "Cardano": {
                    "cli": "cardano-cli",
                    "daemon": "cardano-node",
                    "datadir": str(Path.home() / ".cardano"),
                    "port": 3001
                },
                "Solana": {
                    "cli": "solana",
                    "daemon": "solana-validator",
                    "datadir": str(Path.home() / ".solana"),
                    "port": 8899
                },
                "Polkadot": {
                    "cli": "polkadot",
                    "daemon": "polkadot",
                    "datadir": str(Path.home() / ".polkadot"),
                    "port": 9933
                },
                "Avalanche": {
                    "cli": "avalanche-cli",
                    "daemon": "avalanchego",
                    "datadir": str(Path.home() / ".avalanche"),
                    "port": 9650
                },
                "Cosmos": {
                    "cli": "gaiad",
                    "daemon": "gaiad",
                    "datadir": str(Path.home() / ".gaia"),
                    "port": 26657
                },
                "Algorand": {
                    "cli": "goal",
                    "daemon": "algod",
                    "datadir": str(Path.home() / ".algorand"),
                    "port": 8080
                },
                "Tezos": {
                    "cli": "tezos-client",
                    "daemon": "tezos-node",
                    "datadir": str(Path.home() / ".tezos"),
                    "port": 8732
                },
                "Stellar": {
                    "cli": "stellar-core",
                    "daemon": "stellar-core",
                    "datadir": str(Path.home() / ".stellar"),
                    "port": 11626
                },
                "Kaspa": {
                    "cli": "kaspactl",
                    "daemon": "kaspад",
                    "datadir": str(Path.home() / ".kaspa"),
                    "port": 16110
                },
                "Ergo": {
                    "cli": "ergo-cli",
                    "daemon": "ergo",
                    "datadir": str(Path.home() / ".ergo"),
                    "port": 9053
                }
            },
            "current_coin": "Bitcoin",
            "auto_backup": True,
            "backup_dir": str(Path.home() / "wallet_backups")
        }
        
        if self.config_file.exists():
            with open(self.config_file, 'r') as f:
                self.config = json.load(f)
        else:
            self.config = default_config
            self.save_config()
            
    def save_config(self):
        """Save configuration to file"""
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=2)
            
    def create_menu(self):
        """Create menu bar"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Import Wallet", command=self.import_wallet)
        file_menu.add_command(label="Export Wallet", command=self.export_wallet)
        file_menu.add_command(label="Backup All", command=self.backup_all)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        # Wallet menu
        wallet_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Wallet", menu=wallet_menu)
        wallet_menu.add_command(label="Create New Wallet", command=self.create_wallet)
        wallet_menu.add_command(label="Restore from Seed", command=self.restore_from_seed)
        wallet_menu.add_command(label="Generate Seed Phrase", command=self.generate_seed)
        
        # Tools menu
        tools_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Tools", menu=tools_menu)
        tools_menu.add_command(label="Add Custom Coin", command=self.add_custom_coin)
        tools_menu.add_command(label="Custom Command", command=self.custom_command)
        tools_menu.add_command(label="Settings", command=self.show_settings)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)
        
    def create_main_interface(self):
        """Create main interface"""
        # Top frame - Coin selector and status
        top_frame = ttk.Frame(self.root, padding="10")
        top_frame.pack(fill=tk.X)
        
        # Coin logo display frame
        logo_frame = tk.Frame(top_frame, bg=self.colors['frame_bg'], relief=tk.RAISED, borderwidth=2)
        logo_frame.pack(side=tk.LEFT, padx=10, pady=5)
        
        self.coin_logo_label = tk.Label(logo_frame, bg=self.colors['frame_bg'])
        self.coin_logo_label.pack(padx=5, pady=5)
        
        # Load initial coin logo
        self.load_coin_logo(self.config.get("current_coin", "Bitcoin"))
        
        # Coin selector
        selector_frame = tk.Frame(top_frame, bg=self.colors['bg'])
        selector_frame.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(selector_frame, text="Select Coin:", font=("Arial", 12, "bold")).pack(anchor=tk.W)
        
        self.coin_var = tk.StringVar(value=self.config.get("current_coin", "Bitcoin"))
        coin_combo = ttk.Combobox(selector_frame, textvariable=self.coin_var, 
                                   values=list(self.config["coins"].keys()),
                                   width=20, font=("Arial", 11))
        coin_combo.pack()
        coin_combo.bind("<<ComboboxSelected>>", self.on_coin_change)
        
        ttk.Button(top_frame, text="🔄 Refresh", command=self.refresh_wallet).pack(side=tk.LEFT, padx=5)
        
        self.status_label = ttk.Label(top_frame, text="Status: Ready", font=("Arial", 10))
        self.status_label.pack(side=tk.RIGHT, padx=5)
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Create tabs
        self.create_wallet_tab()
        self.create_transaction_tab()
        self.create_mining_tab()
        self.create_tools_tab()
        self.create_console_tab()
        
    def create_wallet_tab(self):
        """Create wallet management tab"""
        wallet_frame = ttk.Frame(self.notebook)
        self.notebook.add(wallet_frame, text="💰 Wallet")
        
        # Left panel - Wallet info
        left_panel = ttk.Frame(wallet_frame)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Balance display
        balance_frame = ttk.LabelFrame(left_panel, text="Balance", padding="10")
        balance_frame.pack(fill=tk.X, pady=5)
        
        self.balance_label = tk.Label(balance_frame, text="0.00000000", 
                                       font=("Arial", 24, "bold"),
                                       bg=self.colors['frame_bg'],
                                       fg=self.colors['accent'])
        self.balance_label.pack()
        
        # Wallet info
        info_frame = ttk.LabelFrame(left_panel, text="Wallet Information", padding="10")
        info_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        self.wallet_info_text = scrolledtext.ScrolledText(info_frame, height=10, 
                                                           font=("Courier", 10))
        self.wallet_info_text.pack(fill=tk.BOTH, expand=True)
        
        # Right panel - Actions
        right_panel = ttk.Frame(wallet_frame)
        right_panel.pack(side=tk.RIGHT, fill=tk.Y, padx=5, pady=5)
        
        # Wallet actions
        actions_frame = ttk.LabelFrame(right_panel, text="Wallet Actions", padding="10")
        actions_frame.pack(fill=tk.X, pady=5)
        
        wallet_buttons = [
            ("📊 Get Balance", self.get_balance),
            ("📋 List Addresses", self.list_addresses),
            ("➕ New Address", self.new_address),
            ("📥 Import Address", self.import_address),
            ("🔐 Encrypt Wallet", self.encrypt_wallet),
            ("🔓 Unlock Wallet", self.unlock_wallet),
            ("🔒 Lock Wallet", self.lock_wallet),
            ("💾 Backup Wallet", self.backup_wallet),
            ("📤 Dump Privkey", self.dump_privkey),
            ("📥 Import Privkey", self.import_privkey),
        ]
        
        for text, command in wallet_buttons:
            ttk.Button(actions_frame, text=text, command=command, 
                      width=25).pack(pady=2)
        
    def create_transaction_tab(self):
        """Create transaction tab"""
        tx_frame = ttk.Frame(self.notebook)
        self.notebook.add(tx_frame, text="💸 Transactions")
        
        # Send transaction frame
        send_frame = ttk.LabelFrame(tx_frame, text="Send Transaction", padding="10")
        send_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(send_frame, text="To Address:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.send_address_entry = ttk.Entry(send_frame, width=50)
        self.send_address_entry.grid(row=0, column=1, pady=2, padx=5)
        
        ttk.Label(send_frame, text="Amount:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.send_amount_entry = ttk.Entry(send_frame, width=30)
        self.send_amount_entry.grid(row=1, column=1, sticky=tk.W, pady=2, padx=5)
        
        ttk.Label(send_frame, text="Fee:").grid(row=2, column=0, sticky=tk.W, pady=2)
        self.send_fee_entry = ttk.Entry(send_frame, width=30)
        self.send_fee_entry.grid(row=2, column=1, sticky=tk.W, pady=2, padx=5)
        
        ttk.Label(send_frame, text="Comment:").grid(row=3, column=0, sticky=tk.W, pady=2)
        self.send_comment_entry = ttk.Entry(send_frame, width=50)
        self.send_comment_entry.grid(row=3, column=1, pady=2, padx=5)
        
        ttk.Button(send_frame, text="💸 Send Transaction", 
                  command=self.send_transaction).grid(row=4, column=1, pady=10)
        
        # Transaction history
        history_frame = ttk.LabelFrame(tx_frame, text="Transaction History", padding="10")
        history_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Transaction list
        self.tx_tree = ttk.Treeview(history_frame, 
                                    columns=("txid", "amount", "confirmations", "time"),
                                    show="headings", height=15)
        self.tx_tree.heading("txid", text="Transaction ID")
        self.tx_tree.heading("amount", text="Amount")
        self.tx_tree.heading("confirmations", text="Confirmations")
        self.tx_tree.heading("time", text="Time")
        
        self.tx_tree.column("txid", width=400)
        self.tx_tree.column("amount", width=150)
        self.tx_tree.column("confirmations", width=100)
        self.tx_tree.column("time", width=200)
        
        scrollbar = ttk.Scrollbar(history_frame, orient=tk.VERTICAL, command=self.tx_tree.yview)
        self.tx_tree.configure(yscrollcommand=scrollbar.set)
        
        self.tx_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Buttons
        button_frame = ttk.Frame(history_frame)
        button_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(button_frame, text="🔄 Refresh", 
                  command=self.refresh_transactions).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="📋 Copy TXID", 
                  command=self.copy_txid).pack(side=tk.LEFT, padx=5)
        
    def create_mining_tab(self):
        """Create mining tab"""
        mining_frame = ttk.Frame(self.notebook)
        self.notebook.add(mining_frame, text="⛏️ Mining")
        
        # Mining controls
        control_frame = ttk.LabelFrame(mining_frame, text="Mining Controls", padding="10")
        control_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(control_frame, text="Threads:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.mining_threads_entry = ttk.Entry(control_frame, width=10)
        self.mining_threads_entry.insert(0, "1")
        self.mining_threads_entry.grid(row=0, column=1, sticky=tk.W, pady=2, padx=5)
        
        button_frame = ttk.Frame(control_frame)
        button_frame.grid(row=1, column=0, columnspan=2, pady=10)
        
        ttk.Button(button_frame, text="▶️ Start Mining", 
                  command=self.start_mining).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="⏸️ Stop Mining", 
                  command=self.stop_mining).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="📊 Mining Info", 
                  command=self.mining_info).pack(side=tk.LEFT, padx=5)
        
        # Mining output
        output_frame = ttk.LabelFrame(mining_frame, text="Mining Output", padding="10")
        output_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.mining_output = scrolledtext.ScrolledText(output_frame, height=20, 
                                                       font=("Courier", 9))
        self.mining_output.pack(fill=tk.BOTH, expand=True)
        
    def create_tools_tab(self):
        """Create tools tab"""
        tools_frame = ttk.Frame(self.notebook)
        self.notebook.add(tools_frame, text="🔧 Tools")
        
        # Seed phrase tools
        seed_frame = ttk.LabelFrame(tools_frame, text="Seed Phrase Tools", padding="10")
        seed_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(seed_frame, text="🎲 Generate Seed Phrase", 
                  command=self.generate_seed, width=30).pack(pady=5)
        ttk.Button(seed_frame, text="✅ Validate Seed Phrase", 
                  command=self.validate_seed, width=30).pack(pady=5)
        ttk.Button(seed_frame, text="🔄 Restore from Seed", 
                  command=self.restore_from_seed, width=30).pack(pady=5)
        
        self.seed_text = scrolledtext.ScrolledText(seed_frame, height=4, 
                                                   font=("Courier", 10))
        self.seed_text.pack(fill=tk.X, pady=5)
        
        # Address tools
        address_frame = ttk.LabelFrame(tools_frame, text="Address Tools", padding="10")
        address_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(address_frame, text="Address:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.address_entry = ttk.Entry(address_frame, width=50)
        self.address_entry.grid(row=0, column=1, pady=2, padx=5)
        
        button_frame = ttk.Frame(address_frame)
        button_frame.grid(row=1, column=0, columnspan=2, pady=5)
        
        ttk.Button(button_frame, text="✅ Validate Address", 
                  command=self.validate_address).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="📊 Get Address Info", 
                  command=self.get_address_info).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="📱 Generate QR Code", 
                  command=self.generate_qr).pack(side=tk.LEFT, padx=5)
        
        # Backup tools
        backup_frame = ttk.LabelFrame(tools_frame, text="Backup & Restore", padding="10")
        backup_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(backup_frame, text="💾 Backup Current Wallet", 
                  command=self.backup_wallet, width=30).pack(pady=5)
        ttk.Button(backup_frame, text="📥 Restore Wallet", 
                  command=self.restore_wallet, width=30).pack(pady=5)
        ttk.Button(backup_frame, text="💾 Backup All Wallets", 
                  command=self.backup_all, width=30).pack(pady=5)
        
    def create_console_tab(self):
        """Create console tab"""
        console_frame = ttk.Frame(self.notebook)
        self.notebook.add(console_frame, text="🖥️ Console")
        
        # Command input
        input_frame = ttk.Frame(console_frame)
        input_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(input_frame, text="Command:", font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=5)
        self.console_input = ttk.Entry(input_frame, font=("Courier", 10))
        self.console_input.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        self.console_input.bind("<Return>", lambda e: self.execute_console_command())
        
        ttk.Button(input_frame, text="Execute", 
                  command=self.execute_console_command).pack(side=tk.LEFT, padx=5)
        ttk.Button(input_frame, text="Clear", 
                  command=self.clear_console).pack(side=tk.LEFT, padx=5)
        
        # Console output
        self.console_output = scrolledtext.ScrolledText(console_frame, height=30, 
                                                        font=("Courier", 9),
                                                        bg="#0D1B2A", fg="#00D9FF")
        self.console_output.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Quick commands
        quick_frame = ttk.LabelFrame(console_frame, text="Quick Commands", padding="5")
        quick_frame.pack(fill=tk.X, padx=5, pady=5)
        
        quick_commands = [
            ("getinfo", "getinfo"),
            ("getblockcount", "getblockcount"),
            ("getpeerinfo", "getpeerinfo"),
            ("getmininginfo", "getmininginfo"),
            ("help", "help"),
        ]
        
        for label, cmd in quick_commands:
            ttk.Button(quick_frame, text=label, 
                      command=lambda c=cmd: self.quick_command(c)).pack(side=tk.LEFT, padx=2)
        
    # Command execution methods
    def execute_cli_command(self, *args):
        """Execute CLI command for current coin"""
        coin = self.coin_var.get()
        coin_config = self.config["coins"].get(coin)
        
        if not coin_config:
            return None, "Coin not configured"
        
        cli = coin_config["cli"]
        datadir = coin_config.get("datadir")
        
        cmd = [cli]
        if datadir:
            cmd.extend([f"-datadir={datadir}"])
        cmd.extend(args)
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            if result.returncode == 0:
                return result.stdout.strip(), None
            else:
                return None, result.stderr.strip()
        except subprocess.TimeoutExpired:
            return None, "Command timed out"
        except FileNotFoundError:
            return None, f"CLI not found: {cli}"
        except Exception as e:
            return None, str(e)
    
    def log_to_console(self, message, error=False):
        """Log message to console"""
        self.console_output.insert(tk.END, f"{message}\n")
        if error:
            # Highlight errors in red
            start = self.console_output.index("end-2c linestart")
            end = self.console_output.index("end-1c")
            self.console_output.tag_add("error", start, end)
            self.console_output.tag_config("error", foreground="#ff0000")
        self.console_output.see(tk.END)
        
    # Wallet tab methods
    def get_balance(self):
        """Get wallet balance"""
        self.status_label.config(text="Status: Getting balance...")
        output, error = self.execute_cli_command("getbalance")
        
        if error:
            self.log_to_console(f"Error: {error}", error=True)
            messagebox.showerror("Error", error)
        else:
            self.balance_label.config(text=output)
            self.log_to_console(f"Balance: {output}")
        
        self.status_label.config(text="Status: Ready")
        
    def list_addresses(self):
        """List all addresses"""
        self.status_label.config(text="Status: Listing addresses...")
        output, error = self.execute_cli_command("listreceivedbyaddress", "0", "true")
        
        if error:
            self.log_to_console(f"Error: {error}", error=True)
            messagebox.showerror("Error", error)
        else:
            self.wallet_info_text.delete(1.0, tk.END)
            self.wallet_info_text.insert(tk.END, output)
            self.log_to_console("Addresses listed successfully")
        
        self.status_label.config(text="Status: Ready")
        
    def new_address(self):
        """Generate new address"""
        label = tk.simpledialog.askstring("New Address", "Enter label (optional):")
        
        self.status_label.config(text="Status: Generating address...")
        if label:
            output, error = self.execute_cli_command("getnewaddress", label)
        else:
            output, error = self.execute_cli_command("getnewaddress")
        
        if error:
            self.log_to_console(f"Error: {error}", error=True)
            messagebox.showerror("Error", error)
        else:
            self.log_to_console(f"New address: {output}")
            messagebox.showinfo("New Address", f"Address: {output}")
        
        self.status_label.config(text="Status: Ready")
        
    def import_address(self):
        """Import address"""
        address = tk.simpledialog.askstring("Import Address", "Enter address:")
        if not address:
            return
        
        label = tk.simpledialog.askstring("Import Address", "Enter label (optional):")
        
        self.status_label.config(text="Status: Importing address...")
        if label:
            output, error = self.execute_cli_command("importaddress", address, label, "false")
        else:
            output, error = self.execute_cli_command("importaddress", address, "", "false")
        
        if error:
            self.log_to_console(f"Error: {error}", error=True)
            messagebox.showerror("Error", error)
        else:
            self.log_to_console(f"Address imported: {address}")
            messagebox.showinfo("Success", "Address imported successfully")
        
        self.status_label.config(text="Status: Ready")
        
    def encrypt_wallet(self):
        """Encrypt wallet"""
        passphrase = tk.simpledialog.askstring("Encrypt Wallet", 
                                               "Enter passphrase:", show="*")
        if not passphrase:
            return
        
        confirm = tk.simpledialog.askstring("Encrypt Wallet", 
                                           "Confirm passphrase:", show="*")
        if passphrase != confirm:
            messagebox.showerror("Error", "Passphrases do not match")
            return
        
        self.status_label.config(text="Status: Encrypting wallet...")
        output, error = self.execute_cli_command("encryptwallet", passphrase)
        
        if error:
            self.log_to_console(f"Error: {error}", error=True)
            messagebox.showerror("Error", error)
        else:
            self.log_to_console("Wallet encrypted successfully")
            messagebox.showinfo("Success", "Wallet encrypted. Daemon will restart.")
        
        self.status_label.config(text="Status: Ready")
        
    def unlock_wallet(self):
        """Unlock wallet"""
        passphrase = tk.simpledialog.askstring("Unlock Wallet", 
                                               "Enter passphrase:", show="*")
        if not passphrase:
            return
        
        timeout = tk.simpledialog.askinteger("Unlock Wallet", 
                                            "Timeout (seconds):", initialvalue=60)
        if not timeout:
            timeout = 60
        
        self.status_label.config(text="Status: Unlocking wallet...")
        output, error = self.execute_cli_command("walletpassphrase", passphrase, str(timeout))
        
        if error:
            self.log_to_console(f"Error: {error}", error=True)
            messagebox.showerror("Error", error)
        else:
            self.log_to_console(f"Wallet unlocked for {timeout} seconds")
            messagebox.showinfo("Success", f"Wallet unlocked for {timeout} seconds")
        
        self.status_label.config(text="Status: Ready")
        
    def lock_wallet(self):
        """Lock wallet"""
        self.status_label.config(text="Status: Locking wallet...")
        output, error = self.execute_cli_command("walletlock")
        
        if error:
            self.log_to_console(f"Error: {error}", error=True)
            messagebox.showerror("Error", error)
        else:
            self.log_to_console("Wallet locked")
            messagebox.showinfo("Success", "Wallet locked")
        
        self.status_label.config(text="Status: Ready")
        
    def backup_wallet(self):
        """Backup wallet"""
        filename = filedialog.asksaveasfilename(
            defaultextension=".dat",
            filetypes=[("Wallet files", "*.dat"), ("All files", "*.*")]
        )
        
        if not filename:
            return
        
        self.status_label.config(text="Status: Backing up wallet...")
        output, error = self.execute_cli_command("backupwallet", filename)
        
        if error:
            self.log_to_console(f"Error: {error}", error=True)
            messagebox.showerror("Error", error)
        else:
            self.log_to_console(f"Wallet backed up to: {filename}")
            messagebox.showinfo("Success", f"Wallet backed up to:\n{filename}")
        
        self.status_label.config(text="Status: Ready")
        
    def dump_privkey(self):
        """Dump private key"""
        address = tk.simpledialog.askstring("Dump Private Key", "Enter address:")
        if not address:
            return
        
        self.status_label.config(text="Status: Dumping private key...")
        output, error = self.execute_cli_command("dumpprivkey", address)
        
        if error:
            self.log_to_console(f"Error: {error}", error=True)
            messagebox.showerror("Error", error)
        else:
            self.log_to_console(f"Private key for {address}: {output}")
            messagebox.showinfo("Private Key", f"Private key:\n{output}\n\nKEEP THIS SAFE!")
        
        self.status_label.config(text="Status: Ready")
        
    def import_privkey(self):
        """Import private key"""
        privkey = tk.simpledialog.askstring("Import Private Key", "Enter private key:")
        if not privkey:
            return
        
        label = tk.simpledialog.askstring("Import Private Key", "Enter label (optional):")
        
        self.status_label.config(text="Status: Importing private key...")
        if label:
            output, error = self.execute_cli_command("importprivkey", privkey, label, "false")
        else:
            output, error = self.execute_cli_command("importprivkey", privkey, "", "false")
        
        if error:
            self.log_to_console(f"Error: {error}", error=True)
            messagebox.showerror("Error", error)
        else:
            self.log_to_console("Private key imported successfully")
            messagebox.showinfo("Success", "Private key imported successfully")
        
        self.status_label.config(text="Status: Ready")
        
    # Transaction tab methods
    def send_transaction(self):
        """Send transaction"""
        address = self.send_address_entry.get().strip()
        amount = self.send_amount_entry.get().strip()
        comment = self.send_comment_entry.get().strip()
        
        if not address or not amount:
            messagebox.showerror("Error", "Address and amount are required")
            return
        
        confirm = messagebox.askyesno("Confirm Transaction", 
                                      f"Send {amount} to {address}?")
        if not confirm:
            return
        
        self.status_label.config(text="Status: Sending transaction...")
        
        if comment:
            output, error = self.execute_cli_command("sendtoaddress", address, amount, comment)
        else:
            output, error = self.execute_cli_command("sendtoaddress", address, amount)
        
        if error:
            self.log_to_console(f"Error: {error}", error=True)
            messagebox.showerror("Error", error)
        else:
            self.log_to_console(f"Transaction sent: {output}")
            messagebox.showinfo("Success", f"Transaction ID:\n{output}")
            
            # Clear form
            self.send_address_entry.delete(0, tk.END)
            self.send_amount_entry.delete(0, tk.END)
            self.send_comment_entry.delete(0, tk.END)
        
        self.status_label.config(text="Status: Ready")
        
    def refresh_transactions(self):
        """Refresh transaction list"""
        self.status_label.config(text="Status: Loading transactions...")
        output, error = self.execute_cli_command("listtransactions", "*", "50")
        
        if error:
            self.log_to_console(f"Error: {error}", error=True)
            messagebox.showerror("Error", error)
            self.status_label.config(text="Status: Ready")
            return
        
        # Clear existing items
        for item in self.tx_tree.get_children():
            self.tx_tree.delete(item)
        
        # Parse and display transactions
        try:
            import json
            transactions = json.loads(output)
            
            for tx in transactions:
                txid = tx.get("txid", "")
                amount = tx.get("amount", 0)
                confirmations = tx.get("confirmations", 0)
                time = tx.get("time", "")
                
                self.tx_tree.insert("", 0, values=(txid, amount, confirmations, time))
            
            self.log_to_console(f"Loaded {len(transactions)} transactions")
        except Exception as e:
            self.log_to_console(f"Error parsing transactions: {e}", error=True)
        
        self.status_label.config(text="Status: Ready")
        
    def copy_txid(self):
        """Copy selected transaction ID"""
        selection = self.tx_tree.selection()
        if not selection:
            messagebox.showinfo("Info", "Please select a transaction")
            return
        
        item = self.tx_tree.item(selection[0])
        txid = item["values"][0]
        
        self.root.clipboard_clear()
        self.root.clipboard_append(txid)
        messagebox.showinfo("Success", "Transaction ID copied to clipboard")
        
    # Mining tab methods
    def start_mining(self):
        """Start mining"""
        threads = self.mining_threads_entry.get().strip()
        if not threads:
            threads = "1"
        
        self.status_label.config(text="Status: Starting mining...")
        output, error = self.execute_cli_command("setgenerate", "true", threads)
        
        if error:
            self.log_to_console(f"Error: {error}", error=True)
            self.mining_output.insert(tk.END, f"Error: {error}\n")
            messagebox.showerror("Error", error)
        else:
            self.log_to_console(f"Mining started with {threads} thread(s)")
            self.mining_output.insert(tk.END, f"Mining started with {threads} thread(s)\n")
            messagebox.showinfo("Success", f"Mining started with {threads} thread(s)")
        
        self.status_label.config(text="Status: Mining...")
        
    def stop_mining(self):
        """Stop mining"""
        self.status_label.config(text="Status: Stopping mining...")
        output, error = self.execute_cli_command("setgenerate", "false")
        
        if error:
            self.log_to_console(f"Error: {error}", error=True)
            self.mining_output.insert(tk.END, f"Error: {error}\n")
            messagebox.showerror("Error", error)
        else:
            self.log_to_console("Mining stopped")
            self.mining_output.insert(tk.END, "Mining stopped\n")
            messagebox.showinfo("Success", "Mining stopped")
        
        self.status_label.config(text="Status: Ready")
        
    def mining_info(self):
        """Get mining info"""
        self.status_label.config(text="Status: Getting mining info...")
        output, error = self.execute_cli_command("getmininginfo")
        
        if error:
            self.log_to_console(f"Error: {error}", error=True)
            self.mining_output.insert(tk.END, f"Error: {error}\n")
            messagebox.showerror("Error", error)
        else:
            self.log_to_console("Mining info retrieved")
            self.mining_output.insert(tk.END, f"\n{output}\n")
        
        self.status_label.config(text="Status: Ready")
        
    # Tools tab methods
    def generate_seed(self):
        """Generate seed phrase"""
        import secrets
        
        # BIP39 word list (simplified - first 100 words)
        wordlist = [
            "abandon", "ability", "able", "about", "above", "absent", "absorb", "abstract",
            "absurd", "abuse", "access", "accident", "account", "accuse", "achieve", "acid",
            "acoustic", "acquire", "across", "act", "action", "actor", "actress", "actual",
            "adapt", "add", "addict", "address", "adjust", "admit", "adult", "advance",
            "advice", "aerobic", "afford", "afraid", "again", "age", "agent", "agree",
            "ahead", "aim", "air", "airport", "aisle", "alarm", "album", "alcohol",
            "alert", "alien", "all", "alley", "allow", "almost", "alone", "alpha",
            "already", "also", "alter", "always", "amateur", "amazing", "among", "amount",
            "amused", "analyst", "anchor", "ancient", "anger", "angle", "angry", "animal",
            "ankle", "announce", "annual", "another", "answer", "antenna", "antique", "anxiety",
            "any", "apart", "apology", "appear", "apple", "approve", "april", "arch",
            "arctic", "area", "arena", "argue", "arm", "armed", "armor", "army",
            "around", "arrange", "arrest", "arrive", "arrow", "art", "artefact", "artist"
        ]
        
        # Generate 12-word seed phrase
        seed_words = [secrets.choice(wordlist) for _ in range(12)]
        seed_phrase = " ".join(seed_words)
        
        self.seed_text.delete(1.0, tk.END)
        self.seed_text.insert(tk.END, seed_phrase)
        
        self.log_to_console("Seed phrase generated")
        messagebox.showinfo("Seed Phrase Generated", 
                           "12-word seed phrase generated.\nKEEP THIS SAFE!")
        
    def validate_seed(self):
        """Validate seed phrase"""
        seed = self.seed_text.get(1.0, tk.END).strip()
        
        if not seed:
            messagebox.showerror("Error", "Please enter a seed phrase")
            return
        
        words = seed.split()
        
        if len(words) not in [12, 15, 18, 21, 24]:
            messagebox.showerror("Invalid", 
                               f"Seed phrase should be 12, 15, 18, 21, or 24 words.\n"
                               f"Found {len(words)} words.")
        else:
            messagebox.showinfo("Valid", f"Seed phrase format is valid ({len(words)} words)")
        
    def restore_from_seed(self):
        """Restore wallet from seed phrase"""
        seed = self.seed_text.get(1.0, tk.END).strip()
        
        if not seed:
            seed = tk.simpledialog.askstring("Restore from Seed", 
                                            "Enter seed phrase:")
        
        if not seed:
            return
        
        messagebox.showinfo("Info", 
                           "Seed phrase restoration requires coin-specific implementation.\n"
                           "Please refer to your coin's documentation for seed restoration.")
        
        self.log_to_console(f"Seed restoration requested for {self.coin_var.get()}")
        
    def validate_address(self):
        """Validate address"""
        address = self.address_entry.get().strip()
        
        if not address:
            messagebox.showerror("Error", "Please enter an address")
            return
        
        self.status_label.config(text="Status: Validating address...")
        output, error = self.execute_cli_command("validateaddress", address)
        
        if error:
            self.log_to_console(f"Error: {error}", error=True)
            messagebox.showerror("Error", error)
        else:
            self.log_to_console(f"Address validation result:\n{output}")
            messagebox.showinfo("Validation Result", output)
        
        self.status_label.config(text="Status: Ready")
        
    def get_address_info(self):
        """Get address information"""
        address = self.address_entry.get().strip()
        
        if not address:
            messagebox.showerror("Error", "Please enter an address")
            return
        
        self.status_label.config(text="Status: Getting address info...")
        output, error = self.execute_cli_command("getaddressinfo", address)
        
        if error:
            # Try alternative command
            output, error = self.execute_cli_command("validateaddress", address)
        
        if error:
            self.log_to_console(f"Error: {error}", error=True)
            messagebox.showerror("Error", error)
        else:
            self.log_to_console(f"Address info:\n{output}")
            messagebox.showinfo("Address Info", output)
        
        self.status_label.config(text="Status: Ready")
        
    def generate_qr(self):
        """Generate QR code for address"""
        address = self.address_entry.get().strip()
        
        if not address:
            messagebox.showerror("Error", "Please enter an address")
            return
        
        try:
            import qrcode
            from PIL import ImageTk
            
            # Generate QR code
            qr = qrcode.QRCode(version=1, box_size=10, border=5)
            qr.add_data(address)
            qr.make(fit=True)
            
            img = qr.make_image(fill_color="black", back_color="white")
            
            # Save to file
            filename = f"qr_{address[:10]}.png"
            img.save(filename)
            
            self.log_to_console(f"QR code saved to: {filename}")
            messagebox.showinfo("Success", f"QR code saved to:\n{filename}")
            
        except ImportError:
            messagebox.showinfo("Info", 
                              "QR code generation requires 'qrcode' package.\n"
                              "Install with: pip install qrcode[pil]")
        except Exception as e:
            self.log_to_console(f"Error: {e}", error=True)
            messagebox.showerror("Error", str(e))
        
    def restore_wallet(self):
        """Restore wallet from backup"""
        filename = filedialog.askopenfilename(
            title="Select wallet backup",
            filetypes=[("Wallet files", "*.dat"), ("All files", "*.*")]
        )
        
        if not filename:
            return
        
        confirm = messagebox.askyesno("Confirm Restore", 
                                      "This will replace your current wallet.\n"
                                      "Make sure you have a backup!\n\n"
                                      "Continue?")
        if not confirm:
            return
        
        messagebox.showinfo("Info", 
                           "To restore wallet:\n"
                           "1. Stop the daemon\n"
                           "2. Replace wallet.dat in data directory\n"
                           "3. Restart the daemon")
        
        self.log_to_console(f"Wallet restore requested from: {filename}")
        
    def backup_all(self):
        """Backup all wallets"""
        backup_dir = filedialog.askdirectory(title="Select backup directory")
        
        if not backup_dir:
            return
        
        self.status_label.config(text="Status: Backing up all wallets...")
        
        backed_up = 0
        for coin, config in self.config["coins"].items():
            datadir = config.get("datadir")
            if datadir:
                wallet_file = Path(datadir) / "wallet.dat"
                if wallet_file.exists():
                    import shutil
                    backup_file = Path(backup_dir) / f"{coin}_wallet.dat"
                    shutil.copy2(wallet_file, backup_file)
                    self.log_to_console(f"Backed up {coin} wallet")
                    backed_up += 1
        
        self.status_label.config(text="Status: Ready")
        messagebox.showinfo("Success", f"Backed up {backed_up} wallet(s) to:\n{backup_dir}")
        
    # Console tab methods
    def execute_console_command(self):
        """Execute command from console"""
        command = self.console_input.get().strip()
        
        if not command:
            return
        
        self.log_to_console(f"$ {command}")
        
        # Parse command
        parts = command.split()
        
        self.status_label.config(text="Status: Executing command...")
        output, error = self.execute_cli_command(*parts)
        
        if error:
            self.log_to_console(f"Error: {error}", error=True)
        else:
            self.log_to_console(output)
        
        self.status_label.config(text="Status: Ready")
        self.console_input.delete(0, tk.END)
        
    def quick_command(self, command):
        """Execute quick command"""
        self.console_input.delete(0, tk.END)
        self.console_input.insert(0, command)
        self.execute_console_command()
        
    def clear_console(self):
        """Clear console output"""
        self.console_output.delete(1.0, tk.END)
        
    # Menu methods
    def import_wallet(self):
        """Import wallet file"""
        filename = filedialog.askopenfilename(
            title="Select wallet file",
            filetypes=[("Wallet files", "*.dat"), ("All files", "*.*")]
        )
        
        if not filename:
            return
        
        coin = self.coin_var.get()
        config = self.config["coins"].get(coin)
        
        if not config:
            messagebox.showerror("Error", "Coin not configured")
            return
        
        datadir = config.get("datadir")
        
        messagebox.showinfo("Info", 
                           f"To import wallet:\n"
                           f"1. Stop the {coin} daemon\n"
                           f"2. Copy {filename}\n"
                           f"   to {datadir}/wallet.dat\n"
                           f"3. Restart the daemon")
        
    def export_wallet(self):
        """Export wallet file"""
        self.backup_wallet()
        
    def create_wallet(self):
        """Create new wallet"""
        wallet_name = tk.simpledialog.askstring("Create Wallet", "Enter wallet name:")
        
        if not wallet_name:
            return
        
        self.status_label.config(text="Status: Creating wallet...")
        output, error = self.execute_cli_command("createwallet", wallet_name)
        
        if error:
            self.log_to_console(f"Error: {error}", error=True)
            messagebox.showerror("Error", error)
        else:
            self.log_to_console(f"Wallet created: {wallet_name}")
            messagebox.showinfo("Success", f"Wallet '{wallet_name}' created successfully")
        
        self.status_label.config(text="Status: Ready")
        
    def add_custom_coin(self):
        """Add custom coin configuration"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Add Custom Coin")
        dialog.geometry("400x300")
        
        ttk.Label(dialog, text="Coin Name:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        name_entry = ttk.Entry(dialog, width=30)
        name_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(dialog, text="CLI Command:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        cli_entry = ttk.Entry(dialog, width=30)
        cli_entry.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(dialog, text="Daemon Command:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        daemon_entry = ttk.Entry(dialog, width=30)
        daemon_entry.grid(row=2, column=1, padx=5, pady=5)
        
        ttk.Label(dialog, text="Data Directory:").grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)
        datadir_entry = ttk.Entry(dialog, width=30)
        datadir_entry.grid(row=3, column=1, padx=5, pady=5)
        
        ttk.Label(dialog, text="RPC Port:").grid(row=4, column=0, sticky=tk.W, padx=5, pady=5)
        port_entry = ttk.Entry(dialog, width=30)
        port_entry.grid(row=4, column=1, padx=5, pady=5)
        
        def save_coin():
            name = name_entry.get().strip()
            cli = cli_entry.get().strip()
            daemon = daemon_entry.get().strip()
            datadir = datadir_entry.get().strip()
            port = port_entry.get().strip()
            
            if not name or not cli:
                messagebox.showerror("Error", "Name and CLI command are required")
                return
            
            self.config["coins"][name] = {
                "cli": cli,
                "daemon": daemon,
                "datadir": datadir,
                "port": int(port) if port else 0
            }
            
            self.save_config()
            self.log_to_console(f"Added custom coin: {name}")
            messagebox.showinfo("Success", f"Coin '{name}' added successfully")
            dialog.destroy()
            
            # Update coin selector
            coin_values = list(self.config["coins"].keys())
            self.root.nametowidget(".!frame.!combobox").configure(values=coin_values)
        
        ttk.Button(dialog, text="Save", command=save_coin).grid(row=5, column=1, pady=20)
        
    def custom_command(self):
        """Execute custom command"""
        self.notebook.select(4)  # Switch to console tab
        self.console_input.focus()
        
    def show_settings(self):
        """Show settings dialog"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Settings")
        dialog.geometry("400x200")
        
        ttk.Label(dialog, text="Backup Directory:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        backup_entry = ttk.Entry(dialog, width=30)
        backup_entry.insert(0, self.config.get("backup_dir", ""))
        backup_entry.grid(row=0, column=1, padx=5, pady=5)
        
        auto_backup_var = tk.BooleanVar(value=self.config.get("auto_backup", True))
        ttk.Checkbutton(dialog, text="Auto-backup on exit", 
                       variable=auto_backup_var).grid(row=1, column=0, columnspan=2, pady=5)
        
        def save_settings():
            self.config["backup_dir"] = backup_entry.get().strip()
            self.config["auto_backup"] = auto_backup_var.get()
            self.save_config()
            messagebox.showinfo("Success", "Settings saved")
            dialog.destroy()
        
        ttk.Button(dialog, text="Save", command=save_settings).grid(row=2, column=1, pady=20)
        
    def show_about(self):
        """Show about dialog"""
        about_window = tk.Toplevel(self.root)
        about_window.title("About")
        about_window.geometry("500x600")
        about_window.resizable(False, False)
        
        # Logo
        logo_path = Path(__file__).parent / "logo.png"
        if logo_path.exists():
            try:
                from PIL import Image, ImageTk
                logo_img = Image.open(logo_path)
                logo_img = logo_img.resize((128, 128), Image.Resampling.LANCZOS)
                logo_photo = ImageTk.PhotoImage(logo_img)
                logo_label = tk.Label(about_window, image=logo_photo)
                logo_label.image = logo_photo  # Keep reference
                logo_label.pack(pady=20)
            except:
                pass
        
        # Title
        title_label = tk.Label(about_window, text="Ultimate CLI Wallet GUI",
                              font=("Arial", 18, "bold"))
        title_label.pack(pady=10)
        
        # Version
        version_label = tk.Label(about_window, text="Version 2.0",
                                font=("Arial", 12))
        version_label.pack()
        
        # Creators
        creators_frame = tk.Frame(about_window)
        creators_frame.pack(pady=20)
        
        tk.Label(creators_frame, text="Created by:",
                font=("Arial", 11, "bold")).pack()
        tk.Label(creators_frame, text="Magnafic0 unchained",
                font=("Arial", 11), fg="#0066cc").pack()
        tk.Label(creators_frame, text="&",
                font=("Arial", 10)).pack()
        tk.Label(creators_frame, text="Gistgard Reventlov",
                font=("Arial", 11), fg="#0066cc").pack()
        
        # Description
        desc_text = scrolledtext.ScrolledText(about_window, height=12, width=50,
                                             font=("Arial", 10), wrap=tk.WORD)
        desc_text.pack(pady=10, padx=20)
        desc_text.insert(tk.END,
                        "A comprehensive multi-coin wallet manager "
                        "with programmable buttons and full CLI support.\n\n"
                        "Features:\n"
                        "• 23+ coin support (Bitcoin, Ethereum, Aleo, etc.)\n"
                        "• wallet.dat handling\n"
                        "• Seed phrase management\n"
                        "• Transaction management\n"
                        "• Mining integration\n"
                        "• Custom commands\n"
                        "• Backup & restore\n"
                        "• QR code generation\n"
                        "• Address validation\n"
                        "• Private key import/export\n\n"
                        "Supports any cryptocurrency with CLI interface!")
        desc_text.config(state=tk.DISABLED)
        
        # Close button
        ttk.Button(about_window, text="Close",
                  command=about_window.destroy).pack(pady=10)
        
    # Utility methods
    def load_coin_logo(self, coin_name):
        """Load and display coin logo"""
        try:
            from PIL import Image, ImageTk
            
            # Map coin names to logo files
            logo_map = {
                'Bitcoin': 'bitcoin.png',
                'Ethereum': 'ethereum.png',
                'Litecoin': 'litecoin.png',
                'Dogecoin': 'dogecoin.png',
                'Monero': 'monero.png',
                'Aleo': 'aleo.png',
                'Cardano': 'cardano.png',
                'Solana': 'solana.png'
            }
            
            # Get logo filename
            logo_file = logo_map.get(coin_name, 'default.png')
            logo_path = Path(__file__).parent / 'coin_logos' / logo_file
            
            # If specific logo doesn't exist, use default
            if not logo_path.exists():
                logo_path = Path(__file__).parent / 'coin_logos' / 'default.png'
            
            if logo_path.exists():
                # Load and resize logo
                img = Image.open(logo_path)
                img = img.resize((80, 80), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(img)
                
                # Update label
                self.coin_logo_label.configure(image=photo)
                self.coin_logo_label.image = photo  # Keep reference
            else:
                # No logo available, show coin name
                self.coin_logo_label.configure(text=coin_name[:3].upper(),
                                              font=('Arial', 24, 'bold'),
                                              fg=self.colors['accent'])
        except Exception as e:
            # Fallback to text display
            self.coin_logo_label.configure(text=coin_name[:3].upper(),
                                          font=('Arial', 24, 'bold'),
                                          fg=self.colors['accent'])
    
    def on_coin_change(self, event=None):
        """Handle coin selection change"""
        coin = self.coin_var.get()
        self.config["current_coin"] = coin
        self.save_config()
        self.load_coin_logo(coin)
        self.log_to_console(f"Switched to {coin}")
        self.refresh_wallet()
        
    def refresh_wallet(self):
        """Refresh wallet information"""
        self.get_balance()
        self.refresh_transactions()
        
    def process_queue(self):
        """Process command queue"""
        try:
            while True:
                task = self.command_queue.get_nowait()
                task()
        except queue.Empty:
            pass
        
        self.root.after(100, self.process_queue)

def main():
    root = tk.Tk()
    app = WalletGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
