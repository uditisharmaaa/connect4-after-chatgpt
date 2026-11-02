import os
import random

# Constants for board dimensions and player symbols
ROWS = 6
COLS = 7
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']  # Maximum of 5 players

# Function to create and initialize the board
def create_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

# Function to print the game board
def print_board(board):
    os.system('clear')  # Clear the screen (use 'cls' for Windows)
    
    # Print column labels
    column_labels = "  " + "   ".join(chr(i) for i in range(65, 65 + COLS))
    print(column_labels)
    print('+' + ('---+' * COLS))
    
    # Print board rows
    for row in board:
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
        print('+' + ('---+' * COLS))

# Function to select a random starting player
def select_first_player(num_players):
    return random.randint(0, num_players - 1)

# Function to check for a win in the board
def check_win(board, player):
    # Check horizontal, vertical, and diagonal wins
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] == player:
                # Check horizontal
                if c + 3 < COLS and all(board[r][c + i] == player for i in range(4)):
                    return True
                # Check vertical
                if r + 3 < ROWS and all(board[r + i][c] == player for i in range(4)):
                    return True
                # Check diagonal (down-right)
                if r + 3 < ROWS and c + 3 < COLS and all(board[r + i][c + i] == player for i in range(4)):
                    return True
                # Check diagonal (up-right)
                if r - 3 >= 0 and c + 3 < COLS and all(board[r - i][c + i] == player for i in range(4)):
                    return True
    return False

# Function to check if the board is full (draw case)
def check_draw(board):
    return all(board[0][c] != ' ' for c in range(COLS))

# Function to place a checker in a column
def place_checker(board, column, player):
    for r in range(ROWS - 1, -1, -1):  # Start from the bottom of the column
        if board[r][column] == ' ':
            board[r][column] = player
            return True
    return False  # Column is full

# Main game loop
def main():
    board = create_board()
    num_players = 2  # Set this to enable more players if needed
    players = PLAYER_SYMBOLS[:num_players]
    current_player_index = select_first_player(num_players)

    while True:
        print_board(board)
        current_player = players[current_player_index]
        print(f"Player {current_player}, please enter a column (A-{chr(65 + COLS - 1)}): ")

        while True:
            user_input = input().strip().upper()
            if len(user_input) != 1 or not ('A' <= user_input <= chr(65 + COLS - 1)):
                print("Invalid input. Please enter a valid column letter.")
                continue
            
            column = ord(user_input) - 65  # Convert letter to column index
            if place_checker(board, column, current_player):
                break  # Break the loop if checker is placed successfully
            print("Column is full. Please choose another column.")

        if check_win(board, current_player):
            print_board(board)
            print(f"Player {current_player} won!")
            break

        if check_draw(board):
            print_board(board)
            print("The game is a draw!")
            break

        # Switch to the next player
        current_player_index = (current_player_index + 1) % num_players

if __name__ == "__main__":
    main()
