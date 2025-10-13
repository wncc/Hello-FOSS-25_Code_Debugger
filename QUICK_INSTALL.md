# Quick Manual Installation Steps

Follow these commands in order. You'll need PowerShell with Administrator privileges.

---

## Option 1: Automated Installation (Recommended)

### Step 1: Open PowerShell as Administrator
- Press `Win + X`
- Select "Windows PowerShell (Admin)" or "Terminal (Admin)"

### Step 2: Run the installation script
```powershell
cd C:\Users\sayan\Hello-FOSS-25_Code_Debugger
.\install_languages.ps1
```

### Step 3: Install Rust separately
```powershell
# Open a NEW PowerShell window (as regular user)
Invoke-WebRequest -Uri "https://win.rustup.rs/x86_64" -OutFile "rustup-init.exe"
.\rustup-init.exe
# Press 1 and Enter
```

---

## Option 2: Manual Installation

### 1. Install Chocolatey (Package Manager)
```powershell
# Run as Administrator
Set-ExecutionPolicy Bypass -Scope Process -Force
[System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
Invoke-Expression ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
```

### 2. Install PHP
```powershell
choco install php -y
```

### 3. Install Ruby
```powershell
choco install ruby -y
```

### 4. Install .NET SDK (for C#)
```powershell
choco install dotnet-sdk -y
```

### 5. Install Rust
```powershell
# Open NEW PowerShell (regular user, not admin)
Invoke-WebRequest -Uri "https://win.rustup.rs/x86_64" -OutFile "rustup-init.exe"
.\rustup-init.exe
# Press 1 and Enter when prompted
```

### 6. Refresh Environment
```powershell
# Close and reopen PowerShell
```

---

## Verify Installations

After closing and reopening PowerShell, run:

```powershell
# Check all languages
php --version
ruby --version
dotnet --version
rustc --version
```

Expected output:
```
PHP 8.x.x (cli)
ruby 3.3.x
8.0.xxx
rustc 1.xx.x
```

---

## Test the Debugger

```powershell
cd C:\Users\sayan\Hello-FOSS-25_Code_Debugger
python test_complex_new_languages_success.py
```

All tests should now pass! ✅

---

## Troubleshooting

### If PHP not found:
```powershell
refreshenv
# Or restart PowerShell
```

### If Ruby not found:
```powershell
# Check if installed
Get-Command ruby
# If not found, try:
choco uninstall ruby -y
choco install ruby -y
```

### If .NET/csc not found:
```powershell
dotnet --version  # Should work
# csc might need Developer Command Prompt
```

### If Rust not found:
```powershell
# Check cargo bin directory
$env:USERPROFILE\.cargo\bin
# Add to PATH if needed
$env:Path += ";$env:USERPROFILE\.cargo\bin"
```

---

## Quick Commands Reference

| Language | Check Version | Install Command |
|----------|---------------|-----------------|
| PHP | `php --version` | `choco install php -y` |
| Ruby | `ruby --version` | `choco install ruby -y` |
| .NET/C# | `dotnet --version` | `choco install dotnet-sdk -y` |
| Rust | `rustc --version` | Download from rustup.rs |

---

**Need Help?** See INSTALLATION_GUIDE.md for detailed instructions.
