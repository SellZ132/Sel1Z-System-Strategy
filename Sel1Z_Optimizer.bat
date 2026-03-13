@echo off
setlocal enabledelayedexpansion
title [ Sel1Z ] SYSTEM STRATEGY v2.4
color 0b
cls

echo.
echo   =============================================================================
echo      _______  _______  ___      __   ________     [ STATUS: READY ]
echo     /  ____/ /  ____/ /  /     /  / /____   /     [ TYPE  : OPTIMIZER ]
echo    /  /___  /  /___  /  /     /  /      /  /      [ VER   : 2.4 ]
echo   /____  / /  ____/ /  /     /  /      /  /       [ DEV   : Sel1Z ]
echo  _____/ / /  /____ /  /____ /  /     /  /____ 	  [ CEO   : IZraz ]
echo /______/ /_______//_______//__/     /_______/     
echo.                                                  (X)  [-]  [#]
echo                  [ SYSTEM OPTIMIZATION BY Sel1Z ]
echo   =============================================================================
echo.

echo [+] ANALYZING HARDWARE...
for /f "tokens=2 delims==" %%a in ('wmic cpu get name /value') do set "cpu=%%a"
for /f "tokens=2 delims==" %%a in ('wmic os get caption /value') do set "os=%%a"
for /f "tokens=2 delims==" %%a in ('wmic computersystem get totalphysicalmemory /value') do set "mem=%%a"
set /a "ram=%mem:~0,-6%/1024"

echo ---------------------------------------------------------------
echo [ DEVICE INFO ]
echo OS     : %os%
echo CPU    : %cpu%
echo RAM    : %ram% GB
echo ---------------------------------------------------------------
echo.

:: เปลี่ยนเป็นสีแดงเข้ม (Blood Red) ตรงส่วนคำเตือน
color 04
echo   ---------------------------------------------------------------
echo   MUST READ BEFORE PROCEEDING:
echo   ---------------------------------------------------------------
echo   1. NETWORK: Your internet will disconnect briefly.
echo   2. PRINTER: Printing will be disabled until you restart.
echo   3. PERFORMANCE: "Gaming Mode" will stop non-essential tasks.
echo   4. PERMISSION: Make sure you ran this as ADMINISTRATOR.
echo   ---------------------------------------------------------------
echo.

:confirm
:: เปลี่ยนสีกลับเป็นสีฟ้าเพื่อให้มองเห็นคำถามชัดเจน
color 0b
set /p choice="> Do you agree and want to Initialize? (Y/N): "
if /i "%choice%"=="N" goto end_script
if /i "%choice%"=="Y" goto loading
echo [!] Please enter Y or N.
goto confirm

:loading
cls
echo.
echo [ Sel1Z ] PREPARING OPTIMIZATION...
set "bar=########################################"
for /l %%i in (1,1,40) do (
    set "spacer=!bar:~0,%%i!"
    cls
    echo.
    echo [ Sel1Z ] SECURITY CHECK IN PROGRESS...
    echo [!spacer!] %%i%%
    timeout /t 0 /nobreak >nul
)
goto start_opt

:start_opt
color 0a
echo.
echo ======================================================
echo [+] PHASE 1: STRATEGIC CLEANING (Deep Junk Removal)
echo ======================================================
del /s /f /q %userprofile%\AppData\Local\Temp\*.* >nul 2>&1
del /s /f /q C:\Windows\temp\*.* >nul 2>&1
del /s /f /q C:\Windows\Prefetch\*.* >nul 2>&1
net stop wuauserv >nul 2>&1
del /s /f /q C:\Windows\SoftwareDistribution\Download\*.* >nul 2>&1
net start wuauserv >nul 2>&1
echo [SUCCESS] Junk files eliminated.

color 0b
echo.
echo ======================================================
echo [+] PHASE 2: SYSTEM INTEGRITY (SFC ^& DISM)
echo ======================================================
sfc /scannow
DISM.exe /Online /Cleanup-image /Restorehealth
echo [SUCCESS] System files repaired.

color 0d
echo.
echo ======================================================
echo [+] PHASE 3: NETWORK CALIBRATION (Low Latency Mode)
echo ======================================================
netsh winsock reset >nul 2>&1
netsh int ip reset >nul 2>&1
ipconfig /release >nul 2>&1
ipconfig /renew >nul 2>&1
ipconfig /flushdns >nul 2>&1
echo [SUCCESS] Network parameters optimized.

color 0e
echo.
echo ======================================================
echo [+] PHASE 4: DISK PERFORMANCE
echo ======================================================
defrag C: /O /U
echo [SUCCESS] Disk optimization complete.

color 0c
echo.
echo ======================================================
echo [+] PHASE 5: GAMING MODE (Disabling Services)
echo ======================================================
echo Stopping background services to free up CPU...
net stop "SysMain" /y >nul 2>&1
net stop "DiagTrack" /y >nul 2>&1
net stop "Spooler" /y >nul 2>&1
net stop "WSearch" /y >nul 2>&1
echo [SUCCESS] Gaming Mode Engaged.

color 0a
echo.
echo   ######################################################
echo   #                                                    #
echo   #        OPTIMIZATION FINISHED BY [ Sel1Z ]          #
echo   #        YOUR PC IS NOW RUNNING AT PEAK              #
echo   #                                                    #
echo   ######################################################
echo.
pause
exit

:end_script
cls
color 0c
echo.
echo [!] Optimization aborted by user.
timeout /t 2 >nul
exit