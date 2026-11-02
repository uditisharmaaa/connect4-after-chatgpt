import os
import random

ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    os.system('clear')
    print("  " + "   ".join(chr(ord('A') + i) for i in range(len(board[0]))))
    print("+" + "---+" * len(board[0]))
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * len(row))

def is_valid_input(input, cols):
    return len(input) == 1 and input.isalpha() and 'A' <= input <= chr(ord('A') + cols - 1)

def place_checker(board, checker, col):
    for row in reversed(board):
        if row[col] == " ":
            row[col] = checker
            return True
    return False

def check_winner(board, checker):
    def check_line(line):
        count = 0
        for cell in line:
            if cell == checker:
                count += 1
                if count == 4:
                    return True
            else:
                count = 0
        return False
    
    # Check horizontal
    for row in board:
        if check_line(row):
            return True
    
    # Check vertical
    for col in range(len(board[0])):
        if check_line([board[row][col] for row in range(len(board))]):
            return True
    
    # Check diagonal (both directions)
    for row in range(len(board) - 3):
        for col in range(len(board[0])):
            if col + 3 < len(board[0]):
                if all(board[row + i][col + i] == checker for i in range(4)):
                    return True
            if col - 3 >= 0:
                if all(board[row + i][col - i] == checker for i in range(4)):
                    return True

    return False

def is_draw(board):
    return all(cell != " " for row in board for cell in row)

def connect4_game():
    board = create_board(ROWS, COLUMNS)
    players_checker = CHECKERS[:PLAYERS]
    current_player = random.choice(players_checker)
    
    print_board(board)
    while True:
        print(f"Player {current_player}, please enter a column:")
        while True:
            user_input = input().strip().upper()
            if is_valid_input(user_input, len(board[0])):
                column_index = ord(user_input) - ord('A')
                if place_checker(board, current_player, column_index):
                    break
                else:
                    print("Column is full! Try another one.")
            else:
                print("Invalid input! Try again.")
        
        print_board(board)
        
        if check_winner(board, current_player):
            print(f"Player {current_player} won!")
            break
        
        if is_draw(board):
            print("The game is a draw!")
            break
        
        current_player = players_checker[(players_checker.index(current_player) + 1) % PLAYERS]

connect4_game()
