
# Detaillierte Erklärung: `crack_zip()` – Code Behind & Mathematischer Kontext

Diese Funktion stellt das Herzstück des Brute-Force-Angriffs dar. Sie wird in einem separaten Prozess (CMD-Fenster) ausgeführt und übernimmt einen Teilbereich des gesamten Zeichenraums. Ziel ist es, systematisch **alle möglichen Passwortkombinationen** zu testen, die mit einem bestimmten Startzeichen beginnen.

---

## Funktionssignatur

```python
def crack_zip(archiv, min_len=1, max_len=10, teil_index=None):
```

| Parameter    | Beschreibung |
|--------------|--------------|
| `archiv`     | Pfad zur verschlüsselten ZIP-Datei |
| `min_len`    | Minimale Passwortlänge |
| `max_len`    | Maximale Passwortlänge |
| `teil_index` | Gibt an, welchen Teilbereich der Zeichenliste dieser Prozess abarbeiten soll (0–3) |

---

## Aufteilung der Zeichenliste

Die globale Zeichenliste `characters` wird in vier gleich große Abschnitte geteilt (bei `anzahl_prozesse = 4`).  
Jeder Prozess bearbeitet nur die Kombinationen, die mit **einem seiner Startzeichen** beginnen.

```python
bereichsgroesse = len(characters) // 4
```

Beispiel:  
Angenommen, die Zeichenliste enthält **64 Zeichen**, dann:

```
bereichsgroesse = 64 // 4 = 16
```

Die Teilbereiche wären:
- Teil 0 → Zeichen 0–15
- Teil 1 → Zeichen 16–31
- Teil 2 → Zeichen 32–47
- Teil 3 → Zeichen 48–63

Der letzte Teilprozess nimmt ggf. die restlichen Zeichen mit auf.

```python
if i == anzahl_prozesse - 1:
    ende = zeichenlaenge
```
---

## Ziel: Gleichmäßige Verteilung auf Prozesse

```text
┌────────────────────────────┐
│ Zeichenliste (64 Zeichen) │
└────────────────────────────┘
        ↓  ↓  ↓  ↓
   [Teil 0] [Teil 1] ...
   (A-F)    (G-L)   ...
```

---

## Passwortlängen durchlaufen

```python
for n in range(min_len, max_len + 1):
    rest_len = n - 1
```

In dieser Schleife werden **alle gewünschten Passwortlängen** durchlaufen – von `min_len` bis einschließlich `max_len`.

### Beispiel:
```python
min_len = 3
max_len = 5
range(min_len, max_len + 1)  # ergibt: 3, 4, 5
```

Das bedeutet:  
Das Programm wird Passwörter mit **3, 4 und 5 Zeichen** ausprobieren.

---

Da der Brute-Force-Ansatz in dieser Funktion so aufgebaut ist, dass **jedes Passwort mit einem festen Startzeichen beginnt** (aus dem zugewiesenen Teilbereich der Zeichenliste),  
werden nur noch die **verbleibenden Stellen** durch Kombinationen gefüllt.

Deshalb wird die sogenannte `rest_len` so berechnet:

```python
rest_len = n - 1
```

Das bedeutet:  
Wenn die gewünschte Passwortlänge z. B. `n = 4` beträgt, wird:

- 1 Zeichen durch `erster_buchstabe` bestimmt (z. B. 'A')
- Die **restlichen 3 Zeichen** werden durch Kombinationen mit `itertools.product()` gebildet

---

### Visualisierung:

```
Ziel: Passwort mit Länge n = 4
                  ▼
        ┌──────┬────────────────────┐
        │  'A' │  ('1', '2', '!')   │
        └──────┴────────────────────┘
          ▲           ▲
   Startzeichen   rest_len = 3
```

Ergebnis:
```
'A' + '1' + '2' + '!'  →  'A12!'
```

Damit ergibt sich:
- **Gesamtlänge des Passworts** = `n`
- **Kombinationen** werden exakt für die Lücke hinter dem Startzeichen erzeugt


---

## Kombinationen berechnen mit `itertools.product`

```python
for kombi in itertools.product(characters, repeat=rest_len):
```

### Mathematischer Hintergrund: **Kartesisches Produkt**

Gegeben ist ein Zeichensatz \( C \) mit \( |C| \) Zeichen.  
Wir suchen alle Kombinationen der Länge \( r \) mit Wiederholung:

### Formel:

\[
|C|^r
\]

Dabei ist:
- \( |C| \): Anzahl der Zeichen im Zeichensatz
- \( r \): Anzahl der zu kombinierenden Stellen (z. B. 3)

---

### Beispiel:

```python
characters = ['a', 'b']
rest_len = 2
```

Ergebnis von `itertools.product(characters, repeat=2)`:

```
('a', 'a')
('a', 'b')
('b', 'a')
('b', 'b')
```

 → 2 Zeichen, 2 Stellen = \( 2^2 = 4 \) Kombinationen

---

## Zusammensetzen des Passworts

```python
password = erster_buchstabe + ''.join(kombi)
```

Beispiel:
```python
erster_buchstabe = 'A'
kombi = ('1', '2', '!')
password = 'A12!'
```

---

## Prüfung mit 7-Zip

```python
if unzip(archiv, password):
    print("Passwort geknackt!")
    return password
```

Wird das Passwort korrekt erkannt (Rückgabewert 0), bricht die Funktion sofort ab.

---

## Ablaufdiagramm (vereinfacht)

```
Start
 │
 │→ Zeichenbereich auswählen (teil_index)
 │
 │→ Für jede Passwortlänge n:
 │     │
 │     └─ Für jeden Startbuchstaben:
 │            │
 │            └─ Erzeuge Kombinationen der restlichen Zeichen
 │                  │
 │                  └─ Teste zusammengesetztes Passwort mit 7z
 │
 └──> Passwort gefunden? → Ja → return
                        → Nein → weiter
```

---

## Fazit

- Die Funktion erzeugt alle möglichen Kombinationen eines Zeichensatzes der Länge `n`
- Sie ist mathematisch exakt berechenbar
- Sie arbeitet effizient durch Teilung des Zeichenraums
- Ideal zur Veranschaulichung von Brute-Force und Kombinatorik

---

Documentation written by: Jose Luis Ocana (GitHub: [0xZorro](https://github.com/0xZorro))  
Last updated: April 2025

<div align="center">
  <img src="brand.png" alt="by 0xZorro" width="120"/>
  <br/>
  <sub>© 2025 0xZorro</sub>
</div>

---

