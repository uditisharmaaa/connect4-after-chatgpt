import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = ["X", "O"]

def create_board():
    return [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')
    print("  " + "   ".join(chr(65 + i) for i in range(COLUMNS)))
    print("+" + "---+" * COLUMNS)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * COLUMNS)

def is_valid_input(column, board):
    if len(column) != 1 or not column.isalpha() or not (0 <= ord(column) - 65 < COLUMNS):
        return False
    return board[0][ord(column) - 65] == " "

def place_checker(board, column, player):
    column_index = ord(column) - 65
    for row in reversed(board):
        if row[column_index] == " ":
            row[column_index] = player
            return True
    return False

def check_winner(board):
    # Check horizontal, vertical and diagonal connections for a win
    for r in range(ROWS):
        for c in range(COLUMNS):
            if board[r][c] != " ":
                player = board[r][c]
                if c + 3 < COLUMNS and all(board[r][c + i] == player for i in range(4)):
                    return True
                if r + 3 < ROWS:
                    if all(board[r + i][c] == player for i in range(4)):
                        return True
                    if c + 3 < COLUMNS and all(board[r + i][c + i] == player for i in range(4)):
                        return True
                    if c - 3 >= 0 and all(board[r + i][c - i] == player for i in range(4)):
                        return True
    return False

def is_draw(board):
    return all(board[0][c] != " " for c in range(COLUMNS))

def main():
    board = create_board()
    current_player = random.choice(PLAYERS)
    turns = 0

    print_board(board)

    while True:
        column = input(f"Player {current_player}, please enter a column: ").upper()
        
        while not is_valid_input(column, board):
            column = input(f"Invalid input. Player {current_player}, please enter a column: ").upper()

        if place_checker(board, column, current_player):
            print_board(board)
            turns += 1
            
            if check_winner(board):
                print(f"Player {current_player} won!")
                break
            if turns >= ROWS * COLUMNS:
                print("The game is a draw!")
                break

            current_player = PLAYERS[(PLAYERS.index(current_player) + 1) % len(PLAYERS)]
        else:
            print("Column is full, choose another column.")

if __name__ == "__main__":
    main()
