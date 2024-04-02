import datetime
import os

from pickle import PickleError, dump, load
from tkinter import Canvas, Tk
from PIL import Image, ImageTk
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

        self.cell_dimensions:list[tuple[int,int,int,int,int,int]] = []

        self.saved:bool = False
        
        self.images:dict[str, ImageTk.PhotoImage] = {}
        self.cell_selected_callback:Optional[Callable[[tuple[int,int]],None]] = None

    def __setattr__(self, attr: str, val: Any) -> None:
        if attr not in ("saved","images","cell_selected_callback","cell_dimensions"):
            super().__setattr__("saved", False)
        super().__setattr__(attr, val)
        
    def save(self, filename: str) -> str:
        """save

        Saves the gameboard to a file.
        Returns an empty string if successful,
        otherwise returns error message.

        Args:
            filename (str): file of file to save to.

        Returns:
            str: Error message.
        """
        try:
            _callback = self.cell_selected_callback
            _images = self.images
            self.cell_selected_callback = None
            self.images = {}
            with open(filename, "wb") as f:
                dump(self, f)
                self.cell_selected_callback = _callback
                self.images = _images
                self.saved = True
            return ""
        except PickleError as err:
            return f"Error saving '{filename}' - {err}"

    @classmethod
    def load(cls, filename: str) -> tuple[Optional[Self], str]:
        """loads

        Loads the gameboard from a file.
        Returns the gameboard object if successful,
        otherwise returns error message.

        Args:
            filename (str): file of file toload from.

        Returns:
            str: Error message.
        """
        try:
            with open(filename, "rb") as f:
                obj: cls = load(f)
                obj.saved = True
            return obj, ""
        except (PickleError, Exception) as err:
            return None, f"Error loading '{filename}' - {err}"

    def call_back(self, cell_selected_callback:Optional[Callable[[tuple[int,int]],None]]):
        """call_back

        Sets the call back function to invoke when a cell on the board is selected.

        Args:
            cell_selected_callback (Callable[[tuple[int,int]],None]): functiomn to invoke.
        """
        self.cell_selected_callback = cell_selected_callback


    #  Calculated sizes.

    def size_of_row(self, _row: int) -> int:
        return (
            self.top_padding_of_cell[_row]
            + self.height_of_cell[_row]
            + self.bottom_padding_of_cell[_row]
            + self.size_of_horizontal_gutter_after_cell[_row]
        )

    def size_of_rows(self) -> int:
        _size: int = 0
        for _row in range(self.number_of_cells_vertically):
            _size += self.size_of_row(_row)
        return _size

    def size_of_column(self, _column: int) -> int:
        return (
            self.left_padding_of_cell[_column]
            + self.width_of_cell[_column]
            + self.right_padding_of_cell[_column]
            + self.size_of_vertical_gutter_after_cell[_column]
        )

    def size_of_columns(self) -> int:
        _size: int = 0
        for _column in range(self.number_of_cells_horizontally):
            _size += self.size_of_column(_column)
        return _size

    def width_of_inner_board(self) -> int:
        return (
            self.width_of_left_inner_boarder
            + self.size_of_columns()
            + self.width_of_right_inner_boarder
        )

    def height_of_inner_board(self) -> int:
        return (
            self.width_of_top_inner_boarder
            + self.size_of_rows()
            + self.width_of_bottom_inner_boarder
        )

    def width_of_outer_board(self) -> int:
        return (
            self.width_of_left_outer_boarder
            + self.width_of_inner_board()
            + self.width_of_right_outer_boarder
        )

    def height_of_outer_board(self) -> int:
        return (
            self.width_of_top_outer_boarder
            + self.height_of_inner_board()
            + self.width_of_bottom_outer_boarder
        )

    #  Drawing functions.

    def draw(self, root: Tk) -> Canvas:

        #  Create canvas.

        canvas = Canvas(
            root,
            width=self.width_of_outer_board(),
            height=self.height_of_outer_board(),
            highlightthickness=0
        )

        #  Draw outer boarder.

        canvas.create_rectangle(
            (0, 0),
            (
                self.width_of_outer_board(),
                self.height_of_outer_board(),
            ),
            fill=self.colour_of_outer_boarder,
            width=0,
        )

        #  Drawinner boarder.

        canvas.create_rectangle(
            (
                self.width_of_left_outer_boarder,
                self.width_of_top_outer_boarder,
            ),
            (
                self.width_of_left_outer_boarder + self.width_of_inner_board(),
                self.width_of_top_outer_boarder + self.height_of_inner_board(),
            ),
            fill=self.colour_of_inner_boarder,
            width=0,
        )

        #  Draw column area, provides colour for gutter.

        canvas.create_rectangle(
            (
                self.width_of_left_outer_boarder + self.width_of_left_inner_boarder,
                self.width_of_top_outer_boarder + self.width_of_top_inner_boarder,
            ),
            (
                self.width_of_left_outer_boarder
                + self.width_of_left_inner_boarder
                + self.size_of_columns(),
                self.width_of_top_outer_boarder
                + self.width_of_top_inner_boarder
                + self.size_of_rows(),
            ),
            fill=self.colour_of_cell_gutter,
            width=0,
        )

        _left: int = self.width_of_left_outer_boarder + self.width_of_left_inner_boarder
        _top: int = self.width_of_top_outer_boarder + self.width_of_top_inner_boarder

        self.cell_dimensions= []

        for _row in range(self.number_of_cells_vertically):
            for _column in range(self.number_of_cells_horizontally):

                #  Draw cell area including margins.

                canvas.create_rectangle(
                    (
                        _left,
                        _top,
                    ),
                    (
                        _left
                        + self.left_padding_of_cell[_column]
                        + self.width_of_cell[_column]
                        + self.right_padding_of_cell[_column],
                        _top
                        + self.top_padding_of_cell[_row]
                        + self.height_of_cell[_row]
                        + self.bottom_padding_of_cell[_row],
                    ),
                    width=0,
                    fill=self.colour_of_cell_padding[_row][_column],
                )

                #  Draw cell area without margins.

                _x1:int =  _left + self.left_padding_of_cell[_column]
                _y1:int = _top + self.top_padding_of_cell[_row]

                _x2:int = _left + self.left_padding_of_cell[_column] + self.width_of_cell[_column]
                _y2:int = _top+ self.top_padding_of_cell[_row]+ self.height_of_cell[_row]

                canvas.create_rectangle(
                    (_x1, _y1,), (_x2, _y2,),
                    width=0,
                    fill=self.colour_of_cell[_row][_column],
                )
                _left += self.size_of_column(_column)

                #  Show cell decorator.

                if self.cell_decorator[_row][_column] != "":
                    _decorator = self.get_image(self.cell_decorator[_row][_column], self.width_of_cell[_column] ,self.height_of_cell[_row])
                    canvas.create_image(_x1+(self.width_of_cell[_column]/2),_y1+(self.height_of_cell[_row]/2), image=_decorator)  # type:ignore

                #  Show placed token.

                if self.placed_tokens[_row][_column] != "":
                    _token = self.get_token(self.placed_tokens[_row][_column], self.width_of_cell[_column] ,self.height_of_cell[_row])
                    canvas.create_image(_x1+(self.width_of_cell[_column]/2),_y1+(self.height_of_cell[_row]/2), image=_token)  # type:ignore

                #  Record cell area.

                self.cell_dimensions.append((_x1,_x2,_y1,_y2,_row,_column))
                
            _left = self.width_of_left_outer_boarder + self.width_of_left_inner_boarder
            _top += self.size_of_row(_row)

            for _decorator_data in self.board_decorator:
                _decorator = self.get_image(_decorator_data[0], None, None)
                canvas.create_image(_decorator_data[1],_decorator_data[2], image=_decorator)  # type:ignore
            
        canvas.bind("<Button-1>", self.cell_selected) 

        return canvas

    #  Handle cell selection feedback.

    def cell_selected(self, *args:Any)-> None: 
        _x:int = args[0].x
        _y:int = args[0].y

        _row: int = -1
        _column: int = -1

        if self.cell_selected_callback is not None:

            for _cell in self.cell_dimensions:
                if (_cell[0] <= _x < _cell[1]) and (_cell[2] <= _y < _cell[3]):  
                    _row = _cell[4]
                    _column = _cell[5]
                    break
        
            self.cell_selected_callback((_row,_column))  

    #  Handle image retreival, resizing and caching.

    def get_token(self, name:str, width:Optional[int],height:Optional[int])-> Optional[ImageTk.PhotoImage]:

        for _token in self.tokens:
            if _token[0] == name:
                return self.get_image(_token[1],width,height)

    def get_image(self, filename:str, width:Optional[int],height:Optional[int])-> Optional[ImageTk.PhotoImage]:
        if filename in self.images:
            return self.images[filename]
        else:
            try:
                _image = Image.open(filename)   # type:ignore
                if width is not None and height is not None:
                    _resized_image = _image.resize((width, height))  # type:ignore
                else:
                    _resized_image = _image
                _decorator = ImageTk.PhotoImage(_resized_image)
                self.images[filename] = _decorator
                return _decorator
            except Exception:
                return None


    #  Methods for manipulating tokens.

    def list_tokens(self)->list[str]:
        return [_token[0] for _token in self.tokens]
    
    def place_token(self, name:str, row:int, column:int)-> None:
        if name not in self.list_tokens():
            raise ValueError(f"Named token '{name}' does not exist in gameboard definition.")
        
        if not ((row >= 0) and (row < self.number_of_cells_vertically)):
            raise ValueError(f"Row '{row}' is outside the limits (zero based) of the gameboard.")
        
        if not ((column >= 0) and (column < self.number_of_cells_horizontally)):
            raise ValueError(f"Column '{column}' is outside the limits (zero based) of the gameboard.")
        
        self.placed_tokens[row][column] = name

    def move_token(self, name:str, from_row:int, from_column:int, to_row:int, to_column:int):
        self.remove_token(name,from_row,from_column)
        self.place_token(name, to_row, to_column)
        
    def remove_token(self, name:str, row:int, column:int)-> None:
        if name not in self.list_tokens():
            raise ValueError(f"Named token '{name}' does not exist in gameboard definition.")
        
        if not ((row >= 0) and (row < self.number_of_cells_vertically)):
            raise ValueError(f"Row '{row}' is outside the limits (zero based) of the gameboard.")
        
        if not ((column >= 0) and (column < self.number_of_cells_horizontally)):
            raise ValueError(f"Column '{column}' is outside the limits (zero based) of the gameboard.")

        if self.placed_tokens[row][column] != name:
            raise ValueError(f"Token '{name}' is not at location, row '{row}' column '{column}'.")
        
        self.placed_tokens[row][column] = ""