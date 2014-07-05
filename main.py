#!/usr/bin/python
# -*- encoding: utf-8 -*-
#
# Copyright 2014 - Irving Prog
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://github.com/irvingprog/game-of-life
import pygame as pg


class Cell(object):
    def __init__(self, rect, index, pos, tiled, cells):
        super(Cell, self).__init__()
        self.status = None
        self.color = (255, 255, 255)
        self.border_color = (0, 0, 0)
        self.rect = rect
        self.index = index
        self.pos = pos
        self.witdth_tiled, self.height_tiled = tiled
        self.cells = cells
        self.border = 1
        self.neighbours = []

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

    def change_status(self):
        self.status = not self.status

    def meet_neighbours(self):
        row, column = self.pos

        if row > 1:
            before_row = self.index - self.witdth_tiled
            # neighbour up-center
            self.neighbours.append(self.cells[before_row])

        if row > 1 and column > 1:
            # neighbour up-left
            self.neighbours.append(self.cells[before_row - 1])

        if row > 1 and column < self.witdth_tiled:
            # neighbour up-right
            self.neighbours.append(self.cells[before_row + 1])

        if row < self.height_tiled:
            # neighbour bottom-center
            after_file = self.index + self.witdth_tiled
            self.neighbours.append(self.cells[after_file])

        if row < self.height_tiled and column > 1:
            # neighbour bottom-left
            self.neighbours.append(self.cells[after_file - 1])

        if row < self.height_tiled and column < self.witdth_tiled:
            # neighbour bottom-right
            self.neighbours.append(self.cells[after_file + 1])

        if column > 1:
            # neighbour left
            before_cell = self.index - 1
            self.neighbours.append(self.cells[before_cell])

        if column < self.witdth_tiled:
            # neighbour right
            after_cell = self.index + 1
            self.neighbours.append(self.cells[after_cell])

    def check_neighbours(self):
        neighbours = [n for n in self.neighbours if n.status]

        return len(neighbours)

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
        for row in xrange(self.height_tiled):
            for col in xrange(self.witdth_tiled):
                rect = pg.Rect(col * size_tile, row * size_tile,
                               size_tile, size_tile)

                self.cells.append(Cell(rect=rect,
                                       index=len(self.cells),
                                       pos=(row + 1, col + 1),
                                       tiled=(self.witdth_tiled,
                                              self.height_tiled),
                                       cells=self.cells))

        for cell in self.cells:
            cell.meet_neighbours()

        self.auto_generation = False
        self.mouse_draw = False

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
                cell.change_status()

    def update(self):
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                self.check_key_pressed(event.key)

            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                self.mouse_draw = True
                self.check_click_over_cells(event.pos)

            elif event.type == pg.MOUSEBUTTONUP and event.button == 1:
                self.mouse_draw = False

            elif event.type == pg.MOUSEMOTION:
                if self.mouse_draw:
                    self.check_mouse_motion_over_cells(event.pos)

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

    def check_mouse_motion_over_cells(self, pos):
        for cell in self.cells:
            if cell.rect.collidepoint(pos[0], pos[1]):
                cell.status = True

    def check_click_over_cells(self, pos):
        for cell in self.cells:
            if cell.rect.collidepoint(pos[0], pos[1]):
                cell.change_status()

    def get_pos_live_cells(self):
        return [cell.pos for cell in self.cells if cell.status]

    def regeneration(self):
        cells_to_update = []
        for cell in self.cells:
            neighbours = cell.check_neighbours()
            if cell.status:
                if not neighbours in [2, 3]:
                    cells_to_update.append(cell)
            else:
                if neighbours in [3]:
                    cells_to_update.append(cell)

        for cell in cells_to_update:
            cell.change_status()


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