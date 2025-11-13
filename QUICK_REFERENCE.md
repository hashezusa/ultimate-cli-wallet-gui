# Quick Reference Guide

**Ultimate CLI Wallet GUI v2.0**

**Created by: Magnafic0 unchained & Gistgard Reventlov**

## 🚀 Quick Start

```bash
# Launch
./launch_wallet.sh

# Or on Windows
launch_wallet.bat
```

## 📋 Common Tasks

### Get Balance
1. Select coin from dropdown
2. Click "📊 Get Balance"

### Send Transaction
1. Go to "💸 Transactions" tab
2. Enter recipient address
3. Enter amount
4. Click "💸 Send Transaction"

### Generate New Address
1. Go to "💰 Wallet" tab
2. Click "➕ New Address"
3. Copy the address

### Backup Wallet
1. Go to "💰 Wallet" tab
2. Click "💾 Backup Wallet"
3. Choose save location

### View Transactions
1. Go to "💸 Transactions" tab
2. Click "🔄 Refresh"
3. View transaction list

## ⌨️ Keyboard Shortcuts

| Action | Shortcut |
|--------|----------|
| Execute Console Command | Enter |
| Focus Console Input | Click Console tab |
| Copy TXID | Select transaction, click Copy |

## 🔧 Quick Commands

### Wallet Commands
```bash
getbalance              # Get wallet balance
getnewaddress          # Generate new address
listreceivedbyaddress  # List all addresses
getinfo                # Get wallet info
```

### Transaction Commands
```bash
sendtoaddress <addr> <amount>  # Send transaction
listtransactions              # List transactions
gettransaction <txid>         # Get transaction details
```

### Blockchain Commands
```bash
getblockcount          # Get current block height
getblockhash <height>  # Get block hash
getblock <hash>        # Get block details
getpeerinfo           # Get peer information
```

### Mining Commands
```bash
setgenerate true 1    # Start mining (1 thread)
setgenerate false     # Stop mining
getmininginfo        # Get mining info
```

### Security Commands
```bash
encryptwallet <pass>         # Encrypt wallet
walletpassphrase <pass> <t>  # Unlock wallet
walletlock                   # Lock wallet
dumpprivkey <addr>          # Export private key
importprivkey <key>         # Import private key
```

## 🎯 Button Quick Reference

### Wallet Tab Buttons
- **📊 Get Balance** - Display current balance
- **📋 List Addresses** - Show all addresses
- **➕ New Address** - Generate new address
- **📥 Import Address** - Import existing address
- **🔐 Encrypt Wallet** - Encrypt with passphrase
- **🔓 Unlock Wallet** - Unlock encrypted wallet
- **🔒 Lock Wallet** - Lock wallet
- **💾 Backup Wallet** - Create backup
- **📤 Dump Privkey** - Export private key
- **📥 Import Privkey** - Import private key

### Transaction Tab Buttons
- **💸 Send Transaction** - Send coins
- **🔄 Refresh** - Refresh transaction list
- **📋 Copy TXID** - Copy transaction ID

### Mining Tab Buttons
- **▶️ Start Mining** - Begin mining
- **⏸️ Stop Mining** - Stop mining
- **📊 Mining Info** - View mining stats

### Tools Tab Buttons
- **🎲 Generate Seed** - Create seed phrase
- **✅ Validate Seed** - Check seed phrase
- **🔄 Restore from Seed** - Restore wallet
- **✅ Validate Address** - Check address
- **📊 Get Address Info** - Address details
- **📱 Generate QR** - Create QR code
- **💾 Backup Current** - Backup wallet
- **📥 Restore Wallet** - Restore from backup
- **💾 Backup All** - Backup all wallets

## 🔐 Security Checklist

- [ ] Backup wallet before making changes
- [ ] Encrypt wallet with strong passphrase
- [ ] Write down seed phrase on paper
- [ ] Store backups in safe location
- [ ] Verify addresses before sending
- [ ] Test with small amounts first
- [ ] Keep private keys secure
- [ ] Use unique passphrases

## ⚠️ Common Errors

### "CLI not found"
**Fix:** Install coin daemon or configure path in settings

### "Connection refused"
**Fix:** Start the coin daemon (`bitcoind -daemon`)

### "Wallet locked"
**Fix:** Unlock wallet with passphrase

