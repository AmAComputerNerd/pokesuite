import requests

class PokeMove():
    def __init__(self, name):
        name = name.lower().replace(" ", "-")
        self.url = f"https://pokeapi.co/api/v2/move/{name}"
        request = requests.get(self.url)
        request.raise_for_status()
        self.data = request.json()

    def __init__(self, url):
        self.url = url
        request = requests.get(self.url)
        request.raise_for_status()
        self.data = request.json()

    def __raw_data(self):
        '''
        Retrieve the raw data from the API.
        This data is always in JSON format, and should resemble that of the PokeAPI Move JSON formatting.
        Arguments:
            None
        Returns:
            The raw data from the API.
        '''
        return self.data

    def get_name(self):
        return self.data["name"]
    
    def get_url(self):
        return self.url

    def get_data(self):
        return self.data

    def get_id(self):
        return self.data["id"]

    def get_type(self):
        return self.data["type"]["name"]

    def get_power(self):
        return self.data["power"]

    def get_pp(self):
        return self.data["pp"]

    def get_accuracy(self):
        return self.data["accuracy"]

    def get_priority(self):
        return self.data["priority"]

    def get_damage_class(self):
        return self.data["damage_class"]["name"]

    def get_effect_chance(self):
        return self.data["effect_chance"]
    
    def get_effect_entries(self):
        return self.data["effect_entries"]

    def get_effect_entry(self, language):
        for entry in self.data["effect_entries"]:
            if entry["language"]["name"] == language:
                return entry["effect"]
        return None