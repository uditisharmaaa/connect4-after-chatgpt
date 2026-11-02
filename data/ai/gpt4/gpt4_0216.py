import os
import random

# Constants
ROWS = 6
COLS = 7
MAX_PLAYERS = 5
PLAYER_SYMBOLS = ["X", "O", "V", "H", "M"]

def clear_screen():
    """Clears the terminal screen."""
    os.system('clear')

def create_board(rows, cols):
    """Creates a blank game board."""
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """Prints the game board to the terminal."""
    header = "  " + "   ".join(chr(65 + i) for i in range(len(board[0])))  # Column labels (A, B, C, ...)
    print(header)
    print("+---" * len(board[0]) + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * len(board[0]) + "+")

def is_valid_column(column, board):
    """Checks if a column is valid and not full."""
    if column < 0 or column >= len(board[0]):
        return False
    return board[0][column] == " "

def drop_checker(board, column, symbol):
    """Places the symbol in the lowest available position in the given column."""
    for row in range(len(board) - 1, -1, -1):
        if board[row][column] == " ":
            board[row][column] = symbol
            return True
    return False

def check_winner(board, symbol):
    """Checks if the player with the given symbol has won."""
    rows, cols = len(board), len(board[0])
    
    # Check horizontal
    for row in range(rows):
        for col in range(cols - 3):
            if all(board[row][col + i] == symbol for i in range(4)):
                return True

    # Check vertical
    for col in range(cols):
        for row in range(rows - 3):
            if all(board[row + i][col] == symbol for i in range(4)):
                return True

    # Check diagonal (down-right)
    for row in range(rows - 3):
        for col in range(cols - 3):
            if all(board[row + i][col + i] == symbol for i in range(4)):
                return True

    # Check diagonal (up-right)
    for row in range(3, rows):
        for col in range(cols - 3):
            if all(board[row - i][col + i] == symbol for i in range(4)):
                return True

    return False

def check_draw(board):
    """Checks if the board is full."""
    return all(board[0][col] != " " for col in range(len(board[0])))

def next_player(current_player, total_players):
    """Cycles to the next player's turn."""
    return (current_player + 1) % total_players

def main():
    # Configuration
    num_players = 2  # Set to 2 initially
    symbols = PLAYER_SYMBOLS[:num_players]

    # Game Initialization
    board = create_board(ROWS, COLS)
    current_player = random.randint(0, num_players - 1)

    game_over = False
    winner = None

    # Game Loop
    while not game_over:
        clear_screen()
        print_board(board)
        print(f"Player {symbols[current_player]}'s turn!")

        # Get and validate player input
        while True:
            player_input = input("Please enter a column (A-G): ").strip().upper()
            if len(player_input) == 1 and player_input.isalpha():
                column = ord(player_input) - 65  # Convert letter (A, B, ...) to index
                if is_valid_column(column, board):
                    break
            print("Invalid input. Please try again.")

        # Place the checker
        drop_checker(board, column, symbols[current_player])

        # Check for win or draw
        if check_winner(board, symbols[current_player]):
            game_over = True
            winner = symbols[current_player]
        elif check_draw(board):
            game_over = True

        # Switch to the next player
        if not game_over:
            current_player = next_player(current_player, num_players)

    # Game Over
    clear_screen()
    print_board(board)
    if winner:
        print(f"Player {winner} won!")
    else:
        print("It's a draw!")

if __name__ == "__main__":
    main()
