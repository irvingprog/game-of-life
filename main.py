#!/usr/bin/python
# -*- encoding: utf-8 -*-
#
# Copyright 2014 - Irving Prog
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://github.com/irvingprog/tres-en-raya
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
        self.cells = []

        self.witdth_tiled = 64
        self.height_tiled = 48
        size_tile = 640 / self.witdth_tiled

        for f in range(self.height_tiled):
            for c in range(self.witdth_tiled):
                rect = pg.Rect(c*size_tile, f*size_tile,
                               size_tile, size_tile)
                self.cells.append(Cell(rect, (f, c)))

        self.status = False

        gosper_glider = [(6, 31), (7, 29), (7, 31), (8, 19), (8, 20),
                         (8, 27), (8, 28), (8, 41), (8, 42), (9, 18),
                         (9, 22), (9, 27), (9, 28), (9, 41), (9, 42),
                         (10, 7), (10, 8), (10, 17), (10, 23), (10, 27),
                         (10, 28), (11, 7), (11, 8), (11, 17), (11, 21),
                         (11, 23), (11, 24), (11, 29), (11, 31), (12, 17),
                         (12, 23), (12, 31), (13, 18), (13, 22), (14, 19),
                         (14, 20)]

        for cell in self.cells:
            if cell.pos in gosper_glider:
                cell.status = True

    def update(self):
        for event in pg.event.get():

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    exit()
                elif event.key == pg.K_p:
                    self.status = not self.status
                elif event.key == pg.K_s:
                    self.regeneration()
                elif event.key == pg.K_i:
                    print self.get_pos_live_cells()
                elif event.key == pg.K_b:
                    self.borders()

            if event.type == pg.MOUSEBUTTONDOWN:
                for cell in self.cells:
                    if cell.rect.collidepoint(event.pos[0], event.pos[1]):
                        self.change_status(cell)

        if self.status:
            self.regeneration()

    def borders(self):
        for cell in self.cells:
            cell.border = not cell.border

    def draw(self, screen):
        for cell in self.cells:
            cell.draw(screen)

        pg.display.flip()

    def get_pos_live_cells(self):
        return [cell.pos for cell in self.cells if cell.status]

    def change_status(self, cell):
        cell.status = not cell.status

    def regeneration(self):
        cells_to_update = []
        for index, cell in enumerate(self.cells):
            neighbours = self.check_neighbours(index, cell)
            if cell.status:
                if not len(neighbours) in [2, 3]:
                    cells_to_update.append(cell)
            else:
                if len(neighbours) in [3, 6]:
                    cells_to_update.append(cell)

        for cell in cells_to_update:
            self.change_status(cell)

    def check_neighbours(self, index, cell):
        pos_cell = index
        neighbours = []

        if pos_cell > self.witdth_tiled:
            before_file = pos_cell - self.witdth_tiled
            if self.cells[before_file-1].status:
                neighbours.append(1)
            if self.cells[before_file].status:
                neighbours.append(1)
            if self.cells[before_file+1].status:
                neighbours.append(1)

        if pos_cell < (self.witdth_tiled * self.height_tiled
                       - self.witdth_tiled - 1):
            after_file = pos_cell + self.witdth_tiled
            if self.cells[after_file-1].status:
                neighbours.append(1)
            if self.cells[after_file].status:
                neighbours.append(1)
            if self.cells[after_file+1].status:
                neighbours.append(1)

        if pos_cell > 0:
            before_cell = self.cells[pos_cell-1]
            if before_cell.status and not cell.pos[1] == 0:
                neighbours.append(1)

        if pos_cell < len(self.cells) - 1:
            after_cell = self.cells[pos_cell+1]
            if (after_cell.status and
                    not cell.pos[1] == self.witdth_tiled-1):
                neighbours.append(1)

        return neighbours


def main():
    screen = pg.display.set_mode((640, 480))
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