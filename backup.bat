@echo off
set timestamp=%date:~-4,4%%date:~-10,2%%date:~-7,2%_%time:~0,2%%time:~3,2%%time:~6,2%
set timestamp=%timestamp: =0%

echo Creando backup...
xcopy backend backend_backup_%timestamp% /E /H /C /I
echo Backup completado en: backend_backup_%timestamp%
pause
