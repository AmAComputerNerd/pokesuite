import os

# Attempt to import the PokeFind module.
try:
    import pokefind # type: ignore
except ImportError:
    # PokeFind module not found.
    # We'll just set the variable to None, and handle it later.
    pokefind = None

# running variable. Used to control the app loop.
running = True

def script(mode : str = ""):
    '''
    Run the script.

    Arguments:
        mode (str): The default mode to run the script in. Currently, may be either 1 (simple) or 2 (advanced). Any other value will prompt the user to select a mode.\
    Returns:
        None
    '''
    # Data variable. Won't be used just yet, but will enable integration with other scripts.
    session = {}

    # Despite appropriate warnings re: valid values of mode, double check for string modes and convert to int.
    if mode.lower() == "simple":
        mode = '1'
    elif mode.lower() == "advanced":
        mode = '2'

    # Start app loop.
    while running:
        os.system("cmd /c cls")
        print(f'Welcome to the Pokemon Type Calculator!')
        print(f'This program will calculate the most effective type of move to use against a Pokemon opponent.')
        print(f'-----------------------------------------------------------------------------------------------------------------')
        if mode is "":
            # Prompt the user to select a mode.
            print(f'You haven\'t selected a mode yet! Please select a mode.')
            print(f'-----------------------------------------------------------------------------------------------------------------')
            print('(1) Simple - This mode is designed for standalone use. This limits the functionality of the program, but also enables usage without an internet connection or a reliance on external files.')
            print('(2) Advanced - This mode enables a wider range of functionality with the usage of the PokeAPI and the PokeFind module. This mode requires an internet connection, and the `pokefind.py` file to be in the same directory as this file.')
            print('(3) Exit - This mode will exit the program.')
            print(f'-----------------------------------------------------------------------------------------------------------------')
            mode = input('Please select a mode: ')
        if mode == '1':
            # User has selected simple mode.
            # No connections needed, so we can just run the simple() function.
            simple()
        elif mode == '2':
            # User has selected advanced mode.
            # We need to check if the PokeFind module is available.
            # "But not now. I'm busy."
            advanced(None)
            pass
        elif mode == '3':
            # User has selected exit, so we'll exit the program through the trig_exit() function.
            trig_exit()
        
        # Reset mode so User doesn't get stuck in a loop.
        mode = ""
    
    # User has exited the program, or the loop has been broken by other means.
    # Rather than calling exit(), we instead return to provide other (potentially parent) scripts to continue their execution.
    os.system("cmd /c cls")
    input(f'Execution has ended [ENTER]')
    
def simple() -> list:
    '''
    Run through simple execution of the script.

    Arguments:
        None
    Returns:
        Final calculated effectiveness of all moves, where each element of the returned list is a dictionary of moves, where list[0] is super effective moves... and list[3] is immune moves.
    '''
    os.system("cmd /c cls")
    print(f'Pokemon Type Calculator - Simple Mode')
    print(f'-----------------------------------------------------------------------------------------------------------------')
    print(f'Please enter the type(s) of the opponent Pokemon. If the opponent Pokemon has two types, please enter them separated by a comma and space (e.g. fire, water).')
    opponent_types = input(" > ").split(", ")
    print(f'-----------------------------------------------------------------------------------------------------------------')
    print(f'Please enter the type(s) of your Pokemon. Same rules as above apply. [NOTE, you may also leave this space empty. This will not take into account STAB moves, however]')
    self_types = input(" > ").split(", ")
    print(f'-----------------------------------------------------------------------------------------------------------------')
    print(f'Please enter the type(s) of the moves you have available. Same rules as above apply.')
    move_types = input(" > ").split(", ")
    print(f'-----------------------------------------------------------------------------------------------------------------')
    # Proceed with calculations.
    print(f'Calculating...')
    return run_calculations(user=self_types, opponent=opponent_types, moves=move_types, print_results=True)

def advanced(session) -> list:
    '''
    Run through advanced execution of the script.

    Arguments:
        session (Unknown): Unknown
    Returns:
        Final calculated effectiveness of all moves, where each element of the returned list is a dictionary of moves, where list[0] is super effective moves... and list[3] is immune moves.
    '''
    # TODO: Implement advanced mode, and integration with PokeFind.
    os.system("cmd /c cls")
    if pokefind is None:
        # PokeFind module not found.
        print(f'Error: PokeFind module not found. Please ensure that the `pokefind.py` file is in the same directory as this file.')
        input(f'Press ENTER to continue...')
    return []

