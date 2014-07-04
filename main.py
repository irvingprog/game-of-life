#!/usr/bin/python
# -*- encoding: utf-8 -*-
#
# Copyright 2014 - Irving Prog
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://github.com/irvingprog/game-of-life
import pygame as pg


class Cell(object):
    def __init__(self, rect, pos):
        super(Cell, self).__init__()
        self.status = None
        self.color = (255, 255, 255)
        self.border_color = (0, 0, 0)
        self.rect = rect
        self.pos = pos
        self.border = 1

    def set_status(self, status):
        self._status = status

        if self.status:
            self.color = (0, 255, 0)
        else:
            self.color = (0, 0, 0)

    def get_status(self):
        return self._status

    status = property(get_status, set_status,
                      doc='Setter and getter status of cell')

    def __str__(self):
        return "cell, status:{0}, fila:{1[0]} columna; {1[1]}".format(
            self.status, self.pos)

    def draw(self, screen):
        pg.draw.rect(screen, self.color, self.rect)
        if self.border:
            pg.draw.rect(screen, self.border_color, self.rect, self.border)


class GameScene(object):

    def __init__(self):
        self.witdth_tiled = 80
        self.height_tiled = 60
        size_tile = 800 / self.witdth_tiled

        self.cells = []
        for row in range(self.height_tiled):
            for col in range(self.witdth_tiled):
                rect = pg.Rect(col*size_tile, row*size_tile,
                               size_tile, size_tile)
                self.cells.append(Cell(rect, (row+1, col+1)))

        self.auto_generation = False

        gosper_glider = [(7, 32), (8, 30), (8, 32),
                         (9, 20), (9, 21), (9, 28),
                         (9, 29), (9, 42), (9, 43),
                         (10, 19), (10, 23), (10, 28),
                         (10, 29), (10, 42), (10, 43),
                         (11, 8), (11, 9), (11, 18),
                         (11, 24), (11, 28), (11, 29),
                         (12, 8), (12, 9), (12, 18),
                         (12, 22), (12, 24), (12, 25),
                         (12, 30), (12, 32), (13, 18),
                         (13, 24), (13, 32), (14, 19),
                         (14, 23), (15, 20), (15, 21)]

        for cell in self.cells:
            if cell.pos in gosper_glider:
                cell.status = True

    def update(self):
        for event in pg.event.get():

            if event.type == pg.KEYDOWN:
                self.check_key_pressed(event.key)

            if event.type == pg.MOUSEBUTTONDOWN:
                self.check_click_over_cells(event.pos)

        if self.auto_generation:
            self.regeneration()

    def check_key_pressed(self, key):
        if key == pg.K_ESCAPE:
            exit()
        elif key == pg.K_p:
            self.auto_generation = not self.auto_generation
        elif key == pg.K_s:
            self.regeneration()
        elif key == pg.K_i:
            print self.get_pos_live_cells()
        elif key == pg.K_b:
            self.borders()

    def borders(self):
        for cell in self.cells:
            cell.border = not cell.border

    def draw(self, screen):
        for cell in self.cells:
            cell.draw(screen)

        pg.display.flip()

    def check_click_over_cells(self, pos):
        for cell in self.cells:
            if cell.rect.collidepoint(pos[0], pos[1]):
                self.change_status(cell)

    def get_pos_live_cells(self):
        return [cell.pos for cell in self.cells if cell.status]

    def change_status(self, cell):
        cell.status = not cell.status

    def regeneration(self):
        cells_to_update = []
        for index, cell in enumerate(self.cells):
            neighbours = self.check_neighbours(index, cell)
            if cell.status:
                if not neighbours in [2, 3]:
                    cells_to_update.append(cell)
            else:
                if neighbours in [3]:
                    cells_to_update.append(cell)

        for cell in cells_to_update:
            self.change_status(cell)

    def check_neighbours(self, pos_cell, cell):
        neighbours = 0
        row, column = cell.pos

        if row > 1:
            before_row = pos_cell - self.witdth_tiled
            if self.cells[before_row].status:       # neighbour up-center
                neighbours += 1

        if row > 1 and column > 1:                  # neighbour up-left
            if self.cells[before_row-1].status:
                neighbours += 1

        if row > 1 and column < self.witdth_tiled:  # neighbour up-right
            if self.cells[before_row+1].status:
                    neighbours += 1

        if row < self.height_tiled:                 # neighbour bottom-center
            after_file = pos_cell + self.witdth_tiled
            if self.cells[after_file].status:
                neighbours += 1

        if row < self.height_tiled and column > 1:  # neighbour bottom-left
            if self.cells[after_file-1].status:
                neighbours += 1

        if row < self.height_tiled and column < self.witdth_tiled:
            if self.cells[after_file+1].status:     # neighbour bottom-right
                neighbours += 1

        if column > 1:                              # neighbour left
            before_cell = self.cells[pos_cell-1]
            if before_cell.status:
                neighbours += 1

        if column < self.witdth_tiled:              # neighbour right
            after_cell = self.cells[pos_cell+1]
            if after_cell.status:
                neighbours += 1

        return neighbours


def main():
    screen = pg.display.set_mode((800, 600))
    pg.display.set_caption('Game of life')
    pg.init()
    clock = pg.time.Clock()

    scene = GameScene()

    while True:
        scene.update()
        scene.draw(screen)
        clock.tick(40)

if __name__ == '__main__':
    main()