- remove __pycache__ on powershell
Get-ChildItem -Recurse -Directory -Filter "__pycache__" | Remove-Item -Recurse -Confirm

- run pytest with log message (require loggins configured)
pytest -o log_cli=true --log-cli-level=INFO

- remove all __pycacha__ on linux
find . -type d -name "__pycache__" -exec rm -r {} +

