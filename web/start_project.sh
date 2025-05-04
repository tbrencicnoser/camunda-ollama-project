#!/bin/bash

echo "➡️  Stoppe und entferne alle alten Container..."
sudo docker-compose down

echo "✅ Alte Container entfernt."

echo "➡️  Starte alle Container mit Docker Compose..."
sudo docker-compose up -d --build

echo "✅ Docker Compose gestartet."

echo "➡️  Warte kurz, bis die Container stabil laufen..."
sleep 10

echo "➡️  Überprüfe laufende Container:"
sudo docker ps

echo "➡️  Lade das Ollama-Modell (mistral), falls nicht vorhanden..."
sudo docker exec camunda-ollama-project_ollama_1 ollama pull mistral

echo "✅ Ollama-Modell geprüft."

echo "➡️  Starte Web-Container neu, damit er Ollama sicher findet..."
sudo docker-compose restart web

echo "✅ Web-Container neu gestartet."

echo "➡️  Projekt ist jetzt bereit! Öffne im Browser:"
echo "    http://<DEINE-IP>:5000"

echo "👍 Alles läuft! Viel Erfolg bei deiner Präsentation!"
