from pynput import keyboard
from map import Map
from clouds import Clouds
import time
import os
import json
from helicopter import Helicopter as Helico

TICK_SLEEP = 0.05       # тики смены кадров
TREE_UPDATE = 50        # частота появления деревьев
CLOUDS_UPDATE = 100     # частота обновления облаков
FIRE_UPDATE = 75        # частота появления огня
MAP_W, MAP_H = 20, 10   # размеры игрового поля

field = Map(MAP_W, MAP_H)
clouds = Clouds(MAP_W, MAP_H)
helico = Helico(MAP_W, MAP_H)

tick = 1

MOVES = {'w': (-1, 0), 'd': (0, 1), 's': (1, 0), 'a': (0, -1)}

# f - сохранение, g - загрузка сохранения (восстановление)
# обработка нажатия клавиш
def process_key(key):
    global helico, tick, clouds, field
    c = key.char.lower()
    
    # обработка движений вертолета
    if c in MOVES.keys():
        dx, dy = MOVES[c][0], MOVES[c][1]
        helico.move(dx, dy)

    # сохранение игры
    if c == 'f':
        data = {"helicopter": helico.export_data(),
                "clouds": clouds.export_data(),
                "field": field.export_data(),
                "tick": tick}
        with open("level.json", "w") as lvl:
            json.dump(data, lvl)
    
    # загрузка сохранения
    elif c == 'g':
        with open("level.json", "r") as lvl:
            data = json.load(lvl)
            tick = data["tick"] or 1
            helico.import_data(data["helicopter"])
            field.import_data(data["fields"])
            clouds.import_data(data["clouds"])

listener = keyboard.Listener(
    on_press = None,
    on_release = process_key)
listener.start()

while True:
    # print("\033[F"*15) # коряво, но чинит blinking в терминале в windows
    os.system("cls") # clear для mac os/linux
    # print("TICK", tick)
    # print(helico.x, helico.y)
    field.process_helicopter(helico, clouds)
    helico.print_stats()
    field.print_map(helico, clouds)
    tick += 1
    time.sleep(TICK_SLEEP)
    if (tick % TREE_UPDATE == 0):
        field.generate_tree()
    if (tick % FIRE_UPDATE == 0):
        field.update_fires(helico)
    if (tick % CLOUDS_UPDATE == 0):
        clouds.update()
        