from utils import randbool
from utils import randcell
from utils import randcell2
from helicopter import Helicopter

# 0 🟩 - поле
# 1 🌲 - дерево 
# 2 🌊 - река
# 3 🏥 - госпиталь
# 4 🏦 - апгрейд-шоп
# 5 🔥 - огонь
# 🚁 - вертолет
# ⚪️☁️ облако
# ⚡ гроза
# 🛢️ tank
# ❤️ здоровье (lives)
# ⭐ баллы (score)
# ⬛️ 🟧 frame (рамка поля)

CELL_TYPES = '🟩🌲🌊🏥🏦🔥'
TREE_BONUS = 100         # бонусы за потушенное дерево
UPGRADE_PRICE = 5000     # стоимость апгрейда вертолета 
LIFE_COST = 10000        # стоимость улучшения здоровья (lives)

class Map:
    def __init__(self, w, h):
        self.w = w
        self.h = h
        self.cells = [[0 for i in range(w)] for j in range(h)]
        self.generate_forest(5, 10)
        self.generate_river(10)
        self.generate_river(10)
        self.generate_upgrade_shop()
        self.generate_hospital()

    def check_bounds(self, x, y):
        if (x < 0 or y < 0 or x >= self.h or y >= self.w):
             return False
        return True
    
    # рендер игрового поля
    def print_map(self, helico, clouds):
        print('⬛️' * (self.w + 2)) # верхняя рамка
        for ri in range(self.h):
            print('⬛️', end="") # левая рамка
            for ci in range(self.w):
                cell = self.cells[ri][ci]
                if (clouds.cells[ri][ci] == 1):
                    print("⚪️", end="")
                elif (clouds.cells[ri][ci] == 2):
                    print("⚡", end="")
                elif (helico.x == ri and helico.y == ci):
                    print("🚁", end="")
                elif (cell >= 0 and cell < len(CELL_TYPES)):
                    print(CELL_TYPES[cell], end="")               
            print('⬛️') # правая рамка
        print('⬛️' * (self.w + 2)) # нижняя рамка

    # генерация реки
    def generate_river(self, l):
        rc = randcell(self.w, self.h)
        rx, ry = rc[0], rc[1]
        self.cells[rx][ry] = 2
        while l > 0:
            rc2 = randcell2(rx, ry)
            rx2, ry2 = rc2[0], rc2[1]
            if (self.check_bounds(rx2, ry2)):
                self.cells[rx2][ry2] = 2
                rx, ry = rx2, ry2
                l -= 1

    # инициализация леса (начальная)
    def generate_forest(self, r, mxr):
        for ri in range(self.h):
            for ci in range(self.w):
                if randbool(r, mxr):
                    self.cells[ri][ci] = 1

    # генерация дерева
    def generate_tree(self):
        c = randcell(self.w, self.h)
        cx, cy = c[0],c[1]
        if (self.check_bounds(cx, cy) and self.cells[cx][cy] == 0):
            self.cells[cx][cy] = 1
    
    # генерация госпиталя
    def generate_hospital(self):
        c = randcell(self.w, self.h)
        cx, cy = c[0], c[1]
        if self.cells[cx][cy] != 4:
            self.cells[cx][cy] = 3
        else:
            self.generate_hospital()

    # генерация магазина
    def generate_upgrade_shop(self):
        c = randcell(self.w, self.h)
        cx, cy = c[0], c[1]
        self.cells[cx][cy] =  4

    # генерация огня
    def add_fire(self):
        c = randcell(self.w, self.h)
        cx, cy = c[0], c[1]
        if self.cells[cx][cy] == 1:
            self.cells[cx][cy] = 5
    
    # обновление огня
    def update_fires(self, helico):
        for ri in range(self.h):
            for ci in range(self.w):
                cell = self.cells[ri][ci]
                if cell == 5:
                    if helico.score > 0:
                        # количество очков минус за каждое сгоревшее дерево
                        helico.score -= 10
                    # распространение пожара
                    move = [[-1, -1], [0, -1], [1, -1], [1, 0], [1, 1], [0, 1], [-1, 1], [-1, 0]]
                    for n in move:
                        nx, ny = ri + n[0], ci + n[1]
                        if self.check_bounds(nx, ny) is True:
                            if self.cells[nx][ny] == 1:
                                self.cells[nx][ny] = 5
                    self.cells[ri][ci] = 0
        # новые очаги пожара
        for i in range(8):
            self.add_fire()

    # проверка действий вертолета
    def process_helicopter(self, helico, clouds):
        c = self.cells[helico.x][helico.y]
        d = clouds.cells[helico.x][helico.y]
        # пополнение бака водой
        if (c == 2):
            helico.tank = helico.mxtank
        # тушение дерева и получение очков
        if (c == 5 and helico.tank > 0):
            helico.tank -= 1
            helico.score += TREE_BONUS
            self.cells[helico.x][helico.y] = 1
        # увеличение объема бака
        if (c == 4 and helico.score >= UPGRADE_PRICE):
            helico.mxtank +=1
            helico.score -= UPGRADE_PRICE
        # увеличение lives
        if (c == 3 and helico.score >= LIFE_COST):
            helico.lives +=1
            helico.score -= LIFE_COST
        # попадание в грозу, уменьшение lives, или конец игры
        if (d == 2):
            helico.lives -= 1
            if (helico.lives == 0):
                helico.game_over()
    
    # сохранение
    def export_data(self):
        return {"cells": self.cells}
    
    # загрузка сохранения
    def import_data(self, data):
        self.cells = data["cells"] or [[0 for i in range(self.w)] for j in range(self.h)]