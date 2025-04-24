<p align="center">
  <img src="Banner.png" alt="zZipCracker" width="300"/>
</p>

<p align="right">
  <a href="./README_en.md">Switch to English version</a>
</p>

# zZipCracker – Brute-Force ZIP-Knacker-Tool

**zZipCracker** ist ein leichtgewichtiges Python-Tool zum demonstrativen Durchprobieren von Passwörtern geschützter ZIP-Dateien.  
Ideal für Lern- und Sensibilisierungszwecke im Bereich Passwortsicherheit und Brute-Force-Mechanismen.

> ⚠️ Hinweis: Dieses Tool wurde zu **Lern- und Demonstrationszwecken** entwickelt. Keine Anwendung auf fremde Systeme oder Dateien ohne ausdrückliche Erlaubnis!

---

## Features

- Brute-Force-Angriff auf ZIP-Dateien durch systematisches Durchprobieren
- Nutzung der Windows-Kommandozeile zur Prozessverteilung
- Aufteilung der Zeichenliste auf vier parallele Prozesse
- Fortschrittsanzeige pro Zeichenkombination und Passwortlänge
- Minimaler Ressourceneinsatz – ohne externe Bibliotheken außer `tqdm`

---

## Motivation

Dieses Projekt entstand als praktische Übung zum Thema **Passwortsicherheit**, **Brute-Force-Verfahren** und **Parallelisierung unter Windows**.  
Es dient dazu zu verstehen:

- Wie Brute-Force-Angriffe technisch funktionieren
- Warum schwache Passwörter ein großes Risiko darstellen
- Wie sich Prozesse aufteilen und parallelisieren lassen – sogar ohne Frameworks

Die Idee entstand inspiriert durch das Buch _"Ethical Hacking"_ von Florian André Dalwigk.

---

## Voraussetzungen

