# Buchungslimits

Verstehe die Buchungslimits und wie sie funktionieren.

---

## Überblick

Um eine faire Verteilung der Plätze zu gewährleisten, gibt es Limits für die Anzahl gleichzeitiger Buchungen pro Mitglied.

---

## Die Limits im Detail

### Reguläre Buchungen: Maximum 2

Jedes Mitglied kann **maximal 2 aktive reguläre Buchungen** gleichzeitig haben.

- **Aktiv** bedeutet: Die Buchung liegt in der Zukunft oder ist gerade im Gange
- Sobald eine Buchungszeit vorbei ist, zählt sie nicht mehr zum Limit
- Du kannst dann wieder eine neue Buchung vornehmen

### Kurzfristige Buchungen: Maximum 1

Zusätzlich zu den 2 regulären Buchungen kannst du **1 kurzfristige Buchung** haben.

- Kurzfristige Buchungen zählen **nicht** zum regulären 2er-Limit
- Damit sind theoretisch **bis zu 3 Buchungen** gleichzeitig möglich (2 regulär + 1 kurzfristig)
- Siehe [Kurzfristige Buchungen](kurzfristige-buchungen.md) für Details

---

## So werden Limits berechnet

### Was zählt als "aktiv"?

Eine Buchung gilt als **aktiv**, wenn:

1. Das Datum in der **Zukunft** liegt, ODER
2. Das Datum **heute** ist UND die Endzeit noch nicht erreicht wurde

### Beispiel

Es ist Dienstag, 14:30 Uhr. Du hast folgende Buchungen:

| Buchung | Datum | Zeit | Status |
|---------|-------|------|--------|
| Platz 1 | Dienstag | 10:00-11:00 | Nicht aktiv (vorbei) |
| Platz 2 | Dienstag | 16:00-17:00 | Aktiv (Endzeit 17:00 > 14:30) |
| Platz 3 | Mittwoch | 09:00-10:00 | Aktiv (in der Zukunft) |

**Ergebnis**: 2 aktive Buchungen - du kannst keine weitere reguläre Buchung machen.

Um 17:01 Uhr hast du nur noch 1 aktive Buchung und kannst wieder buchen.

---

## Fehlermeldungen

### "Du hast bereits 2 aktive Buchungen"

Diese Meldung erscheint, wenn du versuchst eine Buchung zu machen, aber bereits 2 aktive reguläre Buchungen hast.

**Lösungen:**
- Warte, bis eine deiner Buchungen abgelaufen ist
- Storniere eine bestehende Buchung (mindestens 15 Min. vor Spielbeginn)
- Nutze eine kurzfristige Buchung (falls der Slot innerhalb von 15 Min. beginnt)

### "Du hast bereits eine aktive kurzfristige Buchung"

Diese Meldung erscheint, wenn du eine kurzfristige Buchung machen möchtest, aber bereits eine aktive kurzfristige Buchung hast.

**Lösungen:**
- Warte, bis die kurzfristige Buchung abgelaufen ist
- Kurzfristige Buchungen können nicht storniert werden

---

## Buchung für andere Mitglieder

Wenn du **für ein anderes Mitglied** buchst:

- Das Limit gilt für das Mitglied, **für das gebucht wird** (nicht für dich)
- Beispiel: Du buchst für Max. Die Buchung zählt zu Max' Limit, nicht zu deinem.
- Die Fehlermeldung zeigt dann: "{Name} hat bereits 2 aktive Buchungen"

---

## Tipps

1. **Plane voraus**: Buche nicht zu weit im Voraus, wenn du flexibel bleiben willst
2. **Limits prüfen**: Das Dashboard zeigt dir immer deinen aktuellen Status an
3. **Kurzfristig buchen**: Spontane Slots (< 15 Min.) zählen nicht zum regulären Limit
4. **Stornieren bei Bedarf**: Rechtzeitige Stornierung gibt das Limit wieder frei

---

## Häufige Fragen

**Warum gibt es Limits?**
Die Limits stellen sicher, dass alle Mitglieder faire Chancen haben, Plätze zu buchen. Ohne Limits könnten einzelne Mitglieder alle verfügbaren Zeiten blockieren.

**Zählen stornierte Buchungen zum Limit?**
Nein, nur aktive Buchungen zählen. Nach einer Stornierung wird das Limit sofort freigegeben.

**Was ist der Unterschied zwischen regulär und kurzfristig?**
Kurzfristige Buchungen sind Buchungen innerhalb von 15 Minuten vor Spielbeginn. Sie haben ein separates Limit und können nicht storniert werden. Siehe [Kurzfristige Buchungen](kurzfristige-buchungen.md).
