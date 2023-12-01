from libraries.PokeAbility import PokeAbility
from libraries.PokeBattle import PokeBattle
from libraries.Pokemon import Pokemon

class AdaptabilityAbility(PokeAbility):
    def __init__(self):
        pass

    def on_summon(self, battlefield : PokeBattle):
        # Grab the user from the battlefield.
        user : Pokemon = super().get_user(battlefield)
        # Check if the user already has Adaptability activated.
        if user.get_modifier("stab") == 2:
            # User already has Adaptability activated, do nothing.
            return
        # User does not have Adaptability activated, activate it.
        user.set_modifier("stab", 2)
        return

    def pre_turn(self, battlefield : PokeBattle):
        pass

    def pre_user_damage(self, battlefield : PokeBattle):
        pass

    def pre_target_damage(self, battlefield : PokeBattle):
        pass

    def on_faint(self, battlefield : PokeBattle):
        pass

    def pre_field_tick(self, battlefield : PokeBattle):
        pass

    def pre_effect_tick(self, battlefield : PokeBattle):
        pass

    def post_turn(self, battlefield : PokeBattle):
        pass