# Feature-Inventar

Vollständige Liste aller Funktionen für Mitglieder des TCZ-Buchungssystems.

---

## Kernfunktionen

### Platzbuchung
| Feature | Beschreibung | Priorität |
|---------|--------------|-----------|
| Platz reservieren | Buchung eines 1-Stunden-Slots auf einem der 6 Plätze | Hoch |
| Buchung stornieren | Absage einer Buchung bis 15 Min. vor Spielbeginn | Hoch |
| Kurzfristige Buchung | Spontane Buchung innerhalb 15 Min. vor Spielbeginn | Hoch |
| Für andere buchen | Reservierung für beliebige Vereinsmitglieder | Mittel |
| Buchungsübersicht | Liste aller eigenen aktiven Buchungen | Hoch |

→ [Buchungen-Dokumentation](buchungen/)

---

### Verfügbarkeitsanzeige
| Feature | Beschreibung | Priorität |
|---------|--------------|-----------|
| Dashboard-Raster | Visuelle Übersicht aller Plätze und Zeiten | Hoch |
| Datumsnavigation | Auswahl beliebiger Tage | Mittel |
| Farbcodierung | Unterscheidung von verfügbar/gebucht/gesperrt | Hoch |
| Anonyme Ansicht | Verfügbarkeit ohne Anmeldung einsehen | Niedrig |

---

## Profilverwaltung

### Persönliche Daten
| Feature | Beschreibung | Priorität |
|---------|--------------|-----------|
| Profil bearbeiten | Änderung von Name, Adresse, Telefon | Mittel |
| E-Mail ändern | Änderung der E-Mail-Adresse | Mittel |
| Passwort ändern | Änderung des Passworts | Mittel |
| E-Mail verifizieren | Bestätigung der E-Mail-Adresse | Mittel |

→ [Profil-Dokumentation](profil/)

---

### Profilbild
| Feature | Beschreibung | Priorität |
|---------|--------------|-----------|
| Bild hochladen | Upload eines Profilbildes (max. 5 MB) | Niedrig |
| Bild löschen | Entfernung des Profilbildes | Niedrig |
| Initialen-Anzeige | Automatische Anzeige von Initialen ohne Bild | Niedrig |

→ [Profilbild-Dokumentation](profil/profilbild.md)

---

## Favoriten

| Feature | Beschreibung | Priorität |
|---------|--------------|-----------|
| Favorit hinzufügen | Speichern eines Mitglieds für Schnellzugriff | Mittel |
| Favorit entfernen | Löschen eines gespeicherten Favoriten | Mittel |
| Schnellbuchung | Direkter Zugriff auf Favoriten im Buchungsdialog | Mittel |
| Auto-Hinzufügen | Automatisches Hinzufügen bei Mitgliedersuche | Niedrig |

→ [Favoriten-Dokumentation](favoriten/)

---

## Benachrichtigungen

| Feature | Beschreibung | Priorität |
|---------|--------------|-----------|
| E-Mail für eigene Buchungen | Benachrichtigung bei eigenen Reservierungen | Mittel |
| E-Mail für Fremd-Buchungen | Benachrichtigung wenn andere für mich buchen | Mittel |
| E-Mail bei Sperrungen | Benachrichtigung bei Platzsperrungen | Niedrig |
| E-Mail bei Suspendierung | Benachrichtigung wenn Buchung suspendiert wird | Mittel |
| Master-Schalter | Aktivierung/Deaktivierung aller Benachrichtigungen | Mittel |

→ [Benachrichtigungen-Dokumentation](profil/benachrichtigungen.md)

---

## Mitgliedschaft & Zahlung

| Feature | Beschreibung | Priorität |
|---------|--------------|-----------|
| Zahlungsstatus einsehen | Anzeige ob Beitrag bezahlt | Hoch |
| Zahlungsfrist-Countdown | Anzeige der verbleibenden Tage | Mittel |
| Zahlung bestätigen | Meldung der erfolgten Zahlung | Hoch |
| Buchungssperre | Automatische Sperre bei überfälliger Zahlung | Hoch |

→ [Mitgliedschaft-Dokumentation](mitgliedschaft/)

---

## Statistiken

| Feature | Beschreibung | Priorität |
|---------|--------------|-----------|
| Buchungen gesamt | Gesamtzahl der eigenen Buchungen | Niedrig |
| Stornierungsrate | Prozentsatz stornierter Buchungen | Niedrig |
| Top-Spielpartner | Liste der häufigsten Spielpartner | Niedrig |
| Monatliche Übersicht | Buchungen pro Monat als Balkendiagramm | Niedrig |
| Platz-Präferenzen | Häufigkeit pro Platz | Niedrig |
| Zeit-Präferenzen | Beliebte Uhrzeiten | Niedrig |
| Wochentag-Präferenzen | Beliebte Wochentage | Niedrig |
| Jahr-Filter | Filterung nach Jahr | Niedrig |

→ [Statistiken-Dokumentation](statistiken/)

---

## Authentifizierung

| Feature | Beschreibung | Priorität |
|---------|--------------|-----------|
| Anmeldung | Login mit E-Mail und Passwort | Hoch |
| Abmeldung | Logout aus dem System | Hoch |
| Passwort vergessen | Passwort-Zurücksetzen per E-Mail | Mittel |

---

## Plattformen

### Web-App
Alle oben genannten Features sind in der Web-App verfügbar.

### iOS-App
Die iOS-App bietet die gleichen Kernfunktionen:
- Platzbuchung und -stornierung
- Verfügbarkeitsanzeige
- Favoriten-Verwaltung
- Profilbearbeitung
- Statistiken
- Push-Benachrichtigungen

→ [Feature-Matrix](feature_matrix.md)

---

## Nicht-Mitglieder-Funktionen

| Feature | Beschreibung | Zugang |
|---------|--------------|--------|
| Anonyme Verfügbarkeit | Platzverfügbarkeit ohne Login einsehen | Öffentlich |

---

## Admin-Funktionen (nicht für Mitglieder)

Die folgenden Funktionen sind nur für Administratoren verfügbar:
- Mitglieder erstellen/bearbeiten/deaktivieren
- Platzsperrungen verwalten
- Zahlungsstatus ändern
- Mitgliedschaftstyp ändern
- Audit-Logs einsehen
- CSV-Import von Mitgliedern
