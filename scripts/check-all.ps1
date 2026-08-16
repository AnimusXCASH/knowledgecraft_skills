[CmdletBinding()]
param(
    [switch]$VerboseOutput
)

$ErrorActionPreference = "Stop"

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $ScriptDir
$Runner = Join-Path $ScriptDir "check_all.py"

if (-not (Test-Path $Runner)) {
    Write-Error "Repository checker not found: $Runner"
    exit 2
}

# Prefer the Windows Python launcher when available because that is the
# convention used by this repository. Fall back to python if necessary.
$PyLauncher = Get-Command py -ErrorAction SilentlyContinue

if ($PyLauncher) {
    $PythonCommand = "py"
}
else {
    $Python = Get-Command python -ErrorAction SilentlyContinue
    if (-not $Python) {
        Write-Error "Python was not found. Install Python or make 'py'/'python' available on PATH."
        exit 2
    }
    $PythonCommand = "python"
}

$ArgsList = @(
    $Runner
    "--root"
    $RepoRoot
)

if ($VerboseOutput) {
    $ArgsList += "--verbose-output"
}

& $PythonCommand @ArgsList
$ExitCode = $LASTEXITCODE

if ($ExitCode -ne 0) {
    exit $ExitCode
}
