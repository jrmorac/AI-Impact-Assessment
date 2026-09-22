param(
    [string]$PackageName = "agentic-qa-rca-shareable",
    [string]$OutputDir = ""
)

$ErrorActionPreference = "Stop"

$sourceRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$parentRoot = Split-Path -Parent $sourceRoot

if ([string]::IsNullOrWhiteSpace($OutputDir)) {
    $OutputDir = Join-Path $parentRoot "dist"
}

if (!(Test-Path $OutputDir)) {
    New-Item -ItemType Directory -Path $OutputDir | Out-Null
}

$timestamp = Get-Date -Format "yyyyMMdd-HHmmss"
$zipPath = Join-Path $OutputDir ("{0}-{1}.zip" -f $PackageName, $timestamp)
$stagingRoot = Join-Path $env:TEMP ("{0}-{1}" -f $PackageName, $timestamp)

if (Test-Path $stagingRoot) {
    Remove-Item -Path $stagingRoot -Recurse -Force
}

New-Item -ItemType Directory -Path $stagingRoot | Out-Null
Copy-Item -Path (Join-Path $sourceRoot "*") -Destination $stagingRoot -Recurse -Force

# Remove local/runtime artifacts from the staging copy.
$foldersToRemove = @("__pycache__", ".venv", "venv", ".git")
Get-ChildItem -Path $stagingRoot -Recurse -Directory -Force |
    Where-Object { $foldersToRemove -contains $_.Name } |
    ForEach-Object { Remove-Item -Path $_.FullName -Recurse -Force }

$runtimeFileRegex = @(
    "\\data\\output\\.*\.json$",
    "\\evidence\\rca_sessions\\.*\.json$",
    "\\evidence\\rca_reports\\.*\.md$",
    "\\evidence\\capa_exports\\.*\.csv$",
    "\\evidence\\evidence_log\.csv$"
)

Get-ChildItem -Path $stagingRoot -Recurse -File -Force |
    Where-Object {
        $full = $_.FullName
        $isRuntime = $false
        foreach ($rx in $runtimeFileRegex) {
            if ($full -match $rx) {
                $isRuntime = $true
                break
            }
        }
        $_.Extension -eq ".pyc" -or $isRuntime
    } |
    Remove-Item -Force

if (Test-Path $zipPath) {
    Remove-Item -Path $zipPath -Force
}

Compress-Archive -Path (Join-Path $stagingRoot "*") -DestinationPath $zipPath -CompressionLevel Optimal -Force
Remove-Item -Path $stagingRoot -Recurse -Force

Write-Output "Package created: $zipPath"
