import os
import random

# Constants for players
PLAYERS = ['X', 'O', 'V', 'H', 'M']

ROWS = 6
COLS = 7
COL_LABELS = ['A', 'B', 'C', 'D', 'E', 'F', 'G']

def clear_screen():
    os.system('clear')

def create_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    print(" " + " ".join(COL_LABELS))
    for row in board:
        print("|" + "|".join(row) + "|")
    print("-" * (COLS * 2 + 1))

def get_valid_column(board):
    while True:
        col = input("Choose a column (A-G): ").upper()
        if col not in COL_LABELS:
            print("Invalid column. Please enter a letter from A to G.")
            continue
        col_index = COL_LABELS.index(col)
        if board[0][col_index] != ' ':
            print("Column is full. Choose another one.")
            continue
        return col_index

def drop_piece(board, col, player):
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = player
            return row, col

def check_win(board, player):
    # Check horizontal
    for r in range(ROWS):
        for c in range(COLS - 3):
            if all(board[r][c+i] == player for i in range(4)):
                return True
    # Check vertical
    for c in range(COLS):
        for r in range(ROWS - 3):
            if all(board[r+i][c] == player for i in range(4)):
                return True
    # Check diagonal down-right
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            if all(board[r+i][c+i] == player for i in range(4)):
                return True
    # Check diagonal up-right
    for r in range(3, ROWS):
        for c in range(COLS - 3):
            if all(board[r-i][c+i] == player for i in range(4)):
                return True
    return False

def is_draw(board):
    return all(board[0][c] != ' ' for c in range(COLS))

def main():
    clear_screen()
    print("Welcome to Connect 4!")
    
    # Ask for number of players
    while True:
        try:
            num_players = int(input("Enter number of players (2-5): "))
            if 2 <= num_players <= 5:
                break
            print("Please enter a number between 2 and 5.")
        except ValueError:
            print("That's not a valid number.")
    
    players = PLAYERS[:num_players]
    
    # Random first player
    current_player_idx = random.randint(0, num_players -1)
    
    board = create_board()
    
    while True:
        clear_screen()
        print_board(board)
        player = players[current_player_idx]
        print(f"Player {player}'s turn.")
        col = get_valid_column(board)
        drop_piece(board, col, player)
        
        if check_win(board, player):
            clear_screen()
            print_board(board)
            print(f"Player {player} wins! Congratulations!")
            break
        if is_draw(board):
            clear_screen()
            print_board(board)
            print("It's a draw!")
            break
        
        current_player_idx = (current_player_idx + 1) % num_players

if __name__ == "__main__":
    main()
