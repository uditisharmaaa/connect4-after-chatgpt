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
        letter = chr(65 + i)
        print(letter + "   ", end="")
    print()
    
    # Print board
    for i in range(ROWS):
        print("+---" * COLS + "+")
        print("|", end="")
        for j in range(COLS):
            print(" " + board[i][j] + " |", end="")
        print()
    print("+---" * COLS + "+")

def place_checker(board, col, checker):
    for i in range(ROWS - 1, -1, -1):
        if board[i][col] == " ":
            board[i][col] = checker
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
    
    # Check diagonal (down-right)
    for i in range(ROWS - 3):
        for j in range(COLS - 3):
            if board[i][j] == checker and board[i+1][j+1] == checker and board[i+2][j+2] == checker and board[i+3][j+3] == checker:
                return True
    
    # Check diagonal (down-left)
    for i in range(ROWS - 3):
        for j in range(3, COLS):
            if board[i][j] == checker and board[i+1][j-1] == checker and board[i+2][j-2] == checker and board[i+3][j-3] == checker:
                return True
    
    return False

def check_draw(board):
    for i in range(ROWS):
        for j in range(COLS):
            if board[i][j] == " ":
                return False
    return True

def get_valid_input():
    while True:
        user_input = input()
        
        if len(user_input) != 1:
            print("Invalid input. Please enter a single column letter:")
            continue
        
        if not user_input.isalpha():
            print("Invalid input. Please enter a letter:")
            continue
        
        user_input = user_input.upper()
        col_index = ord(user_input) - 65
        
        if col_index < 0 or col_index >= COLS:
            print("Invalid input. Column out of range. Please try again:")
            continue
        
        return col_index

def main():
    board = create_board()
    players = []
    for i in range(NUM_PLAYERS):
        players.append(CHECKERS[i])
    
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    print_board(board)
    
    game_over = False
    while not game_over:
        current_checker = players[current_player_index]
        print("Player " + current_checker + ", please enter a column:")
        
        col = get_valid_input()
        
        if not place_checker(board, col, current_checker):
            print("Column is full! You lose your turn.")
            current_player_index = (current_player_index + 1) % NUM_PLAYERS
            continue
        
        print_board(board)
        
        if check_win(board, current_checker):
            print("Player " + current_checker + " won!")
            game_over = True
        elif check_draw(board):
            print("The game is a draw!")
            game_over = True
        else:
            current_player_index = (current_player_index + 1) % NUM_PLAYERS

main()
