from libraries.PokeAbility import PokeAbility
from libraries.PokeMove import PokeMove
from libraries.data_objects.PokeMoveData import PokeMoveData
from libraries.data_objects.PokeData import PokeData

class Pokemon():
    def __init__(self, name : str):
        self.data = PokeData(name)

    def __init__(self, data : PokeData):
        self.data = data

    def __chosen_move(self):
        '''
        Retrieve the move that was chosen by the user.

        This function will usually return None, as the __chosen_move variable is
        only set during the short period of time between when the move has been chosen,
        and when the move is executed.

        As such, this function should not be relied upon except in these very specific
        circumstances.

        After the move has been executed, the value in the __chosen_move variable is
        used to set the last_move variable, and the __chosen_move variable is reset to
        None.

        Arguments:
            None
        Returns:
            The move that was chosen by the user.
        '''
        return self.__chosen_move

    def get_name(self) -> str:
        '''
        Retrieve the name of this Pokemon.

        Functionally equivalent to `get_data().get_name()`.

        Arguments:
            None
        Returns:
            The name of this Pokemon.
        '''
        return self.data.get_name()

    def get_url(self) -> str:
        '''
        Retrieve the URL of this Pokemon.

        Functionally equivalent to `get_data().get_url()`.

        Arguments:
            None
        Returns:
            The URL of this Pokemon.
        '''
        return self.data.get_url()

    def get_id(self) -> int:
        '''
        Retrieve the ID of this Pokemon.

        Functionally equivalent to `get_data().get_id()`.

        Arguments:
            None
        Returns:
            The ID of this Pokemon.
        '''
        return self.data.get_id()

    def get_data(self) -> PokeData:
        '''
        Retrieve the PokeData object of this Pokemon.

        This object contains all static/default information about this Pokemon.

        Arguments:
            None
        Returns:
            The PokeData object of this Pokemon.
        '''
        return self.data

    # Ability methods

    def get_ability(self) -> PokeAbility:
        '''
        Retrieve the current ability of this Pokemon.

        Arguments:
            None
        Returns:
            The current ability of this Pokemon.
        '''
        return self.ability

    def has_ability(self, ability : str) -> bool:
        '''
        Check if this Pokemon has the given ability.

        Arguments:
            ability: The ability to check for.
        Returns:
            True if this Pokemon has the given ability, False otherwise.
        '''
        return ability == self.ability.get_name()

    def has_ability(self, ability : PokeAbility) -> bool:
        '''
        Check if this Pokemon has the given ability.

        Arguments:
            ability: The ability to check for.
        Returns:
            True if this Pokemon has the given ability, False otherwise.
        '''
        return self.ability == ability

    # Move methods

    def get_move(self, index : int) -> PokeMove:
        '''
        Retrieve the move at the given index.

        Arguments:
            index: The index of the move to retrieve.
        Returns:
            The move at the given index.
        '''
        return self.moves[index]

    def get_move(self, name : str) -> PokeMove:
        '''
        Retrieve the move with the given name.

        Arguments:
            name: The name of the move to retrieve.
        Returns:
            The move with the given name.
        '''
        for move in self.moves:
            if move.get_name() == name:
                return move
        return None

    def get_moves(self) -> list:
        '''
        Retrieve the list of moves this Pokemon has.

        Arguments:
            None
        Returns:
            The list of moves this Pokemon has.
        '''
        return self.moves

    def has_move(self, move : str) -> bool:
        '''
        Check if this Pokemon has the given move.

        Arguments:
            move: The move to check for.
        Returns:
            True if this Pokemon has the given move, False otherwise.
        '''
        for m in self.moves:
            if m.get_name() == move:
                return True
        return False

    def has_move(self, move : PokeMoveData) -> bool:
        '''
        Check if this Pokemon has the given move.

        Arguments:
            move: The move to check for.
        Returns:
            True if this Pokemon has the given move, False otherwise.
        '''
        return move in self.moves

    def get_last_move(self):
        '''
        Retrieve the last move this Pokemon used.

        Arguments:
            None
        Returns:
            The last move this Pokemon used.
        '''
        return self.last_move

    # Stat methods

    def get_health(self) -> int:
        '''
        Retrieve the current health of this Pokemon.

        This value is a percentage of the Pokemon's total health.

        Arguments:
            None
        Returns:
            The current health of this Pokemon.
        '''
        return round((self.health / self.get_max_health()) * 100, 1)

    def get_exact_health(self) -> int:
        '''
        Retrieve the exact value of this Pokemon's current health.
        
        This value is an integer, not a percentage.

        Functionally equivalent to `get_data().get_health()`.

        Arguments:
            None
        Returns:
            The exact value of this Pokemon's current health.
        '''
        return self.health

    def get_max_health(self) -> int:
        '''
        Retrieve the maximum health of this Pokemon.
        
        This value is an integer, not a percentage.

        Arguments:
            None
        Returns:
            The maximum health of this Pokemon.
        '''
        return self.data.get_stats()["health"]

    def get_attack(self) -> int:
        '''
        Retrieve the attack value of this Pokemon.

        This value is an integer, and includes all modifiers.

        Arguments:
            None
        Returns:
            The attack value of this Pokemon.
        '''
        attack = self.data.get_stats()["attack"]
        attack *= self.get_attack_modifier()
        return round(attack)

    def get_attack_modifier(self) -> int:
        '''
        Retrieve the current attack modifier of this Pokemon.

        This value is an integer, not a percentage.
        The modifier is multiplied by the Pokemon's attack value in the process of calculating damage.

        Arguments:
            None
        Returns:
            The current attack modifier of this Pokemon.
        '''
        return self.modifiers["attack"]

    def get_defense(self) -> int:
        '''
        Retrieve the defense value of this Pokemon.

        This value is an integer, and includes all modifiers.

        Arguments:
            None
        Returns:
            The defense value of this Pokemon.
        '''
        defense = self.data.get_stats()["defense"]
        defense *= self.get_defense_modifier()
        return round(defense)

    def get_defense_modifier(self) -> int:
        '''
        Retrieve the current defense modifier of this Pokemon.

        This value is an integer, not a percentage.
        The modifier is multiplied by the Pokemon's defense value in the process of calculating damage.

        Arguments:
            None
        Returns:
            The current defense modifier of this Pokemon.
        '''
        return self.modifiers["defense"]

    def get_special_attack(self) -> int:
        '''
        Retrieve the special attack value of this Pokemon.

        This value is an integer, and includes all modifiers.

        Arguments:
            None
        Returns:
            The special attack value of this Pokemon.
        '''
        special_attack = self.data.get_stats()["special_attack"]
        special_attack *= self.get_special_attack_modifier()
        return round(special_attack)

    def get_special_attack_modifier(self) -> int:
        '''
        Retrieve the current special attack modifier of this Pokemon.

        This value is an integer, not a percentage.
        The modifier is multiplied by the Pokemon's special attack value in the process of calculating damage.

        Arguments:
            None
        Returns:
            The current special attack modifier of this Pokemon.
        '''
        return self.modifiers["special_attack"]

    def get_special_defense(self) -> int:
        '''
        Retrieve the special defense value of this Pokemon.

        This value is an integer, and includes all modifiers.

        Arguments:
            None
        Returns:
            The special defense value of this Pokemon.
        '''
        special_defense = self.data.get_stats()["special_defense"]
        special_defense *= self.get_special_defense_modifier()
        return round(special_defense)

    def get_special_defense_modifier(self) -> int:
        '''
        Retrieve the current special defense modifier of this Pokemon.

        This value is an integer, not a percentage.
        The modifier is multiplied by the Pokemon's special defense value in the process of calculating damage.

        Arguments:
            None
        Returns:
            The current special defense modifier of this Pokemon.
        '''
        return self.modifiers["special_defense"]

    def get_speed(self) -> int:
        '''
        Retrieve the speed value of this Pokemon.

        This value is an integer, and includes all modifiers.

        Arguments:
            None
        Returns:
            The speed value of this Pokemon.
        '''
        speed = self.data.get_stats()["speed"]
        speed *= self.get_speed_modifier()
        return round(speed)

    def get_speed_modifier(self) -> int:
        '''
        Retrieve the current speed modifier of this Pokemon.

        This value is an integer, not a percentage.
        The modifier is multiplied by the Pokemon's speed value in the process of calculating movement order.

        Arguments:
            None
        Returns:
            The current speed modifier of this Pokemon.
        '''
        return self.modifiers["speed"]

    def get_accuracy(self) -> int:
        '''
        Retrieve the accuracy value of this Pokemon.

        This value is an integer, and includes all modifiers.

        Arguments:
            None
        Returns:
            The accuracy value of this Pokemon.
        '''
        accuracy = self.data.get_stats()["accuracy"]
        accuracy *= self.get_accuracy_modifier()
        return round(accuracy)

    def get_accuracy_modifier(self) -> int:
        '''
        Retrieve the current accuracy modifier of this Pokemon.

        This value is an integer, not a percentage.
        The modifier is multiplied by the Pokemon's accuracy value in the process of calculating damage.

        Arguments:
            None
        Returns:
            The current accuracy modifier of this Pokemon.
        '''
        return self.modifiers["accuracy"]

    def get_evasion(self) -> int:
        '''
        Retrieve the evasion value of this Pokemon.

        This value is an integer, and includes all modifiers.

        Arguments:
            None
        Returns:
            The evasion value of this Pokemon.
        '''
        evasion = self.data.get_stats()["evasion"]
        evasion *= self.get_evasion_modifier()
        return round(evasion)

    def get_evasion_modifier(self) -> int:
        '''
        Retrieve the current evasion modifier of this Pokemon.

        This value is an integer, not a percentage.
        The modifier is multiplied by the Pokemon's evasion value in the process of calculating damage.

        Arguments:
            None
        Returns:
            The current evasion modifier of this Pokemon.
        '''
        return self.modifiers["evasion"]

    # Stat setter methods

    def add_health(self, percentile : int) -> int:
        '''
        Add health to this Pokemon.

        This value is a percentage, and as such, must be an integer between 0 and 100.
        The Pokemon's health will be increased by the given percentage of its maximum health.

        Any excess health will be discarded.

        Arguments:
            percentile: The amount of health to add.
        Returns:
            The new health percentage of this Pokemon.
        '''
        self.health += self.get_max_health() / percentile * 100
        if self.health > self.get_max_health():
            self.health = self.get_max_health()
        return self.get_health()

    def add_health(self, amount : int) -> int:
        '''
        Add health to this Pokemon.

        This value is an integer, and as such, must be positive.
        The Pokemon's health will be increased by the given amount.

        Any excess health will be discarded.

        Arguments:
            amount: The amount of health to add.
        Returns:
            The new health percentage of this Pokemon.
        '''
        self.health += amount
        if self.health > self.get_max_health():
            self.health = self.get_max_health()
        return self.get_health()

    def remove_health(self, percentile : int) -> int:
        '''
        Remove health from this Pokemon.

        This value is a percentage, and as such, must be an integer between 0 and 100.
        The Pokemon's health will be decreased by the given percentage of its maximum health.

        Any excess health will be discarded.

        Arguments:
            percentile: The amount of health to remove.
        Returns:
            The new health percentage of this Pokemon.
        '''
        self.health -= self.get_max_health() / percentile * 100
        if self.health < 0:
            self.health = 0
        return self.get_health()

    def remove_health(self, amount : int) -> int:
        '''
        Remove health from this Pokemon.

        This value is an integer, and as such, must be positive.
        The Pokemon's health will be decreased by the given amount.

        Any excess health will be discarded.

        Arguments:
            amount: The amount of health to remove.
        Returns:
            The new health percentage of this Pokemon.
        '''
        self.health -= amount
        if self.health < 0:
            self.health = 0
        return self.get_health()

    def set_health(self, percentile : int) -> int:
        '''
        Set the health of this Pokemon.

        This value is a percentage, and as such, must be an integer between 0 and 100.
        The Pokemon's health will be set to the given percentage of its maximum health.

        Any value outside of the range will be rounded down or up to the closest valid value.

        Arguments:
            percentile: The new health percentage of this Pokemon.
        Returns:
            The new health percentage of this Pokemon.
        '''
        self.health = self.get_max_health() / percentile * 100
        if self.health < 0:
            self.health = 0
        elif self.health > self.get_max_health():
            self.health = self.get_max_health()
        return self.get_health()

    def set_health(self, amount : int) -> int:
        '''
        Set the health of this Pokemon.

        This value is an integer, and as such, must be positive.
        The Pokemon's health will be set to the given amount.

        Any value outside of the range will be rounded down or up to the closest valid value.

        Arguments:
            amount: The new health of this Pokemon.
        Returns:
            The new health percentage of this Pokemon.
        '''
        self.health = amount
        if self.health < 0:
            self.health = 0
        elif self.health > self.get_max_health():
            self.health = self.get_max_health()
        return self.get_health()

    def add_attack_multiplier(self, multiplier : int) -> int:
        '''
        Add an additional attack multiplier to this Pokemon.

        This value is a multiplier, and as such, must be between the maximum and minimum values of 0.1 and 4.
        The Pokemon's attack multiplier will be increased by the given amount.

        If the provided value is negative, the Pokemon's attack will be decreased by the absolute value of the given multiplier following the same rules.
        The attack multiplier will never rise above 4, thus any excess that would cause the multiplier to rise above 4 will be discarded.

        Arguments:
            amount: The amount of attack to add.
        Returns:
            The new attack multiplier of this Pokemon.
        '''
        if multiplier < 0:
            return self.remove_attack_multiplier(abs(multiplier))
        self.multipliers["attack"] = min(self.multipliers["attack"] + multiplier, 4)
        return self.get_attack_modifier()

    def remove_attack_multiplier(self, multiplier : int) -> int:
        '''
        Remove an attack multiplier from this Pokemon.

        This value is a multiplier, and as such, must be between the maximum and minimum values of 0.1 and 4.
        The Pokemon's attack multiplier will be decreased by the given amount.

        If the provided value is negative, the Pokemon's attack will be increased by the absolute value of the given multiplier following the same rules.
        The attack multiplier will never fall below 0.1, thus any excess that would cause the multiplier to fall below 0.1 will be discarded.

        Arguments:
            amount: The amount of attack to remove.
        Returns:
            The new attack multiplier of this Pokemon.
        '''
        if multiplier < 0:
            return self.add_attack_multiplier(-abs(multiplier))
        self.multipliers["attack"] = max(self.multipliers["attack"] - multiplier, 0.1)
        return self.get_attack_modifier()

    def set_attack_multiplier(self, multiplier : int) -> int:
        '''
        Set the attack multiplier of this Pokemon.

        This value is a multiplier, and as such, must be between the maximum and minimum values of 0.1 and 4.
        The Pokemon's attack multiplier will be set to the given amount.

        Any value outside of the range will be rounded down or up to the closest valid value.

        Arguments:
            amount: The new attack multiplier of this Pokemon.
        Returns:
            The new attack multiplier of this Pokemon.
        '''
        if multiplier < 0.1:
            multiplier = 0.1
        elif multiplier > 4:
            multiplier = 4
        self.multipliers["attack"] = multiplier
        return self.get_attack_modifier()

    def add_defense_multiplier(self, multiplier : int) -> int:
        '''
        Add an additional defense multiplier to this Pokemon.

        This value is a multiplier, and as such, must be between the maximum and minimum values of 0.1 and 4.
        The Pokemon's defense multiplier will be increased by the given amount.

        If the provided value is negative, the Pokemon's defense will be decreased by the absolute value of the given multiplier following the same rules.
        The defense multiplier will never rise above 4, thus any excess that would cause the multiplier to rise above 4 will be discarded.

        Arguments:
            amount: The amount of defense to add.
        Returns:
            The new defense multiplier of this Pokemon.
        '''
        if multiplier < 0:
            return self.remove_defense_multiplier(abs(multiplier))
        self.multipliers["defense"] = min(self.multipliers["defense"] + multiplier, 4)
        return self.get_defense_modifier()

    def remove_defense_multiplier(self, multiplier : int) -> int:
        '''
        Remove a defense multiplier from this Pokemon.

        This value is a multiplier, and as such, must be between the maximum and minimum values of 0.1 and 4.
        The Pokemon's defense multiplier will be decreased by the given amount.

        If the provided value is negative, the Pokemon's defense will be increased by the absolute value of the given multiplier following the same rules.
        The defense multiplier will never fall below 0.1, thus any excess that would cause the multiplier to fall below 0.1 will be discarded.

        Arguments:
            amount: The amount of defense to remove.
        Returns:
            The new defense multiplier of this Pokemon.
        '''
        if multiplier < 0:
            return self.add_defense_multiplier(-abs(multiplier))
        self.multipliers["defense"] = max(self.multipliers["defense"] - multiplier, 0.1)
        return self.get_defense_modifier()
    
    def set_defense_multiplier(self, multiplier : int) -> int:
        '''
        Set the defense multiplier of this Pokemon.

        This value is a multiplier, and as such, must be between the maximum and minimum values of 0.1 and 4.
        The Pokemon's defense multiplier will be set to the given amount.

        Any value outside of the range will be rounded down or up to the closest valid value.

        Arguments:
            amount: The new defense multiplier of this Pokemon.
        Returns:
            The new defense multiplier of this Pokemon.
        '''
        if multiplier < 0.1:
            multiplier = 0.1
        elif multiplier > 4:
            multiplier = 4
        self.multipliers["defense"] = multiplier
        return self.get_defense_modifier()

    def add_special_attack_multiplier(self, multiplier : int) -> int:
        '''
        Add an additional special attack multiplier to this Pokemon.

        This value is a multiplier, and as such, must be between the maximum and minimum values of 0.1 and 4.
        The Pokemon's special attack multiplier will be increased by the given amount.

        If the provided value is negative, the Pokemon's special attack will be decreased by the absolute value of the given multiplier following the same rules.
        The special attack multiplier will never rise above 4, thus any excess that would cause the multiplier to rise above 4 will be discarded.

        Arguments:
            amount: The amount of special attack to add.
        Returns:
            The new special attack multiplier of this Pokemon.
        '''
        if multiplier < 0:
            return self.remove_special_attack_multiplier(abs(multiplier))
        self.multipliers["special_attack"] = min(self.multipliers["special_attack"] + multiplier, 4)
        return self.get_special_attack_modifier()

    def remove_special_attack_multiplier(self, multiplier : int) -> int:
        '''
        Remove a special attack multiplier from this Pokemon.

        This value is a multiplier, and as such, must be between the maximum and minimum values of 0.1 and 4.
        The Pokemon's special attack multiplier will be decreased by the given amount.

        If the provided value is negative, the Pokemon's special attack will be increased by the absolute value of the given multiplier following the same rules.
        The special attack multiplier will never fall below 0.1, thus any excess that would cause the multiplier to fall below 0.1 will be discarded.

        Arguments:
            amount: The amount of special attack to remove.
        Returns:
            The new special attack multiplier of this Pokemon.
        '''
        if multiplier < 0:
            return self.add_special_attack_multiplier(-abs(multiplier))
        self.multipliers["special_attack"] = max(self.multipliers["special_attack"] - multiplier, 0.1)
        return self.get_special_attack_modifier()

    def set_special_attack_multiplier(self, multiplier : int) -> int:
        '''
        Set the special attack multiplier of this Pokemon.

        This value is a multiplier, and as such, must be between the maximum and minimum values of 0.1 and 4.
        The Pokemon's special attack multiplier will be set to the given amount.

        Any value outside of the range will be rounded down or up to the closest valid value.

        Arguments:
            amount: The new special attack multiplier of this Pokemon.
        Returns:
            The new special attack multiplier of this Pokemon.
        '''
        if multiplier < 0.1:
            multiplier = 0.1
        elif multiplier > 4:
            multiplier = 4
        self.multipliers["special_attack"] = multiplier
        return self.get_special_attack_modifier()

    def add_special_defense_multiplier(self, multiplier : int) -> int:
        '''
        Add an additional special defense multiplier to this Pokemon.

        This value is a multiplier, and as such, must be between the maximum and minimum values of 0.1 and 4.
        The Pokemon's special defense multiplier will be increased by the given amount.

        If the provided value is negative, the Pokemon's special defense will be decreased by the absolute value of the given multiplier following the same rules.
        The special defense multiplier will never rise above 4, thus any excess that would cause the multiplier to rise above 4 will be discarded.

        Arguments:
            amount: The amount of special defense to add.
        Returns:
            The new special defense multiplier of this Pokemon.
        '''
        if multiplier < 0:
            return self.remove_special_defense_multiplier(abs(multiplier))
        self.multipliers["special_defense"] = min(self.multipliers["special_defense"] + multiplier, 4)
        return self.get_special_defense_modifier()

    def remove_special_defense_multiplier(self, multiplier : int) -> int:
        '''
        Remove a special defense multiplier from this Pokemon.

        This value is a multiplier, and as such, must be between the maximum and minimum values of 0.1 and 4.
        The Pokemon's special defense multiplier will be decreased by the given amount.

        If the provided value is negative, the Pokemon's special defense will be increased by the absolute value of the given multiplier following the same rules.
        The special defense multiplier will never fall below 0.1, thus any excess that would cause the multiplier to fall below 0.1 will be discarded.

        Arguments:
            amount: The amount of special defense to remove.
        Returns:
            The new special defense multiplier of this Pokemon.
        '''
        if multiplier < 0:
            return self.add_special_defense_multiplier(-abs(multiplier))
        self.multipliers["special_defense"] = max(self.multipliers["special_defense"] - multiplier, 0.1)
        return self.get_special_defense_modifier()
    
    def set_special_defense_multiplier(self, multiplier : int) -> int:
        '''
        Set the special defense multiplier of this Pokemon.

        This value is a multiplier, and as such, must be between the maximum and minimum values of 0.1 and 4.
        The Pokemon's special defense multiplier will be set to the given amount.

        Any value outside of the range will be rounded down or up to the closest valid value.

        Arguments:
            amount: The new special defense multiplier of this Pokemon.
        Returns:
            The new special defense multiplier of this Pokemon.
        '''
        if multiplier < 0.1:
            multiplier = 0.1
        elif multiplier > 4:
            multiplier = 4
        self.multipliers["special_defense"] = multiplier
        return self.get_special_defense_modifier()

    def add_speed_multiplier(self, multiplier : int) -> int:
        '''
        Add an additional speed multiplier to this Pokemon.

        This value is a multiplier, and as such, must be between the maximum and minimum values of 0.1 and 4.
        The Pokemon's speed multiplier will be increased by the given amount.

        If the provided value is negative, the Pokemon's speed will be decreased by the absolute value of the given multiplier following the same rules.
        The speed multiplier will never rise above 4, thus any excess that would cause the multiplier to rise above 4 will be discarded.

        Arguments:
            amount: The amount of speed to add.
        Returns:
            The new speed multiplier of this Pokemon.
        '''
        if multiplier < 0:
            return self.remove_speed_multiplier(abs(multiplier))
        self.multipliers["speed"] = min(self.multipliers["speed"] + multiplier, 4)
        return self.get_speed_modifier()

    def remove_speed_multiplier(self, multiplier : int) -> int:
        '''
        Remove a speed multiplier from this Pokemon.

        This value is a multiplier, and as such, must be between the maximum and minimum values of 0.1 and 4.
        The Pokemon's speed multiplier will be decreased by the given amount.

        If the provided value is negative, the Pokemon's speed will be increased by the absolute value of the given multiplier following the same rules.
        The speed multiplier will never fall below 0.1, thus any excess that would cause the multiplier to fall below 0.1 will be discarded.

        Arguments:
            amount: The amount of speed to remove.
        Returns:
            The new speed multiplier of this Pokemon.
        '''
        if multiplier < 0:
            return self.add_speed_multiplier(-abs(multiplier))
        self.multipliers["speed"] = max(self.multipliers["speed"] - multiplier, 0.1)
        return self.get_speed_modifier()

    def set_speed_multiplier(self, multiplier : int) -> int:
        '''
        Set the speed multiplier of this Pokemon.

        This value is a multiplier, and as such, must be between the maximum and minimum values of 0.1 and 4.
        The Pokemon's speed multiplier will be set to the given amount.

        Any value outside of the range will be rounded down or up to the closest valid value.

        Arguments:
            amount: The new speed multiplier of this Pokemon.
        Returns:
            The new speed multiplier of this Pokemon.
        '''
        if multiplier < 0.1:
            multiplier = 0.1
        elif multiplier > 4:
            multiplier = 4
        self.multipliers["speed"] = multiplier
        return self.get_speed_modifier()

    def add_accuracy_multiplier(self, multiplier : int) -> int:
        '''
        Add an additional accuracy multiplier to this Pokemon.

        This value is a multiplier, and as such, must be between the maximum and minimum values of 0.1 and 4.
        The Pokemon's accuracy multiplier will be increased by the given amount.

        If the provided value is negative, the Pokemon's accuracy will be decreased by the absolute value of the given multiplier following the same rules.
        The accuracy multiplier will never rise above 4, thus any excess that would cause the multiplier to rise above 4 will be discarded.

        Arguments:
            amount: The amount of accuracy to add.
        Returns:
            The new accuracy multiplier of this Pokemon.
        '''
        if multiplier < 0:
            return self.remove_accuracy_multiplier(abs(multiplier))
        self.multipliers["accuracy"] = min(self.multipliers["accuracy"] + multiplier, 4)
        return self.get_accuracy_modifier()

    def remove_accuracy_multiplier(self, multiplier : int) -> int:
        '''
        Remove an accuracy multiplier from this Pokemon.

        This value is a multiplier, and as such, must be between the maximum and minimum values of 0.1 and 4.
        The Pokemon's accuracy multiplier will be decreased by the given amount.

        If the provided value is negative, the Pokemon's accuracy will be increased by the absolute value of the given multiplier following the same rules.
        The accuracy multiplier will never fall below 0.1, thus any excess that would cause the multiplier to fall below 0.1 will be discarded.

        Arguments:
            amount: The amount of accuracy to remove.
        Returns:
            The new accuracy multiplier of this Pokemon.
        '''
        if multiplier < 0:
            return self.add_accuracy_multiplier(-abs(multiplier))
        self.multipliers["accuracy"] = max(self.multipliers["accuracy"] - multiplier, 0.1)
        return self.get_accuracy_modifier()

    def set_accuracy_multiplier(self, multiplier : int) -> int:
        '''
        Set the accuracy multiplier of this Pokemon.

        This value is a multiplier, and as such, must be between the maximum and minimum values of 0.1 and 4.
        The Pokemon's accuracy multiplier will be set to the given amount.

        Any value outside of the range will be rounded down or up to the closest valid value.

        Arguments:
            amount: The new accuracy multiplier of this Pokemon.
        Returns:
            The new accuracy multiplier of this Pokemon.
        '''
        if multiplier < 0.1:
            multiplier = 0.1
        elif multiplier > 4:
            multiplier = 4
        self.multipliers["accuracy"] = multiplier
        return self.get_accuracy_modifier()

    def add_evasion_multiplier(self, multiplier : int) -> int:
        '''
        Add an additional evasion multiplier to this Pokemon.

        This value is a multiplier, and as such, must be between the maximum and minimum values of 0.1 and 4.
        The Pokemon's evasion multiplier will be increased by the given amount.

        If the provided value is negative, the Pokemon's evasion will be decreased by the absolute value of the given multiplier following the same rules.
        The evasion multiplier will never rise above 4, thus any excess that would cause the multiplier to rise above 4 will be discarded.

        Arguments:
            amount: The amount of evasion to add.
        Returns:
            The new evasion multiplier of this Pokemon.
        '''
        if multiplier < 0:
            return self.remove_evasion_multiplier(abs(multiplier))
        self.multipliers["evasion"] = min(self.multipliers["evasion"] + multiplier, 4)
        return self.get_evasion_modifier()

    def remove_evasion_multiplier(self, multiplier : int) -> int:
        '''
        Remove an evasion multiplier from this Pokemon.

        This value is a multiplier, and as such, must be between the maximum and minimum values of 0.1 and 4.
        The Pokemon's evasion multiplier will be decreased by the given amount.

        If the provided value is negative, the Pokemon's evasion will be increased by the absolute value of the given multiplier following the same rules.
        The evasion multiplier will never fall below 0.1, thus any excess that would cause the multiplier to fall below 0.1 will be discarded.

        Arguments:
            amount: The amount of evasion to remove.
        Returns:
            The new evasion multiplier of this Pokemon.
        '''
        if multiplier < 0:
            return self.add_evasion_multiplier(-abs(multiplier))
        self.multipliers["evasion"] = max(self.multipliers["evasion"] - multiplier, 0.1)
        return self.get_evasion_modifier()

    def set_evasion_multiplier(self, multiplier : int) -> int:
        '''
        Set the evasion multiplier of this Pokemon.

        This value is a multiplier, and as such, must be between the maximum and minimum values of 0.1 and 4.
        The Pokemon's evasion multiplier will be set to the given amount.

        Any value outside of the range will be rounded down or up to the closest valid value.

        Arguments:
            amount: The new evasion multiplier of this Pokemon.
        Returns:
            The new evasion multiplier of this Pokemon.
        '''
        if multiplier < 0.1:
            multiplier = 0.1
        elif multiplier > 4:
            multiplier = 4
        self.multipliers["evasion"] = multiplier
        return self.get_evasion_modifier()

    # Effect methods

    def has_effect(self, effect : str) -> bool:
        '''
        Check if this Pokemon has the given effect.

        Arguments:
            effect: The effect to check for.
        Returns:
            True if this Pokemon has the given effect, False otherwise.
        '''
        return effect in self.effects

    def add_effect(self, effect : str) -> None:
        '''
        Add the given effect to this Pokemon.

        Arguments:
            effect: The effect to add.
        Returns:
            None
        '''
        self.effects.add(effect)

    def remove_effect(self, effect : str) -> None:
        '''
        Remove the given effect from this Pokemon.

        Arguments:
            effect: The effect to remove.
        Returns:
            None
        '''
        self.effects.remove(effect)

    def clear_effects(self) -> None:
        '''
        Remove all effects from this Pokemon.

        Arguments:
            None
        Returns:
            None
        '''
        self.effects.clear()

    # Modifier methods

    def get_modifier(self, key : str):
        '''
        Get the value of a modifier, with it's key.

        Arguments:
            key: The key of the modifier to get.
        Returns:
            The value of the modifier with the given key.
        '''
        return self.multipliers[key]

    def set_modifier(self, key : str, value):
        '''
        Set the value of a modifier, with it's key.

        Arguments:
            key: The key of the modifier to set.
            value: The new value of the modifier.
        Returns:
            None
        '''
        self.multipliers[key] = value