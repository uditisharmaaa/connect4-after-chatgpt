import os
import random

# Constants for the board dimensions and number of players
ROWS = 6
COLUMNS = 7
PLAYERS = 2

# Player symbols
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']

def clear_screen():
    os.system('clear')

def create_board(rows, columns):
    return [[' ' for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    column_labels = ' '.join(chr(ord('A') + i) for i in range(len(board[0])))
    print(f"  {column_labels}")
    print("+---" * len(board[0]) + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * len(board[0]) + "+")

def select_random_player(num_players):
    return random.randint(0, num_players - 1)

def is_valid_column(column, board):
    return column.isalpha() and 'A' <= column < chr(ord('A') + len(board[0]))

def is_column_full(column, board):
    return board[0][ord(column) - ord('A')] != ' '

def place_checker(column, player, board):
    col_index = ord(column) - ord('A')
    for row in range(len(board) - 1, -1, -1):
        if board[row][col_index] == ' ':
            board[row][col_index] = PLAYER_SYMBOLS[player]
            return True
    return False

def check_win(player, board):
    symbol = PLAYER_SYMBOLS[player]

    # Check horizontal
    for row in range(len(board)):
        for col in range(len(board[0]) - 3):
            if all(board[row][col + i] == symbol for i in range(4)):
                return True

    # Check vertical
    for row in range(len(board) - 3):
        for col in range(len(board[0])):
            if all(board[row + i][col] == symbol for i in range(4)):
                return True

    # Check positive diagonal
    for row in range(len(board) - 3):
        for col in range(len(board[0]) - 3):
            if all(board[row + i][col + i] == symbol for i in range(4)):
                return True

    # Check negative diagonal
    for row in range(3, len(board)):
        for col in range(len(board[0]) - 3):
            if all(board[row - i][col + i] == symbol for i in range(4)):
                return True

    return False

def check_draw(board):
    return all(board[0][col] != ' ' for col in range(len(board[0])))

def play_game():
    board = create_board(ROWS, COLUMNS)
    current_player = select_random_player(PLAYERS)
    print_board(board)

    while True:
        print(f"Player {PLAYER_SYMBOLS[current_player]}, please enter a column:")
        column = input().strip().upper()

        if not is_valid_column(column, board) or is_column_full(column, board):
            print("Invalid input, try again.")
            continue

        place_checker(column, current_player, board)
        print_board(board)

        if check_win(current_player, board):
            print(f"Player {PLAYER_SYMBOLS[current_player]} won!")
            break
        
        if check_draw(board):
            print("The game is a draw!")
            break

        current_player = (current_player + 1) % PLAYERS

if __name__ == "__main__":
    play_game()
