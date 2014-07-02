#!/usr/bin/python
# -*- encoding: utf-8 -*-
#
# Copyright 2014 - Irving Prog
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://github.com/irvingprog/tres-en-raya
import pygame as pg


class Tile(object):

    def __init__(self, rect):
        super(Tile, self).__init__()
        self.rect = rect
        self.color = (0, 0, 0)

    def draw(self, screen):
        pg.draw.rect(screen, self.color, self.rect, 1)


class Cell(object):
    def __init__(self, rect, pos):
        super(Cell, self).__init__()
        self.state = None
        self.color = (255, 255, 255)
        self.rect = rect
        self.pos = pos

    def set_state(self, state):
        self._state = state

        if self.state:
            self.color = (55, 0, 255)
        else:
            self.color = (255, 0, 255)

    def get_state(self):
        return self._state

    state = property(get_state, set_state,
                     doc='Setter and getter state of cell')

    def __str__(self):
        return "cell, state:{0}, fila:{1[0]} columna; {1[1]}".format(
            self.state, self.pos)

    def draw(self, screen):
        pg.draw.rect(screen, self.color, self.rect)


class GameScene(object):

    def __init__(self):
        self.cells = []
        self.tiled = []

        self.witdth_tiled = 64
        self.height_tiled = 48
        size_tile = 640 / self.witdth_tiled

        for f in range(self.height_tiled):
            for c in range(self.witdth_tiled):
                rect = pg.Rect(c*size_tile, f*size_tile, size_tile, size_tile)
                self.cells.append(Cell(rect, (f, c)))
                self.tiled.append(Tile(rect))

        self.state = False

        a = [(6, 31), (7, 29), (7, 31), (8, 19), (8, 20), (8, 27), (8, 28),
             (8, 41), (8, 42), (9, 18), (9, 22), (9, 27), (9, 28), (9, 41),
             (9, 42), (10, 7), (10, 8), (10, 17), (10, 23), (10, 27), (10, 28),
             (11, 7), (11, 8), (11, 17), (11, 21), (11, 23), (11, 24), (11, 29),
             (11, 31), (12, 17), (12, 23), (12, 31), (13, 18), (13, 22),
             (14, 19), (14, 20)]

        for cell in self.cells:
            if cell.pos in a:
                cell.state = True

    def update(self):
        for event in pg.event.get():

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    exit()
                elif event.key == pg.K_p:
                    self.state = not self.state
                elif event.key == pg.K_s:
                    self.regeneration()
                elif event.key == pg.K_i:
                    self.get_pos_live_cells()

            if event.type == pg.MOUSEBUTTONDOWN:
                for cell in self.cells:
                    if cell.rect.collidepoint(event.pos[0], event.pos[1]):
                        self.change_state(cell)

        if self.state:
            self.regeneration()

    def draw(self, screen):
        for cell in self.cells:
            cell.draw(screen)

        for tile in self.tiled:
            tile.draw(screen)

        pg.display.flip()

    def get_pos_live_cells(self):
        pos = []
        for cell in self.cells:
            if cell.state:
                pos.append(cell.pos)
        print pos

    def change_state(self, cell):
        cell.state = not cell.state

    def regeneration(self):
        cells_to_update = []
        for index, cell in enumerate(self.cells):
            neighboors = self.check_neighboors(index, cell)
            if cell.state:
                if not len(neighboors) in [2, 3]:
                    cells_to_update.append((cell, False))

            else:
                if len(neighboors) in [3]:
                    cells_to_update.append((cell, True))

        for cell, val in cells_to_update:
            cell.state = val

    def check_neighboors(self, index, cell):
        pos_cell = index
        neighboors = []

        if not pos_cell < self.witdth_tiled:
            before_file = pos_cell - self.witdth_tiled
            if self.cells[before_file-1].state:
                neighboors.append(1)
            if self.cells[before_file].state:
                neighboors.append(1)
            if self.cells[before_file+1].state:
                neighboors.append(1)

        if pos_cell < (self.witdth_tiled * self.height_tiled
                       - self.witdth_tiled - 1):
            after_file = pos_cell + self.witdth_tiled
            if self.cells[after_file-1].state:
                neighboors.append(1)
            if self.cells[after_file].state:
                neighboors.append(1)
            if self.cells[after_file+1].state:
                neighboors.append(1)

        if pos_cell > 0:
            before_cell = self.cells[pos_cell-1]
            if before_cell.state and not cell.pos[1] == 0:
                neighboors.append(1)

        if pos_cell < len(self.cells) - 1:
            after_cell = self.cells[pos_cell+1]
            if after_cell.state and not cell.pos[1] == 63:
                neighboors.append(1)

        return neighboors


def main():
    screen = pg.display.set_mode((640, 480))
    pg.display.set_caption('Lifes game')
    pg.init()
    clock = pg.time.Clock()

    scene = GameScene()

    while True:
        scene.update()
        scene.draw(screen)
        clock.tick(40)

if __name__ == '__main__':
    main()