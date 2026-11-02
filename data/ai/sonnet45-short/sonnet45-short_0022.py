# Connect 4 Game
# Intro CS Project

import random
import os

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2  # Change this to 2, 3, 4, or 5 players
PLAYERS = ['X', 'O', 'V', 'H', 'M']

# Initialize the board
def create_board():
    board = []
    for row in range(ROWS):
        board.append([' '] * COLS)
    return board

# Display the board
def print_board(board):
    os.system('clear')
    print("\n  A B C D E F G")
    print(" +" + "-" * (COLS * 2 - 1) + "+")
    for row in range(ROWS):
        print(str(row + 1) + "|", end="")
        for col in range(COLS):
            print(board[row][col], end="|")
        print()
    print(" +" + "-" * (COLS * 2 - 1) + "+")
    print("  A B C D E F G\n")

# Convert column letter to index
def column_to_index(col_letter):
    col_letter = col_letter.upper()
    if col_letter >= 'A' and col_letter <= 'G':
        return ord(col_letter) - ord('A')
    return -1

# Check if a column has space
def is_valid_move(board, col):
    if col < 0 or col >= COLS:
        return False
    return board[0][col] == ' '

# Drop a piece in the column
def drop_piece(board, col, player):
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = player
            return row
    return -1

# Check for a win
def check_win(board, player):
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLS - 3):
            if (board[row][col] == player and
                board[row][col + 1] == player and
                board[row][col + 2] == player and
                board[row][col + 3] == player):
                return True
    
    # Check vertical
    for row in range(ROWS - 3):
        for col in range(COLS):
            if (board[row][col] == player and
                board[row + 1][col] == player and
                board[row + 2][col] == player and
                board[row + 3][col] == player):
                return True
    
    # Check diagonal (down-right)
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if (board[row][col] == player and
                board[row + 1][col + 1] == player and
                board[row + 2][col + 2] == player and
                board[row + 3][col + 3] == player):
                return True
    
    # Check diagonal (down-left)
    for row in range(ROWS - 3):
        for col in range(3, COLS):
            if (board[row][col] == player and
                board[row + 1][col - 1] == player and
                board[row + 2][col - 2] == player and
                board[row + 3][col - 3] == player):
                return True
    
    return False

# Check if the board is full (draw)
def is_board_full(board):
    for col in range(COLS):
        if board[0][col] == ' ':
            return False
    return True

# Main game function
def play_game():
    board = create_board()
    players = PLAYERS[:NUM_PLAYERS]
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    print("Welcome to Connect 4!")
    print(f"Players: {', '.join(players)}")
    print(f"First player: {players[current_player_index]}")
    input("Press Enter to start...")
    
    game_over = False
    
    while not game_over:
        print_board(board)
        current_player = players[current_player_index]
        print(f"Player {current_player}'s turn")
        
        # Get valid input
        valid_move = False
        while not valid_move:
            col_input = input("Enter column (A-G): ")
            
            if len(col_input) != 1:
                print("Please enter a single letter from A to G")
                continue
            
            col = column_to_index(col_input)
            
            if col == -1:
                print("Invalid column! Please enter A-G")
                continue
            
            if not is_valid_move(board, col):
                print("Column is full! Choose another column")
                continue
            
            valid_move = True
        
        # Drop the piece
        drop_piece(board, col, current_player)
        
        # Check for win
        if check_win(board, current_player):
            print_board(board)
            print(f"Player {current_player} wins!")
            game_over = True
        # Check for draw
        elif is_board_full(board):
            print_board(board)
            print("It's a draw!")
            game_over = True
        else:
            # Next player's turn
            current_player_index = (current_player_index + 1) % NUM_PLAYERS
    
    print("\nThanks for playing!")

# Start the game
play_game()
