import os
import random

ROWS = 6
COLS = 7
PLAYERS = 2

symbols = ["X", "O", "V", "H", "M"]
player_symbols = symbols[:PLAYERS]

def create_board():
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')
    column_labels = "  " + "   ".join(chr(65 + i) for i in range(COLS))
    print(column_labels)
    for row in board:
        print("+---" * COLS + "+")
        print("| " + " | ".join(row) + " |")
    print("+---" * COLS + "+")

def check_winner(board, symbol):
    for row in range(ROWS):
        for col in range(COLS - 3):
            if board[row][col] == symbol and board[row][col + 1] == symbol and board[row][col + 2] == symbol and board[row][col + 3] == symbol:
                return True
    for row in range(ROWS - 3):
        for col in range(COLS):
            if board[row][col] == symbol and board[row + 1][col] == symbol and board[row + 2][col] == symbol and board[row + 3][col] == symbol:
                return True
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if board[row][col] == symbol and board[row + 1][col + 1] == symbol and board[row + 2][col + 2] == symbol and board[row + 3][col + 3] == symbol:
                return True
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if board[row][col] == symbol and board[row - 1][col + 1] == symbol and board[row - 2][col + 2] == symbol and board[row - 3][col + 3] == symbol:
                return True
    return False

def check_draw(board):
    return all(board[0][col] != " " for col in range(COLS))

def get_move(board, player):
    while True:
        move = input(f"Player {player}, please enter a column: ").upper()
        if len(move) != 1 or not ('A' <= move <= chr(65 + COLS - 1)):
            print("Invalid column. Try again.")
            continue
        col = ord(move) - 65
        if board[0][col] != " ":
            print("Column full. Try again.")
            continue
        return col

def make_move(board, col, symbol):
    for row in reversed(range(ROWS)):
        if board[row][col] == " ":
            board[row][col] = symbol
            break
        
def play_game():
    board = create_board()
    current_player = random.choice(player_symbols)
    print_board(board)
    
    while True:
        col = get_move(board, current_player)
        make_move(board, col, current_player)
        print_board(board)
        
        if check_winner(board, current_player):
            print(f"Player {current_player} won!")
            break
        elif check_draw(board):
            print("It's a draw!")
            break
        
        current_player = player_symbols[(player_symbols.index(current_player) + 1) % PLAYERS]

play_game()