def trig_exit():
    '''
    Trigger the exit of the program loop, after the current iteration has finished.

    Arguments:
        None
    Returns:
        None
    '''
    global running
    running = False

def run_calculations(user : list = [], opponent : list = [], moves : list = [], generation : int = 8, print_results : bool = False) -> list:
    '''
    Run the calculations for the effectiveness of moves against a Pokemon.

    Arguments:
        user (list): The types of the user's Pokemon. This can be left empty, but will not take into account STAB moves.
        opponent (list): The types of the opponent's Pokemon.
        moves (list): The types of the moves available to the user.
        generation (int): The generation of Pokemon to use (currently, 1-8). Defaults to 8.
        print_results (bool): Whether or not to print the results to the console. Defaults to False.
    Returns:
        Final calculated effectiveness of all moves, where each element of the returned list is a dictionary of moves, where list[0] is super effective moves... and list[3] is immune moves.
    '''

    # To begin, we need to figure out which type chart revision we need.
    # This is done by checking the generation variable.
    # Generation 1 uses the original type chart, without the modern types of Dark, Steel and Fairy.
    # Generation 2-5 uses the revised type chart, featuring the new Dark and Steel types, though not Fairy.
    # Generation 6+ uses the modern type chart, featuring all three new types.
    if generation >= 6:
        version = 0 # Modern type chart.
    elif generation >= 2:
        version = 1 # Revised type chart.
    else:
        version = 2 # Original type chart.
    # We need to get efficiencies for every type.
    # We'll use a dictionary to store the efficiencies.
    efficiencies = {}
    for opponent_type in opponent:
        for move_type in moves:
            # If the move type is within the results of super effective moves, then it's super effective.
            if move_type in __super_effective(opponent_type, attacking=False, revision=version):
                if move_type not in efficiencies:
                    efficiencies[move_type] = 2.0
                else:
                    efficiencies[move_type] *= 2.0
            # It isn't super effective, so we need to check if it's not very effective.
            elif move_type in __least_effective(opponent_type, attacking=False, revision=version):
                if move_type not in efficiencies:
                    efficiencies[move_type] = 0.5
                else:
                    efficiencies[move_type] *= 0.5
            # Not very effective either, so we need to check if it's immune.
            elif move_type in __immune(opponent_type, attacking=False, revision=version):
                if move_type not in efficiencies:
                    efficiencies[move_type] = 0
                else:
                    efficiencies[move_type] *= 0
            # If the move is not super effective, not very effective, or completely ineffective, it is neutral.
            if move_type not in efficiencies:
                efficiencies[move_type] = 1.0
    # Next, we check if the user list has been provided.
    # If it has, we should apply a STAB bonus to applicable moves.
    if len(user) > 0:
        for move_type in moves:
            if move_type in user:
                efficiencies[move_type] *= 1.5
    # Now that we have all of the efficiencies, we can split them into their respective categories.
    super_effective = {}
    neutral = {}
    not_very_effective = {}
    immune = {}
    # We'll use a for loop to iterate through the efficiencies dictionary.
    for move_type in efficiencies:
        if efficiencies[move_type] > 1:
            # The move has higher than normal effectiveness.
            super_effective[move_type] = efficiencies[move_type]
        elif efficiencies[move_type] == 1:
            # The move has normal effectiveness.
            neutral[move_type] = efficiencies[move_type]
        elif efficiencies[move_type] < 1 and efficiencies[move_type] > 0:
            # The move has lower than normal effectiveness.
            not_very_effective[move_type] = efficiencies[move_type]
        elif efficiencies[move_type] == 0:
            # The move is completely ineffective.
            immune[move_type] = efficiencies[move_type]
    # Values have been separated into their categories, but remain unsorted!
    # We'll use a function to sort the values.
    super_effective = __sort_values(super_effective, reverse=True)
    neutral = __sort_values(neutral, reverse=True)
    not_very_effective = __sort_values(not_very_effective, reverse=True)
    immune = __sort_values(immune, reverse=True)
    # Now that the values have been sorted, they can either be returned or printed.
    if not print_results:
        return [super_effective, neutral, not_very_effective, immune]
    os.system(f'cmd /c cls')
    print(f'Pokemon Type Calculator - Results')
    print(f'-----------------------------------------------------------------------------------------------------------------')
    print(f'Opponent Types: {", ".join(opponent)}')
    print(f'Move Types: {", ".join(moves)}')
    print(f'-----------------------------------------------------------------------------------------------------------------')
    print(f'Super Effective:')
    ##################
    if len(super_effective) == 0:
        print(f' - None')
    ##################
    for move_type in super_effective:
        if move_type in user:
            print(f' - {move_type.capitalize()}: {super_effective[move_type]}x (STAB)')
            continue
        print(f' - {move_type.capitalize()}: {super_effective[move_type]}x')
    print(f'-=-=-=-')
    print(f'Neutral:')
    ##################
    if len(neutral) == 0:
        print(f' - None')
    ##################
    for move_type in neutral:
        # We don't need to check for STAB here, as neutral moves are never STAB.
        print(f' - {move_type.capitalize()}: {neutral[move_type]}x')
    print(f'-=-=-=-')
    print(f'Not Very Effective:')
    ##################
    if len(not_very_effective) == 0:
        print(f' - None')
    ##################
    for move_type in not_very_effective:
        if move_type in user:
            print(f' - {move_type.capitalize()}: {not_very_effective[move_type]}x (STAB)')
            continue
        print(f' - {move_type.capitalize()}: {not_very_effective[move_type]}x')
    print(f'-=-=-=-')
    print(f'Immune:')
    ##################
    if len(immune) == 0:
        print(f' - None')
    ##################
    for move_type in immune:
        # We don't need to check for STAB here, as immune moves are never STAB.
        print(f' - {move_type.capitalize()}: {immune[move_type]}x')
    print(f'-----------------------------------------------------------------------------------------------------------------')
    input(f'Press ENTER to return to your previous menu.')
    return [super_effective, neutral, not_very_effective, immune]

