@echo off
REM ============================================================================
REM  ISVZ - Měsíční zpracování veřejných zakázek
REM  
REM  Použití:
REM    run_monthly.bat                - Zpracuje aktuální měsíc
REM    run_monthly.bat 2026 2         - Zpracuje únor 2026
REM    run_monthly.bat skip           - Přeskočí stahování
REM ============================================================================

setlocal enabledelayedexpansion

REM Barvy v Windows konzoli
set "GREEN=[92m"
set "YELLOW=[93m"
set "CYAN=[96m"
set "RED=[91m"
set "RESET=[0m"

cls
echo.
echo ========================================================================
echo   ISVZ - MĚSÍČNÍ ZPRACOVÁNÍ VEŘEJNÝCH ZAKÁZEK
echo ========================================================================
echo.

REM Kontrola parametrů
if "%1"=="skip" (
    set SKIP_DOWNLOAD=1
    echo %YELLOW%⚠️  Stahování bude přeskočeno%RESET%
) else if "%1"=="" (
    set SKIP_DOWNLOAD=0
) else (
    set YEAR=%1
    set MONTH=%2
)

REM Kontrola Python
echo %CYAN%Kontroluji Python...%RESET%
python --version >nul 2>&1
if errorlevel 1 (
    echo %RED%❌ Python není nainstalován nebo není v PATH!%RESET%
    echo    Stáhněte z: https://www.python.org/downloads/
    pause
    exit /b 1
)
python --version
echo %GREEN%✅ Python nalezen%RESET%
echo.

REM Zobrazit čas startu
echo %CYAN%Start: %date% %time%%RESET%
echo.

REM ============================================================================
REM KROK 1: STAHOVÁNÍ
REM ============================================================================

if %SKIP_DOWNLOAD%==0 (
    echo ========================================================================
    echo   📥 KROK 1/3: STAHOVÁNÍ DAT
    echo ========================================================================
    echo.
    
    echo %CYAN%Stahuji VZ soubor (velký, ~1.3 GB)...%RESET%
    if defined YEAR (
        powershell -ExecutionPolicy Bypass -File download_vz.ps1 -Year %YEAR% -Month %MONTH%
    ) else (
        powershell -ExecutionPolicy Bypass -File download_vz.ps1
    )
    
    echo.
    echo %CYAN%Stahuji ostatní kategorie...%RESET%
    if defined YEAR (
        python monthly_process.py --year %YEAR% --month %MONTH% --download
    ) else (
        python monthly_process.py --download
    )
    
    if errorlevel 1 (
        echo %RED%❌ Chyba při stahování%RESET%
    ) else (
        echo %GREEN%✅ Stahování dokončeno%RESET%
    )
) else (
    echo ========================================================================
    echo   ⏭️  KROK 1/3: STAHOVÁNÍ DAT (PŘESKOČENO)
    echo ========================================================================
    echo.
)

echo.

REM ============================================================================
REM KROK 2: ZPRACOVÁNÍ
REM ============================================================================

echo ========================================================================
echo   ⚙️  KROK 2/3: ZPRACOVÁNÍ DAT
echo ========================================================================
echo.

echo %CYAN%Spouštím zpracování (5 automatických kroků):%RESET%
echo   1️⃣  Filtrování otevřených VZ zakázek
echo   2️⃣  Filtrování ICT zakázek z VZ
echo   3️⃣  Filtrování ICT zakázek z DNS
echo   4️⃣  Přidání doporučení (1-5 ⭐)
echo   5️⃣  Generování MD + CSV reportů
echo.

if defined YEAR (
    python monthly_process.py --year %YEAR% --month %MONTH%
) else (
    python monthly_process.py
)

if errorlevel 1 (
    echo.
    echo %RED%❌ Chyba při zpracování%RESET%
    pause
    exit /b 1
) else (
    echo.
    echo %GREEN%✅ Zpracování dokončeno%RESET%
)

echo.

REM ============================================================================
REM KROK 3: POROVNÁNÍ
REM ============================================================================

echo ========================================================================
echo   🔍 KROK 3/3: POROVNÁNÍ S PŘEDCHOZÍM MĚSÍCEM
echo ========================================================================
echo.

echo %CYAN%Generuji rozdílové reporty...%RESET%

if defined YEAR (
    python monthly_process.py --compare %YEAR% %MONTH%
) else (
    python monthly_process.py --compare
)

if errorlevel 1 (
    echo %YELLOW%⚠️  Nepodařilo se vytvořit rozdílové reporty%RESET%
) else (
    echo %GREEN%✅ Rozdílové reporty vytvořeny%RESET%
)

echo.

REM ============================================================================
REM SOUHRN
REM ============================================================================

echo ========================================================================
echo   ✅ DOKONČENO
echo ========================================================================
echo.

echo %CYAN%📁 HLAVNÍ VÝSTUPY:%RESET%
echo.
echo   CSV (Excel ready):
echo   ⭐ output\csv\VZ-ICT.csv
echo      output\csv\VZ-OPEN.csv
echo      output\csv\DNS-ICT.csv
echo.
echo   Markdown reporty:
echo   ⭐ output\reports\VZ-ICT_*.md
echo      output\reports\DIFF_VZ_*.md
echo.

echo.
echo ========================================================================
echo   ✅ MĚSÍČNÍ ZPRACOVÁNÍ DOKONČENO!
echo.
echo   Další kroky:
echo   1. Otevřít output\csv\VZ-ICT.csv v Excelu
echo   2. Filtrovat podle doporučení (1-5 ⭐)
echo   3. Zkontrolovat DIFF reporty pro novinky
echo ========================================================================
echo.

REM Nabídnout otevření složky
set /p OPEN="Otevřít složku s výstupy? (A/n): "
if /i "%OPEN%"=="n" goto :END

start "" "output\csv"

:END
echo.
echo Konec.
pause
