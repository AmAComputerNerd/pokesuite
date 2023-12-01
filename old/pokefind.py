import os
import requests
from libraries.Pokemon import Pokemon
from libraries.PokeMove import PokeMove

pokemon : Pokemon = None

def main():
    global pokemon
    while True:
        os.system("cmd /c cls")
        print(f'Welcome to the Pokefind program!')
        print(f'This program will find a Pokemon\'s stats, type, and abilities based on the name you enter.')
        print(f'--------------------------------------------------------------------------------------------')
        print(f'Please enter the name of the Pokemon you would like to find. (ex. Pikachu)\nYou can also enter \'exit\' to exit the program.')
        pokemonName = input(' > ').lower()
        if pokemonName == "exit":
            break
        pokemon = Pokemon(pokemonName)
        if pokemon.get_data() == None:
            print(f'Pokemon not found!')
            input('Press enter to continue...')
            continue
        while True:
            os.system("cmd /c cls")
            print(f'Pokemon found!')
            print(f'--------------------------------------------------------------------------------------------')
            print(f'Name: {pokemon.get_name().capitalize()}')
            print(f'ID: {pokemon.get_id()}')
            print(f'Type(s): {pokemon.get_types()}')
            print(f'---')
            print(f'What would you like to do?')
            print(f'    [1] View it\'s possible abilities.')
            print(f'    [2] Check it\'s possible moves.')
            print(f'    [3] See it\'s default stats.')
            print(f'    [4] View the evolution chain of the Pokemon.')
            print(f'    [5] Fetch it\'s sprite (URL).')
            print(f'    [6] Check other special factors.')
            print(f'    [7] That\'s all for now (return).')
            choice = input(' > ')
            if choice == "1":
                # User selected to view the Pokemon's possible abilities.
                runAbilityLogic()
            elif choice == "2":
                # User selected to view the Pokemon's possible moves.
                runMoveLogic()
            elif choice == "3":
                # User selected to view the Pokemon's default stats.
                runStatLogic()
            elif choice == "4":
                # User selected to view the Pokemon's evolution family.
                runFamilyLogic()
            elif choice == "5":
                # User selected to view the Pokemon's sprite.
                runSpriteLogic()
            elif choice == "6":
                # User selected to view the Pokemon's special factors.
                runSpecialLogic()
            elif choice == "7":
                break

def runAbilityLogic():
    global pokemon
    while True:
        os.system("cmd /c cls")
        print(f'View {pokemon.get_name()}\'s abilities!')
        print(f'--------------------------------------------------------------------------------------------')
        print(f'What would you like to do?')
        print(f'    [1] View all abilities.')
        print(f'    [2] Check whether or not the Pokemon has a certain ability.')
        print(f'    [3] That\'s all for now (return).')
        choice = input(' > ')
        if choice == "1":
            # User selected to view all the Pokemon's abilities.
            os.system("cmd /c cls")
            print(f'View {pokemon.get_name()}\'s abilities!')
            print(f'--------------------------------------------------------------------------------------------')
            print(f'All of {pokemon.get_name()}\'s abilities are:')
            for ability in pokemon.get_abilities():
                print(f' - {ability}')
            print(f'--------------------------------------------------------------------------------------------')
            input('Press enter to continue...')
        elif choice == "2":
            # User selected to check if the Pokemon has a certain ability.
            os.system("cmd /c cls")
            print(f'Check if {pokemon.get_name()} has a certain ability!')
            print(f'--------------------------------------------------------------------------------------------')
            print(f'Please enter the name of the ability you would like to check for.')
            abilityName = input(' > ').lower()
            if pokemon.has_ability(abilityName):
                print(f'{pokemon.get_name()} has the ability {abilityName}!')
            else:
                print(f'{pokemon.get_name()} does not have the ability {abilityName}!')
            print(f'--------------------------------------------------------------------------------------------')
            input('Press enter to continue...')
        elif choice == "3":
            break

