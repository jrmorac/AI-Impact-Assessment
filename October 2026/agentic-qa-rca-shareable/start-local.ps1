param(
    [int]$Port = 8787,
    [string]$HostAddress = "127.0.0.1",
    [switch]$SkipCheck,
    [switch]$DryRun
)

$ErrorActionPreference = "Stop"

function Test-PortInUse {
    param([int]$CandidatePort)
    try {
        $conn = Get-NetTCPConnection -LocalPort $CandidatePort -State Listen -ErrorAction Stop | Select-Object -First 1
        return $null -ne $conn
    } catch {
        return $false
    }
}

function Get-AvailablePort {
    param(
        [int]$StartPort,
        [int]$MaxAttempts = 50
    )

    $candidate = $StartPort
    for ($i = 0; $i -lt $MaxAttempts; $i++) {
        if (-not (Test-PortInUse -CandidatePort $candidate)) {
            return $candidate
        }
        $candidate++
    }

    throw ("No available port found from {0} to {1}." -f $StartPort, ($StartPort + $MaxAttempts - 1))
}

$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$checkScript = Join-Path $root "check-env.ps1"

Push-Location $root
try {
    if (-not $SkipCheck) {
        & $checkScript -Port $Port
        if ($LASTEXITCODE -ne 0) {
            Write-Output "Environment check failed. Launcher stopped."
            exit $LASTEXITCODE
        }
    }

    $selectedPort = Get-AvailablePort -StartPort $Port
    if ($selectedPort -ne $Port) {
        Write-Output ("Requested port {0} is in use. Using {1}." -f $Port, $selectedPort)
    }

    $command = "python src/web_app.py --host {0} --port {1}" -f $HostAddress, $selectedPort
    Write-Output "Starting local web app..."
    Write-Output $command

    if ($DryRun) {
        Write-Output "Dry-run mode enabled. Server was not started."
        exit 0
    }

    & python src/web_app.py --host $HostAddress --port $selectedPort
    exit $LASTEXITCODE
} finally {
    Pop-Location
}
