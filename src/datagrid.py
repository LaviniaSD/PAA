
class DataGrid():
    def __init__(self):
        self.list = []

class Event():
    def __init__(self, dict = None, **kwargs):
        if dict == None: dict = kwargs
        
        self.id = dict["id"]
        self.owner_id = dict["owner_id"]
        self.creation_date = dict["creation_date"]
        self.count = dict["count"]
        self.name = dict["name"]
        self.content = dict["content"]
    
if __name__ == "__main__":
    pass
        