# ============================================
# zZipCracker – Brute-Force ZIP-Knacker-Tool
# ============================================
# Autor: Jose Luis Ocana (GitHub: 0xZorro)
# Erstellt: 21.04.2025
# Beschreibung: Ein leichtgewichtiges Python-Tool zum demonstrativen Durchprobieren
#               von Passwörtern geschützter ZIP-Dateien. Entwickelt zu Lern- und 
#               Sensibilisierungszwecken. Unterstützt automatische Aufteilung der 
#               Arbeitslast auf parallele Prozesse.
#
# Hinweis: Kommentare sind aktuell auf Deutsch. Eine englische Version ist geplant,
#          um das Projekt international verständlicher zu machen.
#
# Lizenz: MIT-Lizenz (siehe LICENSE-Datei für Details)
# Version: 1.0
# Repository: https://github.com/0xZorro/zZipCracker
# ============================================

# ============================================
# zZipCracker – Brute-Force ZIP Cracking Tool
# ============================================
# Author: Jose Luis Ocana (GitHub: 0xZorro)
# Created:   2025-04-21
# Description: A lightweight Python tool to demonstrate brute-force attacks on
#              password-protected ZIP files. Developed for learning and 
#              awareness purposes. Supports automatic workload splitting 
#              across parallel processes.
#
# Note: Comments are currently in German. An English version is planned to 
#       make the project more accessible to international users.
#
# License: MIT License (see LICENSE file for details)
# Version: 1.0
# Repository: https://github.com/0xZorro/zZipCracker
# ============================================

from argparse import ArgumentParser
from subprocess import Popen, PIPE, STDOUT,  TimeoutExpired
from tqdm import tqdm
import itertools
import string
import os

# ---------- Zeichenliste vorbereiten ----------
all_chars = string.ascii_letters + string.digits + string.punctuation
filtered_chars = []

for c in all_chars:
    if c != '"':    # Entferne das Zeichen ", da es zu Problemen bei der Übergabe an die Kommandozeile führt
        filtered_chars.append(c)

characters = ''.join(filtered_chars)
  
# ---------- Funktion zum Testen eines Passworts ----------
def unzip(archiv, pwd):
    #print(f"Teste Passwort: {pwd}")  # <--- nur zur Kontrolle
    sCmd = f"7z x \"{archiv}\" -p\"{pwd}\" -y"    
    try:
        prozess = Popen(sCmd, stdout=PIPE, stderr=STDOUT)
        stdout, _ = prozess.communicate(timeout=1)  
        return prozess.returncode == 0 # Rückgabewert prüfen – 0 bedeutet, dass das Entpacken erfolgreich war
    except TimeoutExpired:
        #print(f"[TIMEOUT] bei Passwort: {pwd}")
        prozess.kill()
        return False
    
# ---------- Diese Funktion führt den einzelnen Prozess aus ----------#
def crack_zip(archiv, min_len=1, max_len=10, teil_index=None):
    # Hier wird die Zeichenliste auf 4 Prozesse aufgeteilt
    # Hinweis: Eine Erweiterung auf mehr Prozesse erfordert Anpassungen im gesamten Ablauf
    anzahl_prozesse = 4     
    zeichenlaenge = len(characters)
    bereichsgroesse = zeichenlaenge // anzahl_prozesse
    teile = []
    start = 0
    for i in range(anzahl_prozesse):
        # Letzter Bereich nimmt den Rest mit
        if i == anzahl_prozesse - 1:
            ende = zeichenlaenge
        else:
            ende = start + bereichsgroesse

        teil = characters[start:ende]
        teile.append(teil)
        start = ende

   # Bestimme den Teilbereich der Zeichen, den dieser Prozess bearbeiten soll
    startzeichen = teile[teil_index]

    for n in tqdm(range(min_len, max_len + 1), total=max_len - min_len + 1, desc="Passwortlänge", position=0, leave=True):
        rest_len = n - 1
        # Für jedes Startzeichen in diesem Bereich alle möglichen Kombinationen testen
        for erster_buchstabe in startzeichen:
            total_kombis = len(characters) ** rest_len
            for kombi in tqdm(itertools.product(characters, repeat=rest_len),total=total_kombis,desc=f"{erster_buchstabe}xxxx",leave=False):
                password = erster_buchstabe + ''.join(kombi)
                print(f"\rPasswort: {password}", end="", flush=True)
                if unzip(archiv, password):
                    print(f"\nPasswort geknackt: {password}")
                    return password              
    print("Passwort wurde nicht gefunden!")


def main():
    parser = ArgumentParser(description = "ZIP Cracker mit Brute Force Attacke")
    parser.add_argument("archiv", help="Pfad zur Zip-Datei")
    parser.add_argument("min", type=int, help="Minimale Passwortlänge")
    parser.add_argument("max", type=int, help="Maximale Passwortlänge")
    parser.add_argument("teil_index", nargs="?", type=int, help="Index des Zeichenbereichs (für CMD-Prozesse)")  #Dieses Argument ist optional
    args = parser.parse_args() 
    # Im Normalfall wird das Argument teil_index nicht gesetzt.
    # Es dient nur dazu, gezielt einen bestimmten Zeichenbereich manuell zu testen.


    # Wird nur ausgeführt, wenn teil_index gesetzt ist – nützlich zum gezielten Testen eines Bereichs
    # in der Regel aber wird es auf none gelassen und das Programm startet dann automatisch vier Prozesse
    if args.teil_index is not None:
        crack_zip(args.archiv, args.min, args.max, teil_index=args.teil_index)
        return

   # Regelfall: Starte automatisch 4 CMD-Fenster (einen Prozess pro Zeichenbereich)
    try:
        anzahl_teile = 4
        for teil_index in range(anzahl_teile):
            cmd = f'start cmd /k python "{__file__}" "{args.archiv}" {args.min} {args.max} "{teil_index}"'
            os.system(cmd)

    except KeyboardInterrupt:
        print("\n Vorgang manuell abgebrochen (Strg + C).")


if __name__ == "__main__":
    main()
