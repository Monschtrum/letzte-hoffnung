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
      <div class="stat stat--green"><dt>Clankriegs-Siege</dt><dd>{{ stats.clan.warWins | default: "–" }}</dd></div>
    </dl>
    <p class="stats-updated--page">{% if stats.updatedAt and stats.updatedAt != "" %}Datenstand: {{ stats.updatedAt }}{% else %}Die erste Aktualisierung der erweiterten Statistiken steht noch aus.{% endif %}</p>
  </section>

  <section class="stats-section" aria-labelledby="honorees-title">
    <p class="eyebrow">Monatliche Auszeichnungen</p>
    <h2 id="honorees-title">Mitglied des Monats{% if stats.monthly.history.first %}: {{ stats.monthly.history.first.month }}{% endif %}</h2>
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
    {% assign town_hall_levels = stats.townHalls %}
    {% if town_hall_levels.size > 0 %}
      {% assign member_count = stats.members.size %}
      <div class="distribution" role="list" aria-label="Mitglieder nach Rathaus-Level">
        {% for hall in town_hall_levels %}
          {% assign bar_width = hall.count | times: 100.0 | divided_by: member_count %}
          <div class="distribution-row" role="listitem"><span>Rathaus {{ hall.level }}</span><span class="distribution-row__track"><span class="distribution-row__fill" style="width: {{ bar_width }}%"></span></span><strong>{{ hall.count }}</strong></div>
        {% endfor %}
      </div>
    {% else %}
      <p class="stats-empty">Die Rathaus-Level erscheinen mit dem nächsten API-Update.</p>
    {% endif %}
  </section>

  <section class="stats-section" aria-labelledby="donors-title">
    <p class="eyebrow">Saisonleistung</p>
    <h2 id="donors-title">Spendenrangliste dieser Saison</h2>
    {% assign top_donors = stats.members | slice: 0, 3 %}
    {% if top_donors.size > 0 %}
      <div class="data-table-wrap"><table class="data-table"><thead><tr><th scope="col">Platz</th><th scope="col">Mitglied</th><th scope="col">Erhaltene Truppen</th><th scope="col">Gespendete Truppen</th></tr></thead><tbody>
        {% for member in top_donors %}<tr><td class="data-table__rank">{{ forloop.index }}</td><td>{{ member.name }}</td><td class="data-table__numeric">{{ member.donationsReceived }}</td><td class="data-table__numeric">{{ member.donations }}</td></tr>{% endfor %}
      </tbody></table></div>
    {% else %}<p class="stats-empty">Mitgliederwerte werden beim nächsten API-Update geladen.</p>{% endif %}
  </section>

  <section class="stats-section" aria-labelledby="cwl-title">
    <p class="eyebrow">Clankriegs-Liga</p>
    <h2 id="cwl-title">CWL-Verlauf{% if stats.cwl.season != "" %} · {{ stats.cwl.season }}{% endif %}</h2>
    {% if stats.cwl.wars.size > 0 %}
      <div class="data-table-wrap"><table class="data-table"><thead><tr><th scope="col">Gegner</th><th scope="col">Sterne</th><th scope="col">Ausgang</th></tr></thead><tbody>
        {% for war in stats.cwl.wars %}<tr><td>{{ war.opponent | default: "Noch nicht beendet" }}</td><td class="data-table__numeric">{{ war.stars }} : {{ war.opponentStars }}</td><td>{% if war.result > 0 %}<span class="match-result match-result--win">Sieg</span>{% elsif war.result < 0 %}<span class="match-result match-result--loss">Niederlage</span>{% else %}<span class="match-result match-result--tie">Unentschieden</span>{% endif %}</td></tr>{% endfor %}
      </tbody></table></div>
    {% else %}<p class="stats-empty">CWL-Runden werden während der laufenden Liga erfasst und hier ergänzt.</p>{% endif %}
    {% if stats.cwl.history.size > 0 %}
      {% for season in stats.cwl.history %}
        <h3 class="stats-subheading">Frühere Saison · {{ season.season }}</h3>
        <div class="data-table-wrap"><table class="data-table"><thead><tr><th scope="col">Gegner</th><th scope="col">Sterne</th><th scope="col">Ausgang</th></tr></thead><tbody>
          {% for war in season.wars %}<tr><td>{{ war.opponent | default: "Unbekannt" }}</td><td class="data-table__numeric">{{ war.stars }} : {{ war.opponentStars }}</td><td>{% if war.result > 0 %}<span class="match-result match-result--win">Sieg</span>{% elsif war.result < 0 %}<span class="match-result match-result--loss">Niederlage</span>{% else %}<span class="match-result match-result--tie">Unentschieden</span>{% endif %}</td></tr>{% endfor %}
        </tbody></table></div>
      {% endfor %}
    {% endif %}
  </section>

  <section class="stats-section" aria-labelledby="warlog-title">
    <p class="eyebrow">Gemeinsam gekämpft</p>
    <h2 id="warlog-title">Letzte Clankriege</h2>
    {% if stats.warlog.size > 0 %}
      <div class="data-table-wrap"><table class="data-table"><thead><tr><th scope="col">Gegner</th><th scope="col">Sterne</th><th scope="col">Ausgang</th><th scope="col">Teilnehmer</th></tr></thead><tbody>
        {% for war in stats.warlog limit: 10 %}<tr><td>{{ war.opponent.name }}</td><td class="data-table__numeric">{{ war.clan.stars }} : {{ war.opponent.stars }}</td><td>{% if war.result == "win" %}<span class="match-result match-result--win">Sieg</span>{% elsif war.result == "lose" or war.result == "loss" %}<span class="match-result match-result--loss">Niederlage</span>{% elsif war.result == "tie" %}<span class="match-result match-result--tie">Unentschieden</span>{% else %}<span>–</span>{% endif %}</td><td>{{ war.teamSize }}</td></tr>{% endfor %}
      </tbody></table></div>
    {% else %}<p class="stats-empty">Das Kriegsprotokoll ist noch nicht verfügbar oder nicht öffentlich freigegeben.</p>{% endif %}
  </section>

  <section class="stats-section" aria-labelledby="capital-title">
    <p class="eyebrow">Gemeinsam ausgebaut</p>
    <h2 id="capital-title">Clanstadt</h2>
    {% if stats.capitalRaid %}
      <dl class="stats-grid"><div class="stat stat--gold"><dt>Hauptstadt-Punkte</dt><dd>{{ stats.clan.capitalPoints | default: "–" }}</dd></div><div class="stat stat--blue"><dt>Überfallbeute</dt><dd>{{ stats.capitalRaid.capitalTotalLoot | default: "–" }}</dd></div><div class="stat stat--green"><dt>Angriffe</dt><dd>{{ stats.capitalRaid.totalAttacks | default: "–" }}</dd></div><div class="stat stat--red"><dt>Zerstörte Bezirke</dt><dd>{{ stats.capitalRaid.enemyDistrictsDestroyed | default: "–" }}</dd></div></dl>
      {% if stats.capitalRaid.startTime %}<p class="stats-section__intro">Überfall-Wochenende ab {{ stats.capitalRaid.startTime | date: "%d.%m.%Y" }}</p>{% endif %}
      {% if stats.capitalRaid.districts.size > 0 %}<div class="data-table-wrap"><table class="data-table"><thead><tr><th scope="col">Bezirk</th><th scope="col">Rathaus-Level</th><th scope="col">Angriffe</th><th scope="col">Beute</th></tr></thead><tbody>{% for district in stats.capitalRaid.districts %}<tr><td>{{ district.name }}</td><td>{{ district.districtHallLevel }}</td><td class="data-table__numeric">{{ district.attackCount }}</td><td class="data-table__numeric">{{ district.totalLoot }}</td></tr>{% endfor %}</tbody></table></div>{% endif %}
    {% else %}<p class="stats-empty">Clanstadt-Daten erscheinen nach dem nächsten API-Update.</p>{% endif %}
  </section>

  <section class="stats-section" aria-labelledby="members-title">
    <p class="eyebrow">Das sind wir</p>
    <h2 id="members-title">Mitglieder &amp; Aktivität</h2>
    {% if stats.members.size > 0 %}
      <div class="data-table-wrap"><table class="data-table"><thead><tr><th scope="col">Mitglied</th><th scope="col">Rolle</th><th scope="col">Rathaus</th><th scope="col">Trophäen</th><th scope="col">Spenden</th><th scope="col">Erhalten</th></tr></thead><tbody>
        {% for member in stats.members %}
          {% assign role_name = "Mitglied" %}
          {% case member.role %}
            {% when "leader" %}{% assign role_name = "Anführer" %}
            {% when "coLeader" %}{% assign role_name = "Vize-Anführer" %}
            {% when "admin" %}{% assign role_name = "Ältester" %}
            {% when "elder" %}{% assign role_name = "Ältester" %}
          {% endcase %}
          <tr><td>{{ member.name }}</td><td>{{ role_name }}</td><td>{{ member.townHallLevel | default: "–" }}</td><td class="data-table__numeric">{{ member.trophies | default: "–" }}</td><td class="data-table__numeric">{{ member.donations | default: 0 }}</td><td class="data-table__numeric">{{ member.donationsReceived | default: 0 }}</td></tr>
        {% endfor %}
      </tbody></table></div>
    {% else %}<p class="stats-empty">Die Mitgliederliste wird beim nächsten API-Update geladen.</p>{% endif %}
  </section>

  <footer class="site-footer">Clan „Letzte Hoffnung“ (#2LR89PLLL) <span aria-hidden="true">·</span> Gehostet auf GitHub Pages</footer>
</main>
