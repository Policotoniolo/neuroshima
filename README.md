# Neuroshima Game
$${\color{red}WARNING\space CODE\space NOT\space FINISHED}$$	
The script is not yet complete. At present, we can only generate game phases between players, but there are still a number of problems and ergonomics to be reviewed. Unit tests are also planned.

Please let me know if you have any recommendations or improvements if you want, I'd be happy to - it's my first project like this! 

---

The aim of this project is to reproduce the board game Neuroshima Hex ([web site neuroshima](https://neuroshima-hex.azharis.fr/)).
I don't have any licenses or rights, so this is a little project just for practice.

Only 1 vs 1 (the main game mode) will be implemented here. Players will have to play on the same PC.


## Game rules
[ONLINE RULE LINK](https://neuroshima-hex.azharis.fr/rs/NH3_regles_FR.pdf)

Otherwise here's a summary:

The game is played on a hexagonal board made up of 19 hexagons.
![alt text](https://i2.wp.com/www.toysandgeek.fr/images/2014/03/neuroshima-5.jpg)

Each player has an army made up of 35 tiles including one HQ tile (example: army [moloch](https://neuroshima-hex.azharis.fr/armee/tuiles/moloch.html))

#### Aim of the game: 
Each player's aim is to attack his opponent's Headquarters (HQ).
opponent's HQ. At the start of the game, each HQ has 20 “Life Points”.
If, during the course of the game, an HQ loses its last Life Point, it is destroyed and the player controlling it is eliminated from the game.

If, at the end of the game, no HQ has been destroyed, players compare the number of Life Points in their HQs. The player with the least damaged HQ (the one with the most Life Points) wins the game.

#### Game phases:
##### 1. Initiating the game : 
Each player shuffles his deck of face-down tiles (without qg) and the first player is drawn at random.

Le premier joueur puis le second posent chacun leur qg sur le borde

##### 2. Player's turn
On his turn, a player draws tiles until he has 3 (i.e. at no time can he have more than 3 tiles in front of him) and places them face down on the board. 
Special case: only one tile is drawn on turn 1, and 2 on turn 2, to balance out the beginning.

Before doing anything else, he must discard one of these 3 tiles (generally the least useful) into his discard pile. He then chooses what to do with each of the remaining 2 tiles: he can play them, keep them for future turns, or discard them.

A player may discard any number of tiles he has drawn.
Drawn tiles must be visible to both players and placed face-up in front of the player who draws them.

There are two types of tile in the game: Action tiles and Unit tiles. These two types are clearly differentiated so that they can be easily identified: Action tiles feature a single, large black pictogram, while Unit tiles feature a single, large black pictogram. 
pictogram, while Unit tiles contain more information.
Action tiles represent specific, immediate actions. They are not placed on the game board.
Unit tiles represent the units in your army. Each army has 3 types of Unit: HQ, Fighters and Modules. To play a Unit tile, the player places it on a free hex of his choice on the board.


![alt text](image/readme_images/exemple_tuiles.png)

If, before the end of the game, one of the players draws his last Army tile but has
has less than 3 tiles in front of him, he is not obliged to discard any.
Once a player has completed his turn (drawing, playing or discarding tiles and
desired actions), he informs his opponent

##### 3. Combat phase
If the board becomes full, or if a player plays an action tile which triggers a combat, a combat phase is initiated.
Tile effects are applied in order of initiative (black number on unit tiles). Module effects are permanent as long as the module is on the board.
Combat takes place in initiative phases, from largest to smallest. In each phase, the unit tiles apply their other damage.

![alt text](image/readme_images/caracteristiques_tuiles.png)
The battle ends when all initiative phases have been completed.
More details in the link to the online rules.
[LIEN REGLE EN LIGNE](https://neuroshima-hex.azharis.fr/rs/NH3_regles_FR.pdf)


##### 4. End of game and victory 

Once a player has drawn the last tile from his army, he takes his turn as normal. His opponent then takes a final turn, and the Final Combat begins.

The game ends after the Final Combat or as soon as an HQ's Life Points are reduced to zero.

If one of the HQs is destroyed, the game ends and the player whose HQ is still standing wins.

If one of the HQs is destroyed during a battle, the game does not end until the battle is over. If the other HQ is also destroyed, the game ends in a draw.

If neither HQ is destroyed at the end of the Final Combat, the player controlling the HQ with the most Life Points wins.


## CODE EXPLANATION

The entire script can be found in the “scripts” folder.
The code is built around a Model-View-Controller (M-V-C) pattern.

- the model (scripts.model) contains the data to be displayed;
- the view (scripts.view) contains the presentation of the graphical interface;
- the controllers (scripts.controllers) contain the logic for user actions.

The “scripts.utils.function.py” file: contains generic functions.
scripts.utils.config.py": contains generic variables.

The scripts use the Pygame python library to generate the various game elements.


---
### MODEL 

The model contains the various elements of the game, represented by classes:
- Class Tile: represents a tile. Initializes with all tile characteristics (type, attack, hit point, etc.).
- Class Deck: represents an army's deck, i.e. 35 instances of Tile initialized with files from the scripts/armies folder. 
- Class Hand: represents a player's hand, i.e. the 3 tiles available at the start of a turn.
- Class Player: represents a player. He owns an instance of Deck and Hand.
- Class HexBoard: represents the game board. Played tiles are recorded in attributes.

#### Note position and angle of rotation of tiles:

Position on board are cubic coordinates (q,r,s):

![alt text](image/readme_images/cube_coordinates2.png)


Tile, net, shield and attacks are also defined by coordinates. 
These coordinates represent the angle with respect to the position (0,0,0) on the board, and therefore the direction in which the attack (or other) takes place.

An index has been defined according to the angle of rotation of the tile. This recalculates the directions of the tile's attack, shield and net attributes when the tile has been rotated.

### VIEW

a sprite is an object in the pygame library. It represents a kind of image.

The view.py file contains the various elements to be displayed, each represented by a class. They are used in the file's Class View.
list of elements used in the View class:
 - TileView: represents a tile in sprite form, with a few extra features
 - Hexagon: represents a hexagon (a zone) on the board
 - BoardZone: represents all hexagons on the board
 - EndButton: button to end the turn
 - RerollButton: not yet used, will re-initialize the turn
 - DiscardZone: zone for discarding a tile. Simply drag a tile over it
 - KeepZone: Zone used to keep a tile for the player's next turn. Simply drag a tile over it.
 - Button: generates a button on a given board position.

Here, tile positions are calculated in relation to the position (x,y) of screen pixels.


Board positions : 


                                8  (451,155)
                    4 (377,198)               13 (525,199)
        1 (302,241)             9  (451,241)                17 (599,242)
                    5 (376,284)               14 (525,284) 
        2 (301,326)             10 (451,327)                18 (598,328)
                    6 (376,369)               15 (525,370) 
        3 (301,411)             11 (450,413)                19 (598,413)
                    7 (376,455)               16 (524,455)
                                12 (450,499) 

The links between pixels and cube coordinates are as follows:

    {1:[(302,241), (-2,0,2)], 
    2:[(301,326), (-2,1,1)],
    3:[(301,411), (-2,2,0)],
    4:[(377,198), (-1,-1,0)],
    5:[(376,284), (-1,0,-1)],
    6:[(376,369), (-1,1,0)],
    7:[(376,455), (-1,2,-1,)],
    8:[(451,155), (0,-2,2)],
    9:[(451,241), (0,-1,1)],
    10:[(451,327), (0,0,0)],
    11:[(450,413), (0,1,-1)],
    12:[(450,499), (0,2,-2)],
    13:[(525,199), (1,-2,1)],
    14:[(525,284), (1,-1,0)],
    15:[(525,370), (1,0,-1)],
    16:[(524,455), (1,1,-2)],
    17:[(599,242), (2,-2,0)],
    18:[(598,328), (2,-1,-1)],
    19:[(598,413), (2,0,-2)]}

### CONTROLLER
This module is the link between the model and the view.
The main controller is gamecontroller.py (GameController). It contains the logic for the game. It uses different sub-controllers:

- moduleevaluator.py (ModuleEvaluator): 
    Handles evaluation of specific modules in the game.
- tileactioncontroller.py (TileController): 
    Manages tile-specific actions, such as movement or special
    abilities.
- boardcontroller.py (BoardController): 
    Responsible for handling board updates and interactions.
- battleevaluator.py (BattleEvaluator): 
    Evaluates battles between players on the board.
- playerscontroller.py (PlayersController): 
    Handles player-specific actions, such as drawing tiles or
    ending turns.





## LAUNCHING THE GAME

The game is started by executing the “main.py” file.

A window opens

![alt text](image/readme_images/partie1.png)

you can then drag and drop the qg tile onto the board and click on the end-of-turn button. The operation is repeated for the next player.

![alt text](image/readme_images/partie2.png)

Players can then draw tiles and play them. Like the HQs, the tiles are dragged and dropped onto the board. Right-click on a tile to rotate it.

![alt text](image/readme_images/video.gif)

For action tiles, highlighted areas are displayed for actions. Only the combat tile (tile with a kind of explosion on it) doesn't do anything for the moment, as I haven't coded the combats yet.

![alt text](image/readme_images/video2.gif)

There's no ending yet, as battles can't be launched.