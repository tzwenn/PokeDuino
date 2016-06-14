# PokeDuino

Generate a Generation I Pokemon on your computer and transfer it to a GameBoy using an Arduino as Game Link relay.

## Setup

Cut and strip a Game Link Cable open. Solder the inner wires onto jumper cables that you can connect to your Arduino.

     ___________
    |  6  *  2  |
     \_5__3__*_/   (at cable)


| Cable Pin | Name          | Color  |  Arduino Pin |
|-----------|---------------|--------|--------------|
| 2         | Serial Out    | Orange |  6           |
| 3         | Serial In     | Red    |  3           |
| 5         | Serial Clock  | Green  |  2           |
| 6         | GND           | Blue   |  GND         |

***Note that*** the ```Out``` and ```In``` wires are crossed from one end to the other, so it's recommended to completely open one socket and follow the color scheme there.

Clone the repository, upload ```SerialGameLinkProxy.ino``` to the Arduino
and install [pyserial](https://pypi.python.org/pypi/pyserial):

```
$ pip3 install pyserial
```

## Usage

You can use the ```pokecreator.py``` to generate a [PokemonDataStructure](http://bulbapedia.bulbagarden.net/wiki/Pok%C3%A9mon_data_structure_in_Generation_I) that can be piped into ```pokeduino.py``` and transferred to the GameBoy. Any Pokemon received during that trade will be likewise outputted to stdout and can be later restored.

```
$ ./pokecreator.py --species Mew --level 7 --moves Pound PayDay | ./pokeduino.py > received_pokemon.dat
```

See ```--help``` for a comprehensive list of specifiable fields and trade options.

#### Note for non-English games

Nicknames and species names are a mess.

When you use a non-English game, you'll need to set the Pokemon's nickname to match your uppercase native species translation. Otherwise the Pokemon will stick with its English species name as nickname.

Specify the nickname (and also possible original trainer info) at ```pokeduino.py```, since they are not integral part of the Pokemon data structure itself.

```
# German Example
$ ./pokecreator.py -s Bulbasaur | ./pokeduino.py -n BISASAM > received_pokemon.dat
```

## See also

* Adan Scotney's pokemon [trade protocol specification](http://www.adanscotney.com/2014/01/spoofing-pokemon-trades-with-stellaris.html) and [implementation](https://bitbucket.org/adanscotney/gameboy-spoof)
* Bulbapedia's great list of [in-game data structures](http://bulbapedia.bulbagarden.net/wiki/Save_data_structure_in_Generation_I)
* Esteban Fuentealba's [trade spoofer](https://github.com/EstebanFuentealba/Arduino-Spoofing-Gameboy-Pokemon-Trades) running ***on*** Arduino

