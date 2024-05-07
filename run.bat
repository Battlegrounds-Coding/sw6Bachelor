@echo off
setlocal

set "source=%~dp0"
set "dir=%~1"

call "%source%\.venv\Scripts\activate"

if exist "%dir%\" (
    echo Running tests for project %dir%
    python "%source%\src\main.py" --rain="%dir%\data\fixed\RainData.csv" --mode=headless --data="%dir%\data\fixed\DepthDataFixed.csv" --data-control="%dir%\data\optimal\DepthDataOptimal.csv" --time=7000
) else (
    echo "%dir%" is not a directory
)

endlocal