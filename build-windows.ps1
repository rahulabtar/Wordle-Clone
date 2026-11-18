# Run with the Python environment containing requirements-build.txt activated.
$ErrorActionPreference = 'Stop'
Push-Location $PSScriptRoot
try {
    python -c "import struct, sys; sys.exit(0 if sys.platform == 'win32' and struct.calcsize('P') == 8 else 'Build requires 64-bit Windows Python.')"
    if ($LASTEXITCODE -ne 0) { throw 'Use 64-bit Windows Python to build the download.' }

    python -m unittest discover -s Test -p 'test_*.py' -v
    if ($LASTEXITCODE -ne 0) { throw 'Tests failed; build stopped.' }

    python -m PyInstaller --noconfirm --clean --onefile --windowed --name Wordle-Clone --add-data '1-1000.txt:.' mainGUI.py
    if ($LASTEXITCODE -ne 0) { throw 'PyInstaller build failed.' }

    $checksum = (Get-FileHash -LiteralPath 'dist/Wordle-Clone.exe' -Algorithm SHA256).Hash.ToLowerInvariant()
    "$checksum  Wordle-Clone.exe" | Set-Content -LiteralPath 'dist/Wordle-Clone.exe.sha256' -Encoding ascii
    Write-Host "SHA256: $checksum"
    Write-Host 'Built dist/Wordle-Clone.exe. Complete the release checklist before publishing.'
} finally {
    Pop-Location
}
