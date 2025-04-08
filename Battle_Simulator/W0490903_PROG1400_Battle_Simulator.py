import random
import os

# Function that, when called, clears the terminal screen.
def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

# Define Weapon parent class and initialize it's attributes.
class Weapon:
    def __init__(self, name, atk_damage, atk_speed) -> None:
        self.name = name
        self.atk_damage = atk_damage
        self.atk_speed = atk_speed
    
    # Gives a chance to attack twice based on your current weapon's speed.
    def Extra_Attack_Chance(self):
        if self.atk_speed == "slow":
            return random.random() < 0.1
        elif self.atk_speed == "fast":
            return random.random() < 0.2
        else:
            return False

# Define Sword sub-class.
class Sword(Weapon):
    def __init__(self, name, atk_damage, atk_speed) -> None:
        super().__init__(name, atk_damage, atk_speed)

    def Bleed_Chance(self): # Unused (Work-in-progress).
        if random.random() < 0.1:
            return True
        else:
            return False

# Define Bow sub-class.
class Bow(Weapon):
    def __init__(self, name, atk_damage, atk_speed) -> None:
        super().__init__(name, atk_damage, atk_speed)

# Define Character class.
class Character:
    def __init__(self, char_name, char_class, health, defense) -> None:
        self.char_name = char_name
        self.char_class = char_class
        self.health = health
        self.defense = defense
        self.equipped_weapon = None

    # Method to equip the character's weapon of choice.
    def Equip_Weapon(self, equipped_weapon):
        self.equipped_weapon = equipped_weapon
        print(f"{self.char_name} equipped {equipped_weapon.name}!")

    # Method to attack a specified target.
    def Attack(self, target):
        
        if self.equipped_weapon:
            damage = self.equipped_weapon.atk_damage
            print(f"{self.char_name} attacks {target.char_name} with {self.equipped_weapon.name}!")  
            target.Defend(damage)
            
            # If the extra attack chance succeeds, the character attacks again.
            if self.equipped_weapon.Extra_Attack_Chance():
                print(f"\n{self.char_name} attacks again!\n")
                self.Attack(target)
            
    # Method to calculate the damage taken based on the character's defense.
    def Defend(self, damage):
        adjusted_damage = (damage - self.defense)
        self.health -= adjusted_damage

        # If any character has their health reduced to zero or below, then they are defeated and the game is over.
        if self.health <= 0:
            print(f"\n\033[0m{self.char_name} was defeated!") # '\033[0m' resets the terminal colour.
            exit()
        else:
            print(f"{self.char_name} Defends {self.defense} damage! {adjusted_damage} damage taken! {self.health} Health remaining.")

# Main Game
def New_Game(player, enemy):
    
    print("Welcome to Battle Simulator!\n")
    weapon_selection = (input("Please choose your weapon:"
                         "\n[1] Iron Longsword"
                         "\n[2] Steel Claymore"
                         "\n[3] Oak Bow"
                         "\n[4] Yew Longbow"
                         "\n"
                         "\nSelection: "
                        )).strip()

    clear_terminal()

    if weapon_selection.isdigit():
        weapon_selection = int(weapon_selection)
        
        if weapon_selection == 1:
            player.Equip_Weapon(weapons[0])

        elif weapon_selection == 2:
            player.Equip_Weapon(weapons[1])

        elif weapon_selection == 3:
            player.Equip_Weapon(weapons[2])

        elif weapon_selection == 4:
            player.Equip_Weapon(weapons[3])
    else:
        player.Equip_Weapon(random.choice(weapons))

    enemy.Equip_Weapon(random.choice(weapons))

    player_turn = True    
    
    while True:
        
        if player_turn:
            print(f"\033[32m\n{player.char_name}'s Turn!\n") # '\033[32m' changes the terminal foreground colour to Green.
            player.Attack(enemy)
            player_turn = False
       
        else:
            print(f"\033[31m\n{enemy.char_name}'s Turn!\n") # '\033[31m' changes the terminal foreground colour to Red.
            enemy.Attack(player)
            player_turn = True

# Character objects (Player and Enemy).
player1 = Character("Zach", "Knight", 100, 5)
enemy1 = Character("Enemy", "Wizard", 100, 5)

# Weapon objects (List).
weapons = [
Sword("Iron Longsword", 10, "fast"),
Sword("Steel Claymore", 20, "slow"),
Bow("Oak Bow", 10, "fast"),
Bow("Yew Longbow", 20, "slow")
]

New_Game(player1, enemy1)