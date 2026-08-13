param(
    [int]$Port = 8787
)

$ErrorActionPreference = "Stop"

function Write-Check {
    param(
        [string]$Status,
        [string]$Message
    )
    Write-Output ("[{0}] {1}" -f $Status, $Message)
}

$failed = $false
$portInUse = $false
$recommendedPort = $Port
$root = Split-Path -Parent $MyInvocation.MyCommand.Path

Write-Output "Agentic QA DMAIC Shareable - Environment Check"
Write-Output ("Project root: {0}" -f $root)
Write-Output ""

# 1) Python availability
$pythonCmd = Get-Command python -ErrorAction SilentlyContinue
if (-not $pythonCmd) {
    Write-Check "FAIL" "Python was not found in PATH. Install Python and try again."
    $failed = $true
} else {
    Write-Check "PASS" ("Python command found: {0}" -f $pythonCmd.Source)
}

# 2) Python version
if (-not $failed) {
    $versionOutput = python -c "import sys; print('.'.join(map(str, sys.version_info[:3])))"
    $parts = $versionOutput.Trim().Split('.')
    $major = [int]$parts[0]
    $minor = [int]$parts[1]
    if ($major -gt 3 -or ($major -eq 3 -and $minor -ge 10)) {
        Write-Check "PASS" ("Python version is compatible: {0}" -f $versionOutput.Trim())
    } else {
        Write-Check "FAIL" ("Python 3.10+ required. Detected: {0}" -f $versionOutput.Trim())
        $failed = $true
    }
}

# 3) Required package import check
if (-not $failed) {
    $yamlCheck = python -c "import yaml; print('ok')" 2>$null
    if ($LASTEXITCODE -eq 0) {
        Write-Check "PASS" "PyYAML import check passed."
    } else {
        Write-Check "FAIL" "PyYAML is not installed. Run: pip install -r requirements.txt"
        $failed = $true
    }
}

# 4) Expected files/folders
$paths = @(
    "src/main.py",
    "src/web_app.py",
    "web/index.html",
    "project-context/baseline-project.yaml",
    "requirements.txt"
)
foreach ($relative in $paths) {
    $full = Join-Path $root $relative
    if (Test-Path $full) {
        Write-Check "PASS" ("Found: {0}" -f $relative)
    } else {
        Write-Check "FAIL" ("Missing: {0}" -f $relative)
        $failed = $true
    }
}

# 5) Port availability for web app
try {
    $conn = Get-NetTCPConnection -LocalPort $Port -State Listen -ErrorAction Stop | Select-Object -First 1
    if ($conn) {
        Write-Check "WARN" ("Port {0} is already in use. Start web app with another port." -f $Port)
        $portInUse = $true
        $recommendedPort = $Port + 1
    }
} catch {
    Write-Check "PASS" ("Port {0} appears available for the web app." -f $Port)
}

Write-Output ""
if ($failed) {
    Write-Output "Environment check completed with failures. Fix the FAIL items and rerun this script."
    exit 1
}

if ($portInUse) {
    Write-Output ("Using fallback port suggestion: {0}" -f $recommendedPort)
}

Write-Output "Environment check passed. You can start the web app with:"
Write-Output ("python src/web_app.py --host 127.0.0.1 --port {0}" -f $recommendedPort)
exit 0
