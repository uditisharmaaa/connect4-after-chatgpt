import os
import random

# Global constants
ROWS = 6
COLS = 7
MAX_PLAYERS = 5
PLAYER_TOKENS = ["X", "O", "V", "H", "M"]
EMPTY_CELL = " "

# Function to create the game board
def create_board(rows, cols):
    return [[EMPTY_CELL for _ in range(cols)] for _ in range(rows)]

# Function to print the board
def print_board(board):
    os.system('clear')  # Clear the terminal screen
    col_labels = "  " + "   ".join(chr(65 + i) for i in range(len(board[0])))
    print(col_labels)
    print("+---" * len(board[0]) + "+")

    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * len(board[0]) + "+")

# Function to get a valid column from the player
def get_valid_column(player, board):
    while True:
        column = input(f"Player {player}, please enter a column: ").upper()
        if len(column) == 1 and "A" <= column < chr(65 + len(board[0])):
            col_index = ord(column) - 65
            if board[0][col_index] == EMPTY_CELL:
                return col_index
            else:
                print("The column is full. Try another column.")
        else:
            print("Invalid input. Please enter a valid column letter.")

# Function to place the checker in the correct position
def place_checker(player_token, col_index, board):
    for row in reversed(board):
        if row[col_index] == EMPTY_CELL:
            row[col_index] = player_token
            break

# Function to check for a win
def check_win(board, token):
    # Check horizontal
    for row in board:
        for col in range(len(row) - 3):
            if all(cell == token for cell in row[col:col + 4]):
                return True

    # Check vertical
    for col in range(len(board[0])):
        for row in range(len(board) - 3):
            if all(board[row + i][col] == token for i in range(4)):
                return True

    # Check diagonals (\)
    for row in range(len(board) - 3):
        for col in range(len(board[0]) - 3):
            if all(board[row + i][col + i] == token for i in range(4)):
                return True

    # Check diagonals (/)
    for row in range(3, len(board)):
        for col in range(len(board[0]) - 3):
            if all(board[row - i][col + i] == token for i in range(4)):
                return True

    return False

# Function to check for a draw
def check_draw(board):
    return all(cell != EMPTY_CELL for row in board for cell in row)

# Main game loop
def main():
    # Create and initialize the board
    board = create_board(ROWS, COLS)

    # Number of players
    num_players = 2  # Adjust this value for more players

    # Tokens for each player
    players = PLAYER_TOKENS[:num_players]

    # Randomly select the first player
    current_player_index = random.randint(0, num_players - 1)

    # Game loop
    while True:
        print_board(board)

        # Current player
        current_token = players[current_player_index]

        # Get a valid column and place the checker
        column = get_valid_column(current_token, board)
        place_checker(current_token, column, board)

        # Check for a win
        if check_win(board, current_token):
            print_board(board)
            print(f"Player {current_token} won!")
            break

        # Check for a draw
        if check_draw(board):
            print_board(board)
            print("The game is a draw!")
            break

        # Alternate turn to the next player
        current_player_index = (current_player_index + 1) % num_players

if __name__ == "__main__":
    main()
