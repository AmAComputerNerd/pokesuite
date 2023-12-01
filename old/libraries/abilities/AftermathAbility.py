from libraries.PokeAbility import PokeAbility
from libraries.PokeBattle import PokeBattle
from libraries.Pokemon import Pokemon

class AftermathAbility(PokeAbility):
    def __init__(self):
        pass

    def on_summon(self, battlefield : PokeBattle):
        pass
    
    def pre_turn(self, battlefield : PokeBattle):
        pass

    def pre_user_damage(self, battlefield : PokeBattle):
        pass

    def pre_target_damage(self, battlefield : PokeBattle):
        pass

    def on_faint(self, battlefield : PokeBattle):
        # Grab the user and target from the battlefield.
        user : Pokemon = super().get_user(battlefield)
        target : Pokemon = super().get_target(battlefield)
        # Check if the user is the target.
        if user == target:
            # User is the target, do nothing.
            return
        # User is not the target, check whether the target has fainted.
        if target.is_fainted():
            # Target has fainted, do nothing.
            return
        # Target has not fainted, check damage source.
        if user.get_last_damage_source() == "target":
            # Check if the last move used was a contact move.
            if target.get_last_move().get_data().get_damage_class() == "physical":
                # All checks passed, inflict damage.
                target.remove_health(target.get_max_health() / 4)
                battlefield.display_message(f"{user.get_name()}'s Aftermath ability activated! {target.get_name()} took damage from the recoil!")
        return

    def pre_field_tick(self, battlefield : PokeBattle):
        pass

    def pre_effect_tick(self, battlefield : PokeBattle):
        pass

    def post_turn(self, battlefield : PokeBattle):
        pass