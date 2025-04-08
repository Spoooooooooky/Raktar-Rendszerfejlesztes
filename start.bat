@echo off

cd backend || (
    echo Error: 'backend' folder not found.
    exit /b 1
)

:run_command
setlocal
set "cmd=%~1"
call %cmd%
if errorlevel 1 (
    echo Error: Command '%cmd%' failed.
) else (
    echo Success: Command completed.
)
endlocal
goto :eof

echo Initializing Aerich...
call :run_command "aerich init -t raktar_backend.TORTOISE_ORM"
call :run_command "aerich init-db"

echo Running migrations...
for /f "tokens=*" %%A in ('powershell -Command "Start-Process -FilePath aerich -ArgumentList 'migrate' -Wait -Timeout 30 -PassThru | Out-String"') do set "migration_output=%%A"

if "%migration_output%"=="" (
    echo Warning: Migration either took too long or doesn't exist. If there is something to migrate, please run 'aerich migrate' manually.
) else (
    echo %migration_output%
    call :run_command "aerich upgrade"
)

echo Starting backend...
call :run_command "python raktar_backend.py"

pause
