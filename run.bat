@echo off
REM === Chemin vers ton projet ===
cd /d "C:\Users\eric2\Documents\GitHub\In512_Project_Student"

REM === Lancement dans Windows Terminal en onglets ===
wt -w 0 nt --title "Serveur" python scripts/server.py -nb 2 ^
; nt --title "Agent 1" python scripts/agent.py ^
; nt --title "Agent 2" python scripts/agent.py

