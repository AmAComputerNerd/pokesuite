import os

opponent_type = []
available_move_types = []

'''
main()
    > Main function loop for program
'''
def main():
    global opponent_type, available_move_types
    while True:
        opponent_type = []
        available_move_types = []
        os.system("cmd /c cls")
        print("Welcome to the Pokemon Type Calculator!")
        print("This program will calculate the most effective type of move to use against a Pokemon opponent.")
        print("----------------------------------------")
        print("Please enter the type(s) of the opponent Pokemon. If there are multiple types, separate them with a comma and space.")
        opponent_type = input(f' > Types are... ').lower().split(", ")
        print("Please enter the type(s) of the move(s) you have available. If there are multiple types, separate them with a comma and space.")
        available_move_types = input(f' > Types are... ').lower().split(", ")
        print("----------------------------------------")
        most_effective, least_effective, immune = splitMoveEfficiencies(calculateMoveEfficiencies())
        os.system("cmd /c cls")
        print("The most effective move(s) to use against this opponent are:")
        for move_type in sortDict(most_effective):
            print(f" > {move_type} ({sortDict(most_effective)[move_type]}x DMG)")
        print("The least effective move(s) to use against this opponent are:")
        for move_type in sortDict(least_effective):
            print(f" > {move_type} ({sortDict(least_effective)[move_type]}x DMG)")
        print("The move(s) that are immune against this opponent are:")
        for move_type in sortDict(immune):
            print(f" > {move_type} ({sortDict(immune)[move_type]}x DMG)")
        print("----------------------------------------")
        print("Would you like to calculate another type matchup?")
        if input(" > ").lower() in ["no", "n"]:
            break

'''
sortDict(dictionary : dict)
    > Sorts a dictionary by value
@param dictionary the dictionary to sort
@return the sorted dictionary
'''
def sortDict(dictionary : dict):
    value_key_pairs = ((value, key) for (key, value) in dictionary.items())
    sorted_pairs = sorted(value_key_pairs, reverse=True)
    return {k: v for v, k in sorted_pairs}

'''
splitMoveEfficiencies(move_efficiencies : dict)
    > Splits a dictionary of move efficiencies into three dictionaries: most effective, least effective, and immune
@param move_efficiencies the dictionary of move efficiencies
@return a tuple of three dictionaries: most effective, least effective, and immune
'''
def splitMoveEfficiencies(move_efficiencies : dict):
    most_effective = {}
    least_effective = {}
    immune = {}
    for move_type in move_efficiencies:
        if move_efficiencies[move_type] >= 1:
            most_effective[move_type] = move_efficiencies[move_type]
        elif move_efficiencies[move_type] < 1 and move_efficiencies[move_type] > 0:
            least_effective[move_type] = move_efficiencies[move_type]
        else:
            immune[move_type] = move_efficiencies[move_type]
    return most_effective, least_effective, immune

'''
calculateMoveEfficiencies()
    > Calculates the move efficiencies of all available moves against the opponent
@return a dictionary of move efficiencies
'''
def calculateMoveEfficiencies():
    global opponent_type, available_move_types
    move_efficiencies = {}
    for move_type in available_move_types:
        move_efficiencies[move_type] = calculateMoveEfficiency(move_type, opponent_type)
    return move_efficiencies

'''
calculateMoveEfficiency(move_type : str, opponent_types : list)
    > Calculates the move efficiency of a specified move against a list of opponent types
@param move_type the type of the move
@param opponent_types the list of opponent types
'''
def calculateMoveEfficiency(move_type : str, opponent_types : list):
    efficiency = 1.0
    for type in opponent_types:
        if move_type in getMostEffective(type):
            efficiency *= 2
        elif move_type in getLeastEffective(type):
            efficiency *= 0.5
        elif move_type in getImmune(type):
            efficiency *= 0
    return efficiency

