from objects.Logger import Logger
import requests
from requests.exceptions import HTTPError

class PokeAbilityData:
    def __init__(self, name : str = "", url : str = "", logger : Logger = Logger.no_logger()): # type: ignore
        if name != "": self.url = "https://pokeapi.co/api/v2/ability/" + name
        elif url != "": self.url = url
        else: raise ValueError("Either name or url must be provided.")

        self.logger = logger

        # Get the data from the API.
        request = requests.get(self.url)
        # Raise an exception if the request failed.
        logger.route(request.raise_for_status, raise_exceptions=True)  # type: ignore
        # Get the data from the request.
        self.data = request.json()

    @staticmethod
    def test_connection(name : str = "", url : str = "") -> int:
        '''
        Test the connection to the PokeAPI.

        Arguments:
            name (str): The name of the Ability to test the connection with.
            url (str): The URL of the Ability to test the connection with.
        Returns:
            int: The response code of the connection test.
        '''
        try:
            # Test a default connection.
            default = requests.get("https://pokeapi.co/api/v2/ability/1")
            default.raise_for_status()
            # If a name is provided, test a connection with the name.
            if len(name) != 0:
                name_search = requests.get(f"https://pokeapi.co/api/v2/ability/{name}")
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