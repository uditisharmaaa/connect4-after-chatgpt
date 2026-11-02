import random
import os

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

def create_board():
    board = []
    for i in range(ROWS):
        row = []
        for j in range(COLS):
            row.append(" ")
        board.append(row)
    return board

def print_board(board):
    os.system('clear')
    # Print column labels
    print("  ", end="")
    for i in range(COLS):
        print(chr(65 + i) + "   ", end="")
    print()
    
    # Print rows
    for i in range(ROWS):
        print("+---" * COLS + "+")
        print("|", end="")
        for j in range(COLS):
            print(" " + board[i][j] + " |", end="")
        print()
    print("+---" * COLS + "+")

def is_valid_input(col_letter, board):
    # Check if it's a letter
    if len(col_letter) != 1:
        return False
    if not col_letter.isalpha():
        return False
    if not col_letter.isupper():
        return False
    
    # Check if column is in range
    col_index = ord(col_letter) - 65
    if col_index < 0 or col_index >= COLS:
        return False
    
    # Check if column is not full
    if board[0][col_index] != " ":
        return False
    
    return True

def place_checker(board, col_letter, checker):
    col_index = ord(col_letter) - 65
    
    # Find the lowest empty row
    for i in range(ROWS - 1, -1, -1):
        if board[i][col_index] == " ":
            board[i][col_index] = checker
            return True
    
    return False

def check_win(board, checker):
    # Check horizontal
    for i in range(ROWS):
        for j in range(COLS - 3):
            if board[i][j] == checker and board[i][j+1] == checker and board[i][j+2] == checker and board[i][j+3] == checker:
                return True
    
    # Check vertical
    for i in range(ROWS - 3):
        for j in range(COLS):
            if board[i][j] == checker and board[i+1][j] == checker and board[i+2][j] == checker and board[i+3][j] == checker:
                return True
    
    # Check diagonal (top-left to bottom-right)
    for i in range(ROWS - 3):
        for j in range(COLS - 3):
            if board[i][j] == checker and board[i+1][j+1] == checker and board[i+2][j+2] == checker and board[i+3][j+3] == checker:
                return True
    
    # Check diagonal (bottom-left to top-right)
    for i in range(3, ROWS):
        for j in range(COLS - 3):
            if board[i][j] == checker and board[i-1][j+1] == checker and board[i-2][j+2] == checker and board[i-3][j+3] == checker:
                return True
    
    return False

def check_draw(board):
    for i in range(COLS):
        if board[0][i] == " ":
            return False
    return True

def main():
    board = create_board()
    players = []
    for i in range(NUM_PLAYERS):
        players.append(CHECKERS[i])
    
    current_player = random.randint(0, NUM_PLAYERS - 1)
    print_board(board)
    
    game_over = False
    while not game_over:
        checker = players[current_player]
        valid = False
        
        while not valid:
            col_input = input("Player " + checker + ", please enter a column: ")
            if is_valid_input(col_input, board):
                valid = True
            else:
                print("Invalid input. Try again.")
        
        place_checker(board, col_input, checker)
        print_board(board)
        
        if check_win(board, checker):
            print("Player " + checker + " won!")
            game_over = True
        elif check_draw(board):
            print("It's a draw!")
            game_over = True
        else:
            current_player = (current_player + 1) % NUM_PLAYERS

main()
