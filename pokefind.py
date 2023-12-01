import os
from typing import Any

try:
    from objects.data.PokeData import PokeData
    from objects.data.PokeAbilityData import PokeAbilityData
except ImportError:
    os.system("cls")
    print("Error: Required libraries not found. Please run the setup script.")
    input("Press enter to exit.")
    exit()

# running variable. Used to determine if the program is running or not.
running = True

def script():
    '''
    Run the script.

    Arguments:
        None
    Returns:
        None
    '''
    # Start app loop.
    while running:
        os.system("cls")
        print(f"Welcome to PokeFind!")
        print(f"This program enables you to search for any Pokemon, ability, item, or move utilising the PokeAPI.")
        print(f'-----------------------------------------------------------------------------------------------------------------')
        print(f'Please enter the type of data you would like to search for. This should be one of the following: "pokemon", "ability", "item", "move".')
        data_type = input(f'DATA-TYPE > ')
        print(f'-----------------------------------------------------------------------------------------------------------------')
        print(f'Please enter the name of the {data_type} you would like to search for.')
        name = input(f'SEARCH [{data_type.upper()}] > ')
        print(f'-----------------------------------------------------------------------------------------------------------------')
        print(f'Checking for internet connection...', end=" ")
        # Check if an internet connection can be established.
        # For now, until other data types are implemented, we will only check for a connection using either PokeData or PokeAbilityData, and other data types will be ignored.
        if type == "pokemon":
            if PokeData.test_connection() != 200:
                __failure(error_msg="An internet connection could not be established. Please check your internet connection and try again.")
                continue
        elif type == "ability":
            if PokeAbilityData.test_connection() != 200:
                __failure(error_msg="An internet connection could not be established. Please check your internet connection and try again.")
                continue
        elif type == "item":
            # TODO: Implement item data type.
            __failure(error_msg="The item data type is not yet implemented.")
            continue
        elif type == "move":
            # TODO: Implement move data type.
            __failure(error_msg="The move data type is not yet implemented.")
            continue
        print("Done!")
        print(f'-----------------------------------------------------------------------------------------------------------------')
        print(f'Searching for {data_type}...', end=" ")
        # At this point, we know that the API is reachable, so we can again use the search() function to search for the data.
        data = search(data={data_type: name}, search_type=data_type)
        if type(data) == str:
            # The data was either not found, or some other error occurred.
            print("Failed!")
            __failure(error_msg=f"Something happened during the search: {data}")
        elif type(data) == PokeData:
            # Pokemon found! We should print it to console.
            print("Success!")
            print(data)
            input("Press ENTER to continue!")
            continue

def search(data : dict, search_type : str = "") -> PokeData | PokeAbilityData | str:
    '''
    Utilise the API to search for data.

    This function will search and return specific kinds of data based on the search type.

    When searching for a pokemon, the data will be returned as a PokeData object.
    When searching for an ability, the data will be returned as a PokeAbilityData object.
    When searching for an item, the data will be returned as a PokeItemData object.
    When searching for a move, the data will be returned as a PokeMoveData object.

    In all cases, if the data is not found or an internet connection cannot be established, the function will return a string containing the error message.

    Arguments:
        data (dict): A dictionary containing the data to search for. The dictionary should contain the data type as the key, and the data to search for as the value. Other keys and values may be taken into account, depending on the search type.
        search_type (str): The type of data to search for. This should be one of the following: "pokemon", "ability", "item", "move". In the case of no search type being provided, the function will first check if the data dictionary contains a key of either "pokemon", "ability", "item", or "move". If it does, the function will use that key to determine the search type. If it does not, the function will return an error message.
    Returns:
        Union: The data that was searched for. This will be returned as a PokeData, PokeAbilityData, PokeItemData, or PokeMoveData object, depending on the search type. If the data is not found or an internet connection cannot be established, the function will return a string containing the error message.
    '''
    if not search_type:
        # No search type was given. First, we will look for common elements in the data dictionary.
        if data.get("pokemon") != None:
            # The pokemon key exists. This is a pokemon search.
            search_type = "pokemon"
        elif data.get("ability") != None:
            # The ability key exists. This is an ability search.
            search_type = "ability"
        elif data.get("item") != None:
            # The item key exists. This is an item search.
            search_type = "item"
        elif data.get("move") != None:
            # The move key exists. This is a move search.
            search_type = "move"
        else:
            # No common elements were found. This is an invalid search.
            return "Invalid search."
    
    # Now that we have the search type, we can search for the data.
    if search_type == "pokemon":
        return _search_pokemon(name=data.get("pokemon", ""))
    elif search_type == "ability":
        return _search_ability(name=data.get("ability", ""))
    elif search_type == "item":
        return _search_item(name=data.get("item", ""))
    elif search_type == "move":
        return _search_move(name=data.get("move", ""))
    # Invalid or unimplemented search type.
    return "Invalid search."

def _search_pokemon(name : str, data : dict = {}) -> PokeData | str:
    '''
    Search for a pokemon.

    The function will first check if an internet connection can be established. If it cannot, the function will return an error message.
    If the Pokemon is found, the function will return a PokeData object containing the data of the Pokemon.
    If the Pokemon is not found, the function will return an error message.

    Arguments:
        name (str): The name of the Pokemon to search for.
        data (dict): A dictionary containing additional data to search for. This is optional.
    Returns:
        Union: The data that was searched for. This will be returned as a PokeData object. If the data is not found or an internet connection cannot be established, the function will return a string containing the error message.
    '''
    # Check if an internet connection can be established.
    if PokeData.test_connection() != 200:
        return "No internet connection."
    # An internet connection is available. We can now search for the pokemon.
    try:
        pokemon = PokeData(name=name)
    except:
        return "Pokemon not found."
    # The pokemon was found. We can now return the data.
    return pokemon

def _search_ability(name : str, data : dict = {}) -> PokeAbilityData | str:
    '''
    Search for an ability.

    The function will first check if an internet connection can be established. If it cannot, the function will return an error message.
    If the ability is found, the function will return a PokeAbilityData object containing the data of the ability.
    If the ability is not found, the function will return an error message.

    Arguments:
        name (str): The name of the ability to search for.
        data (dict): A dictionary containing additional data to search for. This is optional.
    Returns:
        Union: The data that was searched for. This will be returned as a PokeAbilityData object. If the data is not found or an internet connection cannot be established, the function will return a string containing the error message.
    '''
    # Check if an internet connection can be established.
    if PokeAbilityData.test_connection() != 200:
        return "No internet connection."
    # An internet connection is available. We can now search for the ability.
    try:
        ability = PokeAbilityData(name=name)
    except:
        return "Ability not found."
    # The ability was found. We can now return the data.
    return ability

def _search_item(name : str, data : dict = {}) -> Any:
    pass

def _search_move(name : str, data : dict = {}) -> Any:
    pass

def __failure(error_msg : str = "Something has gone wrong! Please try running the setup script."):
    '''
    Print an error message before calling trig_exit().

    Internal helper function.

    Arguments:
        error_msg (str): The error message to print. This is optional.
    Returns:
        None
    '''
    print(f'-----------------------------------------------------------------------------------------------------------------')
    print(f'ERROR: {error_msg}')
    print(f'Press ENTER to exit.')
    trig_exit()
    
def trig_exit():
    input("")
    exit()

# If this file is ran standalone, run the script() function automagicly.
if __name__ == "__main__":
    script()