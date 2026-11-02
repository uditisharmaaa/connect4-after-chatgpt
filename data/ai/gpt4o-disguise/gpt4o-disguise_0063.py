import os
import random

ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    os.system('clear')
    print("  " + "   ".join(chr(i + ord('A')) for i in range(COLS)))
    print("+" + "---+" * COLS)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * COLS)

def player_input(player):
    return input(f"Player {player}, please enter a column: ").strip().upper()

def place_checker(board, column, checker):
    for row in range(ROWS-1, -1, -1):
        if board[row][column] == " ":
            board[row][column] = checker
            return True
    return False

def check_winner(board, checker):
    for row in range(ROWS):
        for col in range(COLS):
            if board[row][col] == checker:
                if col <= COLS - 4 and all(board[row][col + i] == checker for i in range(4)):
                    return True
                if row <= ROWS - 4 and all(board[row + i][col] == checker for i in range(4)):
                    return True
                if col <= COLS - 4 and row <= ROWS - 4 and all(board[row + i][col + i] == checker for i in range(4)):
                    return True
                if col >= 3 and row <= ROWS - 4 and all(board[row + i][col - i] == checker for i in range(4)):
                    return True
    return False

def full_board(board):
    return all(board[0][col] != " " for col in range(COLS))

def valid_input(inp):
    return len(inp) == 1 and ord('A') <= ord(inp) <= ord('A') + COLS - 1

def random_player():
    return random.randint(0, PLAYERS - 1)

def main():
    board = create_board(ROWS, COLS)
    print_board(board)
    current_player = random_player()
    
    while True:
        column_input = player_input(CHECKERS[current_player])
        if not valid_input(column_input):
            continue

        column = ord(column_input) - ord('A')
        
        if place_checker(board, column, CHECKERS[current_player]):
            print_board(board)
            
            if check_winner(board, CHECKERS[current_player]):
                print(f"Player {CHECKERS[current_player]} won!")
                break
            
            if full_board(board):
                print("It's a draw!")
                break
            
            current_player = (current_player + 1) % PLAYERS
        else:
            print("Column full, turn lost!")

main()