def __super_effective(type : str, attacking : bool = True, revision : int = -1) -> list:
    '''
    Given a type, return a list of types that are super effective, either when attacking or defending.

    Arguments:
        type (str): The type to check.
        attacking (bool): Dictate whether the provided type is attacking (True), or defending (False).
        revision (int): The revision of the type chart to use. Defaults to the latest revision (-1 or 0), where other options are Gen 2-5 (1) and Gen 1 (2).
    Returns:
        list: A list of types that are super effective against the provided type.
    '''
    # Convert the type to lowercase to avoid any issues.
    type = type.lower()

    # Type should be treated as the ATTACKING type.
    if attacking:
        # Start type checking
        if type == "normal":
            # Normal is not super effective AGAINST any type.
            pass
        elif type == "fire":
            if revision == 1:
                # Gen 2-5, in this case, same as Gen 6+.
                pass
            elif revision == 2:
                # Gen 1, no Steel
                return ["grass", "ice", "bug"]
            return ["grass", "ice", "bug", "steel"]
        elif type == "water":
            if revision == 1 or revision == 2:
                # Gen 1-5, in this case, same as Gen 6+.
                pass
            return ["fire", "ground", "rock"]
        elif type == "electric":
            if revision == 1 or revision == 2:
                # Gen 1-5, in this case, same as Gen 6+.
                pass
            return ["water", "flying"]
        elif type == "grass":
            if revision == 1 or revision == 2:
                # Gen 1-5, in this case, same as Gen 6+.
                pass
            return ["water", "ground", "rock"]
        elif type == "ice":
            if revision == 1 or revision == 2:
                # Gen 1-5, in this case, same as Gen 6+.
                pass
            return ["grass", "ground", "flying", "dragon"]
        elif type == "fighting":
            if revision == 1:
                # Gen 2-5, in this case, same as Gen 6+.
                pass
            elif revision == 2:
                # Gen 1, no Steel.
                return ["normal", "ice", "rock", "dark"]
            return ["normal", "ice", "rock", "dark", "steel"]
        elif type == "poison":
            if revision == 1:
                # Gen 2-5, no Fairy.
                return ["grass"]
            elif revision == 2:
                # Gen 1, slight modification to be super effective against Bug.
                return ["grass", "bug"]
            return ["grass", "fairy"]
        elif type == "ground":
            if revision == 1:
                # Gen 2-5, in this case, same as Gen 6+.
                pass
            elif revision == 2:
                # Gen 1, no Steel.
                return ["fire", "electric", "poison", "rock"]
            return ["fire", "electric", "poison", "rock", "steel"]
        elif type == "flying":
            if revision == 1 or revision == 2:
                # Gen 1-5, in this case, same as Gen 6+.
                pass
            return ["grass", "fighting", "bug"]
        elif type == "psychic":
            if revision == 1 or revision == 2:
                # Gen 1-5, in this case, same as Gen 6+.
                pass
            return ["fighting", "poison"]
        elif type == "bug":
            if revision == 1:
                # Gen 2-5, in this case, same as Gen 6+.
                pass
            elif revision == 2:
                # Gen 1, no Dark and slight modification to be super effective against Poison.
                return ["grass", "poison", "psychic"]
            return ["grass", "psychic", "dark"]
        elif type == "rock":
            if revision == 1 or revision == 2:
                # Gen 1-5, in this case, same as Gen 6+.
                pass
            return ["fire", "ice", "flying", "bug"]
        elif type == "ghost":
            if revision == 1:
                # Gen 2-5, in this case, same as Gen 6+.
                pass
            elif revision == 2:
                # Gen 1, immune to Psychic instead of super effective due to programming error.
                return ["ghost"]
            return ["psychic", "ghost"]
        elif type == "dragon":
            if revision == 1 or revision == 2:
                # Gen 1-5, in this case, same as Gen 6+.
                pass
            return ["dragon"]
        elif type == "dark":
            if revision == 1:
                # Gen 2-5, in this case, same as Gen 6+.
                pass
            elif revision == 2:
                # Gen 1, Dark type does not exist.
                return []
            return ["psychic", "ghost"]
        elif type == "steel":
            if revision == 1:
                # Gen 2-5, no Fairy.
                return ["ice", "rock"]
            elif revision == 2:
                # Gen 1, Steel type does not exist.
                return []
            return ["ice", "rock", "fairy"]
        elif type == "fairy":
            if revision == 1 or revision == 2:
                # Gen 1-5, Fairy type does not exist.
                return []
            return ["fighting", "dragon", "dark"]
        # If we get here, the type is invalid.
        return []
    
    # Type should be treated as the DEFENDING type.
    if type == "normal":
        if revision == 1 or revision == 2:
            # Gen 1-5, in this case, same as Gen 6+.
            pass
        return ["fighting"]
    elif type == "fire":
        if revision == 1 or revision == 2:
            # Gen 1-5, in this case, same as Gen 6+.
            pass
        return ["water", "ground", "rock"]
    elif type == "water":
        if revision == 1 or revision == 2:
            # Gen 1-5, in this case, same as Gen 6+.
            pass
        return ["electric", "grass"]
    elif type == "electric":
        if revision == 1 or revision == 2:
            # Gen 1-5, in this case, same as Gen 6+.
            pass
        return ["ground"]
    elif type == "grass":
        if revision == 1 or revision == 2:
            # Gen 1-5, in this case, same as Gen 6+.
            pass
        return ["fire", "ice", "poison", "flying", "bug"]
    elif type == "ice":
        if revision == 1:
            # Gen 2-5, in this case, same as Gen 6+.
            pass
        elif revision == 2:
            # Gen 1, no Steel.
            return ["fire", "fighting", "rock"]
        return ["fire", "fighting", "rock", "steel"]
    elif type == "fighting":
        if revision == 1 or revision == 2:
            # Gen 1-5, no Fairy.
            return ["flying", "psychic"]
        return ["flying", "psychic", "fairy"]
    elif type == "poison":
        if revision == 1:
            # Gen 2-5, in this case, same as Gen 6+.
            pass
        elif revision == 2:
            # Gen 1, slight modification for Bug to be super effective.
            return ["ground", "psychic", "bug"]
        return ["ground", "psychic"]
    elif type == "ground":
        if revision == 1 or revision == 2:
            # Gen 1-5, in this case, same as Gen 6+.
            pass
        return ["water", "grass", "ice"]
    elif type == "flying":
        if revision == 1 or revision == 2:
            # Gen 1-5, in this case, same as Gen 6+.
            pass
        return ["electric", "ice", "rock"]
    elif type == "psychic":
        if revision == 1:
            # Gen 2-5, in this case, same as Gen 6+.
            pass
        elif revision == 2:
            # Gen 1, no Dark and slight modification to be immune to Ghost.
            return ["bug"]
        return ["bug", "ghost", "dark"]
    elif type == "bug":
        if revision == 1:
            # Gen 2-5, in this case, same as Gen 6+.
            pass
        elif revision == 2:
            # Gen 1, slight modification for Poison to be super effective.
            return ["fire", "poison", "flying", "rock"]
        return ["fire", "flying", "rock"]
    elif type == "rock":
        if revision == 1:
            # Gen 2-5, in this case, same as Gen 6+.
            pass
        elif revision == 2:
            # Gen 1, no Steel.
            return ["water", "grass", "fighting", "ground"]
        return ["water", "grass", "fighting", "ground", "steel"]
    elif type == "ghost":
        if revision == 1:
            # Gen 2-5, in this case, same as Gen 6+.
            pass
        elif revision == 2:
            # Gen 1, no Dark.
            return ["ghost"]
        return ["ghost", "dark"]
    elif type == "dragon":
        if revision == 1 or revision == 2:
            # Gen 1-5, no Fairy.
            return ["ice", "dragon"]
        return ["ice", "dragon", "fairy"]
    elif type == "dark":
        if revision == 1:
            # Gen 2-5, no Fairy.
            return ["fighting", "bug"]
        elif revision == 2:
            # Gen 1, Dark type does not exist.
            return []
        return ["fighting", "bug", "fairy"]
    elif type == "steel":
        if revision == 1:
            # Gen 2-5, in this case, same as Gen 6+.
            pass
        elif revision == 2:
            # Gen 1, Steel type does not exist.
            return []
        return ["fire", "fighting", "ground"]
    elif type == "fairy":
        if revision == 1 or revision == 2:
            # Gen 1-5, Fairy type does not exist.
            return []
        return ["poison", "steel"]
    # If we get here, the type is invalid.
    return []

