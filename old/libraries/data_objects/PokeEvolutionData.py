import requests
from libraries.data_objects.PokeSpeciesData import PokeSpeciesData
from libraries.data_objects.ChainLink import ChainLink

class PokeEvolutionData():
    '''
    The PokeEvolutionData class is a wrapper for evolution information about Pokemon. It is used to retrieve information about a Pokemon's evolution chain, such as its 
    child and parent Pokemon.
    '''

    def __init__(self, name : str):
        data = PokeSpeciesData(name=name)
        self.url = data.__raw_data()["evolution_chain"]["url"]
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
        This data is always in JSON format, and should resemble that of the PokeAPI PokeEvolution JSON formatting.
        
        Arguments:
            None
        Returns:
            The raw data from the API.
        '''
        return self.data

    # Identification methods
    # Note: no get_name() method, as the evolution chain does not have a name.

    def get_url(self) -> str:
        '''
        Retrieve the URL of the evolution chain.
        
        Arguments:
            None
        Returns:
            The URL of the evolution chain.
        '''
        return self.url

    def get_id(self) -> int:
        '''
        Retrieve the ID of this EvolutionData in the API.
        
        Arguments:
            None
        Returns:
            The ID of this EvolutionData info.
        '''
        return self.data["id"]

    # Default methods

    def get_chain(self) -> ChainLink:
        '''
        Retrieve the ChainLink object for the given evolution chain.

        The returned ChainLink object is formatted from the absolute parent of the evolution chain.
        The ChainLink object is a custom class that provides convenience methods for retrieving information about the evolution chain.
        
        Arguments:
            None
        Returns:
            The ChainLink object for the given evolution chain.
        '''
        return ChainLink(self.get_absolute_parent())

    def get_absolute_parent(self) -> dict:
        '''
        Retrieve the absolute parent (the very first Pokemon from this chain) of the evolution chain.
        
        The returned JSON will be formatted under the ChainLink format from PokeAPI.
        
        Functionally, this method is equivalent to `get_chain().__raw_data()`, though is provided for clarity.
        
        Arguments:
            None
        Returns:
            The top-most evolution chain, in JSON.
        '''
        return self.data["chain"]

    def get_absolute_child(self) -> dict:
        '''
        Retrieve the absolute child (the very last Pokemon from this chain) of the evolution chain.
        
        The returned JSON will be formatted under the ChainLink format from PokeAPI.

        As this method returns the bottom-most evolution, the "evolves_to" key will always be empty.
        
        Arguments:
            None
        Returns:
            The bottom-most evolution chain, in JSON.
        '''
        chain = self.get_chain()
        while True:
            if chain.is_absolute_child():
                return chain.__raw_data()
            chain = chain.next_link()
            if chain == None:
                raise Exception("Absolute child not found. This should never happen. How the fuck did we get here.")

    def get_chain_length(self) -> int:
        '''
        Retrieve the length of the evolution chain.
        
        This method is provided as a convenience method, as the in-built `len()` method will not work on this method, as it returns a JSON object with multiple unique keys.
        
        Arguments:
            None
        Returns:
            The length of the evolution chain.
        '''
        chain = self.get_chain()
        length = 1
        while chain.next_link() != None:
            length += 1
        return length