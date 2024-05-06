@echo off
setlocal EnableDelayedExpansion

SET _INTERPOLATION_0=
FOR /f "delims=" %%a in ('dirname $0') DO (SET "_INTERPOLATION_0=!_INTERPOLATION_0! %%a")
SET "source=!_INTERPOLATION_0:~1!"
SET _INTERPOLATION_1=
FOR /f "delims=" %%a in ('dirname $0') DO (SET "_INTERPOLATION_1=!_INTERPOLATION_1! %%a")
SET "!_INTERPOLATION_1:~1!dir=%~1"
source "!source!\.venv\bin\activate"
IF "-d" "!dir!" (
  echo "Running tests for project !dir!"
  python "!source!\src\main.py" "--rain=!dir!\data\fixed\RainData.csv" "--mode=headless" "--data=!dir!\data\fixed\DepthDataFixed.csv" "--data-control=!dir!\data\optimal\DepthDataOptimal.csv" "--time=7000"
) ELSE (
  echo "'!dir!' is not a directory"
)
