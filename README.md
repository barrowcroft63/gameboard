# gameboard

# A class to load and manipulate gameboards from 'tab' files

Gameboard 'tab' files are created using the gameboard designer (https://github.com/barrowcroft63/gameboarddesigner.git).
They can be opened, and their tokens manipulated, using this gamboard module.

Installation:

`pip install git+https://github.com/barrowcroft63/gameboard.git`

### Use

Create the gameboard object:

`gameboard: Gameboard = Gameboard()`

Attach a callback that will be invoked when a cell on the gameboard is selected.

`gameboard.cell_selected_callback = self.cell_selected`

The callback should be of the form: 

`Optional[Callable[[tuple[int,int]],None]]`

The integers being passed representing the 'row' and 'column' (zero based) of the selected cell.

#### Loading a gameboard

To load a gameboard use:

`gameboard.load(filename)`

To draw the board use:

`gameboard.draw()`

#### Tokens

When the gameboard is defined a number of named tokens may be added.

To get a list of named tokens use:

`gameboard.list_tokens()`

To place a token use:

`gameboard.place_token(token_name, row, column)`

NOTE: Row and colun numbers are zero based.

To move a token use:

`gameboard.move_token(token_name, from_row, from_column, to_row, to_column)`

To remove a token use:

`gameboard.remove_token(token_name, row, column)`