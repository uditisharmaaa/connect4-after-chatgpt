import os
import random

# Constants
BOARD_ROWS = 6
BOARD_COLUMNS = 7
MAX_PLAYERS = 5
MIN_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    os.system('clear')  # Clear the screen
    cols_labels = "  " + "   ".join(chr(ord('A') + i) for i in range(len(board[0])))
    print(cols_labels)
    for row in board:
        print("+---" * len(row) + "+")
        print("| " + " | ".join(row) + " |")
    print("+---" * len(board[0]) + "+")

def is_valid_input(input_str, columns):
    return len(input_str) == 1 and input_str.isalpha() and 'A' <= input_str <= chr(ord('A') + columns - 1)

def place_checker(board, column, checker):
    for row in reversed(board):
        if row[column] == " ":
            row[column] = checker
            return True
    return False

def check_win(board, checker):
    def check_direction(dx, dy):
        for x in range(len(board[0])):
            for y in range(len(board)):
                if all(
                    0 <= x + dx * i < len(board[0]) and
                    0 <= y + dy * i < len(board) and
                    board[y + dy * i][x + dx * i] == checker
                    for i in range(4)
                ):
                    return True
        return False

    return (
        check_direction(1, 0) or  # Horizontal
        check_direction(0, 1) or  # Vertical
        check_direction(1, 1) or  # Diagonal /
        check_direction(1, -1)    # Diagonal \
    )

def check_draw(board):
    return all(cell != " " for row in board for cell in row)

def play_game():
    board = create_board(BOARD_ROWS, BOARD_COLUMNS)
    num_players = 2  # Set number of players
    players_checkers = CHECKERS[:num_players]
    current_player_idx = random.randint(0, num_players - 1)
    
    print_board(board)
    
    while True:
        current_checker = players_checkers[current_player_idx]
        while True:
            player_input = input(f"Player {current_checker}, please enter a column: ").strip().upper()
            if is_valid_input(player_input, BOARD_COLUMNS):
                column_idx = ord(player_input) - ord('A')
                if place_checker(board, column_idx, current_checker):
                    break
                else:
                    print("Column is full, try another.")
            else:
                print("Invalid input, please try again.")

        print_board(board)
        
        if check_win(board, current_checker):
            print(f"Player {current_checker} won!")
            break
        
        if check_draw(board):
            print("The game is a draw!")
            break
        
        current_player_idx = (current_player_idx + 1) % num_players

play_game()
