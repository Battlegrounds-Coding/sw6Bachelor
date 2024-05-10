@echo off
setlocal

set "source=%~dp0"
set "out_dir=%source%experiment_data_results"
set "dir=%~f1"

for /F "delims=" %%i in ("%dir%") do set "experiment_name=%%~ni"
for /F "delims=" %%i in ("%dir%\..") do set "experiment_dataset=%%~ni"
set "name=%experiment_name%-%experiment_dataset%"

ECHO %name%
call "%source%\.venv\Scripts\activate"


if exist "%out_dir%\" (
    md "%out_dir%"
)

if exist "%dir%\" (
    echo Running tests for project %dir%
    python "%source%src\main.py" ^
        --rain="%dir%\Rain.csv" ^
        --mode=headless ^
        --data="%dir%\DepthSensor.csv" ^
        --data-control="%dir%\DepthControl.csv" ^
        --time=7000 ^
        --name="%name%" ^
        --output="%out_dir%\%name%.csv" ^
        --output-image="%out_dir%\%name%.png"
) else (
    echo "%dir%" is not a directory
)

endlocal
