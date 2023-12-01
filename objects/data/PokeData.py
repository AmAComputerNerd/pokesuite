from typing import Any
import requests
from requests.exceptions import HTTPError

from objects.data.PokeAbilityData import PokeAbilityData
from objects.Logger import Logger

class PokeData:
    def __init__(self, name : str = "", url : str = "", logger : Logger = Logger.no_logger()):
        if name != "": self.url = "https://pokeapi.co/api/v2/pokemon/" + name
        elif url != "": self.url = url
        else: raise ValueError("Either name or url must be provided.")
        
        self.logger = logger

        # Get the data from the API.
        request = requests.get(self.url)
        # Raise an exception if the request fails.
        logger.route(request.raise_for_status, raise_exceptions=True)  # type: ignore
        # Set the data.
        self.data : dict = request.json()

    def _raw_data(self) -> dict:
        '''
        Returns the raw data from the API.

        This is useful for manually getting data from the API.

        Arguments:
            None
        Returns:
            dict: The raw data from the API.
        '''
        return self.data

    def _get_data(self, key : str, default_return = None) -> Any:
        '''
        Retrieve data from the API.

        This is useful for getting data that this wrapper does not natively support.

        Arguments:
            key (str): The key to get data from.
            default_return (any): The default value to return if the key does not exist.
        Returns:
            any: The value of the key in the dictionary, or the provided value OR None if the key doesn't exist.
        '''
        return self.data.get(key, default_return)

    def get_name(self) -> str:
        '''
        Retrieve the name of the Pokemon.

        Arguments:
            None
        Returns:
            str: The name of the Pokemon.
        '''
        return self._get_data("name", "Unknown")

    def get_internal_id(self) -> int:
        '''
        Retrieve the internal ID of the Pokemon.

        Arguments:
            None
        Returns:
            int: The internal ID of the Pokemon.
        '''
        return self._get_data("id", -1)

    def get_height(self) -> float:
        '''
        Retrieve the height of the Pokemon.

        Arguments:
            None
        Returns:
            int: The height of the Pokemon.
        '''
        return self._get_data("height", -1)
    
    def get_weight(self) -> float:
        '''
        Retrieve the weight of the Pokemon.

        Arguments:
            None
        Returns:
            int: The weight of the Pokemon.
        '''
        return self._get_data("weight", -1)

    def get_sorting_priority(self) -> int:
        '''
        Retrieve the sorting priority of the Pokemon.

        Lower numbers are higher priority.
        For Pokemon with the same priority, the name is used as a tiebreaker.

        Arguments:
            None
        Returns:
            int: The sorting priority of the Pokemon.
        '''
        return self._get_data("order", -1)

    def get_abilities(self, slots : list = [], names : list = [], limit : int = -1) -> list:
        '''
        Retrieve the abilities of the Pokemon.
        
        The returned data will always be a list of PokeAbilityData.
        The list is not guarranteed to be any specific length, nor is it guarranteed to have a length at all if the ability cannot be found.

        Arguments:
            slots (list[int]): The slots to retrieve. Any parameters that are out of range are ignored. If empty, this parameter is ignored.
            names (list[str]): The names of the abilities to retrieve. Any parameters that aren't strings are ignored. If empty, this parameter is ignored.
            limit (int): The maximum number of abilities to retrieve. If -1 or out of range, the parameter is ignored.
        Returns:
            list: The abilities of the Pokemon.
        '''
        # Standardise the parameters for guarranteed consistency.
        slots = [slot for slot in slots if slot >= 0 and slot < 6]
        names = [name.lower().replace(" ", "-") for name in names if name != "" and type(name) == str]
        limit = limit if limit > 0 else -1

        # TODO: Test this.
        abilities = self._get_data("abilities", [])
        if len(slots) != 0:
            abilities = [ability for ability in abilities if ability.get("slot", -1) in slots]
        if len(names) != 0:
            abilities = [ability for ability in abilities if ability.get("ability", {}).get("name", "") in names]
        if limit != -1:
            abilities = abilities[:limit]
        # Fetch the URL, and pass each URL into the PokeAbilityData constructor.
        return [PokeAbilityData(url=ability.get("ability", {}).get("url", ""), logger=self.logger) for ability in abilities]

    def get_moves(self, slots : list = [], names : list = [], limit : int = -1) -> list:
        '''
        Retrieve the moves of the Pokemon.
        
        The returned data will always be a list of PokeMoveData.
        The list is not guarranteed to be any specific length, nor is it guarranteed to have a length at all if the move cannot be found.

        Arguments:
            slot (list[int]): The slots to retrieve. Any parameters that are out of range are ignored. If empty, this parameter is ignored.
            names (list[str]): The names of the moves to retrieve. Any parameters that aren't strings are ignored. If empty, this parameter is ignored.
            limit (int): The maximum number of moves to retrieve. If -1 or out of range, the parameter is ignored.
        Returns:
            list: The moves of the Pokemon.
        '''
        # Standardise the parameters for guarranteed consistency.
        slots = [slot for slot in slots if slot >= 0 and slot < 6]
        names = [name.lower().replace(" ", "-") for name in names if name != "" and type(name) == str]
        limit = limit if limit > 0 else -1

        moves = self._get_data("moves", [])
        # TODO: Implement functionality for PokeMoveData.
        return moves
        
    def get_forms(self, names : list = [], limit : int = -1) -> list:
        '''
        Fetch the forms of the Pokemon.

        Some Pokemon have different forms depending on the region they're found in.
        For example, the Alolan region features a different form of the Pokemon Rattata.

        The returned data will always be a list of PokeData.
        The list is not guarranteed to be any specific length, nor is it guarranteed to have a length at all if the form cannot be found.

        Arguments:
            names (list[str]): The names of the forms to retrieve. If empty or not found, the parameter is ignored.
            limit (int): The maximum number of forms to retrieve. If -1 or out of range, the parameter is ignored.
        Returns:
            list: The forms of the Pokemon.
        '''
        forms = self._get_data("forms", [])
        if len(names) != 0:
            forms = [form for form in forms if form.get("name", "") in names]
        if limit != -1:
            forms = forms[:limit]
        # Fetch the URL, and pass each URL into the PokeFormData constructor.
        return [PokeData(url=form.get("url", ""), logger=self.logger) for form in forms]

    def get_sprites(self, front : bool = True, back : bool = True, shiny : bool = False, female : bool = False, other_category : str = "") -> dict:
        '''
        Retrieve the sprites of the Pokemon.

        The returned data will always be a dictionary of sprite URLs.
        Common keys will depend on the parameters provided, but as an example, here are a set of keys that can be found based on category settings:
            front_default (front=True), 
            back_default (back=True), 
            front_female (front=True, female=True), 
            back_female (back=True, female=True), 
            front_shiny (front=True, shiny=True), 
            back_shiny (back=True, shiny=True), 
            front_shiny_female (front=True, shiny=True, female=True), 
            back_shiny_female (back=True, shiny=True, female=True).
        
        Arguments:
            front (bool): Whether to include 'front' sprites in the resulting dictionary.
            back (bool): Whether to include 'back' sprites in the resulting dictionary.
            shiny (bool): Whether to include 'shiny' sprites in the resulting dictionary. Defaults to False.
            female (bool): Whether to include 'female' sprites in the resulting dictionary. Defaults to False.
            other_category (str): An optional category to find sprites within. This may be alternate sprites for different games, or official artwork. If provided, only the sprites within this category can be found and returned.
        Returns:
            dict: The URLs to the sprites of the Pokemon.
        '''
        if len(other_category) != 0: sprites : dict = self._get_data("sprites", {}).get("other", {}).get(other_category, {})
        else: sprites : dict = self._get_data("sprites", {})

        toReturn = {}
        for key in sprites.keys():
            if "front" in key and not front: continue
            if "back" in key and not back: continue
            if "shiny" in key and not shiny: continue
            if "female" in key and not female: continue
            toReturn[key] = sprites[key]
        return toReturn
    
    def get_default_stats(self, stats : list = []) -> dict:
        '''
        Retrieve the default stats of the Pokemon.

        The returned data will always be a dictionary of the default stats of the Pokemon.
        The dictionary will be empty if no stats are found.

        Arguments:
            stats (list[str]): The stats to retrieve. If empty, all stats are retrieved.
        Returns:
            dict: The default stats of the Pokemon.
        '''
        stats = [stat.lower().replace(" ", "-") for stat in stats if stat != "" and type(stat) == str]
        toReturn = {}
        for stat in self._get_data("stats", []):
            if len(stats) != 0 and stat.get("stat", {}).get("name", "") not in stats: continue
            toReturn[stat.get("stat", {}).get("name", "")] = stat.get("base_stat", 0)
        return toReturn

    def get_default_types(self) -> list:
        '''
        Retrieve the default types of the Pokemon.

        The returned data will always be a list of the default types of the Pokemon.
        The list will be empty if no types are found.

        Returns:
            list: The default types of the Pokemon.
        '''
        return [type.get("type", {}).get("name", "") for type in self._get_data("types", [])]

    @staticmethod
    def test_connection(name : str = "", url : str = "") -> int:
        '''
        Test the connection to the PokeAPI.

        Arguments:
            name (str): The name of the Pokemon to test the connection with.
            url (str): The URL of the Pokemon to test the connection with.
        Returns:
            int: The response code of the connection.
        '''
        try:
            # Test a default connection.
            default = requests.get("https://pokeapi.co/api/v2/pokemon/1")
            default.raise_for_status()
            # If a name is provided, test a connection with the name.
            if len(name) != 0:
                name_search = requests.get(f"https://pokeapi.co/api/v2/pokemon/{name}")
                name_search.raise_for_status()
            # If a URL is provided, test a connection with the URL.
            if len(url) != 0:
                url_search = requests.get(url)
                url_search.raise_for_status()
            # All checks have passed, return 'Success' status code
            return 200
        except HTTPError as e:
            # Return the status code of the failed connection.
            return e.response.status_code