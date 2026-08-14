@echo off
setlocal
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" (
  where py >nul 2>nul
  if errorlevel 1 (
    python -m venv .venv
  ) else (
    py -m venv .venv
  )
)
call .venv\Scripts\activate.bat
python -m pip install -r requirements.txt
python -m streamlit run app.py
endlocal
