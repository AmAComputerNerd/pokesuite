import requests
from libraries.PokeBattle import PokeBattle
from abc import ABC, abstractmethod

from libraries.Pokemon import Pokemon
from libraries.data_objects.PokeAbilityData import PokeAbilityData

class PokeAbility(ABC):
    '''
    The PokeAbility class represents a single ability in the Pokemon universe. This class is used for extracting information about a specific ability with ease.
    '''

    def __init__(self, name : str):
        self.data = PokeAbilityData(name=name)

    def __init__(self, data : PokeAbilityData):
        self.data = data

    def __find_language(self, language : str, data : dict):
        '''
        Retrieve a specific language from a list of multiple language entries.

        This function should work with any dictionary as long as the dictionary contains a "language" key, and the value of that key is a dictionary containing a "name" key.

        Arguments:
            language: The language to search for.
            data: The data to search through.
        Returns:
            The dictionary containing the language.
        '''
        for entry in data:
            if entry["language"]["name"] == language:
                return entry
        # no language found, return english
        return self.__find_language("en", data)
    
    def get_name(self) -> str:
        '''
        Retrieve the name of this ability.

        The name of the ability is retrieved using the PokeAPI.

        Arguments:
            None
        Returns:
            The name of the ability.
        '''
        return self.data.get_name()

    def get_id(self) -> int:
        '''
        Retrieve the ID of this ability.

        The ID of the ability is retrieved using the PokeAPI.

        Arguments:
            None
        Returns:
            The ID of the ability.
        '''
        return self.data.get_id()

    def get_description(self) -> str:
        '''
        Retrieve the description of this ability.

        The description of the ability is retrieved using the PokeAPI.

        Arguments:
            None
        Returns:
            The description of the ability.
        '''
        return self.__find_language("en", self.data["effect_entries"])["effect"]

    def get_short_description(self) -> str:
        '''
        Retrieve the short description of this ability.

        The short description of the ability is retrieved using the PokeAPI.

        Arguments:
            None
        Returns:
            The short description of the ability.
        '''
        return self.__find_language("en", self.data["effect_entries"])["short_effect"]

    # Override methods

    @abstractmethod
    def on_summon(self, battlefield : PokeBattle):
        '''
        Ability trigger function.

        This function is called when the user of this ability is summoned to the battlefield.
        It is called after the user has been summoned, and before the user has been given a turn.

        Arguments:
            battlefield: The PokeBattle object to retrieve the user from.
        Returns:
            None
        '''
        pass

    @abstractmethod
    def pre_turn(self, battlefield : PokeBattle):
        '''
        Ability trigger function.

        This function is called before the user of this ability is given a turn.
        More specifically, it is called in the stage between the user being summoned / turn beginning, and both the user and the opponent being given the choice to make a move.
        
        Arguments:
            battlefield: The PokeBattle object to retrieve the user from.
        Returns:
            None
        '''
        pass

    @abstractmethod
    def pre_user_damage(self, battlefield : PokeBattle):
        '''
        Ability trigger function.

        This function is called before the user of this ability takes their turn.
        This is different from the pre_turn function, as this occurs AFTER the user has chosen a move but BEFORE the effects of the move can activate.

        Due to the nature of speed and priority, it is never guaranteed that this function will be called first or even at all.
        If the user faints before this function is called, the next function to be called will be pre_field_tick.

        Arguments:
            battlefield: The PokeBattle object to retrieve the user from.
        Returns:
            None
        '''
        pass

    @abstractmethod
    def pre_target_damage(self, battlefield : PokeBattle):
        '''
        Ability trigger function.

        This function is called before the opponent (target) takes their turn.
        This is different from the pre_turn function, as this occurs AFTER the opponent has chosen a move but BEFORE the effects of the move can activate.

        Due to the nature of speed and priority, it is never guaranteed that this function will be called first or even at all.
        If the opponent faints before this function is called, the next function to be called will be pre_field_tick.

        Arguments:
            battlefield: The PokeBattle object to retrieve the user from.
        Returns:
            None
        '''
        pass

    @abstractmethod
    def on_faint(self, battlefield : PokeBattle):
        '''
        Ability trigger function.

        This function is called when the user of this ability faints.
        It is called after the user has been removed from the battlefield.

        Arguments:
            battlefield: The PokeBattle object to retrieve the user from.
        Returns:
            None
        '''
        pass

    @abstractmethod
    def pre_field_tick(self, battlefield : PokeBattle):
        '''
        Ability trigger function.

        This function is called before the field tick() function is called, thus before weather effects can damage users, and before any current effects will tick down a turn on their timers.
        It is called after both the user and opponent have taken their turns.

        It should be noted that this function will ALWAYS be called, regardless of whether any effects are currently active.

        Arguments:
            battlefield: The PokeBattle object to retrieve the user from.
        Returns:
            None
        '''
        pass

    @abstractmethod
    def pre_effect_tick(self, battlefield : PokeBattle):
        '''
        Ability trigger function.

        This function is called before each active Pokemon's tick() function is called, thus before any damage is dealt to the user.
        Some effects, such as Leech Seed, will not tick down a turn on their timer until after this function is called.
        Likewise, some effects, such as Paralysis, will execute their effects before this function is called due to their nature.

        It should be noted that this function will ALWAYS be called, regardless of whether any effects are currently active.

        Arguments:
            battlefield: The PokeBattle object to retrieve the user from.
        Returns:
            None
        '''
        pass

    @abstractmethod
    def post_turn(self, battlefield : PokeBattle):
        '''
        Ability trigger function.

        This function is called after all actions for the turn have been completed.
        This includes the user and opponent taking their turns, the field tick() function being called, and the user and opponent's tick() functions being called.

        Arguments:
            battlefield: The PokeBattle object to retrieve the user from.
        Returns:
            None
        '''
        pass

    # Convenience methods for child classes

    def get_user(self, battlefield : PokeBattle) -> Pokemon:
        '''
        Retrieve the user of this ability.

        This function retrieves the user of this ability from the PokeBattle object.

        Arguments:
            battlefield: The PokeBattle object to retrieve the user from.
        Returns:
            The user of this ability.
        '''
        raise NotImplementedError("This method is not implemented yet.")

    def get_target(self, battlefield : PokeBattle) -> Pokemon:
        '''
        Retrieve the target of the user of this ability.

        The target is retrieved from the PokeBattle object.

        Arguments:
            battlefield: The PokeBattle object to retrieve the user from.
        Returns:
            The target of the user with this ability.
        '''
        raise NotImplementedError("This method is not implemented yet.")