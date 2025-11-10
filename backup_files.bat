@echo off
echo Creando backups...

copy services\api.js services\api.js.backup
if errorlevel 1 (
    echo Error al hacer backup de api.js
) else (
    echo Backup de api.js creado correctamente
)

copy App.jsx App.jsx.backup
if errorlevel 1 (
    echo Error al hacer backup de App.jsx
) else (
    echo Backup de App.jsx creado correctamente
)

copy components\Layout.jsx components\Layout.jsx.backup
if errorlevel 1 (
    echo Error al hacer backup de Layout.jsx
) else (
    echo Backup de Layout.jsx creado correctamente
)

echo Proceso de backup completado
pause
