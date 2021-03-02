import random


class LabObject:
    def __init__(self, name, q):
        self.name = name
        self.q = q

    def is_bag(self):
        return False

    def is_potion(self):
        return False


class Potion(LabObject):
    potion_types = ["HP_recover", "HP_enhance", "MANA_recover", "MANA_enhance", "NOTHING"]

    def __init__(self, t, q):
        super().__init__("Potion", q)
        self.t = t if t in Potion.potion_types else "NOTHING"

    def __str__(self):
        return "Potion {} of {}".format(self.t, self.q)

    def is_potion(self):
        return True


class Bag(LabObject):
    def __init__(self, q):
        super().__init__("Bag of coins", q)

    def __str__(self):
        return "Bag of coins with {} coins".format(self.q)

    def is_bag(self):
        return True


class Enemy:
    enemy_choices = [(1, "ATTACK"), (2, "DEFEND")]

    def __init__(self, name, hp, mana, aggr, strenght, int):
        self.name = name
        self.hp = hp
        self.mana = mana
        self.aggresivity = aggr  # between 0 and 1
        self.strenght = strenght
        self.int = int

    def change_hp(self, plus_hp):
        self.hp += plus_hp

    def is_dead(self):
        return self.hp <= 0

    def random_choice(self):
        aggr = min(int(self.aggresivity * 100), 100)
        passi = max(100 - aggr, 0)

        choices = [Enemy.enemy_choices[0]] * aggr + [Enemy.enemy_choices[1]] * passi

        return random.choice(choices)

    def update(self):
        pass


class Player:
    player_classes = ["W", "M", "N"]

    warrior_hp_mul = 0.2
    warrior_mana_mul = 0
    mage_hp_mul = 0
    mage_mana_mul = 0.2

    def __init__(self, name, hp, mana, pclass, strenght, int, inventory=None):
        self.name = name

        self.pclass = pclass if pclass in Player.player_classes else "W"

        hp_mul = 0
        if self.pclass == "W":
            hp_mul = Player.warrior_hp_mul
        elif self.pclass == "M":
            hp_mul = Player.mage_hp_mul
        else:
            hp_mul = 0

        mana_mul = 0
        if self.pclass == "W":
            mana_mul = Player.warrior_mana_mul
        elif self.pclass == "M":
            mana_mul = Player.mage_mana_mul
        else:
            mana_mul = 0

        self.hp = hp * (1 + hp_mul)
        self.max_hp = self.hp

        self.mana = mana * (1 + mana_mul)
        self.max_mana = self.mana

        self.strenght = strenght * (1 + hp_mul)
        self.int = int * (1 + mana_mul)

        self.coins = 0
        self.inventory = [] if inventory is None else inventory

    def drink(self, o: Potion):
        index = Potion.potion_types.index(o.t)

        if index == 0:
            self.change_hp(o.q)
        elif index == 1:
            self.enhance_hp(o.q)
        else:
            print("not implemented")
            pass

    def add_object(self, o: LabObject):
        self.inventory.append(o)

    def is_dead(self):
        return self.hp <= 0

    def has_mana(self):
        return self.mana > 0

    def gain_coins(self, cs):
        self.coins += cs

    def lose_coins(self, cs):
        self.coins -= cs
        self.coins = max(0, self.coins)

    def change_hp(self, plus_hp):
        self.hp += plus_hp
        self.hp = min(self.max_hp, self.hp)

    def enhance_hp(self, plus_hp):
        self.max_hp += plus_hp

    def class_to_string(self):
        if self.pclass == "W":
            return "warrior"
        elif self.pclass == "M":
            return "mage"
        else:
            return "NULL"

    def __str__(self):
        class_string = self.class_to_string()
        greeting = "Im {}, a {} with hp:{}, mana: {}, strenght: {}, intellignce: {}".format(self.name, class_string, self.hp, self.mana, self.strenght, self.int)

        return greeting

    def update(self):
        pass


class Node:
    def __init__(self, id, enemies=None, objets=None):
        self.id = id
        self.enemies = [] if enemies is None else enemies
        self.objets = [] if objets is None else objets
        self.is_exit = False

    def update(self):
        pass


class Graph:
    def __init__(self, nodes=None, edges=None):
        self.nodes = [] if nodes is None else nodes
        self.edges = [] if edges is None else edges

    def ids(self):
        return [n.id for n in self.nodes]

    def add_node(self, new_node):
        if new_node.id in self.ids():
            return False
        else:
            self.nodes.append(new_node)
            return True

    def add_edge(self, new_edge):
        (id1, id2) = new_edge
        ids = self.ids()

        if id1 in ids and id2 in ids:
            self.edges.append(new_edge)
            return True
        else:
            return False

    def update(self):
        for node in self.nodes:
            node.update()

    def get_node(self, id):
        for node in self.nodes:
            if id == node.id:
                return node
        return None

    def adjacents(self, id):
        adjs = [id_out for (id_in, id_out) in self.edges if id_in == id]
        return adjs


class Board:
    def __init__(self, graph, player):
        self.graph = graph
        self.player = player
        self.enemies_defeated = 0
        self.pieces_visited = []
        self.number_of_moves = 0

    def update(self):
        self.graph.update()
        self.player.update()

