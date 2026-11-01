# Situs-Anki – Arbeitsablauf (für Claude)

Das Deck entsteht über mehrere Sitzungen. Alles Nötige liegt in diesem Ordner. Eine neue Sitzung braucht kein Vorwissen.

## Einstieg in jede Sitzung
1. Repo holen bzw. aktualisieren: `gh repo clone kilianpanzenboeck1/situs-kreuztrainer` (oder `git pull`), dann `cd situs-kreuztrainer/anki`.
2. `pip install --break-system-packages -q genanki`
3. `python3 tools/status.py` → zeigt das nächste Kapitel.
4. `STYLE.md` lesen: die freigegebene Spezifikation, die verbindlich ist. `config.json` enthält die Menge, die Reihenfolge und die Etappen.

## Ein Kapitel bearbeiten
1. `python3 tools/prepare.py <CH>` → `work/<CH>.md` mit den Originalfragen in Batches (12 Originale ≈ 24 Karten).
2. Batch für Batch schreiben (kompakt als `work/<CH>_bN.src.json` → `python3 tools/compile.py` → oder direkt als JSON-Liste nach `work/<CH>_bN.json`, dann `python3 tools/append.py <CH> work/<CH>_bN.json`):
   - Karten in `cards/<CH>.json` anhängen. Das Format steht im Kopf von `tools/validate.py`. Status bleibt `"draft"`.
   - Pro Originalfrage `variants_per_question` Varianten, mit unterschiedlichen Typen.
   - IDs: `V-<src>-1`, `V-<src>-2`. Bestehende IDs nie umbenennen, denn die GUIDs hängen daran.
   - Teil D: Die Lösung des Professors ist verbindlich. Bei ⚠-Fragen wird der strittige Punkt nicht variiert.
3. Nach jedem Batch `python3 tools/validate.py <CH>` ausführen und die Fehler beheben.
4. Fachliche Selbstprüfung pro Batch:
   - Ist jede Lösung eindeutig?
   - Ist jeder Distraktor wirklich falsch?
   - Stimmt nichts davon im Widerspruch zum Original oder zum Prof?
   - Lateinische Schreibweise korrekt?
   - Lösungen über A–E gestreut?
   Unsichere Karte → umbauen oder streichen, nie raten.
5. Zwischenstand committen: `git add -A && git commit -m "Anki <CH> Batch n"` und pushen. So geht bei einem Abbruch nichts verloren.

## Etappe abschließen
1. Alle Kapitel der Etappe validieren. Dann den Status in `cards/<CH>.json` auf `"review"` setzen.
2. `python3 tools/build.py` → `dist/Situs-Anki.apkg`. Die Datei ist kumulativ und enthält alle Kapitel ab `review`. Stabile GUIDs sorgen dafür, dass ein erneuter Import aktualisiert statt dupliziert.
3. `python3 tools/status.py`, dann committen und pushen.
4. An Kilian liefern:
   - die `.apkg` per SendUserFile
   - eine Kopie in seinen Ordner `…/DPU - 3. Semester/Tamas - Situs/Anki/`, wenn der Computer verbunden ist
   - eine kurze Nachricht: wie viele Karten, welche Kapitel, und was ihm beim Prüfen auffallen sollte
5. Auf Feedback warten:
   - Korrekturen fließen in `cards/*.json` und, falls nötig, in `STYLE.md` ein.
   - Nach seiner Freigabe den Status auf `"released"` setzen. Dann kommt die nächste Etappe.

## Regeln
- Lange Etappen in mehreren Sitzungen erledigen. Nach jedem Batch committen, damit jede Sitzung genau dort weitermacht.
- `source/quiz.json` ist eine Kopie aus dem Kreuztrainer und wird nicht bearbeitet. Neue Strittigkeiten kommen in `flags.json`.
- Bilder liegen in `../img/` (Namen wie in `quiz.json` → `img`). Neue Bildvarianten verwenden nur diese Bilder.