- Python 3.x (getestet unter Windows mit 3.10)
- Installiertes Kommandozeilentool [7-Zip](https://www.7-zip.org/) (mit `7z` im PATH)
- Eine passwortgeschützte ZIP-Datei zum Testen

---

## Installation & Start

1. Repository klonen oder Skript herunterladen:

```bash
git clone https://github.com/0xZorro/zZipCracker.git
```

2. In das Projektverzeichnis wechseln und `zzipcracker.py` ausführen:

```bash
python zzipcracker.py geheim.zip 3 5
```

3. Es öffnen sich automatisch **vier CMD-Fenster**, die parallel versuchen, das Passwort zu knacken.

---

## Funktionsweise: Automatische Aufteilung in Teilprozesse

`zZipCracker` ist so konzipiert, dass es die Brute-Force-Arbeit **auf vier parallele Prozesse verteilt** – **jedes CMD-Fenster übernimmt einen Teilbereich der Zeichenliste**.

### Ablauf (automatisch):

```bash
python zzipcracker.py geheim.zip 3 5
```

1. Das Programm erkennt: „Ich bin der Hauptprozess“
2. Es startet **4 neue CMD-Fenster**
3. Jedes Fenster führt denselben Code aus – **mit eigenem `teil_index`**
4. Dadurch wird die Zeichenliste gleichmäßig aufgeteilt

```
┌────────────────────────────┐
│      Hauptprozess          │
│  (startet 4 CMD-Fenster)   │
└────────────────────────────┘
       ↓      ↓      ↓      ↓
   [CMD 0] [CMD 1] [CMD 2] [CMD 3]
      │        │       │       │
      ▼        ▼       ▼       ▼
 crack_zip() crack_zip() ... crack_zip()
   (Teil 1)   (Teil 2)       (Teil 4)
```

### Manueller Aufruf eines Teilbereichs:

```bash
python zzipcracker.py geheim.zip 3 5 2
```

Führt nur den **dritten Teilprozess** (Index 2) aus – nützlich zum Testen oder gezielten Durchlauf.

### Hinweis:

Der Index `teil_index` (0 bis 3) bestimmt, **mit welchen Startzeichen** der Prozess beginnt.


### Kommandozeilenargumente erklärt

Beim Aufruf des Tools:

```bash
python zzipcracker.py geheim.zip 3 5
```

werden folgende Argumente übergeben:

| Position | Argument         | Bedeutung                                                                 |
|----------|------------------|---------------------------------------------------------------------------|
| `1`      | `geheim.zip`     | Pfad zur ZIP-Datei, die geknackt werden soll                              |
| `2`      | `3`              | **Minimale Passwortlänge** – das Tool beginnt mit Passwörtern ab dieser Länge |
| `3`      | `5`              | **Maximale Passwortlänge** – das Tool testet Passwörter bis zu dieser Länge |
| `4` *(optional)* | `2`        | (Nur bei manuellem Teilprozess) Index des Zeichenbereichs: `0` bis `3`     |

---

🔹 Die Argumente **min** und **max** definieren also den **Längenbereich** der Passwörter, die durchprobiert werden.  
🔹 Wenn kein `teil_index` angegeben wird → startet das Hauptprogramm **vier parallele CMD-Prozesse** automatisch.  
🔹 Wenn ein `teil_index` angegeben ist → wird **nur dieser eine Teilbereich** ausgeführt.


### Dokumentation

- [Deutsche Dokumentation ansehen (crack_zip.md)](./doc_DE/crack_zip.md)

---

## Sicherheitshinweise

Dieses Tool ist **nicht zum illegalen Knacken fremder Archive gedacht**, sondern zur Bewusstmachung:

- Wie schnell ein schwaches Passwort geknackt werden kann
- Wie wichtig es ist, Sonderzeichen, Länge und Zufall zu kombinieren
- Warum Passwortmanager sinnvoll sind

---

## Zukünftige Erweiterungen

Das Projekt `zZipCracker` bietet eine solide Grundlage für experimentelles Brute-Forcing – dennoch bestehen viele spannende Erweiterungsmöglichkeiten:

- **Unterstützung für Passwortlisten (Wordlists)**  
  Möglichkeit, eine externe Datei wie `rockyou.txt` zu laden und gezielt Einträge zu testen, anstatt Kombinationen zu generieren.

- **Zeichenbereich als Argument übergeben**  
  Optionaler CLI-Schalter wie `--charset=abc123` zur individuellen Eingrenzung der Zeichenbasis.  
  Praktisch für gezielte Tests mit nur Kleinbuchstaben, nur Ziffern etc.

- **Mehr als 4 Prozesse unterstützen**  
  Aktuell ist die Zeichenliste hart auf vier Bereiche aufgeteilt.  
  Eine dynamische Aufteilung auf beliebig viele Prozesse (je nach CPU-Kernen) wäre effizienter.  
  ➕ Dazu müsste die Logik zur Bereichsberechnung und Aufrufstruktur angepasst werden.

- **Thread-basierte Verarbeitung innerhalb eines CMD-Fensters**  
  Derzeit arbeitet jeder CMD-Prozess linear.  
  Idee: Innerhalb eines CMDs könnten z. B. **2 oder mehr Threads** jeweils eine Hälfte des Teilbereichs übernehmen.  
  → Effizientere Nutzung moderner Multi-Core-CPUs.

- **Logging der getesteten Passwörter**  
  Optionales Mitschreiben aller getesteten Kombinationen (z. B. bei längeren Sessions zur späteren Analyse).

- **Behandlung des Sonderzeichens `"`**  
  Aktuell wird das doppelte Anführungszeichen (`"`) **aus der Zeichenliste entfernt**, da es zu Problemen in der Shell führt (besonders bei der 7z-Kommandostruktur).  
  Eine robustere Lösung wäre:
  - Escaping oder maskiertes Einfügen (`\"`)
  - Übergabe via Input-File statt Kommandozeile

- **Modularisierung & Code-Cleanup**  
  Aufteilung in eigenständige Module (z. B. `bruteforce.py`, `cli.py`, `log.py`) für bessere Wartbarkeit.

- **Benchmarking-Funktion**  
  Ausgabe der durchschnittlichen Versuche pro Sekunde und benötigten Zeit pro Bereich – zur Performanceanalyse und Optimierung.

---

##  Lizenz

Dieses Projekt steht unter der **MIT-Lizenz**.  
Details findest du in der Datei [LICENSE](LICENSE).

---

## Autor

**Created by Jose Luis Ocana**

Cybersecurity Learner | Python & C++ Tools

(GitHub: [0xZorro](https://github.com/0xZorro))  

TryHackMe: https://tryhackme.com/p/0xZorro

Contact: zorro.jose@gmx.de

---

## Beiträge

Du möchtest mithelfen? Super!  
Forke das Projekt, nimm Änderungen vor und stelle einen Pull Request.  
Halte dich bitte an den Verhaltenskodex und die Projektstandards.

---

## ⚠️ Rechtlicher Hinweis

### Warnung vor Missbrauch:

Dieses Tool dient ausschließlich **zu Bildungs- und Demonstrationszwecken** im Bereich IT-Sicherheit.  
Jeglicher Missbrauch, insbesondere gegen fremde Systeme oder ohne Erlaubnis, ist **illegal** und strafbar.

---

##  Haftungsausschluss

Der Autor übernimmt keinerlei Verantwortung oder Haftung für Schäden, Datenverlust oder rechtliche Konsequenzen, die durch den Einsatz dieser Software entstehen.  
Die Nutzung erfolgt auf **eigene Gefahr** – nur in Testumgebungen verwenden!

---

<div align="center">
  <img src="brand.png" alt="by 0xZorro" width="120"/>
  <br/>
  <sub>© 2025 0xZorro</sub>
</div>

---
