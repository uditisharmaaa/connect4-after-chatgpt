import os
import random

# Constants
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

def create_board(rows, cols):
    """Creates an empty Connect 4 board with the specified number of rows and columns."""
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """Prints the current state of the board."""
    print("  A", end="")
    for col in range(1, NUM_COLS):
        print("   " + chr(65 + col), end="")
    print()
    for row in range(NUM_ROWS):
        for col in range(NUM_COLS):
            print("+---", end="")
        print("+")
        for col in range(NUM_COLS):
            print("| " + board[row][col] + " ", end="")
        print("|")
        if row!= NUM_ROWS - 1:
            for col in range(NUM_COLS):
                print("+---", end="")
            print("+")
    print()

def validate_input(input_str):
    """Checks if the user's input is a valid column letter."""
    return len(input_str) == 1 and "A" <= input_str.upper() <= "G" and input_str.upper() == input_str

def get_column_from_input(input_str):
    """Converts the user's input into a column index."""
    return ord(input_str.upper()) - 65

def is_valid_move(board, col):
    """Checks if a move is valid (i.e., the column is not full)."""
    return board[NUM_ROWS - 1][col] == " "

def make_move(board, player, col):
    """Makes a move on the board by placing the player's checker in the specified column."""
    for row in range(NUM_ROWS - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = player
            break

def check_win(board, player):
    """Checks if the player has won the game."""
    # Check horizontal wins
    for row in range(NUM_ROWS):
        for col in range(NUM_COLS - 3):
            if board[row][col] == player and board[row][col + 1] == player and board[row][col + 2] == player and board[row][col + 3] == player:
                return True

    # Check vertical wins
    for row in range(NUM_ROWS - 3):
        for col in range(NUM_COLS):
            if board[row][col] == player and board[row + 1][col] == player and board[row + 2][col] == player and board[row + 3][col] == player:
                return True

    # Check diagonal wins (top-left to bottom-right)
    for row in range(NUM_ROWS - 3):
        for col in range(NUM_COLS - 3):
            if board[row][col] == player and board[row + 1][col + 1] == player and board[row + 2][col + 2] == player and board[row + 3][col + 3] == player:
                return True

    # Check diagonal wins (bottom-left to top-right)
    for row in range(3, NUM_ROWS):
        for col in range(NUM_COLS - 3):
            if board[row][col] == player and board[row - 1][col + 1] == player and board[row - 2][col + 2] == player and board[row - 3][col + 3] == player:
                return True

    return False

def check_draw(board):
    """Checks if the game is a draw (i.e., the board is full and no player has won)."""
    return all(cell!= " " for row in board for cell in row)

def main():
    # Create the board
    board = create_board(NUM_ROWS, NUM_COLS)

    # Randomly select the first player
    players = CHECKERS[:NUM_PLAYERS]
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    current_player = players[current_player_index]

    while True:
        # Clear the screen
        os.system('clear')

        # Print the board
        print_board(board)

        # Get the current player's move
        while True:
            move = input(f"Player {current_player}, please enter a column: ")
            if validate_input(move):
                col = get_column_from_input(move)
                if is_valid_move(board, col):
                    break
                else:
                    print("Invalid move, column is full. Please try again.")
            else:
                print("Invalid input. Please enter a letter between A and G.")

        # Make the move
        make_move(board, current_player, col)

        # Check if the game is over
        if check_win(board, current_player):
            os.system('clear')
            print_board(board)
            print(f"Player {current_player} won!")
            break
        elif check_draw(board):
            os.system('clear')
            print_board(board)
            print("It's a draw!")
            break

        # Switch to the next player
        current_player_index = (current_player_index + 1) % NUM_PLAYERS
        current_player = players[current_player_index]

if __name__ == "__main__":
    main()
