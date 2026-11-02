import os
import random

# Constants
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2

def initialize_board():
    return [[" " for _ in range(NUM_COLS)] for _ in range(NUM_ROWS)]

def print_board(board):
    os.system('clear')
    # Print column headers
    print("  " + "   ".join(chr(ord('A') + i) for i in range(NUM_COLS)))
    
    # Print the board
    for row in board:
        print("+---" * NUM_COLS + "+")
        print("| " + " | ".join(cell for cell in row) + " |")
    print("+---" * NUM_COLS + "+")

def get_player_checkers(num_players):
    checkers = ["X", "O", "V", "H", "M"]
    return checkers[:num_players]

def is_valid_move(board, col):
    if col < 0 or col >= NUM_COLS:
        return False
    return board[0][col] == " "

def place_checker(board, col, checker):
    for row in range(NUM_ROWS - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return True
    return False

def check_win(board, checker):
    # Check horizontal
    for row in range(NUM_ROWS):
        for col in range(NUM_COLS - 3):
            if all(board[row][col + i] == checker for i in range(4)):
                return True
    
    # Check vertical
    for row in range(NUM_ROWS - 3):
        for col in range(NUM_COLS):
            if all(board[row + i][col] == checker for i in range(4)):
                return True
    
    # Check diagonal (top-left to bottom-right)
    for row in range(NUM_ROWS - 3):
        for col in range(NUM_COLS - 3):
            if all(board[row + i][col + i] == checker for i in range(4)):
                return True
    
    # Check diagonal (bottom-left to top-right)
    for row in range(3, NUM_ROWS):
        for col in range(NUM_COLS - 3):
            if all(board[row - i][col + i] == checker for i in range(4)):
                return True
    
    return False

def is_draw(board):
    return all(cell != " " for row in board for cell in row)

def get_column_from_input(input_str):
    if len(input_str) != 1:
        return -1
    col_char = input_str.upper()
    if not col_char.isalpha():
        return -1
    col = ord(col_char) - ord('A')
    return col

def play_game():
    board = initialize_board()
    players = get_player_checkers(NUM_PLAYERS)
    current_player = random.choice(players)
    
    while True:
        print_board(board)
        while True:
            user_input = input(f"Player {current_player}, please enter a column: ").strip()
            col = get_column_from_input(user_input)
            if col == -1:
                print("Invalid input. Please enter a letter from A to", chr(ord('A') + NUM_COLS - 1))
            elif not is_valid_move(board, col):
                print("Column is full or invalid. Please choose another column.")
            else:
                break
        
        place_checker(board, col, current_player)
        
        if check_win(board, current_player):
            print_board(board)
            print(f"Player {current_player} won!")
            break
        
        if is_draw(board):
            print_board(board)
            print("The game is a draw!")
            break
        
        # Switch player
        current_player = players[(players.index(current_player) + 1) % NUM_PLAYERS]

if __name__ == "__main__":
    play_game()
