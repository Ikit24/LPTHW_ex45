import time
import random
import sys
from sys import exit
from random import randint
from textwrap import dedent


class Scene(object):

    def enter(self):
        print("This scene is not yet configured.")
        exit(1)


class Engine(object):

    def __init__(self, scene_map):
        self.scene_map = scene_map

    def play(self):
        current_scene = self.scene_map.opening_scene()
        # print(f"Opening scene: {current_scene}")  # Debugging line
        # while True:
        #     if current_scene is None:
        #         print("Error: current_scene is None.")
        #         break  # Exit the loop if current_scene is None
        #
        #     next_scene_name = current_scene.enter()
        #     print(f"Next scene name: {next_scene_name}")  # Debugging line
        #
        #     current_scene = self.scene_map.next_scene(next_scene_name)
        #     print(f"New current scene: {current_scene}")  # Debugging line
        #
        #     if current_scene is None:
        #         print(f"Error: Scene '{next_scene_name}' not found.")
        #         break  # Exit the loop if next scene is not found

        while True:
            next_scene_name = current_scene.enter()
            current_scene = self.scene_map.next_scene(next_scene_name)


class Entrance(Scene):

    def enter(self):
        print(dedent("""
             It's 42nd millennium there's only War.
             The Imperium of Man is besieged on all fronts by the mutant, the unclean
             and the heretic. The galaxy burns after an immense ork army assault
             several imperial worlds.

             While fighting a bloody, gruesome battle above planet Candria, your ship
             took serious damage and you and your crew was forced to abandon ship.
             You just managed to enter the escape pod and head to the planet below.
             You crash landed near some old ruins in the middle of a forest. Having 
             no way through the forest you choose to enter the ruins.             
             """))

        print(dedent("""
                Choices:
                1.Enter ruins.
                2.Turn back"""))

        action = input("What will you do?\n> ")

        if action == '1':
            print(dedent("""
                  You enter into the ruins, small beams of sunlight lighting up the
                  area. As you step deeper into the hall, you hear a growl and a loud
                  scream: 'WAAAGH!'
                  The perfidious Orks are present even on this Emperor forsaken planet.
                  You got no choice but to fight!
                  Due to the tough...'landing' your health is lower!
                  """))
            return 'combat'

        elif action == '2':
            print("There is nothing to return to. Only forward, in the Emperor's name!")
            return 'entrance'

        else:
            print("DOES NOT COMPUTE!")
            return 'entrance'


class Combat(Scene):

    def enter(self):
        self.player_health = 70
        self.opponent_health = 100
        self.opponent_waaagh_meter = 0

        while self.player_health > 0 and self.opponent_health > 0:
            self.display_stats()
            self.player_turn()
            if self.opponent_health <= 0:
                break
            self.opponent_turn()

        return self.who_won()

    def display_stats(self):
        print(f"Your Health: {self.player_health}")
        print(f"Opponent Health: {self.opponent_health}")
        print(f"Opponent Waaagh! Meter: {self.opponent_waaagh_meter}")

    def player_turn(self):
        print("\nIt's your turn!")
        choice = input("Choose action: [Attack or Heal]").strip().lower()
        if choice == "attack":
            damage = randint(10, 20)
            self.opponent_health -= damage
            print(f"You attacked the Ork for {damage} damage.")
        elif choice == 'heal':
            heal = randint(5, 15)
            self.player_health += heal
            if self.player_health > 100:
                self.player_health = 100
            print(f"You healed yourself for {heal} health.")
        elif choice == 'shoot!':
            damage = randint(100, 101)
            self.opponent_health -= damage
            print(f"You attacked the Ork for {damage} damage.")
            print(dedent("""
                  You wip out your trusty bolter, hmph only one bullet in it.
                  How...convenient!
                  You aim at the xeno, squeezing the trigger.
                  'BANG!' The blessed bullet flies through the Ork's head!
                  That's how it should be done! A bullet to the face!
                  \n"""))
        else:
            print("\nYou could be 'shoot!' from a bolter for not thinking about the fight!")

    def opponent_turn(self):
        print("\nIt's the Ork's turn!")
        if self.opponent_waaagh_meter >= 10:
            self.opponent_trigger_waaagh()
        else:
            action = random.choice(["attack", "charge_waaagh"])
            if action == "attack":
                damage = randint(10, 20)
                self.player_health -= damage
                print(f"The Ork attacks you for {damage} damage.")
            elif action == "charge_waaagh":
                charge = randint(3, 5)
                self.opponent_waaagh_meter += charge
                print(f"The opponent is charging its Waaagh! meter by {charge}!")

    def opponent_trigger_waaagh(self):
        print("The Ork triggers its Waaagh! Unleashes a powerful attack!")
        self.opponent_waaagh_meter = 0
        damage = randint(20, 50)
        self.player_health -= damage
        print(f"The Ork, empowered by the Waaagh!, unleashes its powerful attack, hitting you for {damage} damage!")

    def who_won(self):
        if self.opponent_health <= 0 or choice == "shoot!":
            print("YOU WON! Praise be to the Emperor!")
            return 'hall'
        elif self.player_health <= 0:
            print("\nYou have fallen in battle.")
            return 'death'
        else:
            print("The battle continues...")
            return None


