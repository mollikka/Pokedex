from utils import fetch_json, dict_to_json
from config import POKEAPI, TYPEAPI

class PokedexEntry:
    def __init__(self, searchterm):
        pokemondata = fetch_json(POKEAPI+searchterm)

        self.name = pokemondata["name"]
        self.weight = pokemondata["weight"]/10

        types = [i["type"]["name"] for i in sorted(pokemondata["types"],key=lambda x:x["slot"])]
        self.primarytype = types[0]
        self.secondarytype = types[1] if len(types)>1 else None

        stats = {i["stat"]["name"]:i["base_stat"] for i in pokemondata["stats"]}
        self.hp = stats["hp"]
        self.defense = stats["defense"]
        self.attack = stats["attack"]
        self.spattack = stats["special-attack"]
        self.spdefense = stats["special-defense"]
        self.speed = stats["speed"]

        self.typeprofile = TypeProfile(self.primarytype, self.secondarytype)

    def __str__(self):
        s = ""
        s += "Name: " + self.name.title() + "    Weight: " + str(self.weight) + "\n"

        s += "Type modifiers against this Pokemon:\n"
        for poketype, modifier in sorted(self.typeprofile.type_modifiers.items(), key=lambda x: x[1]):
            s += poketype.ljust(20).title() + str(modifier) + "\n"

        return s

    def get_json(self):
        d = {
            "name": self.name.title(),
            "weight": self.weight,
            "primarytype": self.primarytype,
            "secondarytype": self.secondarytype,
            "typemods": [{"type":k,"value":v} for k,v in sorted(self.typeprofile.type_modifiers.items(),key=lambda x:x[1]) if v!=1],
            "hp": self.hp,
            "defense": self.defense,
            "attack": self.attack,
            "spattack": self.spattack,
            "spdefense": self.spdefense,
            "speed": self.speed,
        }
        return dict_to_json(d)

class TypeProfile:

    def __init__(self, primarytype, secondarytype):
        self.type_modifiers = {}

        typedata = fetch_json(TYPEAPI+primarytype)
        primary_damage_0 = [i['name'] for i in typedata['damage_relations']['no_damage_from']]
        primary_damage_50 = [i['name'] for i in typedata['damage_relations']['half_damage_from']]
        primary_damage_200 = [i['name'] for i in typedata['damage_relations']['double_damage_from']]

        if secondarytype:
            secondarytypedata = fetch_json(TYPEAPI+secondarytype)
            secondary_damage_0 = [i['name'] for i in secondarytypedata['damage_relations']['no_damage_from']]
            secondary_damage_50 = [i['name'] for i in secondarytypedata['damage_relations']['half_damage_from']]
            secondary_damage_200 = [i['name'] for i in secondarytypedata['damage_relations']['double_damage_from']]
        else:
            secondary_damage_0 = []
            secondary_damage_50 = []
            secondary_damage_200 = []

        for t in primary_damage_0 + secondary_damage_0:
            self.type_modifiers[t] = self.type_modifiers.get(t, 1)*0

        for t in primary_damage_50 + secondary_damage_50:
            self.type_modifiers[t] = self.type_modifiers.get(t, 1)*0.5

        for t in primary_damage_200 + secondary_damage_200:
            self.type_modifiers[t] = self.type_modifiers.get(t, 1)*2