def runMoveLogic():
    global pokemon
    while True:
        os.system("cmd /c cls")
        print(f'View {pokemon.get_name()}\'s moves!')
        print(f'--------------------------------------------------------------------------------------------')
        print(f'What would you like to do?')
        print(f'    [1] View all moves.')
        print(f'    [2] Check whether or not the Pokemon has a certain move.')
        print(f'    [3] That\'s all for now (return).')
        choice = input(' > ')
        if choice == "1":
            # User selected to view all the Pokemon's moves.
            os.system("cmd /c cls")
            print(f'View {pokemon.get_name()}\'s moves!')
            print(f'--------------------------------------------------------------------------------------------')
            print(f'All of {pokemon.get_name()}\'s moves are:')
            for move in pokemon.get_moves():
                print(f' - {move} ({move.get_damage} {move.get_type} DMG)')
            print(f'--------------------------------------------------------------------------------------------')
            input('Press enter to continue...')
        elif choice == "2":
            # User selected to check if the Pokemon has a certain move.
            os.system("cmd /c cls")
            print(f'Check if {pokemon.get_name()} has a certain move!')
            print(f'--------------------------------------------------------------------------------------------')
            print(f'Please enter the name of the move you would like to check for.')
            moveName = input(' > ').lower()
            if pokemon.has_move(moveName):
                print(f'{pokemon.get_name()} has the move {moveName}!')
            else:
                print(f'{pokemon.get_name()} does not have the move {moveName}!')
            print(f'--------------------------------------------------------------------------------------------')
            print(f'Would you like to view more information about this move? (y/n)')
            choice = input(' > ')
            if choice.lower() in ["no", "n"]:
                continue
            move = PokeMove(moveName)
            os.system("cmd /c cls")
            print(f'View more information about \'{moveName}\'!')
            print(f'--------------------------------------------------------------------------------------------')
            print(f'Name: {moveName}')
            print(f'ID: {move.get_id()}')
            print(f'Power: {move.get_damage()}')
            print(f'Accuracy: {move.get_accuracy()}')
            print(f'PP: {move.get_pp()}')
            print(f'Priority: {move.get_priority()}')
            print(f'Type: {move.get_type()}')
            print(f'--------------------------------------------------------------------------------------------')
            print(f'Description: {move.get_description()}')
            print(f'--------------------------------------------------------------------------------------------')
            input('Press enter to continue...')
        elif choice == "3":
            break

def runStatLogic():
    global pokemon
    os.system("cmd /c cls")
    print(f'View {pokemon.get_name()}\'s stats!')
    print(f'--------------------------------------------------------------------------------------------')
    print(f'Health: {pokemon.get_stats()["health"]}')
    print(f'Attack: {pokemon.get_stats()["attack"]}')
    print(f'Defense: {pokemon.get_stats()["defense"]}')
    print(f'Special Attack: {pokemon.get_stats()["specialAttack"]}')
    print(f'Special Defense: {pokemon.get_stats()["specialDefense"]}')
    print(f'Speed: {pokemon.get_stats()["speed"]}')
    print(f'--------------------------------------------------------------------------------------------')
    input('Press enter to continue...')

