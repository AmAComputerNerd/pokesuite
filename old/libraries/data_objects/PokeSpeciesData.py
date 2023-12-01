import requests
from libraries.data_objects.PokeData import PokeData
from libraries.data_objects.PokeEvolutionData import PokeEvolutionData

class PokeSpeciesData():
    '''
    The PokeSpeciesData class is a wrapper for species information about Pokemon. It is used to retrieve information about a Pokemon's species, such as its name, ID, 
    varieties, and other game information.
    '''

    # Special / private methods

    def __init__(self, name : str):
        name = name.lower().replace(" ", "-")
        self.url = f"https://www.pokeapi.co/api/v2/pokemon-species/{name}"
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
        This data is always in JSON format, and should resemble that of the PokeAPI PokeSpecies JSON formatting.
        
        Arguments:
            None
        Returns:
            The raw data from the API.
        '''
        return self.data
    
    # Identification methods

    def get_name(self) -> str:
        '''
        Retrieve the name of the Pokemon species.
        Functionally, this is the same as calling the `get_name()` function of a PokeData object.
        
        Arguments:
            None
        Returns:
            The name of the Pokemon species.
        '''
        return self.data["name"]
    
    def get_url(self) -> str:
        '''
        Retrieve the URL of the Pokemon species.
        This is the URL used to retrieve data from the PokeAPI.
        NOTE: This is NOT a URL to the Pokemon's page, nor a beautified version of the species information. Expect JSON data.

        Arguments:
            None
        Returns:
            The URL of the Pokemon species.
        '''
        return self.url

    def get_id(self) -> int:
        '''
        Retrieve the ID of the Pokemon species in the PokeDex.
        IMPORTANT: This is not the same as the ID of the Pokemon itself, which can be retrieved using the `get_id()` function of a PokeData object.
        The PokeData object can be retrieved manually (i.e. using the name constructor with the result from `get_name()`) or by using the `to_pokedata()` function.
        
        Arguments:
            None
        Returns:
            The ID of the Pokemon species in the PokeDex.
        '''
        return self.data["id"]
    
    # Default methods

    def get_happiness(self) -> int:
        '''
        Retrieve the base happiness level of this Pokemon upon being caught.
        
        Arguments:
            None
        Returns:
            The base happiness level, 0 <= happiness <= 100.
        '''
        return self.data["base_happiness"]
    
    def get_evolution_chain(self) -> PokeEvolutionData:
        '''
        Retrieve the evolution chain of this Pokemon. The returned data should always be assumed to be a PokeEvolutionData object.
        
        Arguments:
            None
        Returns:
            The PokeEvolutionData object.
        '''
        return PokeEvolutionData(self.data["evolution_chain"]["url"])

    # Display methods

    def get_color(self) -> list:
        '''
        Retrieve the colour of this Pokemon. The returned data should always be assumed to be a list of PokeColor objects.
        
        Arguments:
            None
        Returns:
            The list of PokeColor objects.
        '''
        # TODO: Implement PokeColor
        return self.data["color"]["name"]

    def get_egg_groups(self) -> dict:
        '''
        Retrieve the egg groups of this Pokemon. The returned data should always be assumed to be a dictionary, where the key is the name of the egg group, and the value is the URL that leads to more information on this particular group.
        
        Arguments:
            None
        Returns:
            The dictionary of egg groups.
        '''
        return {group["name"] : group["url"] for group in self.data["egg_groups"]}

    def get_capture_rate(self) -> int:
        '''
        Retrieve the capture rate of this Pokemon.
        
        Arguments:
            None
        Returns:
            The capture rate, 0 <= capture rate <= 255.
        '''
        return self.data["capture_rate"]

    def get_generation(self) -> str:
        '''
        Retrieve the NAME of the generation this Pokemon was introduced in.

        Arguments:
            None
        Returns:
            The name of the generation.
        '''
        return self.data["generation"]["name"]

    def get_varieties(self, variety : str = "") -> list:
        '''
        Retrieve either a list of varieties for this Pokemon or a specific Pokemon variety. The returned data should always be assumed to be a dict of PokeData, where the key
        is the name of the variant, and the value is the PokeData object of this variant.
        
        Arguments:
            variety (opt) the variety to retrieve, prefixed with the pokemon's name
        Returns:
            The dictionary of PokeData.
        '''
        variety = variety.lower().replace(" ", "-")

        if variety != "":
            for data in self.data["varieties"]:
                if data["pokemon"]["name"] == variety:
                    return {variety, PokeData(data["pokemon"]["url"])}
        
        return {var["pokemon"]["name"] : PokeData(var["pokemon"]["url"]) for var in self.data["varieties"]}

    # Check methods

    def is_baby(self) -> bool:
        '''
        Check whether this Pokemon is classified as a baby.
        
        Arguments:
            None
        Returns:
            True if this Pokemon is a baby, False otherwise.
        '''
        return self.data["is_baby"]

    def is_legendary(self) -> bool:
        '''
        Check whether this Pokemon is classified as a legendary.
        
        Arguments:
            None
        Returns:
            True if this Pokemon is legendary, False otherwise.
        '''
        return self.data["is_legendary"]

    def is_mythical(self) -> bool:
        '''
        Check whether this Pokemon is classified as mythical.
        
        Arguments:
            None
        Returns:
            True if this Pokemon is mythical, False otherwise.
        '''
        return self.data["is_mythical"]

    # Conversion methods

    def to_pokedata(self) -> PokeData:
        '''
        Convert this PokeSpeciesData object into a PokeData object.
        This is done by retrieving the Pokemon's name and using the name constructor to retrieve the PokeData object.
        NOTE: This is a NEW object. As such, no Pokemon is assigned to this object.
        
        Arguments:
            None
        Returns:
            The PokeData object.
        '''
        return PokeData(self.get_name())