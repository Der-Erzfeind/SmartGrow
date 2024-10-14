# Testskript zur Kommunikation zwsischen Server und Bildanalyse

# imports
import os
import json

# start
image_pipe_path = "/tmp/image_pipe"
image_path = "/home/smartgrow/Server/basilikum.jpg"

# In die Pipe schreiben
with open(image_pipe_path, 'w') as fifo:
    fifo.write(image_path)

result_pipe_path = '/tmp/result_pipe'

# Ergebnis aus der Pipe lesen
with open(result_pipe_path, 'r') as fifo:
    result_json = fifo.read().strip()
    
result_data = json.loads(result_json)
predicted_class = result_data["predicted_class"]
confidence = result_data["confidence"]

print(f'Vorhergesagte Klasse: {predicted_class} (Confidence: {confidence})')

