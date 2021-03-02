# This is a sample Python script.
import sys
from classes_and_stuff import *
from dynamics import *

PLAYER = None
GRAPH = None
BOARD = None

PLAYER_BASE_STRENGHT = 1
PLAYER_BASE_INT = 1

ENEMY_MAX_HP = 200
ENEMY_MAX_MANA = 1000
ENEMY_NAMES = ["skeleton", "slime", "thug", "dog", "demon", "LITCH"]
ENEMY_MAX_STRENGTH = 1
ENEMY_MAX_INT = 1
NORMAL_ENEMY_MUL = 0.3

# objects
MAX_Q = 20

# enemies and number of objects
MAX_OBJ = 2
MAX_ENEMIES = 4

# map parameters
MAX_NODES = 10
DOOR_POSSIBILITY = 0.3


def generate_enemy(max_hp, max_mana, names, max_strenght, max_int):
    max_hp = max_hp * NORMAL_ENEMY_MUL
    hp = int(random.uniform(1, max_hp))
    mana = int(random.uniform(1, max_mana))
    name = random.choice(names)
    
    strenght = random.uniform(0, max_strenght)
    intelligence = random.uniform(0, max_int)

    aggr = random.uniform(0, 1)

    if name == "LITCH":
        hp = ENEMY_MAX_HP
        mana = ENEMY_MAX_MANA
        aggr = 1.0
        strenght = ENEMY_MAX_STRENGTH
        intelligence = ENEMY_MAX_INT

    enemy = Enemy(name, hp, mana, aggr, strenght, intelligence)
    return enemy


def generate_potion(max_q):
    t = random.choice(Potion.potion_types[:-1])
    q = int(random.uniform(1, max_q))

    return Potion(t, q)


def generate_bag(max_q):
    q = 10 * int(random.uniform(1, max_q))

    return Bag(q)

def generate_litch():
    enemy = Enemy("LITCH", ENEMY_MAX_HP, ENEMY_MAX_MANA, 1, ENEMY_MAX_STRENGTH, ENEMY_MAX_INT)

def generate_node(id, max_o, max_e, max_hp, max_mana, names, max_q, max_strenght, max_int):
    o_q = random.choice([i for i in range(max_o + 1)])
    e_q = random.choice([i for i in range(max_e + 1)])

    node = Node(id)

    for i in range(o_q):
        bag_or_potion = random.choice([1,2])

        if bag_or_potion == 1:
            o = generate_potion(max_q)
            node.objets.append(o)
        else:
            o = generate_bag(max_q)
            node.objets.append(o)


    for i in range(e_q):
        enemy = generate_enemy(max_hp, max_mana, names, max_strenght, max_int)

        if not (enemy.name == "LITCH"):
            node.enemies.append(enemy)

    return node

def generate_graph(max_size, door_possibility, max_o, max_e, max_hp, max_mana, names, max_q, max_strenght, max_int):
    size = random.choice([i for i in range(1, max_size)])
    size = max(5, size)

    graph = Graph()

    for i in range(size):
        node = generate_node(i, max_o, max_e, max_hp, max_mana, names, max_q, max_strenght, max_int)

        graph.add_node(node)

    # TODO: see after if you can doo two ways doors
    for i in range(size):
        for j in range(size):
            door_or_not = random.uniform(0,1)

            if door_or_not >= door_possibility and i != j:
                if (i,j) not in graph.edges:
                    graph.add_edge((i, j))
                if (j, i) not in graph.edges:
                    graph.add_edge((j, i))

    litch = generate_litch()
    litch_room = random.choice([i for i in range(size)])
    exit_room = random.choice([i for i in range(1, size)])  # never room zero

    graph.get_node(litch_room).enemies.append(litch)
    graph.get_node(exit_room).is_exit = True

    # TODO: add path from start to exit
    return graph


def get_answer(default=-1):
    answer = input("# your choice (it's a number): ").strip()

    try:
        answer = int(answer)
    except:
        answer = default

    return answer

def create_arena():
    p = Player("ki", 100, 0, "W")
    g = Graph()
    b = Board(g, p)

    return p, g, b


def valid_input(actual_input, choices):
    return actual_input in choices


def choose_from(message, choices):
    is_valid_input = False

    message = message + "\n# (Or type q to quit)\n"

    while not is_valid_input:
        answer = input(message).strip()

        if answer == "q":
            sys.exit(0)

        if valid_input(answer, choices):
            return answer


def begin_game():
    print("#######################################")
    print("#            node traveler            #")
    print("#######################################")

    message = "# Do you want to begin? (Y)es or (N)o ?"
    choices = ["N", "Y"]

    answer = choose_from(message, choices)

    if answer == "N":
        print("# see you later alligator!")
        print("#######################################")
        sys.exit(0)
    else:
        choose_player()

def choose_player():
    print("# do you want to be a warrior or a mage ?")
    print("# 1- WARRIOR (more life)")
    print("# 2- MAGE (more mana)")

    answer = get_answer(1)

    name = input("give us your name: ").strip()

    if answer == 1:
        player = Player(name, 100, 100, "W", PLAYER_BASE_STRENGHT, PLAYER_BASE_INT)
    elif answer == 2:
        player = Player(name, 100, 100, "M", PLAYER_BASE_STRENGHT, PLAYER_BASE_INT)

    PLAYER = player
    GRAPH = generate_graph(MAX_NODES, DOOR_POSSIBILITY, MAX_OBJ, MAX_ENEMIES, ENEMY_MAX_HP, ENEMY_MAX_MANA, ENEMY_NAMES, MAX_Q, ENEMY_MAX_STRENGTH, ENEMY_MAX_INT)

    BOARD = Board(GRAPH, PLAYER)
    zero = GRAPH.get_node(0)


    print("# you are: {}".format(PLAYER))

    enter_room(BOARD, zero, PLAYER)

if __name__ == '__main__':
    begin_game()


