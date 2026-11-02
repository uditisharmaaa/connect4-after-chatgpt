import random
import os

# Constants for board dimensions and players
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]  # Checkers for up to 5 players

def create_board():
    return [[" " for _ in range(NUM_COLS)] for _ in range(NUM_ROWS)]

def print_board(board):
    os.system('clear')
    print("  " + "   ".join(chr(i) for i in range(65, 65 + NUM_COLS)))
    print("+---" * NUM_COLS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * NUM_COLS + "+")

def get_valid_column(board, player):
    while True:
        try:
            col = input(f"Player {player}, please enter a column: ").upper()
            if len(col) != 1 or not ('A' <= col < chr(65 + NUM_COLS)):
                raise ValueError("Invalid column letter.")
            col_idx = ord(col) - 65
            if board[0][col_idx] != " ":
                raise ValueError("Column is full.")
            return col_idx
        except ValueError as e:
            print(e)

def place_checker(board, col, checker):
    for row in reversed(board):
        if row[col] == " ":
            row[col] = checker
            break

def check_for_win(board, checker):
    # Horizontal, vertical, and diagonal checks
    for c in range(NUM_COLS - 3):
        for r in range(NUM_ROWS):
            if board[r][c:c+4] == [checker]*4:
                return True

    for c in range(NUM_COLS):
        for r in range(NUM_ROWS - 3):
            if all(board[r+i][c] == checker for i in range(4)):
                return True

    for c in range(NUM_COLS - 3):
        for r in range(3, NUM_ROWS):
            if all(board[r-i][c+i] == checker for i in range(4)):
                return True

    for c in range(NUM_COLS - 3):
        for r in range(NUM_ROWS - 3):
            if all(board[r+i][c+i] == checker for i in range(4)):
                return True

    return False

def check_for_draw(board):
    return all(board[0][c] != " " for c in range(NUM_COLS))

def connect_four():
    board = create_board()
    players = [CHECKERS[i] for i in range(NUM_PLAYERS)]
    current_player = random.choice(players)
    
    print_board(board)
    
    while True:
        col = get_valid_column(board, current_player)
        place_checker(board, col, current_player)
        print_board(board)
        
        if check_for_win(board, current_player):
            print(f"Player {current_player} won!")
            break

        if check_for_draw(board):
            print("The game is a draw!")
            break
        
        current_player = players[(players.index(current_player) + 1) % NUM_PLAYERS]

if __name__ == "__main__":
    connect_four()
