#!/bin/bash

echo "➡️  Stoppe alle laufenden Container..."
sudo docker-compose stop

echo "✅ Container gestoppt."

echo "➡️  Entferne alle Container, Netzwerke und Volumes (falls nicht mehr gebraucht)..."
sudo docker-compose down -v

echo "✅ Alles entfernt."

echo "➡️  Optional: Zeige noch laufende Docker-Container (sollte leer sein, falls nur dieses Projekt lief)..."
sudo docker ps

echo "👍 Alles sauber gestoppt und entfernt!"

