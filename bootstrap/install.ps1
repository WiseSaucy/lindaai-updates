# LindaAI Bootstrap Installer — Windows (PowerShell)
#
# Usage:
#   irm https://raw.githubusercontent.com/WiseSaucy/lindaai-updates/main/bootstrap/install.ps1 | iex
#   (then paste license key when prompted)
# OR:
#   powershell -Command "& { iwr -useb https://raw.githubusercontent.com/WiseSaucy/lindaai-updates/main/bootstrap/install.ps1 | iex }"
#
# © 2026 LindaAI — Built by Daniel Wise

param(
    [string]$LicenseKey
)

$API = "https://lindaai-api-production.up.railway.app"
$CDN = "https://raw.githubusercontent.com/WiseSaucy/lindaai-updates/main"
$ClaudeDir = Join-Path $env:USERPROFILE ".claude"
$SkillsDir = Join-Path $ClaudeDir "skills"
$AgentsDir = Join-Path $ClaudeDir "agents"
$BrainDir  = Join-Path $ClaudeDir "lindaai-brain"

Write-Host ""
Write-Host "╔════════════════════════════════════════════════════════════╗"
Write-Host "║     LindaAI — License-Gated Bootstrap Installer           ║"
Write-Host "║     © 2026 LindaAI — Built by Daniel Wise                 ║"
Write-Host "╚════════════════════════════════════════════════════════════╝"
Write-Host ""

if (-not $LicenseKey) {
    $LicenseKey = Read-Host "Enter your LindaAI license key"
}

if (-not $LicenseKey) {
    Write-Host "❌ No license key provided. Check your Gumroad email." -ForegroundColor Red
    exit 1
}

$keyPreview = $LicenseKey.Substring(0, [Math]::Min(6, $LicenseKey.Length)) + "..." + $LicenseKey.Substring([Math]::Max(0, $LicenseKey.Length - 4))
Write-Host "🔑 License: $keyPreview"
Write-Host ""

# Machine ID = first MAC address
$MachineId = (Get-NetAdapter | Where-Object Status -eq "Up" | Select-Object -First 1).MacAddress
if (-not $MachineId) { $MachineId = "unknown-machine" }

Write-Host "🌐 Validating license..."
try {
    $ValidateResp = Invoke-RestMethod -Uri "$API/v1/licenses/validate/$LicenseKey?machine_id=$MachineId" -Method Get -ErrorAction Stop
} catch {
    Write-Host "❌ Can't reach LindaAI servers: $_" -ForegroundColor Red
    exit 1
}

if (-not $ValidateResp.valid) {
    Write-Host "❌ License rejected: $($ValidateResp.reason)" -ForegroundColor Red
    Write-Host "   Contact support@lindaai.com"
    exit 1
}

# Download full license details
Write-Host "📜 Fetching license details..."
$LicenseInfo = Invoke-RestMethod -Uri "$API/v1/licenses/download/$LicenseKey" -Method Get
$Tier = $LicenseInfo.tier.ToLower()
if ($Tier -notin @("bronze","silver","gold","platinum","trial")) { $Tier = "bronze" }
Write-Host "✅ Tier: $Tier"
Write-Host ""

# Fetch tier manifest
$Manifest = Invoke-RestMethod -Uri "$CDN/tier-manifest.json" -Method Get
$Skills = [System.Collections.ArrayList]@()
foreach ($s in $Manifest.tiers.bronze.skills) { [void]$Skills.Add($s) }
if ($Tier -in @("silver","gold","platinum")) {
    foreach ($s in $Manifest.tiers.silver.additional_skills) { [void]$Skills.Add($s) }
}
if ($Tier -in @("gold","platinum")) {
    foreach ($s in $Manifest.tiers.gold.additional_skills) { [void]$Skills.Add($s) }
}
if ($Tier -eq "platinum") {
    foreach ($s in $Manifest.tiers.platinum.additional_skills) { [void]$Skills.Add($s) }
}
$Skills = $Skills | Select-Object -Unique