'''
getMostEffective(opponent : str)
    > Returns a list of types that are most effective against a specified defending type
@param opponent the defending type
@return a list of types that are most effective against the defending type
'''
def getMostEffective(opponent : str):
    if opponent == "normal":
        return ["fighting"]
    elif opponent == "fire":
        return ["water", "ground", "rock"]
    elif opponent == "water":
        return ["grass", "electric"]
    elif opponent == "electric":
        return ["ground"]
    elif opponent == "grass":
        return ["fire", "ice", "poison", "flying", "bug"]
    elif opponent == "ice":
        return ["fire", "fighting", "rock", "steel"]
    elif opponent == "fighting":
        return ["flying", "psychic", "fairy"]
    elif opponent == "poison":
        return ["ground", "psychic"]
    elif opponent == "ground":
        return ["water", "grass", "ice"]
    elif opponent == "flying":
        return ["electric", "ice", "rock"]
    elif opponent == "psychic":
        return ["bug", "ghost", "dark"]
    elif opponent == "bug":
        return ["fire", "flying", "rock"]
    elif opponent == "rock":
        return ["water", "grass", "fighting", "ground", "steel"]
    elif opponent == "ghost":
        return ["ghost", "dark"]
    elif opponent == "dragon":
        return ["ice", "dragon", "fairy"]
    elif opponent == "dark":
        return ["fighting", "bug", "fairy"]
    elif opponent == "steel":
        return ["fire", "fighting", "ground"]
    elif opponent == "fairy":
        return ["poison", "steel"]

'''
getLeastEffective(opponent : str)
    > Returns a list of types that are least effective against a specified defending type
@param opponent the defending type
@return a list of types that are least effective against the defending type
'''
def getLeastEffective(opponent : str):
    if opponent == "normal":
        return []
    elif opponent == "fire":
        return ["fire", "grass", "ice", "bug", "steel", "fairy"]
    elif opponent == "water":
        return ["fire", "water", "ice", "steel"]
    elif opponent == "electric":
        return ["electric", "flying", "steel"]
    elif opponent == "grass":
        return ["water", "electric", "grass", "ground"]
    elif opponent == "ice":
        return ["ice"]
    elif opponent == "fighting":
        return ["bug", "rock", "dark"]
    elif opponent == "poison":
        return ["grass", "fighting", "poison", "bug", "fairy"]
    elif opponent == "ground":
        return ["poison", "rock"]
    elif opponent == "flying":
        return ["grass", "fighting", "bug"]
    elif opponent == "psychic":
        return ["fighting", "psychic"]
    elif opponent == "bug":
        return ["grass", "fighting", "ground"]
    elif opponent == "rock":
        return ["normal", "fire", "poison", "flying"]
    elif opponent == "ghost":
        return ["poison", "bug"]
    elif opponent == "dragon":
        return ["fire", "water", "electric", "grass"]
    elif opponent == "dark":
        return ["ghost", "dark"]
    elif opponent == "steel":
        return ["normal", "grass", "ice", "flying", "psychic", "bug", "rock", "dragon", "steel", "fairy"]
    elif opponent == "fairy":
        return ["fighting", "bug", "dark"]
    return []

'''
getImmune(opponent : str)
    > Returns a list of types that are immune against a specified defending type
@param opponent the defending type
@return a list of types that are immune against the defending type
'''
def getImmune(opponent : str):
    if opponent == "normal":
        return ["ghost"]
    elif opponent == "fire":
        return []
    elif opponent == "water":
        return []
    elif opponent == "electric":
        return []
    elif opponent == "grass":
        return []
    elif opponent == "ice":
        return []
    elif opponent == "fighting":
        return []
    elif opponent == "poison":
        return []
    elif opponent == "ground":
        return ["electric"]
    elif opponent == "flying":
        return ["ground"]
    elif opponent == "psychic":
        return []
    elif opponent == "bug":
        return []
    elif opponent == "rock":
        return []
    elif opponent == "ghost":
        return ["normal", "fighting"]
    elif opponent == "dragon":
        return []
    elif opponent == "dark":
        return ["psychic"]
    elif opponent == "steel":
        return ["poison"]
    elif opponent == "fairy":
        return ["dragon"]

