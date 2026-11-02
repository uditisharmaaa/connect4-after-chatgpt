import os
import random

# Constants
ROWS = 6
COLS = 7
MIN_PLAYERS = 2
MAX_PLAYERS = 5
WIN_LENGTH = 4
CHECKERS = ["X", "O", "V", "H", "M"]  # Max 5 players

NUM_PLAYERS = 2  # Set number of players here (2 to 5)

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    cols = len(board[0])
    # Print column headers
    header = "  " + "   ".join(chr(ord('A') + i) for i in range(cols))
    print(header)
    # Print board rows
    line = "+---" * cols + "+"
    for r in range(len(board)):
        print(line)
        print("| " + " | ".join(board[r]) + " |")
    print(line)

def valid_input(user_input, cols):
    if len(user_input) != 1:
        return False
    c = user_input.upper()
    if not ('A' <= c <= chr(ord('A') + cols -1)):
        return False
    return True

def column_index(user_input):
    return ord(user_input.upper()) - ord('A')

def place_checker(board, col, checker):
    # From bottom row upwards
    for r in range(len(board)-1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = checker
            return True
    return False  # Col full

def check_win(board, checker):
    rows = len(board)
    cols = len(board[0])

    # Horizontal check
    for r in range(rows):
        for c in range(cols - WIN_LENGTH +1):
            if all(board[r][c+i] == checker for i in range(WIN_LENGTH)):
                return True

    # Vertical check
    for c in range(cols):
        for r in range(rows - WIN_LENGTH +1):
            if all(board[r+i][c] == checker for i in range(WIN_LENGTH)):
                return True

    # Diagonal down-right
    for r in range(rows - WIN_LENGTH +1):
        for c in range(cols - WIN_LENGTH +1):
            if all(board[r+i][c+i] == checker for i in range(WIN_LENGTH)):
                return True

    # Diagonal up-right
    for r in range(WIN_LENGTH -1, rows):
        for c in range(cols - WIN_LENGTH +1):
            if all(board[r - i][c + i] == checker for i in range(WIN_LENGTH)):
                return True

    return False

def check_draw(board):
    # If any cell is empty, no draw
    for row in board:
        if " " in row:
            return False
    return True

def main():
    # Setup
    players = CHECKERS[:NUM_PLAYERS]
    board = create_board(ROWS, COLS)
    current_player_index = random.randint(0, NUM_PLAYERS - 1)

    while True:
        print_board(board)
        current_checker = players[current_player_index]
        prompt = f"Player {current_checker}, please enter a column: "
        
        valid_move = False
        while not valid_move:
            user_input = input(prompt).strip()
            if not valid_input(user_input, COLS):
                continue
            col = column_index(user_input)
            # Check if column full
            if board[0][col] != " ":
                # Turn lost if full
                valid_move = False
                break
            # place checker
            placed = place_checker(board, col, current_checker)
            if placed:
                valid_move = True
        
        if not valid_move:
            # column full - turn lost, go to next player
            current_player_index = (current_player_index +1) % NUM_PLAYERS
            continue

        # Check win
        if check_win(board, current_checker):
            print_board(board)
            print(f"Player {current_checker} won!")
            break
        # Check draw
        if check_draw(board):
            print_board(board)
            print("The game is a draw!")
            break

        # Next player
        current_player_index = (current_player_index +1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
