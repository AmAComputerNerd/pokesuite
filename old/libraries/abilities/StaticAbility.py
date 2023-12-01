import random
from libraries.Pokemon import Pokemon
from libraries.PokeAbility import PokeAbility
from libraries.PokeBattle import PokeBattle

class StaticAbility(PokeAbility):
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
        pass

    def pre_field_tick(self, battlefield : PokeBattle):
        target : Pokemon = PokeAbility.get_target(battlefield)
        # None check for target - if target has fainted, ability cannot activate
        if target == None:
            return
        # Check if the last target's attack, (1) Hit the user, (2) Was a Physical attack
        if target.missed or not (target.get_last_move().get_data().get_damage_class() == "physical"):
            # Target did not make physical contact with the user, so Static can't activate.
            return
        # Target attack hit. Perform chance checks.
        rand = random.randint(1, 100)
        # Chance check: 30% to apply Paralysis
        if rand <= 30:
            # Chance check passed, activate ability
            target.add_effect("paralysis")
            battlefield.display_message(f"{PokeAbility.get_user().get_name()}'s Static activated! {target.get_name()} was paralysed.")
            return
        # Chance check failed, just return
        return

    def pre_effect_tick(self, battlefield : PokeBattle):
        pass

    def post_turn(self, battlefield : PokeBattle):
        pass