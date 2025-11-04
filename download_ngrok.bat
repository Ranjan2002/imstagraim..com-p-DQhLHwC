@echo off
echo ====================================================================
echo  INSTAGRAM PHISHING DEMO - NGROK SETUP
echo ====================================================================
echo.
echo This will download and setup ngrok for Instagram-like URL
echo.
pause

echo Downloading ngrok...
powershell -Command "Invoke-WebRequest -Uri 'https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-windows-amd64.zip' -OutFile 'ngrok.zip'"

echo Extracting ngrok...
powershell -Command "Expand-Archive -Path 'ngrok.zip' -DestinationPath '.' -Force"

echo Cleaning up...
del ngrok.zip

echo.
echo ====================================================================
echo  NGROK DOWNLOADED!
echo ====================================================================
echo.
echo Next steps:
echo 1. Sign up FREE at: https://dashboard.ngrok.com/signup
echo 2. Get your authtoken from: https://dashboard.ngrok.com/get-started/your-authtoken
echo 3. Run: ngrok config add-authtoken YOUR_TOKEN
echo 4. Run: ngrok http 5000
echo.
echo You'll get a URL like: https://abc-123.ngrok-free.app
echo.
pause
