<#
.SYNOPSIS
    Automatické měsíční zpracování veřejných zakázek z ISVZ - kompletní workflow

.DESCRIPTION
    Tento script provede celý měsíční proces v jednom běhu:
    1. Stažení VZ souboru (velký, 1.3 GB)
    2. Stažení ostatních kategorií (DNS, SON...)
    3. Zpracování (5 kroků: filtr OPEN → ICT → doporučení → reporty)
    4. Porovnání s předchozím měsícem
    
.PARAMETER Year
    Rok (výchozí: aktuální rok)
    
.PARAMETER Month
    Měsíc 1-12 (výchozí: aktuální měsíc)
    
.PARAMETER SkipDownload
    Přeskočit stahování (pokud už máte data)
    
.PARAMETER SkipVZ
    Přeskočit stahování velkého VZ souboru
    
.PARAMETER SkipComparison
    Neprovádět porovnání s předchozím měsícem
    
.EXAMPLE
    .\run_monthly.ps1
    Zpracuje aktuální měsíc (vše automaticky)
    
.EXAMPLE
    .\run_monthly.ps1 -Year 2026 -Month 2
    Zpracuje únor 2026
    
.EXAMPLE
    .\run_monthly.ps1 -SkipDownload
    Jen zpracuje data (bez stahování)
#>

param(
    [int]$Year = (Get-Date).Year,
    [int]$Month = (Get-Date).Month,
    [switch]$SkipDownload,
    [switch]$SkipVZ,
    [switch]$SkipComparison
)

# Barvy pro výstup
function Write-Step {
    param([string]$Message, [string]$Icon = "🔄")
    Write-Host ""
    Write-Host "=" -NoNewline -ForegroundColor Cyan
    Write-Host ("=" * 70) -ForegroundColor Cyan
    Write-Host "  $Icon $Message" -ForegroundColor Yellow
    Write-Host ("=" * 71) -ForegroundColor Cyan
    Write-Host ""
}

function Write-Success {
    param([string]$Message)
    Write-Host "✅ $Message" -ForegroundColor Green
}

function Write-Info {
    param([string]$Message)
    Write-Host "ℹ️  $Message" -ForegroundColor Cyan
}

function Write-Warning {
    param([string]$Message)
    Write-Host "⚠️  $Message" -ForegroundColor Yellow
}

function Write-Error-Custom {
    param([string]$Message)
    Write-Host "❌ $Message" -ForegroundColor Red
}

# Hlavní banner
Clear-Host
Write-Host ""
Write-Host "╔════════════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║                                                                    ║" -ForegroundColor Cyan
Write-Host "║     ISVZ - MĚSÍČNÍ ZPRACOVÁNÍ VEŘEJNÝCH ZAKÁZEK                   ║" -ForegroundColor Yellow
Write-Host "║     Automatický workflow pro $Month/$Year                              ║" -ForegroundColor Yellow
Write-Host "║                                                                    ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# Kontrola Python
Write-Info "Kontroluji Python..."
try {
    $pythonVersion = python --version 2>&1
    Write-Success "Python nalezen: $pythonVersion"
} catch {
    Write-Error-Custom "Python není nainstalován nebo není v PATH!"
    Write-Host "Návod: https://www.python.org/downloads/"
    exit 1
}

# Čas startu
$startTime = Get-Date
Write-Info "Start: $(Get-Date -Format 'dd.MM.yyyy HH:mm:ss')"
Write-Host ""

# ====================
# KROK 1: STAHOVÁNÍ
# ====================

if (-not $SkipDownload) {
    Write-Step "KROK 1/5: STAHOVÁNÍ DAT" "📥"
    
    # VZ soubor (velký)
    if (-not $SkipVZ) {
        Write-Info "Stahuji VZ soubor (velký, ~1.3 GB, může trvat několik minut)..."
        try {
            & .\download_vz.ps1 -Year $Year -Month $Month
            if ($LASTEXITCODE -eq 0) {
                Write-Success "VZ soubor stažen"
            } else {
                Write-Warning "VZ soubor se nepodařilo stáhnout - pokračuji"
            }
        } catch {
            Write-Warning "Chyba při stahování VZ: $_"
            Write-Info "Pokračuji s ostatními soubory..."
        }
    } else {
        Write-Warning "Stahování VZ přeskočeno (--SkipVZ)"
    }
    
    # Ostatní soubory
    Write-Info "Stahuji ostatní kategorie (DNS, SON, SK, RVP)..."
    try {
        python monthly_process.py --year $Year --month $Month --download
        if ($LASTEXITCODE -eq 0) {
            Write-Success "Ostatní soubory staženy"
        } else {
            Write-Warning "Některé soubory se nepodařilo stáhnout"
        }
    } catch {
        Write-Error-Custom "Chyba při stahování: $_"
    }
} else {
    Write-Step "KROK 1/5: STAHOVÁNÍ DAT (PŘESKOČENO)" "⏭️"
    Write-Warning "Stahování přeskočeno - používám existující data"
}

# ====================
# KROK 2: ZPRACOVÁNÍ
# ====================

Write-Step "KROK 2/5: ZPRACOVÁNÍ DAT" "⚙️"

