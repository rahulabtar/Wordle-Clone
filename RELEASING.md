# Publish a Windows release

1. Use Windows x64 with Python 3.14 and install `requirements-build.txt`.
2. Run `build-windows.ps1`. It runs the fast regression checks and creates
   `dist/Wordle-Clone.exe` plus a SHA256 checksum file.
3. Copy the executable to a separate folder, double-click it, and check that
   the board opens and accepts a guess. Close the app.
4. Commit and push the source changes.
5. Create a GitHub Release using the next version tag (the first is `v1.0.0`).
   Attach the executable and checksum file, add brief release notes, and publish.

Players download the executable and open it directly; no installer or Python is
required. The first release targets Windows x64 and is unsigned.
