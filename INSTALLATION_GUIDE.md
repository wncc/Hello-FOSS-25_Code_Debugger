# Installation Guide for Multi-Language Support

This guide will help you install all the required compilers and interpreters for the 9-language debugger on Windows.

---

## 🔧 Languages Currently Working
- ✅ **Python 3.8+** (Already installed)
- ✅ **C** (gcc via MinGW - Already installed)
- ✅ **C++** (g++ via MinGW - Already installed)
- ✅ **JavaScript** (Node.js v22.19.0 - Already installed)

## 📦 Languages Requiring Installation
- ⚠️ **Rust** (rustc compiler)
- ⚠️ **Ruby** (Ruby interpreter)
- ⚠️ **PHP** (PHP CLI)
- ⚠️ **C#** (.NET SDK with csc compiler)

---

## 1️⃣ Install Rust

### Using Rustup (Recommended)

1. **Download Rustup Installer**
   - Visit: https://rustup.rs/
   - Or direct link: https://win.rustup.rs/x86_64

2. **Run the Installer**
   ```powershell
   # Download and run (PowerShell)
   Invoke-WebRequest -Uri "https://win.rustup.rs/x86_64" -OutFile "rustup-init.exe"
   .\rustup-init.exe
   ```

3. **Follow the Installation Prompts**
   - Press `1` to proceed with default installation
   - Wait for the installation to complete

4. **Verify Installation**
   ```powershell
   # Close and reopen PowerShell, then:
   rustc --version
   cargo --version
   ```

   Expected output:
   ```
   rustc 1.xx.x (xxxxx 20xx-xx-xx)
   cargo 1.xx.x (xxxxx 20xx-xx-xx)
   ```

---

## 2️⃣ Install Ruby

### Using RubyInstaller (Recommended for Windows)

1. **Download RubyInstaller**
   - Visit: https://rubyinstaller.org/downloads/
   - Download: **Ruby+Devkit 3.3.x (x64)** (latest stable version)

2. **Run the Installer**
   ```powershell
   # Download (PowerShell)
   Invoke-WebRequest -Uri "https://github.com/oneclick/rubyinstaller2/releases/download/RubyInstaller-3.3.6-1/rubyinstaller-devkit-3.3.6-1-x64.exe" -OutFile "rubyinstaller.exe"
   
   # Run installer
   .\rubyinstaller.exe
   ```

3. **Installation Steps**
   - Check "Add Ruby executables to your PATH"
   - Check "Associate .rb and .rbw files with this Ruby installation"
   - Click "Install"
   - When prompted, run `ridk install` (press Enter to accept defaults)

4. **Verify Installation**
   ```powershell
   # Close and reopen PowerShell, then:
   ruby --version
   gem --version
   ```

   Expected output:
   ```
   ruby 3.3.x (20xx-xx-xx revision xxxxx)
   3.5.x
   ```

---

## 3️⃣ Install PHP

### Using Chocolatey (Easiest)

1. **Install Chocolatey** (if not already installed)
   ```powershell
   # Run as Administrator
   Set-ExecutionPolicy Bypass -Scope Process -Force
   [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
   iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
   ```

2. **Install PHP**
   ```powershell
   # Run as Administrator
   choco install php -y
   ```

3. **Verify Installation**
   ```powershell
   # Close and reopen PowerShell, then:
   php --version
   ```

   Expected output:
   ```
   PHP 8.x.x (cli) (built: xxx)
   ```

### Alternative: Manual Installation

1. **Download PHP**
   - Visit: https://windows.php.net/download/
   - Download: **PHP 8.x VC15 x64 Non Thread Safe**

2. **Extract and Configure**
   ```powershell
   # Extract to C:\php
   Expand-Archive -Path "php-8.x.x-nts-Win32-vs16-x64.zip" -DestinationPath "C:\php"
   
   # Add to PATH
   [Environment]::SetEnvironmentVariable("Path", $env:Path + ";C:\php", "Machine")
   ```

3. **Verify Installation**
   ```powershell
   # Close and reopen PowerShell, then:
   php --version
   ```

---

## 4️⃣ Install .NET SDK (for C#)

### Using Official Installer (Recommended)

1. **Download .NET SDK**
   - Visit: https://dotnet.microsoft.com/download
   - Download: **.NET 8.0 SDK** (latest LTS version)

2. **Run the Installer**
   ```powershell
   # Download (PowerShell)
   Invoke-WebRequest -Uri "https://dotnet.microsoft.com/download/dotnet/thank-you/sdk-8.0.404-windows-x64-installer" -OutFile "dotnet-sdk-installer.exe"
   
   # Run installer
   .\dotnet-sdk-installer.exe
   ```

3. **Installation Steps**
   - Click "Install"
   - Wait for installation to complete

4. **Verify Installation**
   ```powershell
   # Close and reopen PowerShell, then:
   dotnet --version
   
   # Check for csc compiler
   where.exe csc
   ```

   Expected output:
   ```
   8.0.xxx
   C:\Program Files\dotnet\sdk\8.0.xxx\Roslyn\bincore\csc.dll
   ```

   **Note**: `csc` might not be directly in PATH. You may need to use Developer Command Prompt or add it manually.

5. **Add csc to PATH (if needed)**
   ```powershell
   # Find .NET SDK path
   $sdkPath = dotnet --list-sdks | Select-Object -First 1 | ForEach-Object { $_.Split('[')[1].Trim(']') }
   $cscPath = Join-Path $sdkPath "Roslyn\bincore"
   
   # Add to PATH
   [Environment]::SetEnvironmentVariable("Path", $env:Path + ";$cscPath", "Machine")
   ```

---

## 🎯 Quick Installation Commands (All at Once)

**Run PowerShell as Administrator** and execute:

```powershell
# Install Chocolatey (if not installed)
Set-ExecutionPolicy Bypass -Scope Process -Force
iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))

# Install PHP
choco install php -y

# Install Ruby
choco install ruby -y

# Rust (requires separate installer from rustup.rs)
Invoke-WebRequest -Uri "https://win.rustup.rs/x86_64" -OutFile "rustup-init.exe"
.\rustup-init.exe

# .NET SDK
choco install dotnet-sdk -y

# Refresh environment
refreshenv
```

---

## ✅ Verify All Installations

After installing everything, **close and reopen PowerShell**, then run:

```powershell
# Check all compilers/interpreters
python --version
gcc --version
g++ --version
javac -version
node --version
rustc --version
ruby --version
php --version
dotnet --version
```

---

## 🧪 Test the Debugger

After installation, test with all languages:

```powershell
cd C:\Users\sayan\Hello-FOSS-25_Code_Debugger
python test_complex_new_languages_success.py
```

All tests should now execute successfully! 🎉

---

## 🔧 Troubleshooting

### Rust not found after installation
- Close and reopen PowerShell
- Check PATH: `$env:PATH -split ';' | Select-String cargo`
- Manually add: `~/.cargo/bin` to PATH

### Ruby not found
- Verify installation: Check `C:\Ruby33-x64\bin`
- Add to PATH manually if needed

### PHP not found
- Run as Administrator when installing with Chocolatey
- Use `refreshenv` after installation

### csc not found (C#)
- Use **Developer Command Prompt for VS** instead of regular PowerShell
- Or manually add Roslyn folder to PATH

---

## 📚 Additional Resources

- **Rust**: https://www.rust-lang.org/tools/install
- **Ruby**: https://www.ruby-lang.org/en/downloads/
- **PHP**: https://www.php.net/downloads.php
- **C#/.NET**: https://dotnet.microsoft.com/download

---

**Happy Debugging! 🚀**