### "Insufficient funds"
**Fix:** Check balance, wait for confirmations

### "Invalid address"
**Fix:** Verify address format for selected coin

## 📊 Status Indicators

| Status | Meaning |
|--------|---------|
| Ready | Idle, ready for commands |
| Getting balance... | Fetching balance |
| Sending transaction... | Processing send |
| Mining... | Mining in progress |
| Executing command... | Running CLI command |

## 🎨 Tab Overview

| Tab | Purpose |
|-----|---------|
| 💰 Wallet | Balance, addresses, encryption |
| 💸 Transactions | Send, receive, history |
| ⛏️ Mining | Mining controls and output |
| 🔧 Tools | Seeds, QR codes, backups |
| 🖥️ Console | Direct CLI access |

## 🔄 Workflow Examples

### Receive Payment
1. Click "➕ New Address"
2. Copy address
3. Share with sender
4. Wait for transaction
5. Click "🔄 Refresh" to see it

### Send Payment
1. Go to Transactions tab
2. Enter recipient address
3. Enter amount
4. Review details
5. Click "💸 Send Transaction"
6. Confirm in dialog

### Backup Workflow
1. Click "💾 Backup Wallet"
2. Choose location
3. Save as `wallet-backup-DATE.dat`
4. Store securely
5. Test restore on another system

### Mining Workflow
1. Go to Mining tab
2. Set thread count
3. Click "▶️ Start Mining"
4. Monitor output
5. Click "⏸️ Stop Mining" when done

## 💡 Tips & Tricks

### Faster Balance Check
- Use console: `getbalance`
- Press Enter to execute

### Batch Address Generation
1. Go to Console tab
2. Type: `getnewaddress "label1"`
3. Press Enter
4. Repeat for more addresses

### Quick Transaction Lookup
1. Copy TXID
2. Go to Console
3. Type: `gettransaction <paste-txid>`

### Monitor Mining
1. Start mining
2. Console: `getmininginfo`
3. Repeat to see progress

### Export All Addresses
1. Console: `listreceivedbyaddress 0 true`
2. Copy output
3. Save to file

## 🔧 Configuration Tips

### Custom Coin Setup
```json
{
  "cli": "yourcoin-cli",
  "daemon": "yourcoind",
  "datadir": "/path/to/.yourcoin",
  "port": 8332
}
```

### Backup Directory
Set in Tools → Settings:
```
/home/user/wallet_backups
```

### Auto-backup
Enable in Tools → Settings for automatic backups on exit

## 📱 Mobile Access

While this is a desktop app, you can:
1. Use VNC/Remote Desktop
2. Access via SSH with X11 forwarding
3. Use TeamViewer/AnyDesk

## 🔗 Useful Links

- **Bitcoin**: https://bitcoin.org
- **Litecoin**: https://litecoin.org
- **Dogecoin**: https://dogecoin.com
- **Block Explorers**: Search "[coin] block explorer"

## 📞 Getting Help

1. Check README.md for detailed docs
2. Check INSTALL.md for setup issues
3. Review coin-specific documentation
4. Check daemon logs for errors

## 🎯 Best Practices

1. **Always test first** with small amounts
2. **Double-check addresses** before sending
3. **Keep backups** in multiple locations
4. **Update regularly** to latest versions
5. **Monitor transactions** until confirmed
6. **Use strong passwords** for encryption
7. **Keep seeds offline** written on paper
8. **Verify downloads** with checksums

## ⚡ Performance Tips

- Close unused tabs
- Limit transaction history display
- Stop mining when not needed
- Keep daemon updated
- Use SSD for blockchain data

## 🎓 Learning Resources

### Understanding Wallets
- Wallet = Collection of addresses
- Address = Public key for receiving
- Private key = Secret for spending
- Seed phrase = Backup of all keys

### Transaction Basics
- Confirmations = Security level
- Fee = Priority for miners
- Change = Returned to your wallet
- TXID = Transaction identifier

### Mining Basics
- Difficulty = Mining hardness
- Hashrate = Mining speed
- Block reward = Mining payment
- Pool = Group mining

---

**Keep this guide handy for quick reference! 💰🚀**

*Created by Magnafic0 unchained & Gistgard Reventlov*

*Supporting 23+ cryptocurrencies including Bitcoin, Ethereum, Aleo, Cardano, Solana, and more!*
