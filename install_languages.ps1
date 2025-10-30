# Quick Installation Script for Missing Languages
# Run this in PowerShell as Administrator

Write-Host "=====================================================================" -ForegroundColor Cyan
Write-Host "Installing Missing Language Support for Code Debugger" -ForegroundColor Cyan
Write-Host "=====================================================================" -ForegroundColor Cyan
Write-Host ""

# Check if running as Administrator
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

if (-not $isAdmin) {
    Write-Host "ERROR: Please run this script as Administrator!" -ForegroundColor Red
    Write-Host "Right-click PowerShell and select 'Run as Administrator'" -ForegroundColor Yellow
    exit 1
}

# Function to check if command exists
function Test-Command($command) {
    try {
        if (Get-Command $command -ErrorAction Stop) {
            return $true
        }
    } catch {
        return $false
    }
}

Write-Host "[1/4] Checking Chocolatey..." -ForegroundColor Yellow
if (-not (Test-Command choco)) {
    Write-Host "Installing Chocolatey package manager..." -ForegroundColor Green
    Set-ExecutionPolicy Bypass -Scope Process -Force
    [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
    iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
    
    # Refresh environment
    $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
} else {
    Write-Host "Chocolatey already installed!" -ForegroundColor Green
}

Write-Host ""
Write-Host "[2/4] Installing PHP..." -ForegroundColor Yellow
if (Test-Command php) {
    Write-Host "PHP already installed: $(php --version | Select-Object -First 1)" -ForegroundColor Green
} else {
    Write-Host "Installing PHP via Chocolatey..." -ForegroundColor Green
    choco install php -y
    refreshenv
}

Write-Host ""
Write-Host "[3/4] Installing Ruby..." -ForegroundColor Yellow
if (Test-Command ruby) {
    Write-Host "Ruby already installed: $(ruby --version)" -ForegroundColor Green
} else {
    Write-Host "Installing Ruby via Chocolatey..." -ForegroundColor Green
    choco install ruby -y
    refreshenv
}

Write-Host ""
Write-Host "[4/4] Installing .NET SDK (for C#)..." -ForegroundColor Yellow
if (Test-Command dotnet) {
    Write-Host ".NET SDK already installed: $(dotnet --version)" -ForegroundColor Green
} else {
    Write-Host "Installing .NET SDK via Chocolatey..." -ForegroundColor Green
    choco install dotnet-sdk -y
    refreshenv
}

Write-Host ""
Write-Host "=====================================================================" -ForegroundColor Cyan
Write-Host "IMPORTANT: Rust Installation" -ForegroundColor Yellow
Write-Host "=====================================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Rust requires a separate installer. Please follow these steps:" -ForegroundColor White
Write-Host ""
Write-Host "1. Open a new PowerShell window (as regular user, not admin)" -ForegroundColor Green
Write-Host "2. Run this command:" -ForegroundColor Green
Write-Host ""
Write-Host '   Invoke-WebRequest -Uri "https://win.rustup.rs/x86_64" -OutFile "rustup-init.exe"; .\rustup-init.exe' -ForegroundColor Cyan
Write-Host ""
Write-Host "3. Press '1' to proceed with standard installation" -ForegroundColor Green
Write-Host "4. Wait for installation to complete" -ForegroundColor Green
Write-Host "5. Close and reopen PowerShell" -ForegroundColor Green
Write-Host ""

Write-Host "=====================================================================" -ForegroundColor Cyan
Write-Host "Installation Complete!" -ForegroundColor Green
Write-Host "=====================================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next Steps:" -ForegroundColor Yellow
Write-Host "1. Install Rust using the instructions above" -ForegroundColor White
Write-Host "2. Close and reopen PowerShell" -ForegroundColor White
Write-Host "3. Verify installations by running: " -ForegroundColor White
Write-Host "   php --version" -ForegroundColor Cyan
Write-Host "   ruby --version" -ForegroundColor Cyan
Write-Host "   dotnet --version" -ForegroundColor Cyan
Write-Host "   rustc --version" -ForegroundColor Cyan
Write-Host ""
Write-Host "4. Test the debugger:" -ForegroundColor White
Write-Host "   cd <your-project-directory>" -ForegroundColor Cyan
Write-Host "   python test_complex_new_languages_success.py" -ForegroundColor Cyan
Write-Host ""
