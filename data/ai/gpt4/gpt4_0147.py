import os
import random

# Constants
ROWS = 6
COLUMNS = 7
MAX_COLUMNS = 26
MAX_PLAYERS = 5
PLAYERS = ["X", "O", "V", "H", "M"]  # Checker identifiers for up to 5 players

# Initialize the game board
def create_board(rows, columns):
    return [[" " for _ in range(columns)] for _ in range(rows)]

# Print the game board
def print_board(board):
    os.system('clear')  # Clear the screen
    column_labels = [chr(65 + i) for i in range(len(board[0]))]  # 'A', 'B', 'C', ...
    print("  " + "   ".join(column_labels))  # Print column labels
    print("+---" * len(column_labels) + "+")
    
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * len(column_labels) + "+")

# Validate user input for a column
def is_valid_column(column, board):
    if column.isalpha() and column.upper() in [chr(65 + i) for i in range(len(board[0]))]:
        col_index = ord(column.upper()) - 65
        return board[0][col_index] == " "  # Check if the column isn't full
    return False

# Drop the checker in the chosen column
def drop_checker(board, column, checker):
    col_index = ord(column.upper()) - 65
    for row in range(len(board) - 1, -1, -1):  # Start from the bottom of the column
        if board[row][col_index] == " ":
            board[row][col_index] = checker
            return row, col_index  # Return the position of the placed checker

# Check for a win
def check_win(board, player, row, col):
    # Directions: (row_offset, col_offset)
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]  # Horizontal, vertical, diagonal-right, diagonal-left
    
    for dr, dc in directions:
        count = 1
        for multiplier in [1, -1]:  # Check both forward and backward
            r, c = row, col
            while True:
                r += dr * multiplier
                c += dc * multiplier
                if 0 <= r < len(board) and 0 <= c < len(board[0]) and board[r][c] == player:
                    count += 1
                else:
                    break
                if count >= 4:  # Check if 4 in a row is reached
                    return True
    return False

# Check for a draw
def check_draw(board):
    return all(cell != " " for row in board for cell in row)

# Main game loop
def play_connect4():
    # Initialize game settings
    board = create_board(ROWS, COLUMNS)
    num_players = 2  # Number of players (Set by the assignment)
    players = PLAYERS[:num_players]
    
    # Randomly select the starting player
    current_player_index = random.randint(0, num_players - 1)
    
    # Game loop
    winner = None
    while True:
        print_board(board)
        current_player = players[current_player_index]
        print(f"Player {current_player}, it's your turn!")
        
        # Get valid input from the current player
        while True:
            column = input("Please enter a column: ").strip()
            if is_valid_column(column, board):
                break
            print("Invalid input. Please enter a valid column (e.g., A, B, ...).")
        
        # Place the checker
        row, col = drop_checker(board, column, current_player)

        # Check for win
        if check_win(board, current_player, row, col):
            winner = current_player
            break

        # Check for draw
        if check_draw(board):
            break

        # Switch to the next player
        current_player_index = (current_player_index + 1) % num_players

    # Print final board and result
    print_board(board)
    if winner:
        print(f"Player {winner} won!")
    else:
        print("It's a draw!")

# Run the game
if __name__ == "__main__":
    play_connect4()
