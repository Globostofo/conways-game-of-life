from typing import List
import pygame as pg

class Cell:

    colors: List[pg.Color] = [pg.Color("white"),
                              pg.Color("black")]

    def __init__(self, row:int, col:int, size:int, padding:int) -> None:
        self.__alive = False
        self.neighbors = []

        self.CELL_RECT = pg.Rect(col*size+padding, row*size+padding,
                                 size-2*padding, size-2*padding)
        # TODO: upgrade change state system
        self.__FUNC = [self.__die, self.__born]
    
    def is_alive(self) -> bool:
        return self.__alive
    
    def __get_color(self) -> pg.Color:
        return Cell.colors[self.is_alive()]

    def __born(self) -> None:
        self.__alive = True

    def __die(self) -> None:
        self.__alive = False

    def __count_alive_neighbors(self) -> int:
        c = 0
        for neighbor_cell in self.neighbors:
            c += neighbor_cell.is_alive()
        return c
    
    def get_next_state(self) -> bool:
        c = self.__count_alive_neighbors()
        return c == 3 or self.is_alive() and c == 2

    def set_state(self, state: bool) -> None:
        self.__FUNC[state]()

    def draw(self, window: pg.Surface) -> None:
        pg.draw.rect(window, self.__get_color(), self.CELL_RECT)
    