import os
import re
import urllib.request
import json

CLAN_TAG = "2LR89PLLL"
API_TOKEN = os.environ.get("COC_TOKEN")

if not API_TOKEN:
    print("❌ Fehler: Kein COC_TOKEN in GitHub Secrets gefunden!")
    exit(1)

# Clash of Clans API Anforderung über den RoyaleAPI Proxy (umgeht dynamische GitHub-IPs)
url = f"https://cocproxy.royaleapi.dev/v1/clans/%23{CLAN_TAG}"
req = urllib.request.Request(url)
req.add_header("Authorization", f"Bearer {API_TOKEN}")
req.add_header("Accept", "application/json")

try:
    with urllib.request.urlopen(req) as response:
        data = json.loads(response.read().decode('utf-8'))
except Exception as e:
    print(f"❌ API-Fehler: {e}")
    exit(1)

# Erwartete API-Felder prüfen, damit unvollständige Antworten keine Ersatzwerte veröffentlichen.
required_fields = {"clanLevel", "members", "clanPoints", "warWins"}
missing_fields = required_fields.difference(data)
if missing_fields:
    print(f"❌ API-Antwort unvollständig; fehlende Felder: {', '.join(sorted(missing_fields))}")
    exit(1)

level = data["clanLevel"]
members = f"{data['members']}/50"
trophies = data["clanPoints"]
war_wins = data["warWins"]

print(f"✅ Live-Daten empfangen: Level {level} | Mitglieder {members} | Trophäen {trophies} | Siege {war_wins}")

# index.md einlesen
with open("index.md", "r", encoding="utf-8") as f:
    content = f.read()

# Platzhalter in index.md ersetzen
content = re.sub(r'<!--STAT_LEVEL-->.*?<!--/STAT_LEVEL-->', f'<!--STAT_LEVEL-->Level {level}<!--/STAT_LEVEL-->', content)
content = re.sub(r'<!--STAT_MEMBERS-->.*?<!--/STAT_MEMBERS-->', f'<!--STAT_MEMBERS-->{members}<!--/STAT_MEMBERS-->', content)
content = re.sub(r'<!--STAT_TROPHIES-->.*?<!--/STAT_TROPHIES-->', f'<!--STAT_TROPHIES-->{trophies:,} 🏆<!--/STAT_TROPHIES-->', content)
content = re.sub(r'<!--STAT_WINS-->.*?<!--/STAT_WINS-->', f'<!--STAT_WINS-->{war_wins} Siege<!--/STAT_WINS-->', content)

# index.md speichern
with open("index.md", "w", encoding="utf-8") as f:
    f.write(content)

print("🚀 index.md erfolgreich aktualisiert!")
