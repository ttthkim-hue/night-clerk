$ErrorActionPreference = "Stop"
$Project = $env:GOOGLE_CLOUD_PROJECT
if (-not $Project) { throw "Set GOOGLE_CLOUD_PROJECT" }
$Region = if ($env:NIGHT_CLERK_REGION) { $env:NIGHT_CLERK_REGION } else { "us-central1" }
$Root = Split-Path -Parent $PSScriptRoot

Set-Location $Root
gcloud run deploy night-clerk `
  --source . `
  --region $Region `
  --project $Project `
  --allow-unauthenticated `
  --set-env-vars "NIGHT_CLERK_MODE=gcp,NIGHT_CLERK_MODEL=gemini-3.5-flash,GOOGLE_CLOUD_PROJECT=$Project,NIGHT_CLERK_BUCKET=$env:NIGHT_CLERK_BUCKET" `
  --min-instances 0