def runFamilyLogic():
    global pokemon
    while True:
        os.system("cmd /c cls")
        print(f'View {pokemon.get_name()}\'s evolution family!')
        print(f'--------------------------------------------------------------------------------------------')
        print(f'What would you like to do?')
        print(f'    [1] View parent Pokemon.')
        print(f'    [2] View child Pokemon.')
        print(f'    [3] That\'s all for now (return).')
        choice = input(' > ')
        if choice == "1":
            # User selected to view all the Pokemon's parent Pokemon.
            os.system("cmd /c cls")
            print(f'View {pokemon.get_name()}\'s parent Pokemon!')
            print(f'--------------------------------------------------------------------------------------------')
            print(f'The parent Pokemon of {pokemon.get_name()} are:')
            for parent in pokemon.get_parent():
                print(f' <=> {parent}')
                print(f'    - ID: {parent.get_id()}')
                print(f'    - Type(s): {parent.get_type()}')
            if len(pokemon.get_parent()) == 0:
                print(f' <=> None (highest tier)')
            print(f'--------------------------------------------------------------------------------------------')
            input('Press enter to continue...')
        elif choice == "2":
            # User selected to view all the Pokemon's child Pokemon.
            os.system("cmd /c cls")
            print(f'View {pokemon.get_name()}\'s child Pokemon!')
            print(f'--------------------------------------------------------------------------------------------')
            print(f'The child Pokemon of {pokemon.get_name()} are:')
            for child in pokemon.get_child():
                print(f' <=> {child}')
                print(f'    - ID: {child.get_id()}')
                print(f'    - Type(s): {child.get_type()}')
            if len(pokemon.get_child()) == 0:
                print(f' <=> None (lowest tier)')
            print(f'--------------------------------------------------------------------------------------------')
            input('Press enter to continue...')
        elif choice == "3":
            break

def runSpriteLogic():
    global pokemon
    os.system("cmd /c cls")
    print(f'View {pokemon.get_name()}\'s sprites!')
    print(f'--------------------------------------------------------------------------------------------')
    print(f'Front sprite: {pokemon.get_sprite("front")}')
    print(f'Back sprite: {pokemon.get_sprite("back")}')
    print(f'Shiny front sprite: {pokemon.get_sprite("frontShiny")}')
    print(f'Shiny back sprite: {pokemon.get_sprite("backShiny")}')
    print(f'--------------------------------------------------------------------------------------------')
    input('Press enter to continue...')

def runSpecialLogic():
    global pokemon
    while True:
        os.system("cmd /c cls")
        print(f'View {pokemon.get_name()}\'s special information!')
        print(f'--------------------------------------------------------------------------------------------')
        print(f'What would you like to do?')
        print(f'    [1] View the Pokemon\'s height & weight.')
        print(f'    [2] View the Pokemon\'s additional forms.')
        print(f'    [3] View location data for the Pokemon.')
        print(f'    [4] That\'s all for now (return).')
        choice = input(' > ')
        if choice == "1":
            # User selected to view the Pokemon's height & weight.
            os.system("cmd /c cls")
            print(f'View {pokemon.get_name()}\'s height & weight!')
            print(f'--------------------------------------------------------------------------------------------')
            print(f'Height: {pokemon.get_height()}')
            print(f'Weight: {pokemon.get_weight()}')
            print(f'--------------------------------------------------------------------------------------------')
            input('Press enter to continue...')
        elif choice == "2":
            # User selected to view the Pokemon's additional forms.
            os.system("cmd /c cls")
            print(f'View {pokemon.get_name()}\'s additional forms!')
            print(f'--------------------------------------------------------------------------------------------')
            print(f'The additional forms of {pokemon.get_name()} are:')
            for form in pokemon.get_forms():
                print(f' <=> {form}')
                print(f'    - ID: {form.get_id()}')
                print(f'    - Type(s): {form.get_type()}')
            if len(pokemon.get_forms()) == 0:
                print(f' <=> None')
            print(f'--------------------------------------------------------------------------------------------')
            input('Press enter to continue...')
        elif choice == "3":
            # User selected to view the Pokemon's location data.
            os.system("cmd /c cls")
            print(f'View {pokemon.get_name()}\'s location data!')
            print(f'--------------------------------------------------------------------------------------------')
            print(f'Location data for {pokemon.get_name()} is:')
            for location in pokemon.get_locations():
                print(f' <=> {location}')
                print(f'    - ID: {location.get_id()}')
                print(f'    - Type(s): {location.get_type()}')
            if len(pokemon.get_locations()) == 0:
                print(f' <=> None')
            print(f'--------------------------------------------------------------------------------------------')
            input('Press enter to continue...')
        elif choice == "4":
            break

if __name__ == "__main__":
    main()