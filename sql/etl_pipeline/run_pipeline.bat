
@echo off
cd /d "%~dp0"

echo Starting ETL pipeline...
python etl_pipeline.py

if errorlevel 1 (
    echo ETL pipeline failed.
) else (
    echo ETL pipeline completed successfully.
)

pause

