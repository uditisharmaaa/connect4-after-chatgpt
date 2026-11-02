import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]  # Checkers for up to 5 players

# Create the game board
def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

# Print the board
def print_board(board):
    os.system('clear')  # Clear the screen
    col_labels = "  " + "   ".join(chr(65 + i) for i in range(COLUMNS))  # Column letters: A-G
    print(col_labels)
    print("+---" * COLUMNS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLUMNS + "+")

# Check if a move is valid
def is_valid_move(board, col):
    return 0 <= col < COLUMNS and board[0][col] == " "

# Place a checker on the board
def place_checker(board, col, checker):
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return row

# Check for a win condition
def check_win(board, row, col, checker):
    # Check horizontal, vertical, and two diagonal directions
    directions = [
        (0, 1),   # Horizontal
        (1, 0),   # Vertical
        (1, 1),   # Diagonal down-right
        (1, -1)   # Diagonal down-left
    ]
    
    for dr, dc in directions:
        count = 1
        # Check in the positive direction
        r, c = row + dr, col + dc
        while 0 <= r < ROWS and 0 <= c < COLUMNS and board[r][c] == checker:
            count += 1
            r += dr
            c += dc
        # Check in the negative direction
        r, c = row - dr, col - dc
        while 0 <= r < ROWS and 0 <= c < COLUMNS and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc
        # Check if there are 4 in a row
        if count >= 4:
            return True
    return False

# Check if the board is full (draw condition)
def is_draw(board):
    return all(board[0][col] != " " for col in range(COLUMNS))

# Main game function
def play_game():
    # Initialize the board
    board = create_board(ROWS, COLUMNS)
    
    # Select number of players and assign checkers
    players = [CHECKERS[i] for i in range(PLAYERS)]
    
    # Randomly choose the first player
    current_player = random.randint(0, PLAYERS - 1)
    
    # Game loop
    while True:
        print_board(board)
        print(f"Player {players[current_player]}, it's your turn.")
        
        # Get valid column input from the player
        while True:
            user_input = input("Please enter a column (A-G): ").strip().upper()
            if len(user_input) == 1 and 'A' <= user_input <= chr(65 + COLUMNS - 1):
                col = ord(user_input) - 65
                if is_valid_move(board, col):
                    break
                else:
                    print("Column is full. Try again.")
            else:
                print("Invalid input. Please try again.")
        
        # Place checker and check for a win
        row = place_checker(board, col, players[current_player])
        if check_win(board, row, col, players[current_player]):
            print_board(board)
            print(f"Player {players[current_player]} won!")
            break
        
        # Check for a draw
        if is_draw(board):
            print_board(board)
            print("The game is a draw!")
            break
        
        # Switch to the next player
        current_player = (current_player + 1) % PLAYERS

# Run the game
if __name__ == "__main__":
    play_game()
