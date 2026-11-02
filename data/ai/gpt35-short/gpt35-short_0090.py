import os
import random

# Constants
ROWS = 6
COLS = 7
COLUMN_LABELS = ['A', 'B', 'C', 'D', 'E', 'F', 'G']

# Available player tokens
PLAYERS_TOKENS = ['X', 'O', 'V', 'H', 'M']

def clear_screen():
    # Clear the terminal screen to keep the interface neat
    os.system('clear')

def create_board():
    # Create a ROWS x COLS board filled with empty spaces ' '
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    # Display the board with column labels on top and bottom
    print("  " + " ".join(COLUMN_LABELS))
    for row in board:
        print("|" + "|".join(row) + "|")
    print("  " + " ".join(COLUMN_LABELS))

def is_valid_column(col, board):
    # Check if column index is valid and if the column is not full
    if col < 0 or col >= COLS:
        return False
    return board[0][col] == ' '  # Top cell empty means column has space

def get_next_open_row(col, board):
    # Return the index of the lowest empty row in the specified column
    for r in range(ROWS-1, -1, -1):  # Start from bottom row upwards
        if board[r][col] == ' ':
            return r
    return None  # If column is full

def drop_piece(row, col, piece, board):
    # Place the player's piece in the board at given location
    board[row][col] = piece

def winning_move(piece, board):
    # Check all horizontal locations for win
    for r in range(ROWS):
        for c in range(COLS - 3):
            if all(board[r][c+i] == piece for i in range(4)):
                return True

    # Check all vertical locations for win
    for c in range(COLS):
        for r in range(ROWS - 3):
            if all(board[r+i][c] == piece for i in range(4)):
                return True

    # Check positively sloped diagonals (/)
    for r in range(3, ROWS):
        for c in range(COLS - 3):
            if all(board[r - i][c + i] == piece for i in range(4)):
                return True

    # Check negatively sloped diagonals (\)
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            if all(board[r + i][c + i] == piece for i in range(4)):
                return True

    return False

def board_full(board):
    # If no cells in top row are empty => board is full
    return all(cell != ' ' for cell in board[0])

def get_player_input(player, board):
    # Prompt player for a valid column input
    while True:
        choice = input(f"Player {player}'s turn. Choose column (A-G): ").upper()
        if choice not in COLUMN_LABELS:
            print("Invalid column. Please choose from A to G.")
            continue
        col = COLUMN_LABELS.index(choice)
        if not is_valid_column(col, board):
            print("Column full. Choose a different column.")
            continue
        return col

def main():
    clear_screen()
    print("Welcome to Connect 4!")

    # Ask number of players (2 to 5)
    while True:
        try:
            num_players = int(input("Enter number of players (2-5): "))
            if 2 <= num_players <= 5:
                break
            else:
                print("Please enter a number between 2 and 5.")
        except ValueError:
            print("Invalid input, please enter a number.")

    # Select player tokens based on number of players
    players = PLAYERS_TOKENS[:num_players]

    # Randomly select the starting player
    current_player_index = random.randint(0, num_players - 1)

    board = create_board()
    game_over = False

    while not game_over:
        clear_screen()
        print_board(board)
        current_player = players[current_player_index]

        # Get valid player input
        col = get_player_input(current_player, board)
        row = get_next_open_row(col, board)

        # Place the piece on the board
        drop_piece(row, col, current_player, board)

        # Check for win
        if winning_move(current_player, board):
            clear_screen()
            print_board(board)
            print(f"Player {current_player} wins! Congratulations!")
            game_over = True
            continue

        # Check for draw (board full)
        if board_full(board):
            clear_screen()
            print_board(board)
            print("The game is a draw! No more valid moves.")
            game_over = True
            continue

        # Move to next player
        current_player_index = (current_player_index + 1) % num_players

if __name__ == "__main__":
    main()
