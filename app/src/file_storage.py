import json


class EventFileManager:
  def __init__(self):
    self.FILE_PATH = "event.json"
    
  def read_events_from_file(self):
    try :
      with open(self.FILE_PATH, "r") as file:
        return json.load(file)
    except:
      print("File not found")
      return []

  def write_events_to_file(self, events):
    with open(self.FILE_PATH, "w") as file:
      json.dump(events, file)
