import os
import random

# Constants
ROWS = 6
COLUMNS = 7
MAX_COLUMNS = 26
PLAYERS_COUNT = 2
CHECKERS = ["X", "O", "V", "H", "M"]

def clear_screen():
    os.system('clear')

def create_board():
    return [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    clear_screen()
    print("  " + "   ".join(chr(ord('A') + i) for i in range(COLUMNS)))
    print("+---" * COLUMNS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLUMNS + "+")

def switch_player(current_player):
    return (current_player + 1) % PLAYERS_COUNT

def is_valid_column(column):
    return column.isalpha() and 'A' <= column <= chr(ord('A') + COLUMNS - 1)

def is_column_full(board, column_index):
    return board[0][column_index] != " "

def drop_checker(board, column_index, checker):
    for row in range(ROWS-1, -1, -1):
        if board[row][column_index] == " ":
            board[row][column_index] = checker
            break

def check_for_win(board, checker):
    # check horizontal, vertical and diagonal for a win
    def check_direction(r_step, c_step):
        for row in range(ROWS):
            for col in range(COLUMNS):
                if all(0 <= col + k * c_step < COLUMNS and
                       0 <= row + k * r_step < ROWS and
                       board[row + k * r_step][col + k * c_step] == checker
                       for k in range(4)):
                    return True
        return False

    return (
        check_direction(0, 1) or  # horizontal
        check_direction(1, 0) or  # vertical
        check_direction(1, 1) or  # diagonal /
        check_direction(1, -1)    # diagonal \
    )

def is_draw(board):
    return all(board[0][col] != " " for col in range(COLUMNS))

def play_game():
    board = create_board()
    current_player = random.randint(0, PLAYERS_COUNT - 1)
    print_board(board)
    
    while True:
        player_checker = CHECKERS[current_player]
        print(f"Player {player_checker}, please enter a column:")
        
        column = input().upper()
        
        if not is_valid_column(column):
            print("Invalid input, please try again.")
            continue
        
        column_index = ord(column) - ord('A')
        
        if is_column_full(board, column_index):
            print("Column is full, you lose the turn.")
            current_player = switch_player(current_player)
            continue
        
        drop_checker(board, column_index, player_checker)
        print_board(board)
        
        if check_for_win(board, player_checker):
            print(f"Player {player_checker} won!")
            break
        
        if is_draw(board):
            print("The game is a draw!")
            break
        
        current_player = switch_player(current_player)

# Start the game
if __name__ == "__main__":
    play_game()
