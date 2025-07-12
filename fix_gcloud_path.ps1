# Fix Google Cloud SDK PATH issue on Windows
Write-Host "🔧 Fixing Google Cloud SDK PATH..." -ForegroundColor Green

# Define the Google Cloud SDK path
$gcloudPath = "$env:USERPROFILE\AppData\Local\Google\Cloud SDK\google-cloud-sdk\bin"

# Check if the path exists
if (Test-Path $gcloudPath) {
    Write-Host "✅ Found Google Cloud SDK at: $gcloudPath" -ForegroundColor Green
    
    # Add to current session PATH
    $env:PATH = $env:PATH + ";" + $gcloudPath
    Write-Host "✅ Added to current session PATH" -ForegroundColor Green
    
    # Add to user PATH permanently
    $userPath = [System.Environment]::GetEnvironmentVariable("PATH", "User")
    if ($userPath -notlike "*$gcloudPath*") {
        $newPath = $userPath + ";" + $gcloudPath
        [System.Environment]::SetEnvironmentVariable("PATH", $newPath, "User")
        Write-Host "✅ Added to permanent user PATH" -ForegroundColor Green
    } else {
        Write-Host "✅ Already in permanent PATH" -ForegroundColor Yellow
    }
    
    # Test gcloud command
    Write-Host "`n🧪 Testing gcloud command..." -ForegroundColor Blue
    try {
        $gcloudVersion = & gcloud --version 2>&1
        Write-Host "✅ gcloud is working!" -ForegroundColor Green
        Write-Host $gcloudVersion -ForegroundColor Gray
    } catch {
        Write-Host "❌ gcloud test failed: $_" -ForegroundColor Red
    }
    
} else {
    Write-Host "❌ Google Cloud SDK not found at expected path: $gcloudPath" -ForegroundColor Red
    Write-Host "   Please reinstall Google Cloud SDK from: https://cloud.google.com/sdk/docs/install" -ForegroundColor Yellow
}

Write-Host "`n🔄 Please restart PowerShell or run:" -ForegroundColor Blue
Write-Host "   refreshenv" -ForegroundColor Gray
Write-Host "   or close and reopen your terminal" -ForegroundColor Gray 