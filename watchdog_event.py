import os
import json
import subprocess
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from read_json import get_coordinates

def get_coordinates():
    if os.path.exists('my_data.json'):
        with open('my_data.json') as f:
            data = json.load(f)

        coordinates = []
        for feature in data['features']:
            coordinates.append(feature['geometry']['coordinates'])

        os.remove('my_data.json')
        return coordinates
    
    else:
        return None

class MyHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return -1
        elif event.src_path.endswith(".json"):
            time.sleep(1)
            coordinates = get_coordinates() 
            if coordinates != None:
                print(coordinates)
            
            # specify the path to your Python script
            #script_path = "/path/to/your/script.py"
            #subprocess.run(["python", 'watchdog.'])

#if __name__ == "__main__":
event_handler = MyHandler()
observer = Observer()
observer.schedule(event_handler, path='.', recursive=False)
observer.start()
try:
    while True:
        time.sleep(0.9)
except KeyboardInterrupt:
    observer.stop()
observer.join()
