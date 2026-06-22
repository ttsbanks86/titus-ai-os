# Odysseus — Project Brief

## Purpose
Set up and maintain Odysseus, a self-hosted AI workspace.

## Official Repository
https://github.com/pewdiepie-archdaemon/odysseus

## Local URL
http://127.0.0.1:7000

## Install Folder
`C:\Users\tbank\Desktop\Live Cowork\PROJECTS\Odysseus\odysseus`

## Startup
Run:
```powershell
C:\Users\tbank\Desktop\Live Cowork\PROJECTS\Odysseus\Start-Odysseus.ps1
```

## Stop
Run:
```powershell
C:\Users\tbank\Desktop\Live Cowork\PROJECTS\Odysseus\Stop-Odysseus.ps1
```

## Login
Username: `admin`

Temporary password is not stored here. Retrieve from Docker logs when needed:
```powershell
cd "C:\Users\tbank\Desktop\Live Cowork\PROJECTS\Odysseus\odysseus"
docker compose logs odysseus --tail 80
```

Change the password immediately after first login.
