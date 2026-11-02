import os
import random

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
    
    # Print column letters
    print("  ", end="")
    for i in range(COLS):
        letter = chr(65 + i)
        print(letter + "   ", end="")
    print()
    
    # Print board rows
    for row in board:
        print("+---" * COLS + "+")
        print("|", end="")
        for cell in row:
            print(" " + cell + " |", end="")
        print()
    print("+---" * COLS + "+")

def get_column(player_checker):
    while True:
        col_input = input("Player " + player_checker + ", please enter a column: ")
        
        if len(col_input) != 1:
            print("Invalid input. Please enter a single letter.")
            continue
        
        if not col_input.isupper():
            print("Invalid input. Please enter an uppercase letter.")
            continue
        
        col_num = ord(col_input) - 65
        
        if col_num < 0 or col_num >= COLS:
            print("Invalid column. Please try again.")
            continue
        
        return col_num

def place_checker(board, col, checker):
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return True
    return False

def check_win(board, checker):
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLS - 3):
            if (board[row][col] == checker and 
                board[row][col + 1] == checker and 
                board[row][col + 2] == checker and 
                board[row][col + 3] == checker):
                return True
    
    # Check vertical
    for row in range(ROWS - 3):
        for col in range(COLS):
            if (board[row][col] == checker and 
                board[row + 1][col] == checker and 
                board[row + 2][col] == checker and 
                board[row + 3][col] == checker):
                return True
    
    # Check diagonal (down-right)
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if (board[row][col] == checker and 
                board[row + 1][col + 1] == checker and 
                board[row + 2][col + 2] == checker and 
                board[row + 3][col + 3] == checker):
                return True
    
    # Check diagonal (down-left)
    for row in range(ROWS - 3):
        for col in range(3, COLS):
            if (board[row][col] == checker and 
                board[row + 1][col - 1] == checker and 
                board[row + 2][col - 2] == checker and 
                board[row + 3][col - 3] == checker):
                return True
    
    return False

def check_draw(board):
    for row in board:
        for cell in row:
            if cell == " ":
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
        player_checker = players[current_player]
        
        col = get_column(player_checker)
        
        if not place_checker(board, col, player_checker):
            print("Column is full! You lose your turn.")
        else:
            print_board(board)
            
            if check_win(board, player_checker):
                print("Player " + player_checker + " won!")
                game_over = True
            elif check_draw(board):
                print("It's a draw!")
                game_over = True
        
        current_player = (current_player + 1) % NUM_PLAYERS

main()
