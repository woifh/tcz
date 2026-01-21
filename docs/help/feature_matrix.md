# Feature-Matrix: Web vs. iOS

Vergleich der verfügbaren Funktionen zwischen Web-App und iOS-App.

---

## Legende

| Symbol | Bedeutung |
|--------|-----------|
| ✅ | Vollständig verfügbar |
| ⚠️ | Teilweise verfügbar |
| ❌ | Nicht verfügbar |

---

## Buchungsfunktionen

| Feature | Web | iOS | Anmerkungen |
|---------|-----|-----|-------------|
| Platz buchen | ✅ | ✅ | |
| Buchung stornieren | ✅ | ✅ | |
| Kurzfristige Buchung | ✅ | ✅ | |
| Für andere buchen | ✅ | ✅ | |
| Buchungsübersicht | ✅ | ✅ | |
| Buchungslimits-Anzeige | ✅ | ✅ | |

---

## Verfügbarkeitsanzeige

| Feature | Web | iOS | Anmerkungen |
|---------|-----|-----|-------------|
| Dashboard-Raster | ✅ | ✅ | |
| Datumsnavigation | ✅ | ✅ | |
| Farbcodierung | ✅ | ✅ | |
| Echtzeit-Aktualisierung | ✅ | ✅ | |
| Anonyme Ansicht | ✅ | ❌ | iOS erfordert Login |

---

## Profilverwaltung

| Feature | Web | iOS | Anmerkungen |
|---------|-----|-----|-------------|
| Profil bearbeiten | ✅ | ✅ | |
| E-Mail ändern | ✅ | ✅ | |
| Passwort ändern | ✅ | ✅ | |
| E-Mail verifizieren | ✅ | ✅ | |
| Profilbild hochladen | ✅ | ✅ | iOS: Kamera-Integration |
| Profilbild löschen | ✅ | ✅ | |

---

## Favoriten

| Feature | Web | iOS | Anmerkungen |
|---------|-----|-----|-------------|
| Favoriten anzeigen | ✅ | ✅ | |
| Favorit hinzufügen | ✅ | ✅ | |
| Favorit entfernen | ✅ | ✅ | |
| Schnellbuchung | ✅ | ✅ | |

---

## Benachrichtigungen

| Feature | Web | iOS | Anmerkungen |
|---------|-----|-----|-------------|
| E-Mail-Benachrichtigungen | ✅ | ✅ | |
| Benachrichtigungseinstellungen | ✅ | ✅ | |
| Push-Benachrichtigungen | ❌ | ✅ | Nur iOS |

---

## Mitgliedschaft & Zahlung

| Feature | Web | iOS | Anmerkungen |
|---------|-----|-----|-------------|
| Zahlungsstatus anzeigen | ✅ | ✅ | |
| Zahlungsfrist-Countdown | ✅ | ✅ | |
| Zahlung bestätigen | ✅ | ✅ | |

---

## Statistiken

| Feature | Web | iOS | Anmerkungen |
|---------|-----|-----|-------------|
| Übersichtskarten | ✅ | ✅ | |
| Top-Spielpartner | ✅ | ✅ | |
| Monatliche Übersicht | ✅ | ✅ | |
| Platz-Präferenzen | ✅ | ✅ | |
| Zeit-Präferenzen | ✅ | ✅ | |
| Wochentag-Präferenzen | ✅ | ✅ | |
| Jahr-Filter | ✅ | ✅ | |

---

## Authentifizierung

| Feature | Web | iOS | Anmerkungen |
|---------|-----|-----|-------------|
| Login | ✅ | ✅ | iOS: JWT-Token |
| Logout | ✅ | ✅ | |
| Passwort vergessen | ✅ | ✅ | Öffnet Web-Seite |
| Session-Speicherung | ✅ | ✅ | iOS: Keychain |

---

## Plattformspezifische Features

### Nur Web

| Feature | Beschreibung |
|---------|--------------|
| Anonyme Ansicht | Verfügbarkeit ohne Login |
| Vollständige Profil-Seite | Alle Einstellungen an einem Ort |

### Nur iOS

| Feature | Beschreibung |
|---------|--------------|
| Push-Benachrichtigungen | Native iOS-Benachrichtigungen |
| Kamera-Integration | Direktes Fotografieren für Profilbild |
| Offline-Caching | Zwischenspeicherung für schnelleren Zugriff |
| Keychain-Speicherung | Sichere Token-Speicherung |

---

## Technische Unterschiede

| Aspekt | Web | iOS |
|--------|-----|-----|
| Authentifizierung | Session-basiert | JWT-Token |
| Daten-Speicherung | Browser-Cookies | Keychain |
| Benachrichtigungen | Nur E-Mail | E-Mail + Push |
| Offline-Fähigkeit | Eingeschränkt | Caching vorhanden |

---

## Empfehlungen

### Web-App bevorzugen für:
- Erstmalige Registrierung und Setup
- Komplexe Profilbearbeitung
- Anonymes Prüfen der Verfügbarkeit

### iOS-App bevorzugen für:
- Schnelles Buchen unterwegs
- Push-Benachrichtigungen
- Regelmäßige Nutzung
