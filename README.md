# Python Game "Helicopter"
!To run the game in the Windows terminal, you need the Windows Terminal program!

The program [Windows Terminal](https://apps.microsoft.com/detail/9n0dx20hk701?hl=ru-ru&gl=RU) with full Unicode support.

A terminal game with an emoji field where you have to put out trees from fire. 

## Installation
A console with full Unicode support is required to run the terminal game.

This project uses Python3. 

The library [Pygame](https://www.pygame.org) is also used.

To install pygame:
```
pip install pygame
```

The library [Pynput](https://pypi.org/project/pynput/) is also used.

To install pynput:
```
pip install pynput
```

Simply run main.py in folder game:
```
python .\main.py
```

Note: 

## The essence of the game
The main functionality is to extinguish a fire using a helicopter. To do this, you need to use a helicopter to fill a tank with water. Then fly to the fire pixel. During the game, the statistics of successfully extinguished trees and your health will be calculated.

## Main functions of the game
- Initialization of the game field and forest.
- Generation random appearance of rivers, trees, clouds and thunderstorms.
- If the tree burns down, you lose points.
- If we put the tree out, you get points.
- Move the helicopter using the keys WASD
- The helicopter has its own number of lives.
- Track your scores and health as you play
- Hospital for exchanging health for points.
- Saving and loading the game process (To save - F; To load a save - G).
- An upgrade shop where you can increase the number of water tanks.
- The save file is created in the game folder in the .json format.

## How to play
...

## Features to further improve the game
- Rewrite the game for the application window
- Replace emoji with icons

