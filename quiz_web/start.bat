@echo off
rem Inicia o Quiz Web em um clique (Windows).
rem 1) Descobre um Python 3 instalado (py -3 ou python)
rem 2) Instala o Flask (modo usuario, sem admin e sem venv)
rem 3) Sobe o servidor em http://localhost:5000

setlocal
cd /d "%~dp0\.."

where py >nul 2>&1
if %ERRORLEVEL%==0 (
  set "PY=py -3"
  goto :found
)

where python >nul 2>&1
if %ERRORLEVEL%==0 (
  set "PY=python"
  goto :found
)

echo Nao encontrei Python 3 no PATH.
echo Instale em https://www.python.org/downloads/windows/ marcando
echo "Add python.exe to PATH" e rode esse arquivo de novo.
pause
exit /b 1

:found
echo ^>^> Instalando Flask (so se ainda nao tiver)...
%PY% -m pip install --user --quiet --disable-pip-version-check flask
if errorlevel 1 goto :erro

echo ^>^> Abrindo http://localhost:5000  (Ctrl+C para parar)
%PY% -m quiz_web.app
goto :fim

:erro
echo.
echo Falha ao instalar o Flask. Veja a mensagem acima.
pause
exit /b 1

:fim
pause
