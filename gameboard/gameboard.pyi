import datetime
import os

from tkinter import Canvas, Tk
from PIL import ImageTk
from typing import Self, Optional, Any, Callable


class Gameboard:
    def __init__(self) -> None:
        """__init__

        Initialises the gameboard.

        """
        date = datetime.date.today()

        self.name: str = "NEW"

        self.version:str = "1.0.0"
        self.date:str = date.strftime("%Y")
        self.author: str = os.getlogin()

        self.width_of_left_outer_boarder: int = 10
        self.width_of_top_outer_boarder: int = 10
        self.width_of_right_outer_boarder: int = 10
        self.width_of_bottom_outer_boarder: int = 10
        self.colour_of_outer_boarder: str = "#CCCCCC"

        self.width_of_left_inner_boarder: int = 10
        self.width_of_top_inner_boarder: int = 10
        self.width_of_right_inner_boarder: int = 10
        self.width_of_bottom_inner_boarder: int = 10
        self.colour_of_inner_boarder: str = "#BBBBBB"

        self.number_of_cells_horizontally: int =5
        self.number_of_cells_vertically: int = 5
        self.width_of_cell: list[int] = [100,100,100,100,100]
        self.height_of_cell: list[int] = [100,100,100,100,100]
        self.left_padding_of_cell: list[int] = [1,0,0,0,0]
        self.top_padding_of_cell: list[int] = [1,0,0,0,0]
        self.right_padding_of_cell: list[int] = [1,1,1,1,1]
        self.bottom_padding_of_cell: list[int] = [1,1,1,1,1]
        self.size_of_horizontal_gutter_after_cell: list[int] = [0,0,0,0,0]
        self.size_of_vertical_gutter_after_cell: list[int] = [0,0,0,0,0]
        self.colour_of_cell: list[list[str]] = [["#BBBBBB","#BBBBBB","#BBBBBB","#BBBBBB","#BBBBBB"],["#BBBBBB","#BBBBBB","#BBBBBB","#BBBBBB","#BBBBBB"],["#BBBBBB","#BBBBBB","#BBBBBB","#BBBBBB","#BBBBBB"],["#BBBBBB","#BBBBBB","#BBBBBB","#BBBBBB","#BBBBBB"],["#BBBBBB","#BBBBBB","#BBBBBB","#BBBBBB","#BBBBBB"]]
        self.colour_of_cell_padding: list[list[str]] = [["#000000","#000000","#000000","#000000","#000000"],["#000000","#000000","#000000","#000000","#000000"],["#000000","#000000","#000000","#000000","#000000"],["#000000","#000000","#000000","#000000","#000000"],["#000000","#000000","#000000","#000000","#000000"]]
        self.colour_of_cell_gutter: str = "#BBBBBB"
        self.cell_decorator: list[list[str]] = [["","","","",""],["","","","",""],["","","","",""],["","","","",""],["","","","",""],]
        self.board_decorator: list[tuple[str,int,int]] = []
        self.tokens:list[tuple[str, str]] = []
        self.placed_tokens: list[list[str]] = [["","","","",""],["","","","",""],["","","","",""],["","","","",""],["","","","",""],]

        self.saved:bool = False
        
        self.images:dict[str, ImageTk.PhotoImage] = {}
        self.cell_selected_callback:Optional[Callable[[tuple[int,int]],None]]  = None
        
    def save(self, filename: str) -> str:
        ...

    @classmethod
    def load(cls, filename: str) -> tuple[Optional[Self], str]:
        ...

    def call_back(self, cell_selected_callback:Optional[Callable[[tuple[int,int]],None]]):
        ...

    def draw(self, root: Tk) -> Canvas:

        ...


    def list_tokens(self)->list[str]:
        ...

    def place_token(self, name:str, row:int, column:int)-> None:
        ...

    def move_token(self, name:str, from_row:int, from_column:int, to_row:int, to_column:int):
        ...
        
    def remove_token(self, name:str, row:int, column:int)-> None:
        ...