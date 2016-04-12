from sys import argv

from pokedex import PokedexEntry

for poke in argv[1:]:

    print("-------------")
    print(PokedexEntry(poke))

print("-------------")
