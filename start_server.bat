CALL deactivate
CALL .venv\Scripts\activate.bat
REM python -m uvicorn main:app

python -m compileall --invalidation-mode checked-hash

python -m main