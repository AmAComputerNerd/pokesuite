from libraries.PokeAbility import PokeAbility
from libraries.PokeBattle import PokeBattle
from libraries.Pokemon import Pokemon

class AirLockAbility(PokeAbility):
    def __init__(self):
        pass

    def on_summon(self, battlefield : PokeBattle):
        # Check for an active weather condition.
        if battlefield.get_field_effect("weather") is not None:
            # Remove the weather condition.
            battlefield.set_field_effect("weather", None)
            # Display a message.
            battlefield.display_message(f"{super().get_user(battlefield).get_name()}'s Air Lock ability activated! The weather affecting the battlefield calms and disappears!")
    
    def pre_turn(self, battlefield : PokeBattle):
        pass

    def pre_user_damage(self, battlefield : PokeBattle):
        pass

    def pre_target_damage(self, battlefield : PokeBattle):
        pass

    def on_faint(self, battlefield : PokeBattle):
        pass

    def pre_field_tick(self, battlefield : PokeBattle):
        # Check for an active weather condition.
        if battlefield.get_field_effect("weather") is not None:
            # Remove the weather condition.
            battlefield.set_field_effect("weather", None)
            # Display a message.
            battlefield.display_message(f"{super().get_user(battlefield).get_name()}'s Air Lock ability activated! The weather affecting the battlefield calms and disappears!")

    def pre_effect_tick(self, battlefield : PokeBattle):
        pass

    def post_turn(self, battlefield : PokeBattle):
        pass