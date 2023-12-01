import requests
from libraries.data_objects.PokeData import PokeData

class PokeAbilityData():
    '''
    The PokeAbilityData class holds default values for a PokeAbility's properties. It is used to retrieve information about an ability, such as its effects.
    '''

    def __init__(self, name : str):
        name = name.lower().replace(" ", "-")
        self.url = f"https://pokeapi.co/api/v2/ability/{name}"
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

        This data is always in JSON format, and should resemble that of the PokeAPI Ability JSON formatting.
        
        Arguments:
            None
        Returns:
            The raw data from the API.
        '''
        return self.data

    def __find_language(self, language : str, data : dict):
        '''
        Retrieve a specific language from a list of multiple language entries.

        This function should work with any dictionary as long as the dictionary contains a "language" key, and the value of that key is a dictionary containing a "name" key.

        Arguments:
            language: The language to search for.
            data: The data to search through.
        Returns:
            The dictionary containing the language.
        '''
        for entry in data:
            if entry["language"]["name"] == language:
                return entry
        # no language found, return english
        return self.__find_language("en", data)

    def get_internal_name(self):
        '''
        Retrieve the internal name of this ability.

        This is used to refer to the ability internally, without spaces or special characters.

        Arguments:
            None
        Returns:
            The name of the ability.
        '''
        return self.data["name"]

    def get_id(self) -> int:
        '''
        Retrieve the ID of this ability.

        The ID of the ability is retrieved using the PokeAPI.

        Arguments:
            None
        Returns:
            The ID of the ability.
        '''
        return self.data.get_id()

    def get_name(self, lan : str = "en") -> str:
        '''
        Retrieve the name of this ability.

        The name of the ability is retrieved using the PokeAPI.

        Arguments:
            None
        Returns:
            The name of the ability.
        '''
        return self.__find_language(lan, self.data["names"])["name"]

    def get_description(self) -> str:
        '''
        Retrieve the description of this ability.

        The description of the ability is retrieved using the PokeAPI.

        Arguments:
            None
        Returns:
            The description of the ability.
        '''
        return self.__find_language("en", self.data["effect_entries"])["effect"]

    def get_short_description(self) -> str:
        '''
        Retrieve the short description of this ability.

        The short description of the ability is retrieved using the PokeAPI.

        Arguments:
            None
        Returns:
            The short description of the ability.
        '''
        return self.__find_language("en", self.data["effect_entries"])["short_effect"]

    def get_pokemon(self) -> list:
        '''
        Retrieve a list of Pokemon that can have this ability.

        The list of Pokemon is retrieved using the PokeAPI.

        Arguments:
            None
        Returns:
            A list of PokeData objects, representing Pokemon that can have this ability.
        '''
        pokemon = []
        for entry in self.data["pokemon"]:
            pokemon.append(PokeData(entry["pokemon"]["name"]))
        return pokemon

    def is_hidden(self, pokemon : PokeData) -> bool:
        '''
        Check if this ability is hidden.

        The hidden status of the ability is retrieved using the PokeAPI.

        Arguments:
            None
        Returns:
            A boolean representing whether or not this ability is hidden.
        '''
        for entry in self.data["pokemon"]:
            if entry["pokemon"]["name"] == pokemon.get_internal_name():
                return entry["is_hidden"]
        return False