Write-Info "Spouštím zpracování (5 automatických kroků)..."
Write-Host "  1️⃣  Filtrování otevřených VZ zakázek"
Write-Host "  2️⃣  Filtrování ICT zakázek z VZ"
Write-Host "  3️⃣  Filtrování ICT zakázek z DNS"
Write-Host "  4️⃣  Přidání doporučení (1-5 ⭐)"
Write-Host "  5️⃣  Generování MD + CSV reportů"
Write-Host ""

try {
    python monthly_process.py --year $Year --month $Month
    
    if ($LASTEXITCODE -eq 0) {
        Write-Success "Zpracování dokončeno!"
    } else {
        Write-Error-Custom "Chyba při zpracování (exit code: $LASTEXITCODE)"
        Write-Info "Zkontrolujte chybové hlášky výše"
        exit 1
    }
} catch {
    Write-Error-Custom "Chyba při zpracování: $_"
    exit 1
}

# ====================
# KROK 3: POROVNÁNÍ
# ====================

if (-not $SkipComparison) {
    Write-Step "KROK 3/5: POROVNÁNÍ S PŘEDCHOZÍM MĚSÍCEM" "🔍"
    
    Write-Info "Generuji rozdílové reporty..."
    try {
        python monthly_process.py --compare $Year $Month
        
        if ($LASTEXITCODE -eq 0) {
            Write-Success "Rozdílové reporty vytvořeny"
        } else {
            Write-Warning "Nepodařilo se vytvořit rozdílové reporty"
        }
    } catch {
        Write-Warning "Chyba při porovnání: $_"
    }
} else {
    Write-Step "KROK 3/5: POROVNÁNÍ (PŘESKOČENO)" "⏭️"
    Write-Warning "Porovnání přeskočeno"
}

# ====================
# SOUHRN
# ====================

Write-Step "DOKONČENO" "✅"

$monthStr = "{0:D2}" -f $Month

# Statistiky - zkus načíst počty ze souborů
$vzIctPath = "data\VZ\VZ-$Year-$monthStr-ICT.json"
$dnsIctPath = "data\DNS\DNS-$Year-$monthStr-ICT.json"

$vzCount = 0
$dnsCount = 0

if (Test-Path $vzIctPath) {
    try {
        $vzData = Get-Content $vzIctPath -Raw | ConvertFrom-Json
        $vzCount = $vzData.data.Count
    } catch {}
}

if (Test-Path $dnsIctPath) {
    try {
        $dnsData = Get-Content $dnsIctPath -Raw | ConvertFrom-Json
        $dnsCount = $dnsData.data.Count
    } catch {}
}

Write-Host ""
Write-Host "📊 STATISTIKY:" -ForegroundColor Cyan
Write-Host "   ICT zakázky (VZ):  $vzCount" -ForegroundColor White
Write-Host "   ICT zakázky (DNS): $dnsCount" -ForegroundColor White
Write-Host ""

Write-Host "📁 HLAVNÍ VÝSTUPY:" -ForegroundColor Cyan
Write-Host ""
Write-Host "   CSV (Excel ready):" -ForegroundColor Yellow
Write-Host "   ⭐ output\csv\VZ-ICT.csv" -ForegroundColor Green
Write-Host "      output\csv\VZ-OPEN.csv" -ForegroundColor White
Write-Host "      output\csv\DNS-ICT.csv" -ForegroundColor White
Write-Host ""
Write-Host "   Markdown reporty:" -ForegroundColor Yellow
Write-Host "   ⭐ output\reports\VZ-ICT_$Year-$monthStr.md" -ForegroundColor Green
Write-Host "      output\reports\DIFF_VZ_$monthStr-$Year.md" -ForegroundColor White
Write-Host ""
Write-Host "   Vyfiltrované JSON:" -ForegroundColor Yellow
Write-Host "      data\VZ\VZ-$Year-$monthStr-ICT.json" -ForegroundColor White
Write-Host "      data\DNS\DNS-$Year-$monthStr-ICT.json" -ForegroundColor White
Write-Host ""

# Čas běhu
$endTime = Get-Date
$duration = $endTime - $startTime
Write-Host "⏱️  Celkový čas: $($duration.ToString('mm\:ss'))" -ForegroundColor Cyan
Write-Host ""

Write-Host "╔════════════════════════════════════════════════════════════════════╗" -ForegroundColor Green
Write-Host "║                                                                    ║" -ForegroundColor Green
Write-Host "║  ✅ MĚSÍČNÍ ZPRACOVÁNÍ DOKONČENO!                                  ║" -ForegroundColor Green
Write-Host "║                                                                    ║" -ForegroundColor Green
Write-Host "║  Další kroky:                                                      ║" -ForegroundColor Yellow
Write-Host "║  1. Otevřít output\csv\VZ-ICT.csv v Excelu                        ║" -ForegroundColor White
Write-Host "║  2. Filtrovat podle doporučení (1-5 ⭐)                            ║" -ForegroundColor White
Write-Host "║  3. Zkontrolovat DIFF_VZ_$monthStr-$Year.md pro novinky               ║" -ForegroundColor White
Write-Host "║                                                                    ║" -ForegroundColor Green
Write-Host "╚════════════════════════════════════════════════════════════════════╝" -ForegroundColor Green
Write-Host ""

# Otevřít složku s výstupy?
$openFolder = Read-Host "Otevřít složku s výstupy? (A/n)"
if ($openFolder -ne 'n' -and $openFolder -ne 'N') {
    Start-Process "output\csv"
}
