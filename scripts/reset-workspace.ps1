[CmdletBinding()]
param(
    [Parameter(ParameterSetName = "Full", Mandatory = $true)]
    [switch]$Full,

    [Parameter(ParameterSetName = "Research", Mandatory = $true)]
    [switch]$Research,

    [Parameter(ParameterSetName = "Content", Mandatory = $true)]
    [switch]$Content,

    [Parameter(ParameterSetName = "Analytics", Mandatory = $true)]
    [switch]$Analytics,

    [Parameter(ParameterSetName = "Scratch", Mandatory = $true)]
    [switch]$Scratch,

    [switch]$Force
)

$ErrorActionPreference = "Stop"

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $ScriptDir
$KnowledgeCraftRoot = Join-Path $RepoRoot ".knowledgecraft"

switch ($PSCmdlet.ParameterSetName) {
    "Full" {
        $Target = $KnowledgeCraftRoot
        $Label = "the entire generated .knowledgecraft workspace"
    }
    "Research" {
        $Target = Join-Path $KnowledgeCraftRoot "research"
        $Label = "generated research state"
    }
    "Content" {
        $Target = Join-Path $KnowledgeCraftRoot "content"
        $Label = "generated content/LinkedIn state"
    }
    "Analytics" {
        $Target = Join-Path $KnowledgeCraftRoot "analytics"
        $Label = "generated analytics state"
    }
    "Scratch" {
        $Target = Join-Path $KnowledgeCraftRoot "scratch"
        $Label = "generated scratch/integration state"
    }
    default {
        Write-Error "Choose exactly one reset mode: -Full, -Research, -Content, -Analytics, or -Scratch."
        exit 2
    }
}

Write-Host "KnowledgeCraft workspace reset"
Write-Host "Repository: $RepoRoot"
Write-Host "Target:     $Target"
Write-Host "Reset:      $Label"

if (-not (Test-Path -LiteralPath $Target)) {
    Write-Host ""
    Write-Host "Nothing to reset. Target does not exist."
    exit 0
}

if (-not $Force) {
    Write-Host ""
    Write-Host "This permanently deletes generated files under the target above."
    Write-Host "It does not delete .opencode/skills/, AGENTS.md, or papers/."
    $Confirmation = Read-Host "Type RESET to continue"

    if ($Confirmation -cne "RESET") {
        Write-Host "Reset cancelled."
        exit 0
    }
}

Remove-Item -LiteralPath $Target -Recurse -Force

Write-Host ""
Write-Host "KnowledgeCraft reset complete."
Write-Host "Deleted: $Target"
Write-Host "Required directories will be recreated by future workflows."
