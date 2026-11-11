$ErrorActionPreference = 'Stop'
Set-Location -LiteralPath $PSScriptRoot
& .venv/Scripts/python.exe -m PyInstaller --noconfirm --clean --onefile --windowed --name Oracles --add-data 'original/prophet.exe;original' --add-data 'original/samples;original/samples' --add-data 'original/templar.json;original' --add-data 'original/atheon.json;original' --add-data 'original/VaultOfGlass_Templar.png;original' --add-data 'original/VaultOfGlass_Atheon.png;original' app/main.py
if ($LASTEXITCODE -ne 0) { throw 'Build failed' }