def __least_effective(type : str, attacking : bool = True, revision : int = -1) -> list:
    '''
    Given a type, return a list of types that are least effective, either when attacking or defending.

    Arguments:
        type (str): The type to check.
        attacking (bool): Dictate whether the provided type is attacking (True), or defending (False).
        revision (int): The revision of the type chart to use. Defaults to the latest revision (-1 or 0), where other options are Gen 2-5 (1) and Gen 1 (2).
    Returns:
        list: A list of types that are least effective against the provided type.
    '''
    # Convert the type to lowercase to avoid any issues.
    type = type.lower()

    # Type should be treated as the ATTACKING type.
    if attacking:
        if type == "normal":
            if revision == 1 or revision == 2:
                # Gen 1-5, in this case, same as Gen 6+.
                pass
            return ["rock", "steel"]
        elif type == "fire":
            if revision == 1 or revision == 2:
                # Gen 1-5, in this case, same as Gen 6+.
                pass
            return ["fire", "water", "rock", "dragon"]
        elif type == "water":
            if revision == 1 or revision == 2:
                # Gen 1-5, in this case, same as Gen 6+.
                pass
            return ["water", "grass", "dragon"]
        elif type == "electric":
            if revision == 1 or revision == 2:
                # Gen 1-5, in this case, same as Gen 6+.
                pass
            return ["electric", "grass", "dragon"]
        elif type == "grass":
            if revision == 1:
                # Gen 2-5, in this case, same as Gen 6+.
                pass
            elif revision == 2:
                # Gen 1, no Steel.
                return ["fire", "grass", "poison", "flying", "bug", "dragon"]
            return ["fire", "grass", "poison", "flying", "bug", "dragon", "steel"]
        elif type == "ice":
            if revision == 1:
                # Gen 2-5, in this case, same as Gen 6+.
                pass
            elif revision == 2:
                # Gen 1, no Steel and slight modification to be normal effectiveness against Fire.
                return ["water", "ice"]
            return ["fire", "water", "ice", "steel"]
        elif type == "fighting":
            if revision == 1 or revision == 2:
                # Gen 1-5, no Fairy.
                return ["poison", "flying", "psychic", "bug"]
            return ["poison", "flying", "psychic", "bug", "fairy"]
        elif type == "poison":
            if revision == 1 or revision == 2:
                # Gen 1-5, in this case, same as Gen 6+.
                pass
            return ["poison", "ground", "rock", "ghost"]
        elif type == "ground":
            if revision == 1 or revision == 2:
                # Gen 1-5, in this case, same as Gen 6+.
                pass
            return ["grass", "bug"]
        elif type == "flying":
            if revision == 1:
                # Gen 2-5, in this case, same as Gen 6+.
                pass
            elif revision == 2:
                # Gen 1, no Steel.
                return ["electric", "rock"]
            return ["electric", "rock", "steel"]
        elif type == "psychic":
            if revision == 1:
                # Gen 2-5, in this case, same as Gen 6+.
                pass
            elif revision == 2:
                # Gen 1, no Steel.
                return ["psychic"]
            return ["psychic", "steel"]
        elif type == "bug":
            if revision == 1:
                # Gen 2-5, no Fairy.
                return ["fire", "fighting", "poison", "flying", "ghost", "steel"]
            elif revision == 2:
                # Gen 1, no Steel or Fairy, as well as a slight modification to be super effective against Poison.
                return ["fire", "fighting", "flying", "ghost"]
            return ["fire", "fighting", "poison", "flying", "ghost", "steel", "fairy"]
        elif type == "rock":
            if revision == 1:
                # Gen 2-5, in this case, same as Gen 6+.
                pass
            elif revision == 2:
                # Gen 1, no Steel.
                return ["fighting", "ground"]
            return ["fighting", "ground", "steel"]
        elif type == "ghost":
            if revision == 1:
                # Gen 2-5, slight modification to be not too effective against Steel.
                return ["dark", "steel"]
            elif revision == 2:
                # Gen 1, Ghost has no weaknesses (only immunities).
                return []
            return ["dark"]
        elif type == "dragon":
            if revision == 1:
                # Gen 2-5, in this case, same as Gen 6+.
                pass
            elif revision == 2:
                # Gen 1, no Steel, thus Dragon has no weaknesses.
                return []
            return ["steel"]
        elif type == "dark":
            if revision == 1:
                # Gen 2-5, no Fairy as well as a slight modification to be not too effective against Steel.
                return ["fighting", "dark", "steel"]
            elif revision == 2:
                # Gen 1, Dark type does not exist.
                return []
            return ["fighting", "dark", "fairy"]
        elif type == "steel":
            if revision == 1:
                # Gen 2-5, in this case, same as Gen 6+.
                pass
            elif revision == 2:
                # Gen 1, Steel type does not exist.
                return []
            return ["fire", "water", "electric", "steel"]
        elif type == "fairy":
            if revision == 1 or revision == 2:
                # Gen 1-5, Fairy type does not exist.
                return []
            return ["fire", "poison", "steel"]
        # If we get here, the type is invalid or has no less effective types.
        return []

    # Type should be treated as the DEFENDING type.
    if type == "normal":
        # Normal has no weaknesses (only immunities).
        pass
    elif type == "fire":
        if revision == 1:
            # Gen 2-5, no Fairy.
            return ["fire", "grass", "ice", "bug", "steel"]
        elif revision == 2:
            # Gen 1, no Fairy or Steel, as well as a slight modification for Ice to be normal effectiveness.
            return ["fire", "grass", "bug"]
        return ["fire", "grass", "ice", "bug", "steel", "fairy"]
    elif type == "water":
        if revision == 1:
            # Gen 2-5, in this case, same as Gen 6+.
            pass
        elif revision == 2:
            # Gen 1, no Steel.
            return ["fire", "water", "ice"]
        return ["fire", "water", "ice", "steel"]
    elif type == "electric":
        if revision == 1:
            # Gen 2-5, in this case, same as Gen 6+.
            pass
        elif revision == 2:
            # Gen 1, no Steel.
            return ["electric", "flying"]
        return ["electric", "flying", "steel"]
    elif type == "grass":
        if revision == 1 or revision == 2:
            # Gen 1-5, in this case, same as Gen 6+.
            pass
        return ["water", "electric", "grass", "ground"]
    elif type == "ice":
        if revision == 1 or revision == 2:
            # Gen 1-5, in this case, same as Gen 6+.
            pass
        return ["ice"]
    elif type == "fighting":
        if revision == 1:
            # Gen 2-5, in this case, same as Gen 6+.
            pass
        elif revision == 2:
            # Gen 1, no Dark.
            return ["bug", "rock"]
        return ["bug", "rock", "dark"]
    elif type == "poison":
        if revision == 1:
            # Gen 2-5, no Fairy.
            return ["grass", "fighting", "poison", "bug"]
        elif revision == 2:
            # Gen 1, no Fairy as well as a slight modification for Bug to be super effective.
            return ["grass", "fighting", "poison"]
        return ["grass", "fighting", "poison", "bug", "fairy"]
    elif type == "ground":
        if revision == 1 or revision == 2:
            # Gen 1-5, in this case, same as Gen 6+.
            pass
        return ["poison", "rock"]
    elif type == "flying":
        if revision == 1 or revision == 2:
            # Gen 1-5, in this case, same as Gen 6+.
            pass
        return ["grass", "fighting", "bug"]
    elif type == "psychic":
        if revision == 1 or revision == 2:
            # Gen 1-5, in this case, same as Gen 6+.
            pass
        return ["fighting", "psychic"]
    elif type == "bug":
        if revision == 1 or revision == 2:
            # Gen 1-5, in this case, same as Gen 6+.
            pass
        return ["grass", "fighting", "ground"]
    elif type == "rock":
        if revision == 1 or revision == 2:
            # Gen 1-5, in this case, same as Gen 6+.
            pass
        return ["normal", "fire", "poison", "flying"]
    elif type == "ghost":
        if revision == 1 or revision == 2:
            # Gen 1-5, in this case, same as Gen 6+.
            pass
        return ["poison", "bug"]
    elif type == "dragon":
        if revision == 1 or revision == 2:
            # Gen 1-5, in this case, same as Gen 6+.
            pass
        return ["fire", "water", "electric", "grass"]
    elif type == "dark":
        if revision == 1:
            # Gen 2-5, in this case, same as Gen 6+.
            pass
        elif revision == 2:
            # Gen 1, Dark type does not exist.
            return []
        return ["ghost", "dark"]
    elif type == "steel":
        if revision == 1:
            # Gen 2-5, no Fairy, as well as a slight modification for Ghost and Dark to be not very effective.
            return ["normal", "grass", "ice", "flying", "psychic", "bug", "rock", "ghost", "dragon", "dark", "steel"]
        elif revision == 2:
            # Gen 1, Steel type does not exist.
            return []
        return ["normal", "grass", "ice", "flying", "psychic", "bug", "rock", "dragon", "steel", "fairy"]
    elif type == "fairy":
        if revision == 1 or revision == 2:
            # Gen 1-5, Fairy type does not exist.
            return []
        return ["fighting", "bug", "dark"]
    # If we get here, the type is invalid or has no weaknesses.
    return []

