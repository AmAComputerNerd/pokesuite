from libraries.PokeAbility import PokeAbility
from libraries.PokeBattle import PokeBattle
from libraries.Pokemon import Pokemon

class AerilateAbility(PokeAbility):
    def __init__(self):
        pass

    def on_summon(self, battlefield : PokeBattle):
        # Grab the user from the battlefield.
        user : Pokemon = super().get_user(battlefield)
        # Check if the user has any normal type moves.
        battlefield.display_message(f"{user.get_name()}'s Aerilate ability activated! {user.get_name()}'s Normal type moves became Flying type moves!")
        for move in user.get_moves():
            if move.get_type() == "normal":
                # User has a normal type move, change it to flying.
                move.set_type("flying")
                # Add the Aerilate power modifier.
                move.set_power(move.get_power() * 1.3)
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