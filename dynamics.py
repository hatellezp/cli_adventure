import sys

from main import get_answer
from classes_and_stuff import *
import random

DEFENSE_RATIO = 0.7
FLEE_POSSIBILITY = 0.3
BACK_EXPOSED = 0.2
ATTACK_VALUE = 10

PLAYER_CHOICES = [(1, "ATTACK"), (2, "DEFEND"), (3, "TRY TO FLEE")]

CHOICES_IDS = [choice[0] for choice in PLAYER_CHOICES]

def choice_from_id(id):
    for choice in PLAYER_CHOICES:
        if choice[0] == id:
            return choice
    return -1, "NOTHING"

def display_status(board, enemy=None):
    player = board.player
    graph = board.graph

    first_part = "[player: {} hp: {} mana: {} moves: {}]".format(player.name, player.hp, player.mana, board.number_of_moves)
    first_part_length = len(first_part)

    second_part_length = 0
    second_part = ""
    if enemy is not None:
        second_part = "[enemy: {} hp: {} mana: {}]".format(enemy.name, enemy.hp, enemy.mana)
        second_part_length = len(second_part)


    length = max(first_part_length, second_part_length)


    first_part_left = (length - first_part_length) // 2
    first_part_right = (length - first_part_length) - first_part_left

    second_part_left = (length - second_part_length) // 2
    second_part_right = (length - second_part_length) - second_part_left

    first_part = "# " + first_part_left*" " + first_part + first_part_right*" " + " #"
    second_part = "# " + second_part_left * " " + second_part + second_part_right * " " + " #"

    length = max(len(first_part), len(second_part))

    status = "#"*length + "\n" + first_part
    if enemy is not None:
        status += "\n" + second_part

    status += "\n" + "#"*length

    print(status)


def combat(player: Player, enemy: Enemy, board: Board):
    print("# You encounter a {}!".format(enemy.name))

    if enemy.is_dead():
        print("# but it is in fact nothing else than remains!")
    else:

        enemy_attack = int(ATTACK_VALUE * enemy.strenght)
        player_attack = int(ATTACK_VALUE * player.strenght)

        terminating_condition = False
        flee = 0
        while not terminating_condition:
            board.update()
            enemy.update()
            display_status(board, enemy)
            flee = 0

            print("# what do you do?")
            for (choice_number, choice) in PLAYER_CHOICES:
                print("# {}- {}".format(choice_number, choice))

            choice = get_answer()
            enemy_choice = enemy.random_choice()

            if choice in CHOICES_IDS:
                choice = choice_from_id(choice)
                choice_number = choice[0]
                choice = choice[1]
                enemy_choice_id = enemy_choice[0]
                enemy_choice = enemy_choice[1]

                comb = choice_number, enemy_choice_id

                if comb == (1, 1):  # attack attack
                    print("# you and your enemy both attack!")

                    print("# you lose {} hp".format(enemy_attack))
                    print("# your enemy loses {} hp".format(player_attack))

                    player.change_hp(-enemy_attack)
                    enemy.change_hp(-player_attack)
                elif comb == (1, 2):
                    print("# you attack and you enemy defends")
                    attack_value = int(player_attack * DEFENSE_RATIO)
                    print("# your enemy loses {} hp".format(attack_value))

                    enemy.change_hp(-attack_value)
                elif comb == (2, 1):
                    print("# you defend and you enemy attack")
                    attack_value = int(enemy_attack * DEFENSE_RATIO)
                    print("# you lose {} hp".format(attack_value))

                    player.change_hp(-attack_value)
                elif comb == (2, 2):
                    print("# you both defend, but it is for nothing")
                elif comb == (3, 1):
                    flee = random.uniform(0, 1)
                    print("# you try to flee!")

                    if flee < FLEE_POSSIBILITY:
                        print("# but the enemy attack you anyway")
                        attack_value = int(enemy_attack * (1 + BACK_EXPOSED))
                        print("# you lose {} hp".format(attack_value))

                        player.change_hp(-attack_value)
                elif comb == (3, 2):
                    lee = random.uniform(0, 1)
                    print("# you try to flee")

                    if flee < FLEE_POSSIBILITY:
                        print("# you can't flee!")
                else:
                    print("# no idea how we got here")
            else:
                print("# you didn't knew what to do!")
                print("# you enemy choose to {}".format(enemy_choice[1]))

                enemy_choice_id = enemy_choice[0]
                if enemy_choice_id == 1:  # attack
                    print("# you lose {} hp".format(enemy_attack))

                    player.change_hp(-enemy_attack)
                elif enemy_choice_id == 2:
                    print("# your enemy defended but it was for nothing")
                else:
                    print("# your enemy doesn't know what to do either!")

            terminating_condition = flee >= FLEE_POSSIBILITY or enemy.is_dead() or player.is_dead()

        if flee >= FLEE_POSSIBILITY:
            print("# you flee the combat")
        elif enemy.is_dead() and not player.is_dead():
            print("# you succeed in terminating your enemy!")
        elif player.is_dead():
            print("### YOU DIED ###")
            end_adventure(board, player)


