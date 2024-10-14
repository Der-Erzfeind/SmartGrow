# Testskript zur Kommunikation zwischen Server und Bildanalyse

# imports
import os

image_pipe_path = "/tmp/image_pipe"
result_pipe_path = "/tmp/result_pipe"

def processing_dummy(image_path):
    print("Image Path:", image_path)
    return("Result")

while True:
    with open(image_pipe_path, "r") as fifo:
        image_path = fifo.read().strip()

    result = processing_dummy(image_path)

    with open(result_pipe_path, "w") as fifo:
        fifo.write(str(result))

