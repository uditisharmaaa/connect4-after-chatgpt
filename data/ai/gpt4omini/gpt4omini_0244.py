import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = ['X', 'O', 'V', 'H', 'M']

def create_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')
    print("  " + "   ".join(chr(65 + i) for i in range(COLS)))
    print("+---+" + "---+".join([""] * COLS))
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---+" + "---+".join([""] * COLS))

def is_valid_input(column):
    if len(column) != 1 or not column.isalpha():
        return False
    col_index = ord(column.upper()) - 65
    return 0 <= col_index < COLS

def get_column_choice(player):
    while True:
        column = input(f"Player {player}, please enter a column: ").strip()
        if is_valid_input(column):
            return ord(column.upper()) - 65
        print("Invalid input. Please enter a valid column letter (A-G).")

def drop_checker(board, column, checker):
    for row in reversed(board):
        if row[column] == ' ':
            row[column] = checker
            return True
    return False

def check_win(board, checker):
    # Check horizontal, vertical and diagonal
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] == checker:
                if c <= COLS - 4 and all(board[r][c + i] == checker for i in range(4)):
                    return True
                if r <= ROWS - 4 and all(board[r + i][c] == checker for i in range(4)):
                    return True
                if r <= ROWS - 4 and c <= COLS - 4 and all(board[r + i][c + i] == checker for i in range(4)):
                    return True
                if r >= 3 and c <= COLS - 4 and all(board[r - i][c + i] == checker for i in range(4)):
                    return True
    return False

def check_draw(board):
    return all(board[0][col] != ' ' for col in range(COLS))

def connect4():
    board = create_board()
    current_player_index = random.randint(0, len(PLAYERS) - 1)
    
    while True:
        print_board(board)
        current_player = PLAYERS[current_player_index]
        
        # Get column choice and drop checker
        column = get_column_choice(current_player)
        if drop_checker(board, column, current_player):
            if check_win(board, current_player):
                print_board(board)
                print(f"Player {current_player} won!")
                break
            if check_draw(board):
                print_board(board)
                print("The game is a draw!")
                break
            current_player_index = (current_player_index + 1) % len(PLAYERS)
        else:
            print("Column is full! Please choose another column.")

if __name__ == "__main__":
    connect4()
