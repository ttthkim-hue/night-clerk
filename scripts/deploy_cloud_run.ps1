$ErrorActionPreference = "Stop"
$Project = $env:GOOGLE_CLOUD_PROJECT
if (-not $Project) { throw "Set GOOGLE_CLOUD_PROJECT" }
if (-not $env:NIGHT_CLERK_BUCKET) { throw "Set NIGHT_CLERK_BUCKET" }
$Region = if ($env:NIGHT_CLERK_REGION) { $env:NIGHT_CLERK_REGION } else { "us-central1" }
$ModelLocation = if ($env:GOOGLE_CLOUD_LOCATION) { $env:GOOGLE_CLOUD_LOCATION } else { "global" }
$Root = Split-Path -Parent $PSScriptRoot

Set-Location $Root

gcloud run deploy night-clerk `
  --source . `
  --region $Region `
  --project $Project `
  --allow-unauthenticated `
  --set-env-vars "NIGHT_CLERK_MODE=gcp,NIGHT_CLERK_MODEL=gemini-3.5-flash,GOOGLE_CLOUD_PROJECT=$Project,GOOGLE_CLOUD_LOCATION=$ModelLocation,GOOGLE_GENAI_USE_VERTEXAI=true,NIGHT_CLERK_BUCKET=$env:NIGHT_CLERK_BUCKET,NIGHT_CLERK_PUBLIC_DEMO_ONLY=true" `
  --min-instances 0 `
  --max-instances 1 `
  --concurrency 4

Write-Host "Cloud Run deployed. Verify /health and run one /jobs request before recording the demo."
