@echo off
setlocal EnableExtensions
title Medical Case OCR
cd /d "%~dp0"
set "PYTHON_EXE=%LocalAppData%\Microsoft\WindowsApps\python.exe"
if not exist "%PYTHON_EXE%" set "PYTHON_EXE=python"
"%PYTHON_EXE%" --version >nul 2>nul || (echo Python 3.10+ was not found.&pause&exit /b 1)
if not exist ".venv\Scripts\python.exe" "%PYTHON_EXE%" -m venv .venv
if not exist ".venv\Scripts\python.exe" (echo Cannot create virtual environment.&pause&exit /b 1)
set "APP_PY=.venv\Scripts\python.exe"
"%APP_PY%" -m pip install -r requirements.txt
if errorlevel 1 (echo Dependency installation failed.&pause&exit /b 1)
"%APP_PY%" -c "import streamlit,fitz,numpy,onnxruntime,cv2,pyclipper,shapely; from rapidocr_onnxruntime import RapidOCR" >nul 2>nul
if errorlevel 1 (echo OCR dependencies are incomplete.&pause&exit /b 1)
for /f "tokens=5" %%P in ('netstat -ano ^| findstr ":8501" ^| findstr "LISTENING"') do set "RUNNING_PID=%%P"
if defined RUNNING_PID goto open_browser
start "MedicalCaseOCR" /min "%APP_PY%" -m streamlit run ocr_app.py --server.headless true --server.address 127.0.0.1 --server.port 8501
for /l %%N in (1,1,20) do (ping 127.0.0.1 -n 2 >nul&netstat -ano|findstr ":8501"|findstr "LISTENING" >nul&&goto open_browser)
echo Startup timeout. Please rerun this script.
pause
exit /b 1
:open_browser
start "" http://127.0.0.1:8501
echo Ready: http://127.0.0.1:8501
exit /b 0
