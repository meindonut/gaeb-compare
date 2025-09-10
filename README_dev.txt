commands for manual installation:

python -m venv .venv
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process -Force
.venv/Scripts/activate.ps1
pip install gaeb-parser
pip install pyside6             # for gui
pip install pandas              # for data handling
pip install openpyxl            # to import excel files
pip install diff-match-patch    # for text comparison
pip install nltk                # for tokeniation
pip install beautifulsoup4      # for xml import lvs
pip install lxml                # for bs4 to import xml files
pip install scikit-learn        # for file comparision
pip install pyinstaller         # for dist
pip install pytest              # for testing


Bugs:
- 

Schnelle wichtige To-Dos:
- 

Fehlerhafte Tests:
- Laden / Speicher des LV schlägt fehl --> keine richtigen Datenbank

Wichtige To-Dos:
- Positionsinformationen optional in Vergleich mit reinnehmen (wichtig für Vergleiche mit Mutter LV)
- Scrollen verhindern im Import Fenster
- Integrationstest

Mögliche Bugs / grob falsche Verwendung:
- Verhindern, dass beim Import zwei gleiche Kurztexte zum überschreiben einer Datei führen (normalerweise sollten keine zwei gleichen Kurztexte in einem Untergewerk vorkommen)
- Verhindern, dass ein ganzes Verzeichnes überschrieben wird oder eine Datei doppelt importiert wird

Komfort To-Dos:
- Import Fenster übersichtlicher gestalten z.B. mit Tree View
- Prozentzahl Ähnlichkeit mit Farbe hinterlegen
- Prüfen der importierenden xml Datei mit xsd Datei
- Importherkunft mit Textformatierung auswählen im Importprozess ?
- All-in-one Vergleich mit Markierung relevanter Textpassagen
- Abkürzungen für Gewerke in Importprozess abfragen
- Suche
    - Anzahl in Datei bei Datenbank suche
    - Markierung der gefundenen Wörter 
- TreeView farbliche Hinterlegung der Ebenen

Code aufräumen und Vereinfachen To-Dos:
- window_project auf relative pfade umstellen und datei operationen zum file_manager auslagern
- Datenbank Felder einheitlich definieren
- requirements datei erstellen und ps dateien für oben erstellen
- window_project function load_data_to_right_of_index integrieren

Erstellungs To-Dos:
- Textergänzungen müssen separat gehandelt werden -> 'ComplTSA' 'ComplTSB' 'TextComplement'
- Github Integration für Versionierung
- Ausgabe
    - Angabe was exportiert werden soll (Fenster mit Häkchen?)
    - Excel Export -> wie Textergänzungen?
    - XML Export -> komplex

Großer Ausblick zum automatisierten Ausschreibungstool:
- Untestützende Auswahl an passenden Positionen mithilfe:
    - Auswahl von Projektparametern: Name, Neubau/Umbau, Umbaukonzept
    - Führung entlang von Anlagenteilen mit Übersichts-Plänen: MS, GS, NS, NP, EP
- Anzeige und Bearbeitung relevanter Parameter in Positionen mitlhilfe:
    - Verknüpfung zu Plan mit Hinweisen
    - DropDown mitVorschlägen
    - Automatische Verknüpfung zu alten Projekten