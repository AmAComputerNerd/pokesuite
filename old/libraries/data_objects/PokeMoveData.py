import requests
from libraries.PokeMove import PokeMove

class PokeMoveData():
    '''
    The PokeMoveData class holds default values for a PokeMove's properties. It is used to retrieve information about a move, such as its power, accuracy, and type.
    '''

    def __init__(self, name : str):
        name = name.lower().replace(" ", "-")
        self.url = f"https://pokeapi.co/api/v2/move/{name}"
        request = requests.get(self.url)
        request.raise_for_status()
        self.data = request.json()

    def __init__(self, url):
        self.url = url
        request = requests.get(self.url)
        request.raise_for_status()
        self.data = request.json()

    def __init__(self, move : PokeMove):
        self.move = move
        self.url = "https://pokeapi.co/api/v2/move/" + move.name.lower().replace(" ", "-")

    def __raw_data(self):
        '''
        Retrieve the raw data from the API.
        This data is always in JSON format, and should resemble that of the PokeAPI Move JSON formatting.
        
        Arguments:
            None
        Returns:
            The raw data from the API.
        '''
        return self.data

    # Identification methods

    def get_name(self) -> str:
        '''
        Retrieve the name of this move.
        
        Arguments:
            None
        Returns:
            The name of this move.
        '''
        return self.data["name"]

    def get_url(self) -> str:
        '''
        Retrieve the URL of this move.
        
        Arguments:
            None
        Returns:
            The URL of this move.
        '''
        return self.url

    def get_id(self) -> int:
        '''
        Retrieve the ID of this move.
        
        Arguments:
            None
        Returns:
            The ID of this move.
        '''
        return self.data["id"]

    # Default methods

    def get_power(self) -> int:
        '''
        Retrieve the power of this move.

        The power of a move is the base amount of damage it deals.

        If the move does not have a power (does no damage), 0 is returned.

        Arguments:
            None
        Returns:
            The power of this move.
        '''
        if self.data["power"] is None:
            return 0
        return self.data["power"]

    def get_pp(self) -> int:
        '''
        Retrieve the PP of this move.

        The PP of a move is the amount of times it can be used before it must recharge.
        When a move reaches 0 PP, it cannot be used until it has recharged (normally through items).

        If the move does not have a PP, 0 is returned.

        Arguments:
            None
        Returns:
            The PP of this move.
        '''
        if self.data["pp"] is None:
            return 0
        return self.data["pp"]
    
    def get_accuracy(self) -> int:
        '''
        Retrieve the accuracy of this move.

        The accuracy of a move is the chance that it will hit its target.
        
        If the move does not have an accuracy, it will be assumed to have 100% accuracy.

        Arguments:
            None
        Returns:
            The accuracy of this move.
        '''
        return self.data["accuracy"]
    
    def get_type(self) -> str:
        '''
        Retrieve the type of this move.

        The type of a move determines the elemental type of damage it deals.
        This can influence the effectiveness of the move, dependant on the target Pokemon's type(s) and/or items + abilities.

        Arguments:
            None
        Returns:
            The type of this move (name).
        '''
        return self.data["type"]["name"]

    def get_priority(self) -> int:
        '''
        Retrieve the priority of this move.

        The priority of a move determines the order in which it is used.
        Higher is better.
        
        Moves with a priority of 0 are used after all other moves.

        Arguments:
            None
        Returns:
            The priority of this move.
        '''
        return self.data["priority"]

    def get_damage_class(self) -> str:
        '''
        Retrieve the damage class of this move.

        The damage class of a move determines the type of damage it deals.
        This can influence the effectiveness of the move, as target abilities and items can influence it's result.
        
        Arguments:
            None
        Returns:
            The damage class of this move.
        '''
        return self.data["damage_class"]["name"]

    def get_stat_changes(self) -> dict:
        '''
        Retrieve the stat changes applied by the move.

        If the move does not apply any stat changes, an empty dictionary is returned.

        Arguments:
            None
        Returns:
            The stat changes applied by the move.
        '''
        return {stat["stat"]["name"] : stat["change"] for stat in self.data["stat_changes"]}

    def get_effect_changes(self) -> dict:
        '''
        Retrieve the effect changes of the move.

        As of now, this is not implemented in the game.
        The API does not provide any information on this, so until other methods are developed, this will ALWAYS return an empty dictionary.

        If the move does not have any effect changes, an empty dictionary is returned.

        Arguments:
            None
        Returns:
            The effect changes of the move.
        '''
        return {}

    # Meta methods

    def get_ailment(self) -> str:
        '''
        Retrieve the ailment associated with the move.

        This ailment is applied to the target after being damaged, if the ailment chance is successful.

        If the move does not have an associated ailment, None is returned.

        Arguments:
            None
        Returns:
            The ailment associated with the move.
        '''
        if self.data["meta"]["ailment"] is None:
            return None
        return self.data["meta"]["ailment"]["name"]

    def get_ailment_chance(self) -> int:
        '''
        Retrieve the chance of the ailment being applied.

        If the move does not have an associated ailment, 0 is returned.
        The chance is a percentage. Any value above 100% is treated as 100%, just as any value below 0% is treated as 0%.

        Arguments:
            None
        Returns:
            The chance of the ailment being applied.
        '''
        if self.data["meta"]["ailment_chance"] <= 0:
            return 0
        if self.data["meta"]["ailment_chance"] >= 100:
            return 100
        return self.data["meta"]["ailment_chance"]

    def get_crit_rate(self) -> int:
        '''
        Retrieve the extra critical hit rate of the move.

        The critical hit rate is the chance of the move dealing double damage.
        The returned value is a percentage. Any value above 100% is treated as 100%, just as any value below 0% is treated as 0%.

        The resulting value is added to the user's base critical hit rate prior to damage being calculated.

        Arguments:
            None
        Returns:
            The critical hit rate of the move.
        '''
        if self.data["meta"]["crit_rate"] <= 0:
            return 0
        elif self.data["meta"]["crit_rate"] >= 100:
            return 100
        return self.data["meta"]["crit_rate"]

    def get_min_hits(self) -> int:
        '''
        Retrieve the minimum number of hits the move can deal.

        This value refers to multi-hit moves, such as Fury Cutter, and represents the minimum number of times this move can trigger in a turn.

        If the move does not have a minimum number of hits (that is, it is not a multi-hit move), None is returned.

        Arguments:
            None
        Returns:
            The minimum number of hits the move can deal.
        '''
        if self.data["meta"]["min_hits"] is None:
            return None
        return self.data["meta"]["min_hits"]

    def get_max_hits(self) -> int:
        '''
        Retrieve the maximum number of hits the move can deal.

        This value refers to multi-hit moves, such as Fury Cutter, and represents the maximum number of times this move can trigger in a turn.

        If the move does not have a maximum number of hits (that is, it is not a multi-hit move), None is returned.

        Arguments:
            None
        Returns:
            The maximum number of hits the move can deal.
        '''
        if self.data["meta"]["max_hits"] is None:
            return None
        return self.data["meta"]["max_hits"]

    def get_min_turns(self) -> int:
        '''
        Retrieve the minimum number of turns the move can last.

        This value refers to multi-turn moves, such as Solar Beam, and represents the minimum number of turns this move can last.

        If the move does not have a minimum number of turns (that is, it is not a multi-turn move), None is returned.

        Arguments:
            None
        Returns:
            The minimum number of turns the move can last.
        '''
        if self.data["meta"]["min_turns"] is None:
            return None
        return self.data["meta"]["min_turns"]

    def get_max_turns(self) -> int:
        '''
        Retrieve the maximum number of turns the move can last.

        This value refers to multi-turn moves, such as Solar Beam, and represents the maximum number of turns this move can last.

        If the move does not have a maximum number of turns (that is, it is not a multi-turn move), None is returned.

        Arguments:
            None
        Returns:
            The maximum number of turns the move can last.
        '''
        if self.data["meta"]["max_turns"] is None:
            return None
        return self.data["meta"]["max_turns"]

    def get_drain(self) -> int:
        '''
        Retrieve the percentage of HP drained by the move.

        The returned percentage should be treated as the "percentage of damage dealt to the target TO heal/damage the user for".

        The following can be assumed based on the returned value:
            * If the drain is zero, this move does not drain HP in any way.
            * If the drain is positive, the move drains the calculated HP from the damage this turn, and adds it to the user's HP. This is the case for moves such as Leech Life.
            * If the drain is negative, the move drains the calculated HP from the damage this turn, and removes it from the user. This is also known as Recoil damage.

        For example:
            * A move with a drain of 50 and calculated damage of 100 will damage the target for 100 HP, and heal the user for 50 HP.
            * A move with a drain of -25 and calculated damage of 200 will damage the target for 200 HP, and damage the user for 50 HP.

        Arguments:
            None
        Returns:
            The amount of HP drained by the move.
        '''
        return self.data["meta"]["drain"]

    def get_healing(self) -> int:
        '''
        Retrieve the amount of HP healed by the move.

        If the move does not heal HP, 0 is returned.
        Otherwise, the returned value is the percentage of HP healed (based on the Pokemon's max health).

        The total amount of HP healed can be calculated as follows:
            * healed_hp = (max_hp * healing) / 100

        Arguments:
            None
        Returns:
            The amount of HP healed by the move.
        '''
        return self.data["meta"]["healing"]

    def get_flinch_chance(self) -> int:
        '''
        Retrieve the chance of the target flinching after being damaged this move.

        The returned percentage refers to the chance for the target's next move to fail.
        This is not the same as Confusion, which causes the target to occasionally damage itself instead of the user while active.
        
        The chance for the target to flinch will be reset after their next move is used.

        If the move does not have a flinch chance, 0 is returned.

        Arguments:
            None
        Returns:
            The chance of the target flinching.
        '''
        return self.data["meta"]["flinch_chance"]

    def get_target_stat_chance(self) -> int:
        '''
        Retrieve the chance of the target's stats being changed.

        This chance is tested every time the move is used, and will be ineffective if the target's stats are already at their maximum or minimum values.

        NOTE: This refers to the TARGET Pokemon, not the user.

        If the move does not have a stat chance, 0 is returned.

        Arguments:
            None
        Returns:
            The chance of the target's stats being changed.
        '''
        return self.data["meta"]["stat_chance"]

    # Check methods

    def does_heal(self, onlyDrain : bool = False, onlyTrueHealing : bool = False):
        '''
        Check if the move heals HP.

        Arguments:
            onlyDrain (bool): If True, only returns True if the move drains HP. Returns False if the move heals HP.
            onlyTrueHealing (bool): If True, only returns True if the move heals HP without draining it.
        Returns:
            True if the move heals HP, False otherwise.
        '''
        if onlyDrain:
            return self.get_drain() > 0 and self.get_healing() == 0
        elif onlyTrueHealing:
            return self.get_healing() > 0 and self.get_drain() == 0
        return self.get_healing() > 0 or self.get_drain() > 0

    def does_ailment(self, status : str = None) -> bool:
        '''
        Check if this move inflicts a status condition, either any, or optionally, a specific ailment.

        Arguments:
            status (opt): The status condition to check for. Defaults to None.
        Returns:
            True if this move inflicts either the specified ailment or simply any status condition, False otherwise.
        '''
        if status is None:
            return self.get_ailment() is not None
        return self.get_ailment() == status

    def does_stat_change(self, *, stats = "") -> bool:
        '''
        Check if this move inflicts a stat change.

        Arguments:
            stats (opt): A string containing the stats to check for. Defaults to "".
        Returns:
            True if this move inflicts a stat change, False otherwise.
        '''
        if stats == "":
            return self.get_stat_changes() != {}
        for stat in stats:
            if stat not in self.get_stat_changes():
                return False
        return True

    def does_effect_change(self, *, effects = "") -> bool:
        '''
        Check if this move inflicts an effect change.

        Arguments:
            effects (opt): A string containing the effects to check for. Defaults to "".
        Returns:
            True if this move inflicts an effect change, False otherwise.
        '''
        if effects == "":
            return self.get_effect_changes() != {}
        for effect in effects:
            if effect not in self.get_effect_changes():
                return False
        return True

    def is_multihit_move(self) -> bool:
        '''
        Check if this move is a multi-hit move.

        The following steps are taken to determine if this move is a multi-hit move:
            * If the move has a minimum number of hits with an integer value.
            * If the move has a maximum number of hits with an integer value.
            * Both values are not equal to each other.

        Arguments:
            None
        Returns:
            True if this move is a multi-hit move, False otherwise.
        '''
        if self.get_min_hits() is None or self.get_max_hits() is None:
            return False
        return self.get_min_hits() != self.get_max_hits()

    def is_multiturn_move(self) -> bool:
        '''
        Check if this move is a multi-turn move.

        The following steps are taken to determine if this move is a multi-turn move:
            * If the move has a minimum number of turns with an integer value.
            * If the move has a maximum number of turns with an integer value.
            * Both values are not equal to each other.

        Arguments:
            None
        Returns:
            True if this move is a multi-turn move, False otherwise.
        '''
        if self.get_min_turns() is None or self.get_max_turns() is None:
            return False
        return self.get_min_turns() != self.get_max_turns()