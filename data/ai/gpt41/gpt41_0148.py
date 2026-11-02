import os
import random
import string

# ==== Constants ====
ROWS = 6
COLUMNS = 7
MAX_COLUMNS = 26
NUM_PLAYERS = 2  # Can be 2-5 as per assignment; 2 for final submission
PLAYER_CHECKERS = ['X', 'O', 'V', 'H', 'M']
EMPTY_CELL = ' '

# ==== Utility Functions ====

def clear_screen():
    os.system('clear')  # For Unix/Linux compatibility

def create_board(rows, cols):
    return [[EMPTY_CELL for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    cols = len(board[0])
    # Print column headers
    headers = '  ' + '   '.join([string.ascii_uppercase[i] for i in range(cols)])
    print(headers)
    print('+' + '---+' * cols)
    for row in board:
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
        print('+' + '---+' * cols)

def column_letter_to_index(letter):
    if letter.upper() in string.ascii_uppercase[:COLUMNS]:
        return string.ascii_uppercase.index(letter.upper())
    return -1

def is_valid_column_input(letter, board):
    if len(letter) != 1 or letter not in string.ascii_uppercase[:COLUMNS]:
        return False
    col_idx = column_letter_to_index(letter)
    # Check if column is not completely full
    return board[0][col_idx] == EMPTY_CELL

def get_next_open_row(board, col):
    for row in reversed(range(len(board))):
        if board[row][col] == EMPTY_CELL:
            return row
    return -1  # Column is full

def place_checker(board, row, col, checker):
    board[row][col] = checker

def switch_player(current_ix):
    return (current_ix + 1) % NUM_PLAYERS

def board_full(board):
    return all(cell != EMPTY_CELL for cell in board[0])

def check_for_win(board, checker):
    rows = len(board)
    cols = len(board[0])

    # Horizontal
    for r in range(rows):
        for c in range(cols-3):
            if all(board[r][c+i] == checker for i in range(4)):
                return True

    # Vertical
    for c in range(cols):
        for r in range(rows-3):
            if all(board[r+i][c] == checker for i in range(4)):
                return True

    # Diagonal (positive slope)
    for r in range(rows-3):
        for c in range(cols-3):
            if all(board[r+i][c+i] == checker for i in range(4)):
                return True
    
    # Diagonal (negative slope)
    for r in range(3, rows):
        for c in range(cols-3):
            if all(board[r-i][c+i] == checker for i in range(4)):
                return True
    return False

# ==== Main Game Function ====

def main():
    board = create_board(ROWS, COLUMNS)
    available_checkers = PLAYER_CHECKERS[:NUM_PLAYERS]

    # Randomly select the first player
    current_player = random.randint(0, NUM_PLAYERS - 1)

    while True:
        clear_screen()
        print_board(board)
        print(f"Player {available_checkers[current_player]}, please enter a column:")

        # Get and validate input
        while True:
            col_input = input().strip().upper()
            if not is_valid_column_input(col_input, board):
                # Check if input is a valid column and not full
                if len(col_input) != 1 or col_input not in string.ascii_uppercase[:COLUMNS]:
                    print(f"Invalid input. Enter a letter between A and {string.ascii_uppercase[COLUMNS-1]}.")
                elif board[0][column_letter_to_index(col_input)] != EMPTY_CELL:
                    print("Column is full. You lose your turn.")
                    current_player = switch_player(current_player)
                    break
                else:
                    print("Invalid input. Try again.")
            else:
                col_ix = column_letter_to_index(col_input)
                row_ix = get_next_open_row(board, col_ix)
                place_checker(board, row_ix, col_ix, available_checkers[current_player])
                # After move, print updated board if the player lost turn due to full column
                clear_screen()
                print_board(board)
                # Check for win
                if check_for_win(board, available_checkers[current_player]):
                    print(f"Player {available_checkers[current_player]} won!")
                    return
                # Check for draw
                if board_full(board):
                    print("It's a draw!")
                    return
                # Next player's turn
                current_player = switch_player(current_player)
                break

if __name__ == "__main__":
    main()