def __immune(type : str, attacking : bool = True, revision : int = -1) -> list:
    '''
    Given a type, return a list of types that are immune, either when attacking or defending.

    Arguments:
        type (str): The type to check.
        attacking (bool): Dictate whether the provided type is attacking (True), or defending (False).
        revision (int): The revision of the type chart to use. Defaults to the latest revision (-1 or 0), where other options are Gen 2-5 (1) and Gen 1 (2).
    Returns:
        list: A list of types that are immune to the provided type.
    '''
    # Convert the type to lowercase to avoid any issues.
    type = type.lower()

    # Type should be treated as the ATTACKING type.
    if attacking:
        if type == "normal":
            if revision == 1 or revision == 2:
                # Gen 1-5, in this case, same as Gen 6+.
                pass
            return ["ghost"]
        elif type == "fire":
            # Fire is not immune AGAINST anything.
            pass
        elif type == "water":
            # Water is not immune AGAINST anything.
            pass
        elif type == "electric":
            if revision == 1 or revision == 2:
                # Gen 1-5, in this case, same as Gen 6+.
                pass
            return ["ground"]
        elif type == "grass":
            # Grass is not immune AGAINST anything.
            pass
        elif type == "ice":
            # Ice is not immune AGAINST anything.
            pass
        elif type == "fighting":
            if revision == 1 or revision == 2:
                # Gen 1-5, in this case, same as Gen 6+.
                pass
            return ["ghost"]
        elif type == "poison":
            if revision == 1:
                # Gen 2-5, in this case, same as Gen 6+.
                pass
            elif revision == 2:
                # Gen 1, no Steel.
                return []
            return ["steel"]
        elif type == "ground":
            if revision == 1 or revision == 2:
                # Gen 1-5, in this case, same as Gen 6+.
                pass
            return ["flying"]
        elif type == "flying":
            # Flying is not immune AGAINST anything.
            pass
        elif type == "psychic":
            if revision == 1:
                # Gen 2-5, in this case, same as Gen 6+.
                pass
            elif revision == 2:
                # Gen 1, no Dark.
                return []
            return ["dark"]
        elif type == "bug":
            # Bug is not immune AGAINST anything.
            pass
        elif type == "rock":
            # Rock is not immune AGAINST anything.
            pass
        elif type == "ghost":
            if revision == 1:
                # Gen 2-5, in this case, same as Gen 6+.
                pass
            elif revision == 2:
                # Gen 1, slight modification for Psychic to be immune.
                return ["normal", "psychic"]
            return ["normal"]
        elif type == "dragon":
            if revision == 1 or revision == 2:
                # Gen 1-5, no Fairy.
                return []
            return ["fairy"]
        elif type == "dark":
            if revision == 1:
                # Gen 2-5, in this case, same as Gen 6+.
                pass
            elif revision == 2:
                # Gen 1, Dark type does not exist.
                return []
            # Dark is not immune AGAINST anything.
            pass
        elif type == "steel":
            if revision == 1:
                # Gen 2-5, in this case, same as Gen 6+.
                pass
            elif revision == 2:
                # Gen 1, Steel type does not exist.
                return []
            # Steel is not immune AGAINST anything.
            pass
        elif type == "fairy":
            if revision == 1 or revision == 2:
                # Gen 1-5, Fairy type does not exist.
                return []
            # Fairy is not immune AGAINST anything.
            pass
        # If we get here, the type is invalid or has no immunities.
        return []

    # Type should be treated as the DEFENDING type.
    if type == "normal":
        if revision == 1 or revision == 2:
            # Gen 1-5, in this case, same as Gen 6+.
            pass
        return ["ghost"]
    elif type == "fire":
        # Fire is not immune TO anything.
        pass
    elif type == "water":
        # Water is not immune TO anything.
        pass
    elif type == "electric":
        # Electric is not immune TO anything.
        pass
    elif type == "grass":
        # Grass is not immune TO anything.
        pass
    elif type == "ice":
        # Ice is not immune TO anything.
        pass
    elif type == "fighting":
        # Fighting is not immune TO anything.
        pass
    elif type == "poison":
        # Poison is not immune TO anything.
        pass
    elif type == "ground":
        if revision == 1 or revision == 2:
            # Gen 1-5, in this case, same as Gen 6+.
            pass
        return ["electric"]
    elif type == "flying":
        if revision == 1 or revision == 2:
            # Gen 1-5, in this case, same as Gen 6+.
            pass
        return ["ground"]
    elif type == "psychic":
        if revision == 1:
            # Gen 2-5, in this case, same as Gen 6+.
            pass
        elif revision == 2:
            # Gen 1, slight modification for Ghost to be immune.
            return ["ghost"]
        # Psychic is not immune TO anything.
        pass
    elif type == "bug":
        # Bug is not immune TO anything.
        pass
    elif type == "rock":
        # Rock is not immune TO anything.
        pass
    elif type == "ghost":
        if revision == 1 or revision == 2:
            # Gen 1-5, in this case, same as Gen 6+.
            pass
        return ["normal", "fighting"]
    elif type == "dragon":
        # Dragon is not immune TO anything.
        pass
    elif type == "dark":
        if revision == 1:
            # Gen 2-5, in this case, same as Gen 6+.
            pass
        elif revision == 2:
            # Gen 1, Dark type does not exist.
            return []
        return ["psychic"]
    elif type == "steel":
        if revision == 1:
            # Gen 2-5, in this case, same as Gen 6+.
            pass
        elif revision == 2:
            # Gen 1, Steel type does not exist.
            return []
        return ["poison"]
    elif type == "fairy":
        if revision == 1 or revision == 2:
            # Gen 1-5, Fairy type does not exist.
            return []
        return ["dragon"]
    # If we get here, the type is invalid or has no immunities.
    return []

def __sort_values(dictionary : dict, reverse : bool = False) -> dict:
    '''
    Sort a dictionary by its values.

    Arguments:
        dictionary (dict): The dictionary to sort.
        reverse (bool): Whether to sort in reverse order (descending order).
    Returns:
        dict: The sorted dictionary.
    '''
    value_key_pairs = ((value, key) for (key, value) in dictionary.items())
    sorted_pairs = sorted(value_key_pairs, reverse=reverse)
    return {k: v for v, k in sorted_pairs}

# If this file is ran standalone, run the script() function automagicly.
if __name__ == "__main__":
    script()