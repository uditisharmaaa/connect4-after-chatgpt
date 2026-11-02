import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]  # Use up to the first PLAYERS elements

def initialize_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    os.system('clear')
    header = "  " + "   ".join(chr(i) for i in range(65, 65 + len(board[0])))
    print(header)
    print("+---" * len(board[0]) + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * len(board[0]) + "+")

def get_column_choice(player):
    while True:
        choice = input(f"Player {player}, please enter a column: ").upper()
        if len(choice) == 1 and 'A' <= choice <= chr(65 + COLS - 1):
            return ord(choice) - 65
        else:
            print("Invalid input. Please enter a valid column letter.")

def drop_checker(board, col, checker):
    for row in reversed(board):
        if row[col] == " ":
            row[col] = checker
            return True
    return False

def has_winner(board, player):
    # Horizontal check
    for row in range(ROWS):
        for col in range(COLS - 3):
            if all(board[row][c] == player for c in range(col, col + 4)):
                return True
    # Vertical check
    for col in range(COLS):
        for row in range(ROWS - 3):
            if all(board[r][col] == player for r in range(row, row + 4)):
                return True
    # Diagonal (down-right) check
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if all(board[row + i][col + i] == player for i in range(4)):
                return True
    # Diagonal (up-right) check
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if all(board[row - i][col + i] == player for i in range(4)):
                return True
    return False

def is_draw(board):
    return all(cell != " " for row in board for cell in row)

def play_game():
    board = initialize_board(ROWS, COLS)
    players = CHECKERS[:PLAYERS]
    current_player = players[random.randint(0, PLAYERS - 1)]
    
    print_board(board)
    
    while True:
        col = get_column_choice(current_player)
        if drop_checker(board, col, current_player):
            print_board(board)
            if has_winner(board, current_player):
                print(f"Player {current_player} won!")
                break
            if is_draw(board):
                print("The game is a draw!")
                break
            current_index = players.index(current_player)
            current_player = players[(current_index + 1) % PLAYERS]
        else:
            print(f"Column {chr(65 + col)} is full. Player {current_player} loses the turn.")

if __name__ == "__main__":
    play_game()
