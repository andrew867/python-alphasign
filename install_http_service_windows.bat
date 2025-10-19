@echo off
REM Alpha Sign HTTP Service Installation Script for Windows
REM This script installs the HTTP service on Windows

echo Installing Alpha Sign HTTP Service for Windows...

REM Check if running as administrator
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo Error: This script must be run as Administrator
    echo Right-click and select "Run as administrator"
    pause
    exit /b 1
)

REM Create installation directory
set INSTALL_DIR=C:\alphasign
if not exist "%INSTALL_DIR%" (
    echo Creating installation directory: %INSTALL_DIR%
    mkdir "%INSTALL_DIR%"
)

REM Copy service files
echo Installing service files...
copy alphasign_http_service.py "%INSTALL_DIR%\"
xcopy alphasign "%INSTALL_DIR%\alphasign\" /E /I /Y

REM Install Python dependencies
echo Installing Python dependencies...
pip install -r requirements.txt

REM Create log directory
set LOG_DIR=%INSTALL_DIR%\logs
if not exist "%LOG_DIR%" (
    echo Creating log directory: %LOG_DIR%
    mkdir "%LOG_DIR%"
)

REM Create a simple startup script
echo Creating startup script...
echo @echo off > "%INSTALL_DIR%\start_service.bat"
echo cd /d "%INSTALL_DIR%" >> "%INSTALL_DIR%\start_service.bat"
echo python alphasign_http_service.py --host 0.0.0.0 --port 8888 --sign-ip 192.168.133.54 --sign-port 10001 >> "%INSTALL_DIR%\start_service.bat"

REM Create a test script
echo Creating test script...
echo @echo off > "%INSTALL_DIR%\test_service.bat"
echo echo Testing Alpha Sign HTTP Service... >> "%INSTALL_DIR%\test_service.bat"
echo curl "http://localhost:8888/AlphaSign?msg=Test Message" >> "%INSTALL_DIR%\test_service.bat"
echo curl "http://localhost:8888/status" >> "%INSTALL_DIR%\test_service.bat"
echo pause >> "%INSTALL_DIR%\test_service.bat"

echo.
echo Installation complete!
echo.
echo To start the service manually:
echo   cd %INSTALL_DIR%
echo   python alphasign_http_service.py
echo.
echo To test the service:
echo   %INSTALL_DIR%\test_service.bat
echo.
echo To install as Windows service, use NSSM:
echo   nssm install AlphaSignHTTP "%INSTALL_DIR%\start_service.bat"
echo   nssm start AlphaSignHTTP
echo.
echo Service will log to: %INSTALL_DIR%\alphasign-http.log
echo.
pause
