MAX_POST_LENGTH = 280  # X-Limit, bei Bedarf anpassen

def beautify_text(text):
    """
    Fügt Emojis und Hashtags hinzu und teilt lange Meldungen in mehrere Teile.
    Gibt eine Liste von Strings zurück.
    """
    base_tags = "#Berlin #Verkehr"
    emojis = ""

    text_lower = text.lower()
    if "sperrung" in text_lower or "gesperrt" in text_lower:
        emojis += "⛔🚧 "
    elif "bau" in text_lower:
        emojis += "🚧 "
    elif "störung" in text_lower or "gefähr" in text_lower:
        emojis += "⚠️ "
    elif "verspätung" in text_lower:
        emojis += "⏰ "

    hashtags = [base_tags]
    if "U-Bahn" in text or "S-Bahn" in text:
        hashtags.append("#ÖPNV")
    if "Bus" in text:
        hashtags.append("#Bus")
    if "Autobahn" in text or "A100" in text:
        hashtags.append("#Autobahn")

    # Kombination von Emojis + Text + Hashtags
    final_text = f"{emojis}{text}\n\n{' '.join(hashtags)}"

    # Thread-Logik: Text teilen, falls zu lang
    if len(final_text) <= MAX_POST_LENGTH:
        return [final_text]

    # Teilt nach Zeilen, um Threads zu erstellen
    parts = []
    lines = final_text.split("\n")
    current = ""
    for line in lines:
        if len(current) + len(line) + 1 > MAX_POST_LENGTH:
            parts.append(current.strip())
            current = line
        else:
            current += "\n" + line
    if current.strip():
        parts.append(current.strip())

    return parts

