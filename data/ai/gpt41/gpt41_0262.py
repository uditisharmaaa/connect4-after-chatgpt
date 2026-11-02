import os
import random

# ==== CONSTANTS ====
ROWS = 6
COLUMNS = 7
MAX_COLUMNS = 26           # For generalization
NUM_PLAYERS = 2            # Set to 2 as per instructions
PLAYER_TOKENS = ['X', 'O', 'V', 'H', 'M']

# Assign tokens according to number of players
PLAYERS = PLAYER_TOKENS[:NUM_PLAYERS]

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    """Create a rows x cols board filled with ' ' spaces."""
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    # Print column headers
    header = '  ' + '   '.join(chr(ord('A') + i) for i in range(len(board[0])))
    print(header)
    print('+' + '---+' * len(board[0]))

    # Print rows
    for row in board:
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
        print('+' + '---+' * len(board[0]))

def get_column_index(column_input, num_cols):
    # get index from letter; must be uppercase and in the valid range
    if len(column_input) != 1:
        return -1
    col = ord(column_input.upper()) - ord('A')
    if 0 <= col < num_cols:
        return col
    else:
        return -1

def is_valid_move(board, col_index):
    # Returns True if at least top-most row in the column is empty, False otherwise
    return board[0][col_index] == ' '

def place_checker(board, col_index, token):
    # Place checker's token in the lowest available row in col_index. Return the row placed
    for row in reversed(range(ROWS)):
        if board[row][col_index] == ' ':
            board[row][col_index] = token
            return row
    return -1  # Should not happen if checked before

def check_for_win(board, token):
    # Horizontal check
    for row in range(ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row][col + i] == token for i in range(4)):
                return True
    # Vertical check
    for col in range(COLUMNS):
        for row in range(ROWS - 3):
            if all(board[row + i][col] == token for i in range(4)):
                return True
    # Diagonal down-right check
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if all(board[row + i][col + i] == token for i in range(4)):
                return True
    # Diagonal up-right check
    for row in range(3, ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row - i][col + i] == token for i in range(4)):
                return True
    return False

def is_draw(board):
    # Draw if top row is fully filled
    return all(cell != ' ' for cell in board[0])

def main():
    board = create_board(ROWS, COLUMNS)
    current_player = random.randint(0, NUM_PLAYERS - 1)

    clear_screen()
    print_board(board)

    while True:
        token = PLAYERS[current_player]
        print(f"Player {token}, please enter a column:")

        while True:
            col_input = input().strip().upper()
            col_index = get_column_index(col_input, COLUMNS)

            if col_index == -1:
                print(f"Invalid input. Please enter a letter between A and {chr(ord('A') + COLUMNS - 1)}:")
                continue

            if not is_valid_move(board, col_index):
                print("This column is full! Turn lost.")
                # End while loop, do not let player retry (lose turn as per specification)
                col_index = None
                break

            # Place checker and proceed
            row_index = place_checker(board, col_index, token)
            break

        clear_screen()
        print_board(board)

        # Only check for win/draw if a move was made (skip if move was lost)
        if col_index is not None:
            if check_for_win(board, token):
                print(f"Player {token} won!")
                return
            elif is_draw(board):
                print("It's a draw!")
                return

        # Switch to next player (if turn not lost, normal cycle; if lost, goes to next player regardless)
        current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == '__main__':
    main()
