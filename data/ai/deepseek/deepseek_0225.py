import os
import random

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
PLAYERS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]

def initialize_board():
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    # Clear the screen
    os.system('clear')
    
    # Print column headers
    header = "  " + "   ".join([chr(ord('A') + i) for i in range(COLS)])
    print(header)
    
    # Print board rows
    for row in board:
        line = "+" + "+".join(["---"] * COLS) + "+"
        print(line)
        content = "|" + "|".join([f" {cell} " for cell in row]) + "|"
        print(content)
    
    # Print bottom border
    print("+" + "+".join(["---"] * COLS) + "+")

def is_valid_move(board, col):
    if col < 0 or col >= COLS:
        return False
    return board[0][col] == " "

def make_move(board, col, player):
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = player
            return True
    return False

def check_win(board, player):
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLS - 3):
            if (board[row][col] == player and 
                board[row][col+1] == player and 
                board[row][col+2] == player and 
                board[row][col+3] == player):
                return True
    
    # Check vertical
    for row in range(ROWS - 3):
        for col in range(COLS):
            if (board[row][col] == player and 
                board[row+1][col] == player and 
                board[row+2][col] == player and 
                board[row+3][col] == player):
                return True
    
    # Check diagonal (down-right)
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if (board[row][col] == player and 
                board[row+1][col+1] == player and 
                board[row+2][col+2] == player and 
                board[row+3][col+3] == player):
                return True
    
    # Check diagonal (up-right)
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if (board[row][col] == player and 
                board[row-1][col+1] == player and 
                board[row-2][col+2] == player and 
                board[row-3][col+3] == player):
                return True
    
    return False

def is_board_full(board):
    for row in board:
        if " " in row:
            return False
    return True

def play_game():
    board = initialize_board()
    current_player = random.randint(0, NUM_PLAYERS - 1)
    
    while True:
        print_board(board)
        player_symbol = PLAYERS[current_player]
        print(f"Player {player_symbol}, please enter a column: ")
        
        # Get input from user
        while True:
            try:
                col_input = input().upper()
                if len(col_input) != 1 or ord(col_input) < ord('A') or ord(col_input) >= ord('A') + COLS:
                    print(f"Invalid input. Please enter a letter from A to {chr(ord('A') + COLS - 1)}: ")
                    continue
                
                col = ord(col_input) - ord('A')
                if is_valid_move(board, col):
                    break
                else:
                    print("Column is full. Please choose another column: ")
            except:
                print(f"Invalid input. Please enter a letter from A to {chr(ord('A') + COLS - 1)}: ")
        
        # Make the move
        make_move(board, col, player_symbol)
        
        # Check for win
        if check_win(board, player_symbol):
            print_board(board)
            print(f"Player {player_symbol} won!")
            break
        
        # Check for draw
        if is_board_full(board):
            print_board(board)
            print("Game ended in a draw!")
            break
        
        # Switch player
        current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == "__main__":
    play_game()
