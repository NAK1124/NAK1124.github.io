"""
Task: Build Your Own Mini Pokémon Battle System

You will design two classes: Pokemon and Trainer.
These classes will work together to simulate a very simple Pokémon-style interaction.

-----------------------------------------------------
STEP 1: Define the Pokemon Class
-----------------------------------------------------
Each Pokemon object should have the following attributes:
  - name (str)
  - level (int)
  - max_hp (int)
  - curr_hp (int, starts equal to max_hp)
  - atk (attack power, int)
  - def (defense power, int)
  - owner (a Trainer object that owns this Pokémon)
  - fainted (boolean, starts as False)

Methods to implement:
  1. take_damage(damage): reduce curr_hp by damage. If curr_hp <= 0, set fainted = True.
  2. attack(other_pokemon): calculate damage as:
       damage = max(1, self.atk - other_pokemon.def)
     then call other_pokemon.take_damage(damage).
  3. heal(): restore curr_hp to max_hp and set fainted = False.
"""
from __future__ import annotations
from typing import Optional

class Pokemon:
    """
    A class that describes a Pokemon object from the game Pokemon

    === Public Attributes ===
    level: level of the Pokemon
    max_hp: max hp allowed for the Pokemon
    curr_hp: current hp of the Pokemon
    atk_power: atk power of the Pokemon
    def_power: defense power of the Pokemon
    owner: a Trainer that owns the Pokemon
    fainted: True if the Pokemon is fainted, False otherwise

    >>> pikachu = Pokemon("Pikachu", 10, 100, 20, 5)
    >>> bulbasaur = Pokemon("Bulbasaur", 10, 150, 15, 10)
    >>> pikachu.attack(bulbasaur)
    Pikachu attacks Bulbasaur for 10 damage!
    >>> bulbasaur.curr_hp
    140
    >>> bulbasaur.attack(pikachu)
    Bulbasaur attacks Pikachu for 10 damage!
    >>> pikachu.curr_hp
    90
    >>> bulbasaur.heal()
    >>> bulbasaur.curr_hp
    150
    """
    name: str
    level: int
    max_hp: int
    curr_hp: int
    atk_power: int
    def_power: int
    owner: Optional[Trainer]
    fainted: bool

    def __init__(self, name: str, level: int, max_hp: int,
                 atk_power: int, def_power: int) -> None:
        self.name = name
        self.level = level
        self.max_hp = max_hp
        self.curr_hp = max_hp
        self.atk_power = atk_power
        self.def_power = def_power
        self.owner = None
        self.fainted = False

    def take_damage(self, damage: int) -> None:
        """
        Decrease the curr_hp by damage.

        If curr_hp <= 0 after the method, the Pokemon gets fainted
        """
        self.curr_hp -= damage
        if self.curr_hp <= 0:
            self.fainted = True

    def attack(self, other_pokemon) -> None:
        """
        Attack <other_pokemon> Pokemon.

        Call the take_damage method from <other_pokemon> to inflict damage.

        """
        calculate_dmg = max(1, self.atk_power - other_pokemon.def_power)
        other_pokemon.take_damage(calculate_dmg)
        print(f"{self.name} attacks {other_pokemon.name} for {calculate_dmg} damage!")
        print(f"{other_pokemon.name} has {other_pokemon.curr_hp} HP left")

    def heal(self) -> None:
        """
        Heal the Pokemon.

        By healing, we mean making curr_hp to be max_hp and
        fainted to be False
        """
        self.curr_hp = self.max_hp
        self.fainted = False

"""
-----------------------------------------------------
STEP 2: Define the Trainer Class
-----------------------------------------------------
Each Trainer object should have the following attributes:
  - name (str)
  - level (int)
  - pokeballs (int, number of Pokémon they can still catch)
  - owned_pokemon (a list of Pokemon objects they own)

Methods to implement:
  1. catch(pokemon): if trainer has pokeballs left, add pokemon to owned_pokemon,
     set pokemon.owner = self, and reduce pokeballs by 1.
  2. choose_pokemon(): return one of the owned Pokémon (for now, just return the first one in the list).
"""
class Trainer:
    def __init__(self, name, level, pokeballs):
        self.name = name
        self.level = level
        self.pokeballs = pokeballs
        self.owned_pokemon = []

    def catch(self, pokemon):
        if self.pokeballs > 0:
            self.owned_pokemon.append(pokemon)
            pokemon.owner = self
            self.pokeballs -= 1
            print(f"{self.name} caught {pokemon.name}")
        else:
            print(f"{self.name} has no Pokeballs left!")

    def choose_pokemon(self):
        if self.owned_pokemon:
            return self.owned_pokemon[0]
        else:
            print(f"{self.name} has no Pokémon!")
            return None

    def heal_all(self):
        print(f"{self.name} healed all their Pokemon")
        for p in self.owned_pokemon:
            p.heal()



"""
-----------------------------------------------------
STEP 3: Test Your Classes
-----------------------------------------------------
Write code that:
  1. Creates two trainers (Ash and Misty).
  2. Gives each trainer a Pokémon (e.g., Pikachu and Staryu).
  3. Simulates a small battle where Pikachu attacks Staryu a few times.
  4. Shows when a Pokémon faints.
  5. Lets the trainer heal their Pokémon afterward.

-----------------------------------------------------
Example Output (what your program might print):
-----------------------------------------------------
Ash caught Pikachu!
Misty caught Staryu!

Pikachu attacks Staryu for 8 damage!
Staryu has 12 HP left.
Pikachu attacks Staryu for 8 damage!
Staryu has 4 HP left.
Pikachu attacks Staryu for 8 damage!
Staryu fainted!
"""
def simple_battle(pokemon1, pokemon2):
    print(f"Battle starts between {pokemon1.name} and {pokemon2.name}")

    while True:
        pokemon1.attack(pokemon2)
        if pokemon2.fainted:
            print(f"{pokemon2.name} fainted!")
            print(f"{pokemon1.name} wins!")
            break

        pokemon2.attack(pokemon1)
        if pokemon1.fainted:
            print(f"{pokemon1.name} fainted!")
            print(f"{pokemon2.name} wins!")
            break

    print("Battle over!")

if __name__ == "__main__":
    import doctest
    doctest.testmod()
    print("Battle Simulation Starts")

    ash = Trainer("Ash", 3, 5)
    misty = Trainer("Misty", 50, 8)

    pikachu = Pokemon("Pikachu", 10, 30, 12, 5)
    staryu = Pokemon("Staryu", 5, 24, 8, 6)

    ash.catch(pikachu)
    misty.catch(staryu)

    simple_battle(pikachu, staryu)

    ash.heal_all()
    misty.heal_all()

    print("Battle simulation complete")
