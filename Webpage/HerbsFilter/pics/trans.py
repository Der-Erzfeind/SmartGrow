import os

# Wörterbuch für die Übersetzungen
translation_dict = {
    "anethum graveolens": "Dill",
    "artemisia dracunculus": "Tarragon",
    "borago officinalis": "Borage",
    "chives": "Chives",  # bereits auf Englisch
    "coriandrum sativum": "Cilantro",
    "eruca sativa": "Arugula",
    "foeniculum vulgare": "Fennel",
    "laurus nobilis": "Bay Leaf",
    "levisticum officinale": "Lovage",
    "melissa officinalis": "Lemon Balm",
    "ocimum basilicum": "Basil",
    "origanum majorana": "Marjoram",
    "origanum vulgare": "Oregano",
    "petroselinum crispum": "Parsley",
    "rosmarinus officinalis": "Rosemary",
    "rumex acetosa": "Sorrel",
    "salvia officinalis": "Sage",
    "thymus vulgaris": "Thyme",
    "wild garlic": "Wild Garlic"  # bereits auf Englisch
}

# Funktion zum Umbenennen der Dateien
def rename_photos(pic):
    for filename in os.listdir(pic):
        # Dateiname und Erweiterung trennen
        name, ext = os.path.splitext(filename)

        # In Kleinbuchstaben umwandeln, um Konsistenz zu gewährleisten
        name_lower = name.lower()

        # Neuen Namen basierend auf dem Wörterbuch finden
        new_name = translation_dict.get(name_lower, name) + ext

        # Alte und neue Dateipfade erstellen
        old_file = os.path.join(directory, filename)
        new_file = os.path.join(directory, new_name)

        # Datei umbenennen
        os.rename(old_file, new_file)
        print(f"'{filename}' wurde in '{new_name}' umbenannt")

# Verzeichnis mit den Fotos
directory = "pic"  # Passe diesen Pfad an

rename_photos(directory)
