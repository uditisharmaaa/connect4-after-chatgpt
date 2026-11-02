import os
import random
import string

# ==== CONSTANTS ====
NUM_PLAYERS = 2                 # Changeable (between 2 and 5)
PLAYER_CHECKERS = ["X", "O", "V", "H", "M"]
NUM_ROWS = 6                    # Changeable
NUM_COLS = 7                    # Changeable (max 26)
WIN_LENGTH = 4                  # Number of checkers in a row to win

# ===== GLOBALS =====
PLAYERS = PLAYER_CHECKERS[:NUM_PLAYERS]
COLUMN_LABELS = list(string.ascii_uppercase[:NUM_COLS])
EMPTY_CELL = " "

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    return [[EMPTY_CELL for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    # print column labels
    print("  " + "   ".join(COLUMN_LABELS))
    # print top line
    print("+" + "---+" * NUM_COLS)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * NUM_COLS)

def get_lowest_empty_row(board, col):
    for row in range(NUM_ROWS-1, -1, -1):
        if board[row][col] == EMPTY_CELL:
            return row
    return None

def is_board_full(board):
    for row in board:
        if EMPTY_CELL in row:
            return False
    return True

def valid_column_input(input_str):
    return (len(input_str) == 1 and input_str in COLUMN_LABELS)

def check_win(board, checker):
    # Horizontal check
    for row in range(NUM_ROWS):
        for col in range(NUM_COLS - WIN_LENGTH + 1):
            if all(board[row][col+i] == checker for i in range(WIN_LENGTH)):
                return True

    # Vertical check
    for row in range(NUM_ROWS - WIN_LENGTH + 1):
        for col in range(NUM_COLS):
            if all(board[row+i][col] == checker for i in range(WIN_LENGTH)):
                return True

    # Diagonal (down-right) check
    for row in range(NUM_ROWS - WIN_LENGTH + 1):
        for col in range(NUM_COLS - WIN_LENGTH + 1):
            if all(board[row+i][col+i] == checker for i in range(WIN_LENGTH)):
                return True

    # Diagonal (up-right) check
    for row in range(WIN_LENGTH-1, NUM_ROWS):
        for col in range(NUM_COLS - WIN_LENGTH + 1):
            if all(board[row-i][col+i] == checker for i in range(WIN_LENGTH)):
                return True

    return False

def get_player_input(board, player):
    while True:
        player_input = input(f"Player {player}, please enter a column: ").strip()
        if not valid_column_input(player_input):
            print("Invalid input. Please enter a valid column letter.")
            continue

        col = COLUMN_LABELS.index(player_input)
        if board[0][col] != EMPTY_CELL:
            print("Column is already full. You lose your turn.")
            return None # Indicate the turn is lost due to full column

        return col

def play_game():
    board = create_board(NUM_ROWS, NUM_COLS)
    player_idx = random.randint(0, NUM_PLAYERS - 1)  # Random starting player
    winner = None

    clear_screen()
    print_board(board)

    while True:
        current_player = PLAYERS[player_idx]
        col = get_player_input(board, current_player)
        clear_screen()
        if col is None:
            print_board(board)
            player_idx = (player_idx + 1) % NUM_PLAYERS
            continue

        row = get_lowest_empty_row(board, col)
        board[row][col] = current_player

        print_board(board)

        if check_win(board, current_player):
            print(f"Player {current_player} won!")
            break

        if is_board_full(board):
            print("The game is a draw!")
            break

        # Next player's turn
        player_idx = (player_idx + 1) % NUM_PLAYERS

if __name__ == "__main__":
    play_game()
