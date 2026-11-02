import os
import random
import string

# Constants (you can change these for testing, but submit with these values)
ROWS = 6
COLS = 7  # max 26
NUM_PLAYERS = 2  # between 2 and 5
CHECKERS = ["X", "O", "V", "H", "M"]
WIN_LENGTH = 4  # number of checkers in a row to win

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    board = []
    for _ in range(rows):
        board.append([" "] * cols)
    return board

def print_board(board):
    cols = len(board[0])
    # Header letters
    letters = [chr(ord('A') + i) for i in range(cols)]
    print("  " + "   ".join(letters))
    # Board grid
    for r in range(len(board)):
        print("+---" * cols + "+")
        row_str = ""
        for c in range(cols):
            row_str += "|" + " " + board[r][c] + " "
        row_str += "|"
        print(row_str)
    print("+---" * cols + "+")

def get_lowest_empty_row(board, col):
    # Start from bottom row upwards
    for r in range(len(board) - 1, -1, -1):
        if board[r][col] == " ":
            return r
    return None

def is_draw(board):
    for r in range(len(board)):
        for c in range(len(board[0])):
            if board[r][c] == " ":
                return False
    return True

def in_bounds(r, c, rows, cols):
    return 0 <= r < rows and 0 <= c < cols

def check_win(board, symbol):
    rows = len(board)
    cols = len(board[0])
    needed = WIN_LENGTH

    # Directions: (dr, dc)
    directions = [
        (0, 1),   # horizontal right
        (1, 0),   # vertical down
        (1, 1),   # diagonal down-right
        (-1, 1),  # diagonal up-right
    ]

    for r in range(rows):
        for c in range(cols):
            if board[r][c] != symbol:
                continue
            for dr, dc in directions:
                count = 1
                nr = r + dr
                nc = c + dc
                while count < needed and in_bounds(nr, nc, rows, cols) and board[nr][nc] == symbol:
                    count += 1
                    nr += dr
                    nc += dc
                if count >= needed:
                    return True
    return False

def get_valid_column_input(cols):
    while True:
        user_input = input("Please enter a column (A-{}): ".format(chr(ord('A') + cols - 1)))
        if not user_input:
            print("Invalid input. Please enter a single letter.")
            continue
        user_input = user_input.strip().upper()
        if len(user_input) != 1:
            print("Invalid input. Please enter a single letter.")
            continue
        if user_input < 'A' or user_input > chr(ord('A') + cols - 1):
            print("Invalid column. Please choose between A and {}.".format(chr(ord('A') + cols - 1)))
            continue
        return ord(user_input) - ord('A')

def main():
    # Validate constants
    cols = COLS
    rows = ROWS
    if cols < 1 or cols > 26:
        print("Error: COLS must be between 1 and 26.")
        return
    if NUM_PLAYERS < 2 or NUM_PLAYERS > 5:
        print("Error: NUM_PLAYERS must be between 2 and 5.")
        return

    players = CHECKERS[:NUM_PLAYERS]
    board = create_board(rows, cols)

    # Randomly select starting player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)

    # Initial board print
    clear_screen()
    print_board(board)
    print("Player {}, you start!".format(players[current_player_index]))

    while True:
        # Show board at the start of each player's turn
        clear_screen()
        print_board(board)
        print("Player {}, please enter a column:".format(players[current_player_index]))

        col = get_valid_column_input(cols)

        # Try to place the checker
        row_to_place = get_lowest_empty_row(board, col)
        if row_to_place is None:
            # Column full: lose the turn
            print("Column {} is full. Player {} loses the turn.".format(chr(ord('A') + col), players[current_player_index]))
            input("Press Enter to continue...")
            current_player_index = (current_player_index + 1) % NUM_PLAYERS
            continue

        board[row_to_place][col] = players[current_player_index]

        # Check for win
        if check_win(board, players[current_player_index]):
            clear_screen()
            print_board(board)
            print("Player {} won!".format(players[current_player_index]))
            break

        # Check for draw
        if is_draw(board):
            clear_screen()
            print_board(board)
            print("It's a draw!")
            break

        # Next player's turn
        current_player_index = (current_player_index + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
