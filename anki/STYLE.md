# Situs-Anki – Spezifikation (Tamás-Stil)

Status: Entwurf, wartet auf Freigabe durch Kilian. Änderungen hier eintragen, bevor die nächste Etappe startet.

## Ziel
Anki-Deck aus der Situs-Fragensammlung (Teile A–D, 822 Fragen). Kilian kann alle Originalfragen sicher – das Deck besteht vor allem aus **neuen Alternativfragen**, die denselben Stoff aus anderem Blickwinkel prüfen.

## Grundlage & Vorrang
- Nur Inhalte aus der Sammlung (Fragenkatalog 2024, IMPP-Seminarfolien, Altfragen, Katalog Dr. Sebestény) plus Standardlehrbuch (Prometheus, Sobotta, Schiebler).
- Lösungen von Dr. Sebestény (Teil D) sind verbindlich. Keine Variante darf ihnen widersprechen.
- Fragen mit `notes` / `src: korr` oder in `flags.json` → Rückseite bekommt „⚠“-Hinweis; aus dem strittigen Punkt wird keine neue Frage gebaut.
- Keine erfundenen Fakten. Unsicheres Detail → nicht abfragen.

## Tamás-Stil
- Single Choice, 5 Optionen A–E, genau eine richtig.
- Stämme: „Welche Aussage trifft zu / trifft nicht zu?“, unvollständiger Satz („Die Bruchpforte … liegt stets …“), „Welche Struktur …?“, „Die markierte Struktur in der Abbildung …“.
- Oft ein einleitender klinischer/funktioneller Satz (IMPP-artig).
- Lateinische Nomenklatur wie im Katalog (A., V., N., Lig., M.).
- Plausible Distraktoren: Nachbarstrukturen, verwechselbare Gefäße/Nerven, Seitenverwechslung, falsche Wirbelhöhe. Nichts Absurdes.
- Keine doppelten Optionen, keine Synonyme als zwei Optionen. Richtige Antwort über A–E streuen.

## Varianten-Typen (pro Originalfrage `variants_per_question`, gemischt)
- `umkehrung` – zu ↔ nicht zu, Antwort wird Frage.
- `perspektive` – Lage, Versorgung (arteriell/venös/Lymphe/Nerv), Herkunft, Funktion, Klinik derselben Struktur.
- `nachbarschaft` – „Welche Struktur liegt unmittelbar dorsal/medial von …?“
- `klinik` – 1–2 Sätze Vignette, dann anatomische Frage.
- `bild` – neue Frage zur vorhandenen Abbildung (anderer Buchstabe/andere Eigenschaft). Keine neuen Bilder.

## Kartenaufbau
- Vorderseite: Stamm, A–E, ggf. Abbildung.
- Rückseite: richtige Antwort · Erklärung (2–4 Sätze) · je Distraktor ein Satz, warum falsch · Eselsbrücke (optional) · Quelle (Teil/Kapitel/Nr.) · ggf. ⚠-Hinweis.
- Originalfragen in eigenem Unterstapel `… ::Original` (aussetzbar).

## Beispiel
> Das Herzskelett trennt Vorhof- und Kammermyokard. Welche Aussage trifft **nicht** zu?
> A Der Anulus fibrosus dexter umrahmt das Ostium atrioventriculare dextrum.
> B Das His-Bündel durchbricht das Herzskelett im Trigonum fibrosum dextrum.
> C Der Anulus fibrosus sinister umrahmt die Mitralklappe.
> D Das Herzskelett dient den Segelklappen als Ansatz.
> E Das Herzskelett leitet die Erregung von den Vorhöfen auf die Kammern weiter.
> Lösung E – das Herzskelett isoliert elektrisch; Überleitung nur über das His-Bündel.
