@echo off
rem Mesa de modelos 3D: abre http://localhost:8765 en el navegador.
cd /d "%~dp0.."
start "" http://localhost:8765
python devtools\workbench.py
pause
