import toml
from .logging_utils import log_warning

class HumanConfig():
    def __init__(self, path):
        self.dict = self.load_human_config(path)
        self.used_indices = [int(key.replace("human", "")) for key in self.dict.keys()]

    def load_human_config(self, path):
        try:
            with open(path, "r") as f:
                human_config = toml.load(f)
                return human_config

        except FileNotFoundError:
            log_warning(f"Human Config file {path} not found.")
    
    def save_human_config(self, path):
        with open(path, 'w') as f:
            toml.dump(self.dict, f)
            print(f"Config file was saved to {path}.")
            
    def __len__(self):
        return len(self.dict)
    
    def get_newID(self):
        new_ID = 0
        while True:
            if new_ID not in self.used_indices:
                return new_ID
            new_ID += 1

    def newID_init(self):
        newHuman_ID = self.get_newID()
        self.used_indices.append(newHuman_ID)
        newHuman_name = f"human{newHuman_ID}"
        
        self.dict[newHuman_name] = {}
        self.dict[newHuman_name]["trajectories"] = None
        self.dict[newHuman_name]["traj_start"] = None
        self.dict[newHuman_name]["human_context"] = None
        
        return newHuman_ID
    
    def delete_ID(self, humanID):
        self.used_indices.remove(humanID)
        self.dict.pop(f"human{humanID}")

    def get_element(self, humanID, elementName):
        return self.dict[f"human{humanID}"][elementName]

    def set_element(self, humanID, elementName, value):
        self.dict[f"human{humanID}"][elementName] = value