class Hall(Scene):

    def enter(self):
        print(dedent("""
              Tired from the battle with the Ork you walk away,
              entering a great, some kind of Great hall.
              Two passages are before you
              """))

        print(dedent("""
                Choices:
                1.Left.
                2.Right."""))

        action = input("What will you do?\n> ")

        if action == '1':
            print(dedent("""
                  Walking through the unlit corridor, memories start to
                  come forward. Friends, comrades, the enlisting, the war,
                  the eternal war against things that warp the mind...
                  
                  Suddenly a cracking noise pulls you out of your daydreaming.
                  You hear a door slamming shut and your feet starts to get wet.
                  Wet!? Here? Impossible!
                  
                  Looks like you activated some kind of trap.
                  """))
            return 'trap'
        elif action == '2':
            return 'finish'
        else:
            print("DOES NOT COMPUTE!")


class Clock(Scene):
    def __init__(self, duration=10):
        self.duration = duration  # Set the duration, default is 10 seconds

    def start(self):
        print(f"Timer started for {self.duration} seconds.")

        print(dedent("""
              'The way is shut. It was made by those who are Dead,
              and the Dead keep it, until the time comes.'
              """))
        for remaining in range(self.duration, 0, -1):
            # Display the time remaining on the same line
            sys.stdout.write(f"\rTime remaining: {remaining} seconds")
            sys.stdout.flush()
            time.sleep(1)

        print("\nTime's up!")
        return 'death'


class Trap(Scene):
    def __init__(self):
        self.clock = Clock()  # Initialize the Clock within Trap

    def enter(self):
        print(dedent("""
              Just great! First the greenskin now this! This day just keeps getting
              better!

              'Complete flooding of the room in 10 seconds!' You hear it from the
              dark, probably it is some kind of old trap.
              """))
        print(dedent("""
                Choices:
                1. Swim forward, you might hit a switch.
                2. Try to force open the door!
                """))

        action = input("What will you do?\n> ")

        if action == '1':
            result = self.clock.start()  # Start the timer
            return result  # Return the result from the clock (which is 'death')

        elif action == '2':
            print(dedent("""
                  With full force you are pushing the door, in the dark.
                  It just won't budge.
                  You claw as a wild animal but can't seem to get a grip,
                  even a switch would be better, but alas that is not the
                  case.
                  """))
            return 'death'


class Death(Scene):

    quips = [
        "You die and now the xeno celebrates...great...",
        "You are dead what would the Emperor think?",
        "By the Inquisition! What a shame!",
        "I have a small puppy that's better at this.",
        "You're worse than a Grot!"
    ]

    def enter(self):
        print(Death.quips[randint(0, len(self.quips) - 1)])
        exit(1)


class Victory(Scene):

    def enter(self):
        print(dedent("""
              Sounds like there is a lot of going on outside.
              As you tumble into the blinding sunlight, you
              see that there is a full scale planetary invasion
              is going on, of course the Orks won't take a rest.
              
              Nor should you!
              
              You see the outline of a comissar in the distance.
              Probably yelling and giving orders to the fellow
              soilders of the Imperium. You take a deep breath
              and start to walk towards him.
              
              'Another day in the service of mankind' you think.
              
              Victory...?      
              """))
        exit(1)


class Map(object):
    scenes = {

        'entrance': Entrance(),
        'death': Death(),
        'finish': Victory(),
        'combat': Combat(),
        'hall': Hall(),
        'trap': Trap(),
        'clock': Clock(),

    }

    def __init__(self, start_scene):
        self.start_scene = start_scene

    def next_scene(self, scene_name):
        return Map.scenes.get(scene_name)

    def opening_scene(self):
        return self.next_scene(self.start_scene)


scene_map = Map('entrance')
game = Engine(scene_map)
game.play()
