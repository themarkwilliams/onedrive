@echo off
rem Renames OneDrive photos (FINAL mode). Task Till Dawn: "OneDrive Photo Namer", every 30 minutes.
rem Runs under mark-modules' job runner: JSON log in C:\Code\.logs\onedrive-photo-namer.rename.log (homelab#254).
cd /d "%~dp0.."
call "%~dp0..\..\mark-modules\bin\runjob.cmd" --timeout 25m onedrive-photo-namer rename -- uv run main.py FINAL
set rc=%errorlevel%
rem TTD runs "cmd /K <script>": close the window there, return to the prompt when run by hand
echo %cmdcmdline% | find /i "%~nx0" >nul && exit %rc%
exit /b %rc%
