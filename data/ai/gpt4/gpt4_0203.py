import random
import os

# Global constants
BOARD_ROWS = 6
BOARD_COLS = 7
MAX_PLAYERS = 5
PLAYERS = ["X", "O", "V", "H", "M"][:MAX_PLAYERS]

def create_board(rows, cols):
    """Creates an empty board with given dimensions."""
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """Prints the Connect 4 board to the terminal."""
    os.system('clear')  # Clears the terminal
    col_labels = "  " + "   ".join(chr(65 + i) for i in range(BOARD_COLS))  # A, B, C...
    print(col_labels)
    print("+---" * BOARD_COLS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * BOARD_COLS + "+")

def is_valid_input(column, board):
    """Checks if the user input is a valid column."""
    if not column.isalpha() or len(column) != 1:
        return False
    col_index = ord(column.upper()) - 65
    return 0 <= col_index < BOARD_COLS and board[0][col_index] == " "

def get_empty_row(col_index, board):
    """Finds the lowest empty row in a given column."""
    for row_index in range(BOARD_ROWS - 1, -1, -1):
        if board[row_index][col_index] == " ":
            return row_index

def check_winner(board, player):
    """Checks if the given player has won the game."""
    # Horizontal check
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS - 3):
            if all(board[row][col + i] == player for i in range(4)):
                return True
    # Vertical check
    for row in range(BOARD_ROWS - 3):
        for col in range(BOARD_COLS):
            if all(board[row + i][col] == player for i in range(4)):
                return True
    # Diagonal check (top-left to bottom-right)
    for row in range(BOARD_ROWS - 3):
        for col in range(BOARD_COLS - 3):
            if all(board[row + i][col + i] == player for i in range(4)):
                return True
    # Diagonal check (bottom-left to top-right)
    for row in range(3, BOARD_ROWS):
        for col in range(BOARD_COLS - 3):
            if all(board[row - i][col + i] == player for i in range(4)):
                return True
    return False

def is_draw(board):
    """Checks if the game is a draw."""
    return all(board[0][col] != " " for col in range(BOARD_COLS))

def main():
    # Initialize the game
    board = create_board(BOARD_ROWS, BOARD_COLS)
    num_players = 2  # Set up for 2 players as per instructions
    players = PLAYERS[:num_players]
    current_player = random.choice(players)  # Randomly select the first player
    print_board(board)

    while True:
        # Prompt the current player for input
        print(f"Player {current_player}, please enter a column:")
        user_input = input().strip().upper()
        
        # Validate input
        if not is_valid_input(user_input, board):
            print("Invalid input! Please try again.")
            continue
        
        # Place the checker
        col_index = ord(user_input) - 65
        row_index = get_empty_row(col_index, board)
        board[row_index][col_index] = current_player

        # Update the board and print it
        print_board(board)

        # Check for a win
        if check_winner(board, current_player):
            print(f"Player {current_player} won!")
            break

        # Check for a draw
        if is_draw(board):
            print("The game is a draw!")
            break

        # Switch to the next player
        current_player = players[(players.index(current_player) + 1) % num_players]

if __name__ == "__main__":
    main()
