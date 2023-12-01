from typing import TypeVar
from libraries.data_objects.PokeData import PokeData
from libraries.data_objects.PokeEvolutionData import PokeEvolutionData
from libraries.data_objects.PokeSpeciesData import PokeSpeciesData

class ChainLink():
    # Set up the type hinting for the ChainLink class.
    _Self = TypeVar('_Self', bound='ChainLink')

    # Special / private methods

    def __init__(self, data, last : _Self = None):
        self.data = data
        self.last = last

    def __raw_data(self):
        '''
        Retrieve the raw data from the API.

        This data is always in JSON format, and should resemble that of the PokeAPI ChainLink JSON formatting.
        
        Arguments:
            None
        Returns:
            The raw data from the API.
        '''
        return self.data

    # Identification methods

    def get_name(self) -> str:
        '''
        Retrieve the name of the currently selected Pokemon.

        Arguments:
            None
        Returns:
            The name of the currently selected Pokemon.
        '''
        return self.data["species"]["name"]

    def get_pokedata(self) -> PokeData:
        '''
        Retrieve a PokeData object of this ChainLink's species.
        
        NOTE: This object is not cached, and will be created anew each time this method is called.
        Likewise, there won't be a reference to a Pokemon object, as the PokeData object is generated in a static context.

        Arguments:
            None
        Returns:
            A PokeData object of this ChainLink's species.
        '''
        return PokeData(name=self.data["species"]["name"])

    def get_species(self) -> PokeSpeciesData:
        '''
        Retrieve a PokeSpeciesData object of this ChainLink's species.

        Arguments:
            None
        Returns:
            A PokeSpeciesData object of this ChainLink's species.
        '''
        return PokeSpeciesData(name=self.data["species"]["name"])

    # Evolution methods

    def is_divergent(self) -> bool:
        '''
        Determine if this ChainLink is divergent.

        A divergent ChainLink is one that has multiple evolutions, and thus has multiple children.
        A non-divergent ChainLink is one that has only one evolution, and thus has only one child.

        Arguments:
            None
        Returns:
            True if this ChainLink is divergent, False otherwise.
        '''
        return len(self.data["evolves_to"]) > 1

    def next_link(self, divergentPath : int = 0) -> _Self:
        '''
        Proceed to the next ChainLink in the evolution chain.

        If this ChainLink is divergent, the divergentPath parameter will determine which path to take.
        If this ChainLink is not divergent, the divergentPath parameter will be ignored.

        If this ChainLink is the last in the chain, this method will return None.
        If the divergentPath parameter is out of bounds, the first child will be returned.

        Arguments:
            divergentPath : The path to take if this ChainLink is divergent.
        Returns:
            A ChainLink object of the next Pokemon in the evolution chain.
        '''
        if len(self.data["evolves_to"]) == 0:
            return None

        if self.is_divergent() and divergentPath < len(self.data["evolves_to"]):
            return ChainLink(self.data["evolves_to"][divergentPath], self)
        return ChainLink(self.data["evolves_to"][0], self)

    def next_link(self, childName : str = "") -> _Self:
        '''
        Proceed to the next ChainLink in the evolution chain.
        
        If this ChainLink is divergent, the childName parameter will determine which path to take.
        If this ChainLink is not divergent, the childName parameter will be ignored.

        If this ChainLink is the last in the chain, this method will return None.
        If the childName parameter does not match any of the children, the first child will be returned.

        Arguments:
            childName : The name of the child to take if this ChainLink is divergent.
        Returns:
            A ChainLink object of the next Pokemon in the evolution chain.
        '''
        if len(self.data["evolves_to"]) == 0:
            return None

        if self.is_divergent():
            for child in self.data["evolves_to"]:
                if child["species"]["name"] == childName:
                    return ChainLink(child, self)
        return ChainLink(self.data["evolves_to"][0], self)

    def previous_link(self) -> _Self:
        '''
        Retrieve the previous ChainLink in the evolution chain.
        
        If this ChainLink is the first in the chain, this method will return None.

        Arguments:
            None
        Returns:
            A ChainLink object of the previous Pokemon in the evolution chain.
        '''
        return self.last

    # Display methods

    def get_evolution_details(self) -> dict:
        '''
        Retrieve the evolution details of the currently selected Pokemon
        (as in, the requirements for the previous/parent Pokemon to evolve into this one).

        If this ChainLink is the first in the chain, this method will return an empty dictionary.

        Arguments:
            None
        Returns:
            The evolution details of this ChainLink.
        '''
        if self.is_absolute_parent():
            return {}
        
        dictionary = {}
        for evo in self.data["evolution_data"]:
            for key, value in evo.items():
                if key == "trigger":
                    continue
                dictionary[key] = value
        return dictionary

    def get_evolution_trigger(self) -> str:
        '''
        Retrieve the evolution trigger of the currently selected Pokemon
        (as in, the trigger for the previous/parent Pokemon to evolve into this one).

        If this ChainLink is the first in the chain, this method will return an empty string.

        Arguments:
            None
        Returns:
            The evolution trigger of this ChainLink.
        '''
        if self.is_absolute_parent():
            return ""
        return self.data["evolution_data"][0]["trigger"]["name"]

    # Check methods

    def is_absolute_parent(self) -> bool:
        '''
        Determine if this ChainLink is the absolute parent of the evolution chain.
        
        The absolute parent is the first Pokemon in the chain, and is the only Pokemon that does not have a previous evolution.

        Arguments:
            None
        Returns:
            True if this ChainLink is the absolute parent, False otherwise.
        '''
        return self.last == None

    def is_absolute_child(self) -> bool:
        '''
        Determine if this ChainLink is the absolute child of the evolution chain.
       
        The absolute child is the last Pokemon in the chain, and is the only Pokemon that cannot evolve any further.

        NOTE: Unlike the absolute parent, there can be multiple absolute children due to early divergencies.

        Arguments:
            None
        Returns:
            True if this ChainLink is an absolute child, False otherwise.
        '''
        return len(self.data["evolves_to"]) == 0

    def is_parent(self, childName : str) -> bool:
        '''
        Determine if THIS ChainLink is the parent of the specified child
        (that is, if the specified child is a direct evolution of this ChainLink).

        If this ChainLink is an absolute child, this method will return False.

        Arguments:
            childName : The name of the child to check.
        Returns:
            True if this ChainLink is the parent of the specified child, False otherwise.
        '''
        if self.is_absolute_child():
            return False
        return self.data["species"]["name"] == childName

    def is_parent(self, child : _Self) -> bool:
        '''
        Determine if THIS ChainLink is the parent of the specified child
        (that is, if the specified child is a direct evolution of this ChainLink).

        If this ChainLink is an absolute child, this method will return False.

        Arguments:
            child : The ChainLink of the child to check.
        Returns:
            True if this ChainLink is the parent of the specified child, False otherwise.
        '''
        if self.is_absolute_child():
            return False
        return self.next_link(child.get_name()) == child

    def is_child(self, parent : _Self) -> bool:
        '''
        Determine if THIS ChainLink is the child of the specified parent
        (that is, if the specified parent is a previous evolution of this ChainLink).

        If this ChainLink is an absolute parent, this method will return False.

        NOTE: Unlike `is_parent()`, this method requires a ChainLink object as the parent parameter.
        There is no alternative method that takes a string as the parent parameter.

        Arguments:
            parent : The parent to check.
        Returns:
            True if this ChainLink is the child of the specified parent, False otherwise.
        '''
        if self.is_absolute_parent():
            return False
        return self.last == parent