import json
import os
import re
import sys
import time
import urllib.request
from datetime import datetime, timezone
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
    "UPDATED": datetime.now(timezone.utc).strftime("%d.%m.%Y %H:%M UTC"),
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


def fetch_optional(endpoint):
    request = urllib.request.Request(f"https://cocproxy.royaleapi.dev/v1/{endpoint}")
    request.add_header("Authorization", f"Bearer {API_TOKEN}")
    request.add_header("Accept", "application/json")
    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            return json.loads(response.read().decode("utf-8"))
    except (HTTPError, OSError, ValueError) as error:
        print(f"⚠️ Zusatzdaten für {endpoint} nicht verfügbar: {error}")
        return None


stats_path = Path(__file__).resolve().parent / "_data" / "clan_stats.json"
try:
    stats = json.loads(stats_path.read_text(encoding="utf-8"))
except (OSError, ValueError):
    stats = {}

now = datetime.now(timezone.utc)
month_key = now.strftime("%Y-%m")
month = stats.get("monthly", {})
monthly_current = month.get("current", {})
if monthly_current.get("month") != month_key:
    tracking_started = monthly_current.get("trackingStarted", "")
    if monthly_current.get("month") and tracking_started[8:10] == "01":
        warrior_tag, warrior = max(
            monthly_current.get("warStars", {}).items(),
            key=lambda item: item[1].get("stars", 0),
            default=[None, {}],
        )
        donor_tag, donor = max(
            monthly_current.get("donations", {}).items(),
            key=lambda item: item[1].get("donations", 0),
            default=[None, {}],
        )
        monthly_current["awards"] = {
            "warrior": {"tag": warrior_tag, **warrior} if warrior_tag else None,
            "donor": {"tag": donor_tag, **donor} if donor_tag else None,
        }
        month.setdefault("history", []).insert(0, monthly_current)
    monthly_current = {
        "month": month_key,
        "trackingStarted": now.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "warStars": {},
        "donations": {},
    }

members = data.get("memberList", [])
previous_donations = stats.get("memberDonationTotals", {})
current_donations = {}
for member in members:
    tag = member.get("tag")
    if not tag:
        continue
    donated = member.get("donations", 0)
    current_donations[tag] = donated
    delta = donated - previous_donations.get(tag, donated)
    if delta < 0:
        delta = donated
    if delta:
        entry = monthly_current["donations"].setdefault(tag, {"name": member.get("name", "Unbekannt"), "donations": 0})
        entry["name"] = member.get("name", entry["name"])
        entry["donations"] += delta

seen_war_attacks = stats.get("seenWarAttacks", {})


def record_war_attacks(war):
    if not isinstance(war, dict) or not isinstance(war.get("clan"), dict):
        return
    opponent = war.get("opponent") or {}
    clan = war["clan"]
    clan_tag = clan.get("tag", "").lstrip("#")
    opponent_tag = opponent.get("tag", "").lstrip("#")
    if clan_tag == CLAN_TAG:
        own_clan = clan
    elif opponent_tag == CLAN_TAG:
        own_clan = opponent
    else:
        return
    war_key = f"{war.get('startTime', '')}:{':'.join(sorted((clan_tag, opponent_tag)))}"
    seen = seen_war_attacks.setdefault(war_key, [])
    for player in own_clan.get("members", []):
        for attack in player.get("attacks", []):
            attack_id = f"{player.get('tag', '')}:{attack.get('order', '')}"
            if attack_id in seen:
                continue
            seen.append(attack_id)
            tag = player.get("tag", "")
            entry = monthly_current["warStars"].setdefault(tag, {"name": player.get("name", "Unbekannt"), "stars": 0, "attacks": 0})
            entry["name"] = player.get("name", entry["name"])
            entry["stars"] += attack.get("stars", 0)
            entry["attacks"] += 1


