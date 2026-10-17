@echo off
setlocal
cd /d "%~dp0"
where py >nul 2>&1
if not errorlevel 1 goto with_py
where python >nul 2>&1
if not errorlevel 1 goto with_python
echo [PASTORALE] Python 3.10+ introuvable. Installez Python et relancez.
goto fail
:with_py
py -3 "%~dp0demarrer_pastorale.py" %*
if errorlevel 1 goto fail
exit /b 0
:with_python
python "%~dp0demarrer_pastorale.py" %*
if errorlevel 1 goto fail
exit /b 0
:fail
echo.
echo [PASTORALE] Demarrage en echec. Le message d'erreur est ci-dessus.
pause
exit /b 1
