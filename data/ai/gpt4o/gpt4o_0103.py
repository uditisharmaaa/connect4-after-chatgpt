import random
import os

# Constants
ROWS = 6
COLUMNS = 7
MAX_PLAYERS = 5
PLAYERS = ['X', 'O', 'V', 'H', 'M']  # Players symbols
NUM_PLAYERS = 2  # Change to 3, 4, or 5 for more players

def clear_screen():
    os.system('clear')

def create_board(rows, columns):
    return [[' ' for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    columns_labels = "  " + "   ".join(chr(65 + i) for i in range(len(board[0])))
    print(columns_labels)
    for row in board:
        print("+---" * len(row) + "+")
        print("| " + " | ".join(row) + " |")
    print("+---" * len(board[0]) + "+")

def valid_input(user_input, board):
    if len(user_input) == 1 and user_input.isalpha():
        column_index = ord(user_input.upper()) - ord('A')
        if 0 <= column_index < len(board[0]):
            return column_index
    return None

def place_checker(board, column_index, player):
    for row in reversed(board):
        if row[column_index] == ' ':
            row[column_index] = player
            return True
    return False

def check_winner(board, player):
    def horizontal_win():
        for row in board:
            for col in range(len(row) - 3):
                if row[col] == player and row[col+1] == player and row[col+2] == player and row[col+3] == player:
                    return True
        return False

    def vertical_win():
        for col in range(len(board[0])):
            for row in range(len(board) - 3):
                if board[row][col] == player and board[row+1][col] == player and board[row+2][col] == player and board[row+3][col] == player:
                    return True
        return False

    def diagonal_win():
        for row in range(len(board) - 3):
            for col in range(len(board[0]) - 3):
                if board[row][col] == player and board[row+1][col+1] == player and board[row+2][col+2] == player and board[row+3][col+3] == player:
                    return True
            for col in range(3, len(board[0])):
                if board[row][col] == player and board[row+1][col-1] == player and board[row+2][col-2] == player and board[row+3][col-3] == player:
                    return True
        return False

    return horizontal_win() or vertical_win() or diagonal_win()

def check_draw(board):
    for row in board:
        if ' ' in row:
            return False
    return True

def connect_four():
    board = create_board(ROWS, COLUMNS)
    print_board(board)

    current_player = random.choice(PLAYERS[:NUM_PLAYERS])
    players_cycle = iter(PLAYERS[:NUM_PLAYERS])

    while True:
        print(f"Player {current_player}, please enter a column:")
        user_input = input().strip()
        column_index = valid_input(user_input, board)
        
        if column_index is not None and place_checker(board, column_index, current_player):
            print_board(board)

            if check_winner(board, current_player):
                print(f"Player {current_player} won!")
                break
            
            if check_draw(board):
                print("The game is a draw!")
                break
            
            current_player = next(players_cycle, None)
            if current_player is None:
                players_cycle = iter(PLAYERS[:NUM_PLAYERS])
                current_player = next(players_cycle)
        else:
            print("Invalid input, try again!")

connect_four()
