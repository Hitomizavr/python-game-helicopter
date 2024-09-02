from utils import randcell
import os
class Helicopter:
    def __init__(self, w, h):
        rc = randcell(w, h)
        rx, ry = rc[0], rc[1]
        self.h = h
        self.w = w
        self.x = rx
        self.y = ry
        self.tank = 0
        self.mxtank = 1
        self.lives = 20
        self.score = 0

    # логика движения
    def move(self, dx, dy):
        nx, ny = dx + self.x, dy + self.y
        if (nx >= 0 and ny >= 0 and nx < self.h and ny < self.w):
            self.x, self.y = nx, ny

    # вывод статистики
    def print_stats(self):
        print('🛢️', self.tank, '/', self.mxtank, end="|")
        print('❤️', self.lives, end=" | ")
        print('⭐', self.score)

    # завершение игры
    def game_over(self):
        os.system("cls") # clear для mac os/linux
        print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
        print("X                                   X")
        print("X    GAME OVER, YOUR SCORE IS", self.score, "    X")
        print("X                                   X")
        print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
        exit(0)
    
    # сохранение
    def export_data(self):
        return {"score": self.score,
                "lives": self.lives,
                "x": self.x, "y": self.y,
                "tank": self.tank, "mxtank": self.mxtank }
    
    # загрузка сохранения
    def import_data(self, data):
        self.x = data["x"] or 0
        self.y = data["y"] or 0
        self.tank = data["tank"] or 0
        self.mxtank = data["mxtank"] or 1
        self.lives = data["lives"] or 3
        self.score = data["score"] or 0