def end_adventure(board: Board, player: Player):
    print("# you found the exit, you gained {} coins".format(player.coins))
    display_status(board)

    sys.exit(0)


def object_interaction(player: Player, o: LabObject, board: Board):
    if o.is_bag():
        print("# you see a bag of coins with {} coins".format(o.q))

        print("# what do you want to do ?")
        print("# 1- TAKE")
        print("# 2- CONTINUE")

        answer = get_answer()

        if answer == 1:
            print("# you take the coins")
            player.gain_coins(o.q)
        elif answer == 2:
            print("# you choose to continue")
        else:
            print("# you try something weird with the bag but it does nothing")

    elif o.is_potion():
        print("# you see a potion of {} with a value {}".format(o.t, o.q))

        print("# what do you want to do ?")
        print("# 1- TAKE")
        print("# 2- DRINK")
        print("# 3-CONTINUE")

        answer = get_answer()

        if answer == 1:
            print("# you put the potion in your inventory")
            player.add_object(o)
        elif answer == 2:
            print("# you drink immediately the potion")
            player.drink(o)
        elif answer == 3:
            print("# you decide to continue without touching the potion")
        else:
            print("# you try something weird with the bag but it does nothing")
    else:
        print("# you don't know what to do with this, you continue your search")


def enter_room(board, node, player):
    if node.is_exit:
        print("# you find the exit!") 
        end_adventure(board, player)
    
    graph = board.graph
    adjs = graph.adjacents(node.id)

    enemies = node.enemies
    objets = node.objets

    # print(enemies)

    enemies = [enemy for enemy in enemies if not enemy.is_dead()]

    bags = [o for o in objets if o.is_bag()]
    potions = [o for o in objets if o.is_potion()]

    print("#####################################")
    print("#        you enter a new room       #")
    print("#####################################")

    print("# there are {} doors".format(len(adjs)))

    if len(enemies) == 0:
        print("# no enemies alive lucky!")
    else:
        print("# you see {} enemies, you will have to deal somehow with them all".format(len(enemies)))

    print("# you see {} bag(s) of coins".format(len(bags)))
    print("# you see {} potion(s)".format(len(potions)))

    for enemy in enemies:
        combat(player, enemy, board)


    for o in objets:
        object_interaction(player, o, board)


    print("# rembember, there are {} doors".format(len(adjs)))

    door = 1
    for adj in adjs:
        print("# door {} with number {}".format(door, adj))
        door += 1

    print("# you go to which door ?")


    god_choice = random.choice([i for i in range(1, len(adjs) +1)])
    answer = get_answer(god_choice)

    # print("adjs is", adjs, "and you choose", answer)
    print("# you (or the world) decide to go to door {}".format(answer))
    new_room = graph.get_node(answer)

    enter_room(board, new_room, player)





