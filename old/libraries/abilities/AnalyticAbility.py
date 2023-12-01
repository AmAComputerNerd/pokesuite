from libraries.PokeAbility import PokeAbility
from libraries.PokeBattle import PokeBattle
from libraries.Pokemon import Pokemon

class AnalyticAbility(PokeAbility):
    def __init__(self):
        self.target_moved = False

    def on_summon(self, battlefield : PokeBattle):
        pass
    
    def pre_turn(self, battlefield : PokeBattle):
        pass

    def pre_user_damage(self, battlefield : PokeBattle):
        # Check if the target moved already.
        if self.target_moved:
            # Get the user.
            user = PokeAbility.get_user(battlefield)
            # Increase move damage by 30%.
            user.__chosen_move().set_power(user.__chosen_move().get_power() * 1.3)
            # Display a message.
            battlefield.display_message(f"{user.get_name()}'s Analytic ability activated! {user.get_name()}'s move power increased by 30%!")
        return

    def pre_target_damage(self, battlefield : PokeBattle):
        # Set the target moved flag.
        self.target_moved = True

    def on_faint(self, battlefield : PokeBattle):
        pass

    def pre_field_tick(self, battlefield : PokeBattle):
        pass

    def pre_effect_tick(self, battlefield : PokeBattle):
        pass

    def post_turn(self, battlefield : PokeBattle):
        # Reset the target moved flag.
        self.target_moved = False