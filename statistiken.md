---
title: "Clan-Statistiken | Letzte Hoffnung"
description: "Live-Daten, Clanstruktur, Kriegsverlauf und Mitglieder-Auszeichnungen von Letzte Hoffnung."
permalink: /statistiken/
---

{% assign stats = site.data.clan_stats %}
<main class="clan-page stats-page">
  <nav class="page-nav" aria-label="Hauptnavigation">
    <a class="page-nav__link" href="{{ '/' | relative_url }}">Startseite</a>
    <a class="page-nav__link page-nav__link--active" href="{{ '/statistiken/' | relative_url }}" aria-current="page">Statistiken</a>
  </nav>

  <header class="stats-intro">
    <div>
      <p class="eyebrow">Letzte Hoffnung · #2LR89PLLL</p>
      <h1>Zahlen, die uns verbinden</h1>
      <p>Ein laufender Blick auf unsere Mitglieder, gemeinsame Kriege und die Fortschritte in der Clanstadt.</p>
    </div>
    <a class="button button--secondary" href="https://www.clashofstats.com/clans/2LR89PLLL/summary" target="_blank" rel="noopener noreferrer">Clan-Profil <span aria-hidden="true">↗</span></a>
  </header>

  <section class="stats-section" aria-labelledby="overview-title">
    <p class="eyebrow">Der aktuelle Stand</p>
    <h2 id="overview-title">Clan auf einen Blick</h2>
    <dl class="stats-grid">
      <div class="stat stat--gold"><dt>Clan-Level</dt><dd>{{ stats.clan.level | default: "–" }}</dd></div>
      <div class="stat stat--red"><dt>Mitglieder</dt><dd>{{ stats.clan.members | default: "–" }}/50</dd></div>
      <div class="stat stat--blue"><dt>Clanpunkte</dt><dd>{{ stats.clan.points | default: "–" }}</dd></div>
      <div class="stat stat--green"><dt>CK-Siege</dt><dd>{{ stats.clan.warWins | default: "–" }}</dd></div>
    </dl>
    <p class="stats-updated--page">{% if stats.updatedAt and stats.updatedAt != "" %}Datenstand: {{ stats.updatedAt }}{% else %}Die erste Aktualisierung der erweiterten Statistiken steht noch aus.{% endif %}</p>
  </section>

  <section class="stats-section" aria-labelledby="honorees-title">
    <p class="eyebrow">Monatliche Auszeichnungen</p>
    <h2 id="honorees-title">Member des Monats{% if stats.monthly.history.first %}: {{ stats.monthly.history.first.month }}{% endif %}</h2>
    {% if stats.monthly.history.first %}
      {% assign latest_month = stats.monthly.history.first %}
      <div class="honoree-grid">
        <article class="honoree">
          <span>⚔️ Bester Krieger</span>
          {% if latest_month.awards.warrior.name %}<strong>{{ latest_month.awards.warrior.name }}</strong><small>{{ latest_month.awards.warrior.stars }} Sterne in {{ latest_month.awards.warrior.attacks }} Angriffen</small>{% else %}<strong>Keine Wertung</strong><small>Im Zeitraum wurden keine Angriffe erfasst.</small>{% endif %}
        </article>
        <article class="honoree honoree--green">
          <span>🎁 Größter Spender</span>
          {% if latest_month.awards.donor.name %}<strong>{{ latest_month.awards.donor.name }}</strong><small>{{ latest_month.awards.donor.donations }} Truppen gespendet</small>{% else %}<strong>Keine Wertung</strong><small>Im Zeitraum wurden keine Spenden erfasst.</small>{% endif %}
        </article>
      </div>
    {% else %}
      <p class="stats-empty">Die erste Monatsauszeichnung wird nach dem ersten vollständig erfassten Monat veröffentlicht.</p>
    {% endif %}
  </section>

  <section class="stats-section" aria-labelledby="village-title">
    <p class="eyebrow">Unsere Dörfer</p>
    <h2 id="village-title">Rathaus-Verteilung</h2>
    {% assign town_hall_levels = stats.townHalls | sort %}
    {% if town_hall_levels.size > 0 %}
      {% assign member_count = stats.members.size %}
      <div class="distribution" role="list" aria-label="Mitglieder nach Rathaus-Level">
        {% for hall in town_hall_levels %}
          {% assign bar_width = hall[1] | times: 100.0 | divided_by: member_count %}
          <div class="distribution-row" role="listitem"><span>Rathaus {{ hall[0] }}</span><span class="distribution-row__track"><span class="distribution-row__fill" style="width: {{ bar_width }}%"></span></span><strong>{{ hall[1] }}</strong></div>
        {% endfor %}
      </div>
    {% else %}
      <p class="stats-empty">Die Rathaus-Level erscheinen mit dem nächsten API-Update.</p>
    {% endif %}
  </section>

  <section class="stats-section" aria-labelledby="donors-title">
    <p class="eyebrow">Saisonleistung</p>
    <h2 id="donors-title">Top-Spender dieser Saison</h2>
    {% assign top_donors = stats.members | slice: 0, 3 %}
    {% if top_donors.size > 0 %}
      <div class="data-table-wrap"><table class="data-table"><thead><tr><th scope="col">#</th><th scope="col">Mitglied</th><th scope="col">Erhalten</th><th scope="col">Gespendet</th></tr></thead><tbody>
        {% for member in top_donors %}<tr><td>{{ forloop.index }}</td><td>{{ member.name }}</td><td>{{ member.donationsReceived }}</td><td>{{ member.donations }}</td></tr>{% endfor %}
      </tbody></table></div>
    {% else %}<p class="stats-empty">Mitgliederwerte werden beim nächsten API-Update geladen.</p>{% endif %}
  </section>

  <section class="stats-section" aria-labelledby="cwl-title">
    <p class="eyebrow">Liga-Kriege</p>
    <h2 id="cwl-title">CWL-Verlauf{% if stats.cwl.season != "" %} · {{ stats.cwl.season }}{% endif %}</h2>
    {% if stats.cwl.wars.size > 0 %}
      <div class="data-table-wrap"><table class="data-table"><thead><tr><th scope="col">Gegner</th><th scope="col">Sterne</th><th scope="col">Ergebnis</th></tr></thead><tbody>
        {% for war in stats.cwl.wars %}<tr><td>{{ war.opponent | default: "Noch nicht beendet" }}</td><td>{{ war.stars }} : {{ war.opponentStars }}</td><td>{% if war.result > 0 %}Sieg{% elsif war.result < 0 %}Niederlage{% else %}Unentschieden{% endif %}</td></tr>{% endfor %}
      </tbody></table></div>
    {% else %}<p class="stats-empty">CWL-Runden werden während der laufenden Liga erfasst und hier ergänzt.</p>{% endif %}
    {% if stats.cwl.history.size > 0 %}
      {% for season in stats.cwl.history %}
        <h3 class="stats-subheading">Frühere Saison · {{ season.season }}</h3>
        <div class="data-table-wrap"><table class="data-table"><thead><tr><th scope="col">Gegner</th><th scope="col">Sterne</th><th scope="col">Ergebnis</th></tr></thead><tbody>
          {% for war in season.wars %}<tr><td>{{ war.opponent | default: "Unbekannt" }}</td><td>{{ war.stars }} : {{ war.opponentStars }}</td><td>{% if war.result > 0 %}Sieg{% elsif war.result < 0 %}Niederlage{% else %}Unentschieden{% endif %}</td></tr>{% endfor %}
        </tbody></table></div>
      {% endfor %}
    {% endif %}
  </section>

  <section class="stats-section" aria-labelledby="warlog-title">
    <p class="eyebrow">Gemeinsam gekämpft</p>
    <h2 id="warlog-title">Letzte Clankriege</h2>
    {% if stats.warlog.size > 0 %}
      <div class="data-table-wrap"><table class="data-table"><thead><tr><th scope="col">Gegner</th><th scope="col">Sterne</th><th scope="col">Ergebnis</th><th scope="col">Größe</th></tr></thead><tbody>
        {% for war in stats.warlog limit: 10 %}<tr><td>{{ war.opponent.name }}</td><td>{{ war.clan.stars }} : {{ war.opponent.stars }}</td><td>{{ war.result | default: "–" }}</td><td>{{ war.teamSize }} Spieler</td></tr>{% endfor %}
      </tbody></table></div>
    {% else %}<p class="stats-empty">Das Kriegsprotokoll ist noch nicht verfügbar oder nicht öffentlich freigegeben.</p>{% endif %}
  </section>

  <section class="stats-section" aria-labelledby="capital-title">
    <p class="eyebrow">Gemeinsam ausgebaut</p>
    <h2 id="capital-title">Clanstadt</h2>
    {% if stats.capitalRaid %}
      <dl class="stats-grid"><div class="stat stat--gold"><dt>Clan-Hauptstadt-Punkte</dt><dd>{{ stats.clan.capitalPoints | default: "–" }}</dd></div><div class="stat stat--blue"><dt>Beute im Raid</dt><dd>{{ stats.capitalRaid.capitalTotalLoot | default: "–" }}</dd></div><div class="stat stat--green"><dt>Angriffe</dt><dd>{{ stats.capitalRaid.totalAttacks | default: "–" }}</dd></div><div class="stat stat--red"><dt>Bezirke zerstört</dt><dd>{{ stats.capitalRaid.enemyDistrictsDestroyed | default: "–" }}</dd></div></dl>
      {% if stats.capitalRaid.startTime %}<p class="stats-section__intro">Raid-Wochenende ab {{ stats.capitalRaid.startTime | date: "%d.%m.%Y" }}</p>{% endif %}
      {% if stats.capitalRaid.districts.size > 0 %}<div class="data-table-wrap"><table class="data-table"><thead><tr><th scope="col">Bezirk</th><th scope="col">Bezirkshalle</th><th scope="col">Angriffe</th><th scope="col">Beute</th></tr></thead><tbody>{% for district in stats.capitalRaid.districts %}<tr><td>{{ district.name }}</td><td>Level {{ district.districtHallLevel }}</td><td>{{ district.attackCount }}</td><td>{{ district.totalLoot }}</td></tr>{% endfor %}</tbody></table></div>{% endif %}
    {% else %}<p class="stats-empty">Clanstadt-Daten erscheinen nach dem nächsten API-Update.</p>{% endif %}
  </section>

  <section class="stats-section" aria-labelledby="members-title">
    <p class="eyebrow">Das sind wir</p>
    <h2 id="members-title">Mitglieder &amp; Aktivität</h2>
    {% if stats.members.size > 0 %}
      <div class="data-table-wrap"><table class="data-table"><thead><tr><th scope="col">Mitglied</th><th scope="col">Rolle</th><th scope="col">Rathaus</th><th scope="col">Trophäen</th><th scope="col">Spenden</th><th scope="col">Erhalten</th></tr></thead><tbody>
        {% for member in stats.members %}<tr><td>{{ member.name }}</td><td>{{ member.role }}</td><td>{{ member.townHallLevel | default: "–" }}</td><td>{{ member.trophies | default: "–" }}</td><td>{{ member.donations | default: 0 }}</td><td>{{ member.donationsReceived | default: 0 }}</td></tr>{% endfor %}
      </tbody></table></div>
    {% else %}<p class="stats-empty">Die Mitgliederliste wird beim nächsten API-Update geladen.</p>{% endif %}
  </section>

  <footer class="site-footer">Clan „Letzte Hoffnung“ (#2LR89PLLL) <span aria-hidden="true">·</span> Gehostet auf GitHub Pages</footer>
</main>
