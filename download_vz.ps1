<#
.SYNOPSIS
Stahuje ISVZ JSON soubor pro zvoleny mesic a rok.

.DESCRIPTION
Stahne soubor VZ-<YYYY>-<MM>.json z ISVZ portalu. Primarne pouziva BITS pro
spolehlive stahovani velkych souboru, pri chybe pouzije Invoke-WebRequest.
Podporuje -WhatIf a -Confirm.

.PARAMETER Year
Rok souboru (YYYY). Vychozi je aktualni rok.

.PARAMETER Month
Mesic souboru (1-12). Vychozi je aktualni mesic.

.PARAMETER DataDir
Cilovy adresar pro stazene soubory.

.PARAMETER Force
Prepise existujici soubor bez potvrzeni.

.EXAMPLE
./download_vz.ps1 -Year 2026 -Month 1

.EXAMPLE
./download_vz.ps1 -Year 2026 -Month 1 -DataDir .\data -Force
#>
[CmdletBinding(SupportsShouldProcess = $true, ConfirmImpact = 'Medium')]
param(
    [Parameter()]
    [ValidateRange(2000, 2100)]
    [int]$Year = (Get-Date).Year,

    [Parameter()]
    [ValidateRange(1, 12)]
    [int]$Month = (Get-Date).Month,

    [Parameter()]
    [ValidateNotNullOrEmpty()]
    [string]$DataDir = "data\VZ",

    [Parameter()]
    [switch]$Force
)

# Vytvor adresare pokud neexistuji
if (-not (Test-Path -Path "data")) {
    New-Item -ItemType Directory -Path "data" | Out-Null
}
if (-not (Test-Path -Path $DataDir)) {
    New-Item -ItemType Directory -Path $DataDir | Out-Null
}

# Nový formát: VZ-YYYY-MM.json (pro lepší chronologické řazení)
$MonthStr = "{0:D2}" -f $Month
$FileName = "VZ-$Year-$MonthStr.json"
$Url = "https://isvz.nipez.cz/sites/default/files/content/opendata-rvz/$FileName"
$DestPath = Join-Path $DataDir $FileName

Write-Information "======================================================================" -InformationAction Continue
Write-Information "  STAHOVANI VZ SOUBORU PRO $Month/$Year" -InformationAction Continue
Write-Information "======================================================================" -InformationAction Continue
Write-Information "URL: $Url" -InformationAction Continue
Write-Information "Cil: $DestPath" -InformationAction Continue

# Zkontroluj zda uz existuje
if (Test-Path -Path $DestPath) {
    $Size = (Get-Item -Path $DestPath).Length / 1MB
    $Message = "Soubor jiz existuje ($([math]::Round($Size, 1)) MB)."
    if (-not $Force) {
        $ShouldOverwrite = $PSCmdlet.ShouldContinue($Message, "Prepsat existujici soubor?")
        if (-not $ShouldOverwrite) {
            Write-Information "Stahovani zruseno." -InformationAction Continue
            return
        }
    }
}

Write-Information "Stahuji... (muze trvat nekolik minut)" -InformationAction Continue

try {
    if ($PSCmdlet.ShouldProcess($DestPath, "Stahnout soubor")) {
        # Pouzij BITS pro spolehlive stahovani velkych souboru
        Import-Module BitsTransfer -ErrorAction Stop

        $Job = Start-BitsTransfer `
            -Source $Url `
            -Destination $DestPath `
            -DisplayName "Stahovani $FileName" `
            -Description "ISVZ data pro $Month/$Year" `
            -Asynchronous `
            -ErrorAction Stop

        # Zobraz progress
        while ($Job.JobState -eq "Transferring" -or $Job.JobState -eq "Connecting") {
            if ($Job.BytesTotal -gt 0) {
                $Progress = [math]::Round(($Job.BytesTransferred / $Job.BytesTotal) * 100, 1)
                $TransferredMB = [math]::Round($Job.BytesTransferred / 1MB, 1)
                $TotalMB = [math]::Round($Job.BytesTotal / 1MB, 1)

                Write-Progress `
                    -Activity "Stahovani $FileName" `
                    -Status "$TransferredMB MB z $TotalMB MB ($Progress %)" `
                    -PercentComplete $Progress
            }

            Start-Sleep -Seconds 1
        }

        Complete-BitsTransfer -BitsJob $Job -ErrorAction Stop
        Write-Progress -Activity "Stahovani" -Completed

        $FinalSize = (Get-Item -Path $DestPath).Length / 1MB
        Write-Information "Stazeno uspesne." -InformationAction Continue
        Write-Information "Velikost: $([math]::Round($FinalSize, 1)) MB" -InformationAction Continue
        Write-Information "Umisteni: $DestPath" -InformationAction Continue
    }
}
catch {
    Write-Error "Chyba pri stahovani: $_"

    # Pokud BITS selze, zkus Invoke-WebRequest
    Write-Information "Zkousim alternativni metodu..." -InformationAction Continue

    try {
        if ($PSCmdlet.ShouldProcess($DestPath, "Stahnout soubor (alternativni metoda)")) {
            Invoke-WebRequest -Uri $Url -OutFile $DestPath -ErrorAction Stop

            $FinalSize = (Get-Item -Path $DestPath).Length / 1MB
            Write-Information "Stazeno uspesne." -InformationAction Continue
            Write-Information "Velikost: $([math]::Round($FinalSize, 1)) MB" -InformationAction Continue
        }
    }
    catch {
        Write-Error "Alternativni metoda take selhala: $_"
        Write-Information "Zkuste stahnout rucne z prohlizece:" -InformationAction Continue
        Write-Information "$Url" -InformationAction Continue
        exit 1
    }
}

Write-Information "Hotovo. Nyni muzete spustit zpracovani:" -InformationAction Continue
Write-Information "python monthly_process.py --year $Year --month $Month" -InformationAction Continue