'''
def checkType(type : str, opponent : str):
    if type == "normal":
        if opponent == "ghost":
            return 0
        elif opponent == "rock" or opponent == "steel":
            return 0.5
    elif type == "fire":
        if opponent == "fire" or opponent == "water" or opponent == "rock" or opponent == "dragon":
            return 0.5
        elif opponent == "grass" or opponent == "ice" or opponent == "bug" or opponent == "steel":
            return 2
    elif type == "water":
        if opponent == "water" or opponent == "grass" or opponent == "dragon":
            return 0.5
        elif opponent == "fire" or opponent == "ground" or opponent == "rock":
            return 2
    elif type == "electric":
        if opponent == "ground":
            return 0
        elif opponent == "electric" or opponent == "grass" or opponent == "dragon":
            return 0.5
        elif opponent == "water" or opponent == "flying":
            return 2
    elif type == "grass":
        if opponent == "fire" or opponent == "grass" or opponent == "poison" or opponent == "flying" or opponent == "bug" or opponent == "dragon" or opponent == "steel":
            return 0.5
        elif opponent == "water" or opponent == "ground" or opponent == "rock":
            return 2
    elif type == "ice":
        if opponent == "fire" or opponent == "water" or opponent == "ice" or opponent == "steel":
            return 0.5
        elif opponent == "grass" or opponent == "ground" or opponent == "flying" or opponent == "dragon":
            return 2
    elif type == "fighting":
        if opponent == "ghost":
            return 0
        elif opponent == "poison" or opponent == "flying" or opponent == "psychic" or opponent == "bug" or opponent == "fairy":
            return 0.5
        elif opponent == "normal" or opponent == "ice" or opponent == "rock" or opponent == "dark" or opponent == "steel":
            return 2
    elif type == "poison":
        if opponent == "steel":
            return 0
        elif opponent == "poison" or opponent == "ground" or opponent == "rock" or opponent == "ghost":
            return 0.5
        elif opponent == "grass" or opponent == "fairy":
            return 2
    elif type == "ground":
        if opponent == "flying":
            return 0
        elif opponent == "grass" or opponent == "bug":
            return 0.5
        elif opponent == "fire" or opponent == "electric" or opponent == "poison" or opponent == "rock" or opponent == "steel":
            return 2
    elif type == "flying":
        if opponent == "electric" or opponent == "rock" or opponent == "steel":
            return 0.5
        elif opponent == "grass" or opponent == "fighting" or opponent == "bug":
            return 2
    elif type == "psychic":
        if opponent == "dark":
            return 0
        elif opponent == "psychic" or opponent == "steel":
            return 0.5
        elif opponent == "fighting" or opponent == "poison":
            return 2
    elif type == "bug":
        if opponent == "fire" or opponent == "fighting" or opponent == "poison" or opponent == "flying" or opponent == "ghost" or opponent == "steel" or opponent == "fairy":
            return 0.5
        elif opponent == "grass" or opponent == "psychic" or opponent == "dark":
            return 2
    elif type == "rock":
        if opponent == "fighting" or opponent == "ground" or opponent == "steel":
            return 0.5
        elif opponent == "fire" or opponent == "ice" or opponent == "flying" or opponent == "bug":
            return 2
    elif type == "ghost":
        if opponent == "normal":
            return 0
        elif opponent == "dark":
            return 0.5
        elif opponent == "psychic" or opponent == "ghost":
            return 2
    elif type == "dragon":
        if opponent == "fairy":
            return 0
        elif opponent == "steel":
            return 0.5
        elif opponent == "dragon":
            return 2
    elif type == "dark":
        if opponent == "fighting" or opponent == "dark" or opponent == "fairy":
            return 0.5
        elif opponent == "psychic" or opponent == "ghost":
            return 2
    elif type == "steel":
        if opponent == "fire" or opponent == "water" or opponent == "electric" or opponent == "steel":
            return 0.5
        elif opponent == "ice" or opponent == "rock" or opponent == "fairy":
            return 2
    elif type == "fairy":
        if opponent == "fire" or opponent == "poison" or opponent == "steel":
            return 0.5
        elif opponent == "fighting" or opponent == "dragon" or opponent == "dark":
            return 2
    return 1
'''

'''
allEqual(*, strings)
    > Checks if all provided strings are equal
@param strings the strings to check
@return true if all strings are equal, false otherwise
'''
def allEqual(*, strings):
    string = strings[0]
    for i in strings:
        if string == i:
            continue
        return False
    return True

# run program ONLY if this file is run directly
if __name__ == "__main__":
    main()