current_war = fetch_optional(f"clans/%23{CLAN_TAG}/currentwar")
record_war_attacks(current_war)
warlog = fetch_optional(f"clans/%23{CLAN_TAG}/warlog?limit=10")
league_group = fetch_optional(f"clans/%23{CLAN_TAG}/currentwar/leaguegroup")
cwl_wars = []
if isinstance(league_group, dict) and league_group.get("season"):
    for round_data in league_group.get("rounds", []):
        for war_tag in round_data.get("warTags", []):
            if not war_tag or war_tag == "#0":
                continue
            war = fetch_optional(f"clanwarleagues/wars/%23{war_tag.lstrip('#')}")
            if not isinstance(war, dict):
                continue
            war_clan = war.get("clan", {})
            war_opponent = war.get("opponent", {})
            if CLAN_TAG not in (war_clan.get("tag", "").lstrip("#"), war_opponent.get("tag", "").lstrip("#")):
                continue
            record_war_attacks(war)
            clan = war_clan
            opponent = war_opponent
            if clan.get("tag", "").lstrip("#") != CLAN_TAG:
                clan, opponent = opponent, clan
            clan_stars = clan.get("stars", 0)
            opponent_stars = opponent.get("stars", 0)
            clan_score = (clan_stars, clan.get("destructionPercentage", 0))
            opponent_score = (opponent_stars, opponent.get("destructionPercentage", 0))
            cwl_wars.append({
                "season": league_group.get("season", ""),
                "state": war.get("state", ""),
                "opponent": opponent.get("name", ""),
                "stars": clan_stars,
                "opponentStars": opponent_stars,
                "result": (clan_score > opponent_score) - (clan_score < opponent_score),
            })
            break

raid_seasons = fetch_optional(f"clans/%23{CLAN_TAG}/capitalraidseasons?limit=1")
town_halls = {}
for member in members:
    hall_level = member.get("townHallLevel")
    if hall_level is not None:
        town_halls[str(hall_level)] = town_halls.get(str(hall_level), 0) + 1

if isinstance(seen_war_attacks, dict) and len(seen_war_attacks) > 20:
    seen_war_attacks = dict(list(seen_war_attacks.items())[-20:])

previous_cwl = stats.get("cwl", {})
cwl_history = previous_cwl.get("history", [])
if isinstance(league_group, dict) and league_group.get("season"):
    season = league_group.get("season", "")
    previous_season = previous_cwl.get("season", "")
    if previous_season and season and previous_season != season and previous_cwl.get("wars"):
        cwl_history.insert(0, {"season": previous_season, "wars": previous_cwl["wars"]})
    cwl_season = season
else:
    cwl_season = previous_cwl.get("season", "")
    cwl_wars = previous_cwl.get("wars", [])

stats.update({
    "updatedAt": now.strftime("%d.%m.%Y %H:%M UTC"),
    "clan": {"level": level, "members": data["members"], "points": trophies, "warWins": war_wins, "capitalPoints": data.get("clanCapitalPoints", 0)},
    "members": sorted(members, key=lambda member: member.get("donations", 0), reverse=True),
    "townHalls": town_halls,
    "currentWar": current_war,
    "warlog": warlog.get("items", []) if isinstance(warlog, dict) else stats.get("warlog", []),
    "cwl": {"season": cwl_season, "wars": cwl_wars, "history": cwl_history},
    "capitalRaid": (raid_seasons.get("items") or [None])[0] if isinstance(raid_seasons, dict) else stats.get("capitalRaid"),
    "memberDonationTotals": current_donations,
    "seenWarAttacks": seen_war_attacks,
    "monthly": {"current": monthly_current, "history": month.get("history", [])},
})

stats_path.parent.mkdir(parents=True, exist_ok=True)
temporary_stats_path = stats_path.with_suffix(".json.tmp")
temporary_stats_path.write_text(json.dumps(stats, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
temporary_stats_path.replace(stats_path)
print(f"✅ Erweiterte Clan-Statistiken gespeichert: {stats_path}")
