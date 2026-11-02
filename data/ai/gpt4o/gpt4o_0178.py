import os
import random

# Constant variables
ROWS = 6
COLUMNS = 7
MAX_PLAYERS = 5
PLAYER_CHARS = ["X", "O", "V", "H", "M"]  # Supports up to 5 players

def clear_screen():
    # Clears the console screen
    os.system('clear')

def create_board(rows, cols):
    # Initializes a board with whitespaces
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    # Print the column labels
    print("  ", "   ".join([chr(65 + i) for i in range(len(board[0]))]))
    print("+---" * len(board[0]) + "+")

    # Print the board
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * len(row) + "+")

def is_valid_input(col_letter):
    # Checks if the input is a valid column letter
    return 65 <= ord(col_letter) < 65 + COLUMNS

def place_checker(board, col, checker):
    # Places the checker in the specified column
    for row in range(ROWS-1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return True
    return False

def check_win(board, checker):
    # Check horizontally
    for row in range(ROWS):
        for col in range(COLUMNS - 3):
            if board[row][col:col + 4] == [checker]*4:
                return True

    # Check vertically
    for col in range(COLUMNS):
        for row in range(ROWS - 3):
            if [board[r][col] for r in range(row, row + 4)] == [checker]*4:
                return True

    # Check diagonal (bottom-left to top-right)
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if [board[row + i][col + i] for i in range(4)] == [checker]*4:
                return True

    # Check diagonal (top-left to bottom-right)
    for row in range(3, ROWS):
        for col in range(COLUMNS - 3):
            if [board[row - i][col + i] for i in range(4)] == [checker]*4:
                return True

    return False

def check_draw(board):
    # Checks if the board is completely filled
    return all(board[0][col] != " " for col in range(COLUMNS))

def connect4_game(players=2):
    # Ensure the number of players is between 2 and MAX_PLAYERS
    players = max(2, min(players, MAX_PLAYERS))
    player_checkers = PLAYER_CHARS[:players]

    board = create_board(ROWS, COLUMNS)
    current_player_index = random.randint(0, players - 1)
    current_checker = player_checkers[current_player_index]

    clear_screen()
    print_board(board)

    while True:
        # Get current player's turn input
        print(f"Player {current_checker}, please enter a column:")
        col_letter = input().strip().upper()

        clear_screen()

        if not is_valid_input(col_letter):
            print("Invalid input. Please enter a valid column.")
            print_board(board)
            continue

        col = ord(col_letter) - 65

        if not place_checker(board, col, current_checker):
            print("Column is full, turn is skipped.")
       
        else:
            if check_win(board, current_checker):
                print_board(board)
                print(f"Player {current_checker} won!")
                break

            if check_draw(board):
                print_board(board)
                print("It's a draw!")
                break

            # Switch to the next player
            current_player_index = (current_player_index + 1) % players
            current_checker = player_checkers[current_player_index]

        print_board(board)

connect4_game(players=2)
