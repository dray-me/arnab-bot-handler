class User:
    def __init__(self, data):
        self.id = data.get("id")
        self.xp = data.get("xp", 0)
