import requests
from libraries.Pokemon import Pokemon
from libraries.PokeMove import PokeMove
from libraries.PokeAbility import PokeAbility
from libraries.data_objects.PokeAbilityData import PokeAbilityData
from libraries.data_objects.PokeMoveData import PokeMoveData
from libraries.data_objects.PokeSpeciesData import PokeSpeciesData

class PokeData():
    '''
    The PokeData class represents a Pokemon's default values and information. This class is used to retrieve information about a Pokemon, such as its name, ID, sprites, 
    abilities, types, stats, moves, and species.
    '''

    def __init__(self, name : str):
        self.pokemon = None
        name = name.lower().replace(" ")
        self.url = f"https://www.pokeapi.co/api/v2/pokemon/{name}"
        request = requests.get(self.url)
        request.raise_for_status()
        self.data = request.json()

    def __init__(self, url):
        self.pokemon = None
        self.url = url
        request = requests.get(self.url)
        request.raise_for_status()
        self.data = request.json()

    def __init__(self, pokemon : Pokemon):
        self.pokemon = pokemon
        self.url = f"https://www.pokeapi.co/api/v2/pokemon/{pokemon.get_name()}"
        request = requests.get(self.url)
        request.raise_for_status()
        self.data = request.json()
    
    def __raw_data(self):
        '''
        Retrieve the raw data from the API.
        This data is always in JSON format, and should resemble that of the PokeAPI Pokemon JSON formatting.
        
        Arguments:
            None
        Returns:
            The raw data from the API.
        '''
        return self.data

    # Identification methods

    def get_name(self) -> str:
        '''
        Retrieve the name of the Pokemon.
        
        Arguments:
            None
        Returns:
            The name of the Pokemon.
        '''
        return self.data["name"]

    def get_url(self) -> str:
        '''
        Retrieve the URL of the Pokemon.
        
        Arguments:
            None
        Returns:
            The URL of the Pokemon.
        '''
        return self.url

    def get_id(self) -> int:
        '''
        Retrieve the ID of the Pokemon in the PokeDex.
        
        Arguments:
            None
        Returns:
            The ID of the Pokemon in the PokeDex.
        '''
        return self.data["id"]

    # Default methods

    def get_sprites(self, spriteType : str = "") -> list:
        '''
        Retrieve either a specific sprite or list of sprite URLs. The returned data should always be assumed to be a list of URLs.
        
        Arguments:
            spriteType (opt) the type of sprite to retrieve {front, back, front_shiny, back_shiny}
        Returns:
            A list of sprite URLs.
        '''
        spriteType = spriteType.lower().replace(" ", "_")
        if spriteType == "front":
            return [self.data["sprites"]["front_default"]]
        elif spriteType == "back":
            return [self.data["sprites"]["back_default"]]
        elif spriteType == "front_shiny":
            return [self.data["sprites"]["front_shiny"]]
        elif spriteType == "back_shiny":
            return [self.data["sprites"]["back_shiny"]]

        return [self.data["sprites"]["front_default"], self.data["sprites"]["back_default"], self.data["sprites"]["front_shiny"], self.data["sprites"]["back_shiny"]]

    def get_abilities(self, ability : str = "", generic : bool = True) -> list:
        '''
        Retrieve either a specific ability or list of abilities. The returned data should always be assumed to be a list of PokeAbility.

        Arguments:
            ability (opt) the ability to retrieve
            generic (opt) [default=True] whether or not to retrieve data-only (PokeAbilityData) objects or full (PokeAbility) objects
        Returns:
            A list of PokeAbility or PokeAbilityData objects.
        '''
        ability = ability.lower().replace(" ", "_")

        if ability != "":
            if self.has_ability(ability):
                if generic:
                    return [PokeAbilityData(ability)]
                return [PokeAbility(ability)]

        if generic:
            return [PokeAbilityData(data["ability"]["url"]) for data in self.data["abilities"]]
        return [PokeAbility(ability["ability"]["url"]) for ability in self.data["abilities"]]
    
    def get_types(self) -> list:
        '''
        Retrieve all types of the Pokemon. Values can be fed into the `poketype.py` script for more information.
        
        Arguments:
            None
        Returns:
            A list of types.
        '''
        return [type["type"]["name"] for type in self.data["types"]]

    def get_stats(self) -> dict:
        '''
        Retrieve DEFAULT stats of the Pokemon. This does not include EVs, IVs, or any other stat modifiers. The returned data should always be assumed to be a dictionary 
        representing the stats of the Pokemon, where the key is the stat name in lowercase and underscores replacing whitespace, and the value is the default amount for this
        Pokemon.
        
        Arguments:
            None
        Returns:
            A dictionary of stats.
        '''
        return {stat["stat"]["name"] : stat["base_stat"] for stat in self.data["stats"]}

    def get_moves(self, move : str = "", generic : bool = True) -> list:
        '''
        Retrieve either a specific move or list of moves. The returned data should always be assumed to be a list of PokeMove.
        
        Arguments:
            move (opt) the move to retrieve
            generic (opt) [default=True] whether or not to retrieve data-only (PokeMoveData) objects or full (PokeMove) objects
        Returns:
            A list of PokeMove or PokeMoveData objects.
        '''
        move = move.lower().replace(" ", "_")

        if move != "":
            if self.has_ability(move):
                if generic:
                    return [PokeMoveData(move)]
                return [PokeMove(move)]

        if generic:
            return [PokeMoveData(data["move"]["url"]) for data in self.data["moves"]]
        return [PokeMove(data["move"]["url"]) for data in self.data["moves"]]

    def get_species(self) -> PokeSpeciesData:
        '''
        Retrieve the species information of this Pokemon. The returned data should always be assumed to be a PokeSpeciesData object.
        
        Arguments:
            None
        Returns:
            A PokeSpeciesData object.
        '''
        return PokeSpeciesData(self.data["species"]["url"])

    # Display methods

    def get_base_experience(self) -> int:
        '''
        Retrieve the base experience of the Pokemon. This is mostly used for display purposes.
        
        Arguments:
            None
        Returns:
            The base experience of the Pokemon.
        '''
        return self.data["base_experience"]

    def get_height(self) -> float:
        '''
        Retrieve the height of the Pokemon. This is mostly used for display purposes.
        
        Arguments:
            None
        Returns:
            The height of the Pokemon.
        '''
        return self.data["height"]

    def get_weight(self) -> float:
        '''
        Retrieve the weight of the Pokemon. This is mostly used for display purposes.
        
        Arguments:
            None
        Returns:
            The weight of the Pokemon.
        '''
        return self.data["weight"] 

    def get_sorting_order(self) -> int:
        '''
        Retrieve the sorting order of the Pokemon. This is mostly used for display purposes.
        
        Arguments:
            None
        Returns:
            The sorting order of the Pokemon.
        '''
        return self.data["order"]

    # Check methods

    def is_default_pokemon(self) -> bool:
        '''
        Check if the Pokemon is a default Pokemon - that is, the lowest in the evolution chain.
        Functionally, this is a shortcut for `self.get_species().get_evolution_chain().get_absolute_child()`.
        
        Arguments:
            None
        Returns:
            True if the Pokemon is a default Pokemon, False otherwise.
        '''
        return self.get_species().get_evolution_chain().get_absolute_child() == self

    def has_ability(self, ability : PokeAbility) -> bool:
        '''
        Check if the Pokemon can use a specific ability.

        Arguments:
            ability the PokeAbility to check for
        Returns:
            True if the Pokemon can use the ability, False otherwise.
        '''
        return self.has_ability(ability.get_data())
    
    def has_ability(self, abilityData : PokeAbilityData) -> bool:
        '''
        Check if the Pokemon can use a specific ability.

        Arguments:
            abilityData the PokeAbilityData to check for
        Returns:
            True if the Pokemon can use the ability, False otherwise.
        '''
        for data in self.data["abilities"]:
            if data["ability"]["name"] == abilityData.get_name():
                return True
        return False

    def has_ability(self, abilityName : str) -> bool:
        '''
        Check if the Pokemon can use a specific ability.

        Arguments:
            abilityName the ability name to check for
        Returns:
            True if the Pokemon can use the ability, False otherwise.
        '''
        return self.has_ability(PokeAbility(abilityName))

    def has_move(self, move : PokeMove) -> bool:
        '''
        Check if the Pokemon can learn a specific move.

        Arguments:
            move the PokeMove to check for
        Returns:
            True if the Pokemon can learn the move, False otherwise.
        '''
        return self.has_move(move.get_data())

    def has_move(self, moveData : PokeMoveData) -> bool:
        '''
        Check if the Pokemon can learn a specific move.

        Arguments:
            moveData the PokeMoveData to check for
        Returns:
            True if the Pokemon can learn the move, False otherwise.
        '''
        for data in self.data["moves"]:
            if data["move"]["name"] == moveData.get_name():
                return True
        return False

    def has_move(self, moveName : str) -> bool:
        '''
        Check if the Pokemon can learn a specific move.

        Arguments:
            moveName the move name to check for
        Returns:
            True if the Pokemon can learn the move, False otherwise.
        '''
        return self.has_move(PokeMove(moveName))

    # Conversion methods

    def to_pokemon(self) -> Pokemon:
        '''
        Convert the PokemonData object to a Pokemon object.
        
        NOTE: Converted object will initialise with default stats UNLESS the PokemonData object was initialised with a Pokemon object.
        
        Arguments:
            None
        Returns:
            A Pokemon object.
        '''
        if self.pokemon == None:
            return Pokemon(self)
        return self.pokemon