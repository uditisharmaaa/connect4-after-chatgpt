import os
import random
import string
import sys

# -------- Constants --------
ROWS = 6
COLS = 7              # Max 26 supported
PLAYERS = 2           # Between 2 and 5
CHECKERS = ["X", "O", "V", "H", "M"][:PLAYERS]
EMPTY_CELL = " "
WIN_CONDITION = 4
COLUMN_LABELS = list(string.ascii_uppercase[:COLS])

# -------- Helper Functions --------

def clear_screen():
    os.system('clear')

def create_board():
    return [[EMPTY_CELL for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    # Print column headers
    print()
    for label in COLUMN_LABELS:
        print(f'  {label} ', end='')
    print()
    print('+' + '---+' * COLS)
    
    for row in board:
        print('|', end='')
        for cell in row:
            print(f' {cell} |', end='')
        print()
        print('+' + '---+' * COLS)
        
def get_player_input(current_checker, board):
    prompt = f'Player {current_checker}, please enter a column: '
    while True:
        choice = input(prompt).strip().upper()
        # Validate input: single letter, correct range
        if len(choice) != 1 or choice not in COLUMN_LABELS:
            print("Invalid column. Please enter a letter for an available column.")
            continue
        col = COLUMN_LABELS.index(choice)
        # Check if column is full
        if board[0][col] != EMPTY_CELL:
            print("Column is full. You lose your turn!")
            return None  # Lose turn
        return col

def drop_checker(board, col, checker):
    # Drop the checker to the lowest empty cell in the column
    for row in reversed(range(ROWS)):
        if board[row][col] == EMPTY_CELL:
            board[row][col] = checker
            return row, col
    return None

def check_win(board, checker):
    # Check horizontal, vertical, diagonal for win
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLS - WIN_CONDITION + 1):
            if all(board[row][col + i] == checker for i in range(WIN_CONDITION)):
                return True
    # Check vertical
    for row in range(ROWS - WIN_CONDITION + 1):
        for col in range(COLS):
            if all(board[row + i][col] == checker for i in range(WIN_CONDITION)):
                return True
    # Check positive diagonal (/)
    for row in range(WIN_CONDITION - 1, ROWS):
        for col in range(COLS - WIN_CONDITION + 1):
            if all(board[row - i][col + i] == checker for i in range(WIN_CONDITION)):
                return True
    # Check negative diagonal (\)
    for row in range(ROWS - WIN_CONDITION + 1):
        for col in range(COLS - WIN_CONDITION + 1):
            if all(board[row + i][col + i] == checker for i in range(WIN_CONDITION)):
                return True
    return False

def check_draw(board):
    # If no empty cells in top row, board is full
    return all(cell != EMPTY_CELL for cell in board[0])

# -------- Main Game Function --------

def main():
    board = create_board()
    player_order = list(range(PLAYERS))
    first_player = random.choice(player_order)
    turn = first_player
    clear_screen()
    print_board(board)
    
    while True:
        checker = CHECKERS[turn]
        col = get_player_input(checker, board)
        clear_screen()

        if col is None:
            # Column full: lose turn, but still print state
            print_board(board)
            turn = (turn + 1) % PLAYERS
            continue
        
        result = drop_checker(board, col, checker)
        print_board(board)

        if check_win(board, checker):
            print(f"Player {checker} won!")
            break
        if check_draw(board):
            print("The game is a draw.")
            break

        turn = (turn + 1) % PLAYERS

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nGame interrupted.")