$Agents = @()
if ($Tier -eq "platinum") {
    $Agents = $Manifest.tiers.platinum.agents
}

Write-Host "📦 Installing $($Skills.Count) skills + $($Agents.Count) agents..."

New-Item -ItemType Directory -Force -Path $SkillsDir, $AgentsDir, $BrainDir | Out-Null

# Download skills
$installedSkills = 0
foreach ($skill in $Skills) {
    $url = "$CDN/skills/$skill.md"
    $dir = Join-Path $SkillsDir $skill
    New-Item -ItemType Directory -Force -Path $dir | Out-Null
    try {
        Invoke-WebRequest -Uri $url -OutFile (Join-Path $dir "SKILL.md") -UseBasicParsing -ErrorAction Stop
        $installedSkills++
    } catch {}
}

# Download agents
$installedAgents = 0
foreach ($agent in $Agents) {
    $url = "$CDN/agents/$agent.md"
    try {
        Invoke-WebRequest -Uri $url -OutFile (Join-Path $AgentsDir "$agent.md") -UseBasicParsing -ErrorAction Stop
        $installedAgents++
    } catch {}
}

# Voice Pack (Platinum only)
if ($Tier -eq "platinum") {
    Write-Host "🎤 Installing bundled Voice Pack..."
    foreach ($vs in @("voice","voicesetup")) {
        $dir = Join-Path $SkillsDir $vs
        New-Item -ItemType Directory -Force -Path $dir | Out-Null
        try {
            Invoke-WebRequest -Uri "$CDN/skills/$vs.md" -OutFile (Join-Path $dir "SKILL.md") -UseBasicParsing -ErrorAction SilentlyContinue
        } catch {}
    }
    try {
        Invoke-WebRequest -Uri "$CDN/scripts/speak-last-response.ps1" -OutFile (Join-Path $ClaudeDir "speak-last-response.ps1") -UseBasicParsing -ErrorAction SilentlyContinue
    } catch {}
}

# Brain folder scaffold
$brainReadme = Join-Path $BrainDir "README.md"
if (-not (Test-Path $brainReadme)) {
    @"
# Your LindaAI Brain

Drop reference files in this folder — LindaAI reads them as context.

Suggested files:
- goals.md — your current goals
- active-deals.md — deals in progress
- contacts.md — key people

© 2026 LindaAI — Built by Daniel Wise
"@ | Set-Content $brainReadme
}

# Save license locally
$LicensePath = Join-Path $ClaudeDir "lindaai\license.json"
New-Item -ItemType Directory -Force -Path (Split-Path $LicensePath) | Out-Null
@{
    key = $LicenseKey
    tier = $Tier
    machine_id = $MachineId
    installed_at = (Get-Date).ToString("yyyy-MM-ddTHH:mm:ssZ")
} | ConvertTo-Json | Set-Content $LicensePath

Write-Host ""
Write-Host "╔════════════════════════════════════════════════════════════╗"
Write-Host "║               ✅  LINDAAI INSTALLED                        ║"
Write-Host "╠════════════════════════════════════════════════════════════╣"
Write-Host "║  Tier:    $Tier"
Write-Host "║  Skills:  $installedSkills installed"
Write-Host "║  Agents:  $installedAgents installed"
Write-Host "║                                                            ║"
Write-Host "║  Next: Restart Claude Code and type any LindaAI command    ║"
Write-Host "║  Update anytime with: /linda-sync                          ║"
Write-Host "╚════════════════════════════════════════════════════════════╝"
Write-Host ""

# Speak confirmation
Add-Type -AssemblyName System.Speech
$synth = New-Object System.Speech.Synthesis.SpeechSynthesizer
$synth.SpeakAsync("LindaAI $Tier installed. Welcome partner. LindaAI has your back.") | Out-Null
