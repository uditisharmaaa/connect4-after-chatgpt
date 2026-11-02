import os
import random

def init_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board, cols):
    os.system('clear')  # Clear the terminal screen
    print("  " + "   ".join(chr(65 + i) for i in range(cols)))
    for row in board:
        print("+---" * cols + "+")
        print("| " + " | ".join(row) + " |")
    print("+---" * cols + "+")

def is_valid_input(input, cols):
    return len(input) == 1 and input.isalpha() and ord(input.upper()) - 65 < cols

def place_checker(board, col, checker):
    for row in reversed(board):
        if row[col] == " ":
            row[col] = checker
            return True
    return False

def check_winner(board, rows, cols, checkers):
    for r in range(rows):
        for c in range(cols):
            if board[r][c] in checkers:
                checker = board[r][c]
                # Horizontal
                if c <= cols - 4 and all(board[r][c+i] == checker for i in range(4)):
                    return True
                # Vertical
                if r <= rows - 4 and all(board[r+i][c] == checker for i in range(4)):
                    return True
                # Diagonal /
                if r <= rows - 4 and c <= cols - 4 and all(board[r+i][c+i] == checker for i in range(4)):
                    return True
                # Diagonal \
                if r >= 3 and c <= cols - 4 and all(board[r-i][c+i] == checker for i in range(4)):
                    return True
    return False

def check_draw(board):
    return all(cell != " " for row in board for cell in row)

def connect_4_game():
    rows = 6
    cols = 7
    num_players = 2
    checkers = ["X", "O", "V", "H", "M"]
    
    board = init_board(rows, cols)
    print_board(board, cols)
    
    turn = random.randint(0, num_players - 1)
    players = [checkers[i] for i in range(num_players)]
    
    while True:
        print(f"Player {players[turn]}, please enter a column:")
        col_input = input().upper()
        
        if not is_valid_input(col_input, cols):
            print("Invalid input, please try again.")
            continue
        
        col = ord(col_input) - 65
        
        if not place_checker(board, col, players[turn]):
            print("Column is full, you lose your turn.")
            turn = (turn + 1) % num_players
            continue
        
        print_board(board, cols)
        
        if check_winner(board, rows, cols, players[turn]):
            print(f"Player {players[turn]} won!")
            break
        
        if check_draw(board):
            print("The game is a draw!")
            break
            
        turn = (turn + 1) % num_players

connect_4_game()
