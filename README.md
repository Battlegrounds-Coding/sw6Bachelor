# sw6Bachelor


Run all test with:
pytest

To get packages:
flit install

To get packages in venv: (venv will build with all deppendencies found in pyproject.toml ad default)
py -m pip install .[package_name fx test]

Libraries used:
-  testing = pytest


When creating tests.
- all file names should have the test prefix.
- All function defines need to have the test_ prefix to be registered by pytest
- A test file should reflect a single source file
- The file structure should reflect the source file structure.

When adding files.
- All files should be placed in the src/python_package folder.