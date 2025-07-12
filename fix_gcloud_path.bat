@echo off
echo 🔧 Fixing Google Cloud SDK PATH...
echo ================================================

REM Define the Google Cloud SDK path
set GCLOUD_PATH=%USERPROFILE%\AppData\Local\Google\Cloud SDK\google-cloud-sdk\bin

REM Check if the path exists
if exist "%GCLOUD_PATH%" (
    echo ✅ Found Google Cloud SDK at: %GCLOUD_PATH%
    
    REM Add to current session PATH
    set PATH=%PATH%;%GCLOUD_PATH%
    echo ✅ Added to current session PATH
    
    REM Add to user PATH permanently using PowerShell
    powershell -Command "& {$userPath = [System.Environment]::GetEnvironmentVariable('PATH', 'User'); if ($userPath -notlike '*%GCLOUD_PATH%*') { $newPath = $userPath + ';%GCLOUD_PATH%'; [System.Environment]::SetEnvironmentVariable('PATH', $newPath, 'User'); Write-Host '✅ Added to permanent user PATH' -ForegroundColor Green } else { Write-Host '✅ Already in permanent PATH' -ForegroundColor Yellow }}"
    
    REM Test gcloud command
    echo.
    echo 🧪 Testing gcloud command...
    gcloud --version
    if %ERRORLEVEL% EQU 0 (
        echo ✅ gcloud is working!
    ) else (
        echo ❌ gcloud test failed
    )
    
) else (
    echo ❌ Google Cloud SDK not found at expected path: %GCLOUD_PATH%
    echo    Please reinstall Google Cloud SDK from: https://cloud.google.com/sdk/docs/install
)

echo.
echo 🔄 Please restart your command prompt or PowerShell
echo    for the PATH changes to take effect in new sessions
echo.
pause 