import random
import os

# Constants
ROWS = 6
COLS = 7
PLAYERS = ['X', 'O', 'V', 'H', 'M'][:5]  # Adjust for 2-5 players

# Initialize the board
def create_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

# Print the board
def print_board(board):
    os.system('clear')  # For Linux/OS X, use 'cls' for Windows
    print(" A B C D E F G")
    for row in board:
        print('|' + '|'.join(row) + '|')
    print("-" * (COLS * 2 + 1))

# Check for valid move
def is_valid_move(board, col):
    return board[0][col] == ' '

# Place a piece on the board
def make_move(board, col, player):
    for row in reversed(board):
        if row[col] == ' ':
            row[col] = player
            break

# Check for win
def check_win(board, player):
    # Check horizontal, vertical and diagonal
    for c in range(COLS - 3):
        for r in range(ROWS):
            if all(board[r][c+i] == player for i in range(4)):
                return True

    for c in range(COLS):
        for r in range(ROWS - 3):
            if all(board[r+i][c] == player for i in range(4)):
                return True

    for c in range(COLS - 3):
        for r in range(ROWS - 3):
            if all(board[r+i][c+i] == player for i in range(4)):
                return True
            if all(board[r+3-i][c+i] == player for i in range(4)):
                return True
    return False

# Check for draw
def check_draw(board):
    return all(board[0][c] != ' ' for c in range(COLS))

# Convert input letter to column index
def column_to_index(letter):
    return 'ABCDEFG'.index(letter)

# Main function
def connect_4():
    board = create_board()
    num_players = 2  # Adjustable if needed
    current_player = random.choice(PLAYERS[:num_players])
    
    while True:
        print_board(board)
        print(f"Player {current_player}'s turn")
        
        # Input validation
        valid_input = False
        while not valid_input:
            try:
                column_choice = input("Choose column (A-G): ").upper()
                col = column_to_index(column_choice)
                if is_valid_move(board, col):
                    valid_input = True
                else:
                    print("Column is full, choose another one!")
            except (ValueError, IndexError):
                print("Invalid input! Please enter a letter A-G.")
        
        make_move(board, col, current_player)

        if check_win(board, current_player):
            print_board(board)
            print(f"Player {current_player} wins!")
            break

        if check_draw(board):
            print_board(board)
            print("It's a draw!")
            break
        
        # Switch to next player
        current_player = PLAYERS[(PLAYERS.index(current_player) + 1) % num_players]

if __name__ == '__main__':
    connect_4()
