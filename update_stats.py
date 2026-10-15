import json
import os
import re
import sys
import time
import urllib.request
from urllib.error import HTTPError
from pathlib import Path

CLAN_TAG = "2LR89PLLL"
API_TOKEN = os.environ.get("COC_TOKEN")

if not API_TOKEN:
    print("❌ Fehler: Kein COC_TOKEN in den Umgebungsvariablen gefunden!", file=sys.stderr)
    sys.exit(1)

# Clash of Clans API Anforderung über den RoyaleAPI Proxy (umgeht dynamische GitHub-IPs)
url = f"https://cocproxy.royaleapi.dev/v1/clans/%23{CLAN_TAG}"
req = urllib.request.Request(url)
req.add_header("Authorization", f"Bearer {API_TOKEN}")
req.add_header("Accept", "application/json")

retryable_statuses = {429, 500, 502, 503, 504}
max_attempts = 4
for attempt in range(1, max_attempts + 1):
    try:
        with urllib.request.urlopen(req, timeout=20) as response:
            data = json.loads(response.read().decode("utf-8"))
        break
    except HTTPError as error:
        if error.code not in retryable_statuses or attempt == max_attempts:
            print(f"❌ API-Fehler: {error}", file=sys.stderr)
            sys.exit(1)

        retry_after = error.headers.get("Retry-After") if error.headers else None
        try:
            delay = float(retry_after) if retry_after else 2**attempt
        except ValueError:
            delay = 2**attempt
        delay = min(max(delay, 1), 30)
        print(f"⚠️ API vorübergehend nicht verfügbar (HTTP {error.code}); erneuter Versuch in {delay:g}s.")
    except (OSError, ValueError) as error:
        if attempt == max_attempts:
            print(f"❌ API-Fehler nach {max_attempts} Versuchen: {error}", file=sys.stderr)
            sys.exit(1)

        delay = 2**attempt
        print(f"⚠️ API-Aufruf vorübergehend fehlgeschlagen; erneuter Versuch in {delay}s.")

    time.sleep(delay)

if not isinstance(data, dict):
    print("❌ API-Antwort hat ein unerwartetes Format.", file=sys.stderr)
    sys.exit(1)

# Erwartete API-Felder prüfen, damit unvollständige Antworten keine Ersatzwerte veröffentlichen.
required_fields = ("clanLevel", "members", "clanPoints", "warWins")
missing_fields = [field for field in required_fields if field not in data]
if missing_fields:
    print(f"❌ API-Antwort unvollständig; fehlende Felder: {', '.join(missing_fields)}", file=sys.stderr)
    sys.exit(1)

for field in required_fields:
    if type(data[field]) is not int or data[field] < 0:
        print(f"❌ Ungültiger API-Wert für {field}.", file=sys.stderr)
        sys.exit(1)

level = data["clanLevel"]
members = f"{data['members']}/50"
trophies = data["clanPoints"]
war_wins = data["warWins"]

print(f"✅ Live-Daten empfangen: Level {level} | Mitglieder {members} | Trophäen {trophies:,} | Siege {war_wins}")

index_path = Path(__file__).resolve().parent / "index.md"
try:
    content = index_path.read_text(encoding="utf-8")
except OSError as error:
    print(f"❌ index.md konnte nicht gelesen werden: {error}", file=sys.stderr)
    sys.exit(1)

replacements = {
    "LEVEL": f"Level {level}",
    "MEMBERS": members,
    "TROPHIES": f"{trophies:,} 🏆",
    "WINS": f"{war_wins} Siege",
}
for name, value in replacements.items():
    pattern = re.compile(rf"<!--STAT_{name}-->.*?<!--/STAT_{name}-->", re.DOTALL)
    content, count = pattern.subn(
        lambda _match: f"<!--STAT_{name}-->{value}<!--/STAT_{name}-->",
        content,
    )
    if count != 1:
        print(f"❌ Platzhalter für {name} {count}-mal gefunden; erwartet wird genau einmal.", file=sys.stderr)
        sys.exit(1)

temporary_path = index_path.with_suffix(".md.tmp")
try:
    temporary_path.write_text(content, encoding="utf-8")
    temporary_path.replace(index_path)
except OSError as error:
    print(f"❌ index.md konnte nicht aktualisiert werden: {error}", file=sys.stderr)
    sys.exit(1)

print("🚀 index.md erfolgreich aktualisiert!")
