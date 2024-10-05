import os
import pandas as pd

# Bestimme das Verzeichnis, in dem sich das Python-Skript befindet
script_dir = os.path.dirname(os.path.realpath(__file__))

# Lade die ursprüngliche CSV-Datei
file_path = os.path.join(script_dir, 'PlantDB_5335_U0.csv')  # Datei im selben Ordner wie das Skript
df = pd.read_csv(file_path)

# Liste der deutschen Kräuternamen und deren lateinische Namen, einschließlich der neuen Kräuter
herb_list = [
    ("Basilikum", "Ocimum basilicum"),
    ("Petersilie", "Petroselinum crispum"),
    ("Schnittlauch", "Allium schoenoprasum"),
    ("Rosmarin", "Rosmarinus officinalis"),
    ("Thymian", "Thymus vulgaris"),
    ("Koriander", "Coriandrum sativum"),
    ("Dill", "Anethum graveolens"),
    ("Minze", "Mentha"),
    ("Oregano", "Origanum vulgare"),
    ("Estragon", "Artemisia dracunculus"),
    ("Salbei", "Salvia officinalis"),
    ("Lorbeer", "Laurus nobilis"),
    ("Zitronenmelisse", "Melissa officinalis"),
    ("Majoran", "Origanum majorana"),
    ("Fenchelkraut", "Foeniculum vulgare"),
    ("Kerbel", "Anthriscus cerefolium"),
    ("Bärlauch", "Allium ursinum"),
    ("Zitronenthymian", "Thymus citriodorus"),
    ("Lovage (Liebstöckel)", "Levisticum officinale"),
    ("Apfelminze", "Mentha suaveolens"),
    ("Anisysop", "Agastache foeniculum"),
    ("Giersch", "Aegopodium podagraria"),
    ("Pfefferminze", "Mentha piperita"),
    ("Schafgarbe", "Achillea millefolium"),
    ("Rucola", "Eruca sativa"),
    ("Sauerampfer", "Rumex acetosa"),
    ("Borretsch", "Borago officinalis"),
    ("Pimpernelle", "Sanguisorba minor"),
    ("Kresse", "Lepidium sativum")
]

# Erstelle ein DataFrame, um die gefundenen Kräuter zu speichern
matched_herbs_df = pd.DataFrame(columns=df.columns)

# Suche nach den Kräutern anhand des lateinischen Namens
for german, latin in herb_list:
    matches = df[df['display_pid'].str.contains(latin, case=False, na=False)]
    if not matches.empty:
        matches['German'] = german
        matched_herbs_df = pd.concat([matched_herbs_df, matches])

# Speicher die gefundenen Kräuter in einer neuen CSV-Datei im selben Ordner wie das Skript
final_herb_file_path = os.path.join(script_dir, 'final_kitchen_herbs.csv')
matched_herbs_df.to_csv(final_herb_file_path, index=False)

print(f"Die Datei wurde gespeichert unter: {final_herb_file_path}")
