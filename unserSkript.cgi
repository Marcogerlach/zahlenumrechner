#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cgi
import cgitb
import html
import sys
import os
import urllib.parse

# Aktiviere CGI-Debugging
cgitb.enable()

# Setze die richtige Kodierung für Windows
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except:
        pass

def umrechnen_von_dezimal(zahl, ziel_basis):
    """Rechnet eine Dezimalzahl in die gewünschte Basis um."""
    if zahl == 0:
        return "0"
    
    ergebnis = ""
    while zahl > 0:
        rest = zahl % ziel_basis
        if rest > 9:
            digit = chr(rest - 10 + ord('A'))
        else:
            digit = str(rest)
        ergebnis = digit + ergebnis
        zahl //= ziel_basis
    
    return ergebnis

def umrechnen_zu_dezimal(zahl, von_basis):
    """Rechnet eine Zahl aus einer beliebigen Basis in Dezimal um."""
    if zahl.startswith("-"):
        return -1
    
    dezimal = 0
    for i, c in enumerate(zahl.upper()):
        if c.isdigit():
            wert = int(c)
        elif 'A' <= c <= 'F':
            wert = ord(c) - ord('A') + 10
        else:
            return -1
        
        if wert >= von_basis:
            return -1
        
        dezimal = dezimal * von_basis + wert
    
    return dezimal

def umrechnen_allgemein(zahl, von_basis, ziel_basis):
    """Hauptfunktion für die Umrechnung zwischen beliebigen Zahlensystemen."""
    if von_basis < 2 or von_basis > 16 or ziel_basis < 2 or ziel_basis > 16:
        return None
    
    if von_basis == 10:
        try:
            dezimal_zahl = int(zahl)
            if dezimal_zahl < 0:
                return None
            return umrechnen_von_dezimal(dezimal_zahl, ziel_basis)
        except ValueError:
            return None
    else:
        dezimal = umrechnen_zu_dezimal(zahl, von_basis)
        if dezimal == -1:
            return None
        return umrechnen_von_dezimal(dezimal, ziel_basis)

def get_basis_name(basis):
    """Gibt den Namen der Basis zurück."""
    names = {
        2: "Binär",
        8: "Oktal", 
        10: "Dezimal",
        16: "Hexadezimal"
    }
    return names.get(basis, f"Basis {basis}")

def print_result_page(zahl, von_basis, ziel_basis, ergebnis, error=False):
    """Druckt die Ergebnisseite."""
    print("Content-Type: text/html; charset=utf-8")
    print()
    
    error_class = " error" if error else ""
    result_title = "❌ Fehler" if error else "✅ Ergebnis"
    
    print(f"""<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Zahlenumrechner - {result_title}</title>
    <link rel="stylesheet" href="unserStyle.css">
</head>
<body>
    <div class="container">
        <header>
            <h1>🔢 Zahlenumrechner</h1>
            <p>Ergebnis der Umrechnung</p>
        </header>
        
        <main>
            <div class="result-section{error_class}">
                <h3>{result_title}</h3>""")
    
    if not error:
        print(f"""
                <div style="margin: 20px 0;">
                    <strong>Eingabe:</strong> {html.escape(zahl)} ({get_basis_name(von_basis)})<br>
                    <strong>Umrechnung:</strong> {get_basis_name(von_basis)} → {get_basis_name(ziel_basis)}
                </div>
                <div class="result-value">{html.escape(ergebnis)}</div>
                <p>Die Zahl <strong>{html.escape(zahl)}</strong> in {get_basis_name(von_basis)} entspricht <strong>{html.escape(ergebnis)}</strong> in {get_basis_name(ziel_basis)}.</p>""")
    else:
        print(f"""
                <div class="result-value">{html.escape(ergebnis)}</div>
                <p>Bitte überprüfen Sie Ihre Eingabe und versuchen Sie es erneut.</p>""")
    
    print("""
                <a href="unsereSeite.html" class="back-btn">← Zurück zum Umrechner</a>
            </div>
            
            <div class="info-section">
                <h3>Hinweise:</h3>
                <ul>
                    <li><strong>Binär (Basis 2):</strong> Nur die Ziffern 0 und 1 sind erlaubt</li>
                    <li><strong>Oktal (Basis 8):</strong> Ziffern von 0 bis 7 sind erlaubt</li>
                    <li><strong>Dezimal (Basis 10):</strong> Ziffern von 0 bis 9 sind erlaubt</li>
                    <li><strong>Hexadezimal (Basis 16):</strong> Ziffern 0-9 und Buchstaben A-F sind erlaubt</li>
                </ul>
            </div>
        </main>
        
        <footer>
            <p>&copy; 2025 Zahlenumrechner | Made with ❤️ in Python</p>
        </footer>
    </div>
</body>
</html>""")

def main():
    """Hauptfunktion des CGI-Skripts."""
    try:
        # Hole Daten aus GET-Parameter (Query String) oder POST
        if os.environ.get('REQUEST_METHOD') == 'POST':
            # POST-Daten lesen
            form = cgi.FieldStorage()
            zahl = form.getvalue("zahl", "").strip()
            von_basis_str = form.getvalue("von_basis", "")
            ziel_basis_str = form.getvalue("ziel_basis", "")
        else:
            # GET-Parameter aus QUERY_STRING lesen
            query_string = os.environ.get('QUERY_STRING', '')
            params = urllib.parse.parse_qs(query_string)
            zahl = params.get('zahl', [''])[0].strip()
            von_basis_str = params.get('von_basis', [''])[0]
            ziel_basis_str = params.get('ziel_basis', [''])[0]
        
        # Validiere die Eingaben
        if not zahl:
            print_result_page("", 0, 0, "Bitte geben Sie eine Zahl ein!", error=True)
            return
        
        try:
            von_basis = int(von_basis_str)
            ziel_basis = int(ziel_basis_str)
        except (ValueError, TypeError):
            print_result_page(zahl, 0, 0, "Ungültige Basis ausgewählt!", error=True)
            return
        
        # Führe die Umrechnung durch
        ergebnis = umrechnen_allgemein(zahl, von_basis, ziel_basis)
        
        if ergebnis is None:
            error_msg = f"Ungültige Eingabe! Die Zahl '{zahl}' ist nicht gültig für {get_basis_name(von_basis)}."
            print_result_page(zahl, von_basis, ziel_basis, error_msg, error=True)
        else:
            print_result_page(zahl, von_basis, ziel_basis, ergebnis, error=False)
            
    except Exception as e:
        # Fehlerbehandlung
        print("Content-Type: text/html; charset=utf-8")
        print()
        print(f"""<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <title>Fehler - Zahlenumrechner</title>
    <link rel="stylesheet" href="unserStyle.css">
</head>
<body>
    <div class="container">
        <header>
            <h1>❌ Systemfehler</h1>
        </header>
        <main>
            <div class="result-section error">
                <h3>Ein unerwarteter Fehler ist aufgetreten</h3>
                <div class="result-value">Fehler: {html.escape(str(e))}</div>
                <a href="unsereSeite.html" class="back-btn">← Zurück zum Umrechner</a>
            </div>
        </main>
    </div>
</body>
</html>""")

if __name__ == "__main__":
    main()