import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def create_board():
    """ Create a game board with initialized empty spaces. """
    return [[' ' for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    """ Print the game board to the console. """
    os.system('clear')
    headers = ' '.join(chr(65 + i) for i in range(COLUMNS))
    print(f"  {headers}")
    for row in board:
        print("+---" * COLUMNS + "+")
        print("| " + ' | '.join(row) + " |")
    print("+---" * COLUMNS + "+")

def is_valid_column(column):
    """ Check if the column label is valid within board boundaries. """
    return column.isalpha() and 0 <= ord(column.upper()) - 65 < COLUMNS

def get_next_open_row(board, col):
    """ Return the next open row in the given column. """
    for r in range(ROWS-1, -1, -1):
        if board[r][col] == ' ':
            return r
    return None

def place_checker(board, row, col, checker):
    """ Place a checker in the board at the specified location. """
    board[row][col] = checker

def check_for_win(board, checker):
    """ Check if there is a winning sequence for the given checker. """
    # Check horizontal locations for win
    for c in range(COLUMNS - 3):
        for r in range(ROWS):
            if all(board[r][c+i] == checker for i in range(4)):
                return True

    # Check vertical locations for win
    for c in range(COLUMNS):
        for r in range(ROWS - 3):
            if all(board[r+i][c] == checker for i in range(4)):
                return True

    # Check positively sloped diagonals
    for c in range(COLUMNS - 3):
        for r in range(ROWS - 3):
            if all(board[r+i][c+i] == checker for i in range(4)):
                return True

    # Check negatively sloped diagonals
    for c in range(COLUMNS - 3):
        for r in range(3, ROWS):
            if all(board[r-i][c+i] == checker for i in range(4)):
                return True

    return False

def check_for_draw(board):
    """ Check if the board is fully occupied and has no winner. """
    return all(board[0][c] != ' ' for c in range(COLUMNS))

def main():
    board = create_board()
    print_board(board)
    current_turn = random.randint(0, PLAYERS - 1)
    game_over = False
    
    while not game_over:
        checker = CHECKERS[current_turn]
        valid_input = False
        
        while not valid_input:
            column_choice = input(f"Player {checker}, please enter a column: ").strip()
            if len(column_choice) == 1 and is_valid_column(column_choice):
                col = ord(column_choice.upper()) - 65
                row = get_next_open_row(board, col)
                
                if row is not None:
                    place_checker(board, row, col, checker)
                    valid_input = True
                else:
                    print("Column is full. Try another one.")
            else:
                print("Invalid input. Please enter a valid column letter.")

        print_board(board)

        if check_for_win(board, checker):
            print(f"Player {checker} won!")
            game_over = True
        elif check_for_draw(board):
            print("The game is a draw!")
            game_over = True
        else:
            current_turn = (current_turn + 1) % PLAYERS

if __name__ == "__main__":
    main()
