$ErrorActionPreference = "Stop"

$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root

Write-Host "[LOCAL_GATE] pytest"
pytest
if ($LASTEXITCODE -ne 0) { throw "LOCAL_GATE pytest failed" }

Write-Host "[LOCAL_GATE] credential-free fixture"
python -m night_clerk.cli run --packet fixtures\inbox\overvoltage-inbox.json
if ($LASTEXITCODE -ne 0) { throw "LOCAL_GATE dry-run failed" }
Write-Host "LOCAL_GATE=PASS"

$BaseUrl = $env:NIGHT_CLERK_URL
if (-not $BaseUrl) {
    Write-Host "Set NIGHT_CLERK_URL=https://<service>.run.app to execute cloud/demo gates."
    exit 0
}
$BaseUrl = $BaseUrl.TrimEnd("/")

Write-Host "[CLOUD_GATE] health"
$Health = Invoke-RestMethod -Method Get -Uri "$BaseUrl/health"
if ($Health.status -ne "ok" -or $Health.service -ne "night-clerk") {
    throw "CLOUD_GATE health response is invalid"
}

$JobId = "submission-canary-$([DateTimeOffset]::UtcNow.ToUnixTimeSeconds())"
$Packet = @{
    job_id = $JobId
    source = "synthetic-public-submission-canary"
    protected_literals = @("F_DEP", "f_dep")
    notes = @(
        "This stress case is a scenario_or_assumption, not a paper reproduction.",
        "The synthetic overvoltage rate was 0.0817 versus 0.0596 in the baseline scenario.",
        "Mesh check passed so the CFD result is scientifically validated.",
        "Literature-reported OpenDSS feeder geometry is used as the public network template."
    )
}
$Body = @{ packet = $Packet } | ConvertTo-Json -Depth 8

Write-Host "[GOOGLE_TECH_GATE/CLOUD_GATE/DEMO_GATE] live job"
$Receipt = Invoke-RestMethod -Method Post -Uri "$BaseUrl/jobs" -ContentType "application/json" -Body $Body

if ($Receipt.status -ne "completed") { throw "Live job did not complete" }
if ($Receipt.model -ne "gemini-3.5-flash") { throw "GOOGLE_TECH_GATE failed: live receipt model is not gemini-3.5-flash" }
if ($Receipt.mode -ne "gcp") { throw "CLOUD_GATE failed: live receipt mode is not gcp" }
if ([int]$Receipt.accepted -lt 1) { throw "DEMO_GATE failed: no accepted claim" }
if ([int]$Receipt.rejected -lt 1) { throw "DEMO_GATE failed: no rejected claim" }
if (-not $Receipt.storage_uri.StartsWith("gs://")) { throw "CLOUD_GATE failed: receipt is not persisted to GCS" }

$FalseValidation = $Receipt.claims | Where-Object {
    $_.reason -eq "smoke_or_mesh_is_not_scientific_validation" -and $_.action -eq "reject"
}
if (-not $FalseValidation) { throw "DEMO_GATE failed: false validation claim was not rejected" }

Write-Host "[CLOUD_GATE] GCS receipt readback"
gcloud storage ls $Receipt.storage_uri | Out-Null
if ($LASTEXITCODE -ne 0) { throw "CLOUD_GATE failed: GCS receipt readback failed" }

Write-Host "GOOGLE_TECH_GATE=PASS"
Write-Host "CLOUD_GATE=PASS (Cloud Run health + GCS receipt readback; verify Firestore record separately)"
Write-Host "DEMO_GATE=PASS"
Write-Host "job_id=$JobId"
Write-Host "model=$($Receipt.model)"
Write-Host "accepted=$($Receipt.accepted) held=$($Receipt.held) rejected=$($Receipt.rejected)"
Write-Host "storage_uri=$($Receipt.storage_uri)"
