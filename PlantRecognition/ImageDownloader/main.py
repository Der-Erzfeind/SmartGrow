from dotenv import load_dotenv
import serpapi
import csv
import os
import requests


def download_images(save_dir, img_link, file_name, timeout=60):
    # ueberpruefe ob Speicherpfad existent wenn nicht erstelle ihn
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    if not file_name.endswith('.jpg'):
        file_name += '.jpg'

    # Lege vollstaendigen Pfad an
    img_path = os.path.join(save_dir, file_name)

    # Herunterladen und abspeichern des Bildes
    try:
        response = requests.get(img_link, timeout=timeout)
        with open(img_path, 'wb') as img_file:
            img_file.write(response.content)

        print(f'Bild erfolgreich gespeichert unter - "{img_path}"')
    except Exception as e:
        print(f'Fehler beim Herunterladen und Speichern: {str(e)}')


load_dotenv()

api_key = os.getenv('SERPAPI_KEY')
client = serpapi.Client(api_key=api_key)

desired_images = 2

image_count = 0

with open('sources.csv', 'w', newline='', encoding='utf-8') as csvfile:
    csv_writer = csv.writer(csvfile, delimiter=';')
    csv_writer.writerow(['Titel', 'Quelle', 'Website-Link', 'Bild-Link'])

    page_number = 0

    while image_count < desired_images:
        results = client.search({
            'engine': 'google_images',
            'tbm': 'isch',
            'q': 'Petersilie Pflanze',
            'gl': 'de',
            'ijn': page_number,
            'tbs': 'il:cl'
        })

        if 'images_results' not in results:
            break                           # Beende Suche wenn keine Bilder mehr verfuegbar

        for image_result in results['images_results']:
            title = image_result['title'] if 'title' in image_result else ''
            source = image_result['source'] if 'source' in image_result else ''
            pic_link = image_result['original'] if 'original' in image_result else ''
            web_link = image_result['link'] if 'link' in image_result else ''
            csv_writer.writerow([title, source, web_link, pic_link])

            # Download
            if 'original' in image_result:
                download_images('C:\\DataSets\\scrapedIMG', image_result['original'], str(image_count + 1))

            image_count += 1

            if image_count >= desired_images:
                break

        page_number += 1

if image_count == desired_images:
    print('Done writing to CSV file.')
elif image_count > desired_images:
    print('Mehr Bilder als gewuenscht')
else:
    print('Weniger Bilder als gewuenscht')

# Herunterladen der Bilder
# if 'images_results' not in results:
#     print('Error keine Bilder')
# else:
#     img_name = 0
#
#     for result in results['images_results']:
#
#         if img_name == desired_images:
#             break
#
#         download_images('C:\\DataSets\\scrapedIMG\\Basil', result['original'], str(img_name + 1))
#         img_name += 1
