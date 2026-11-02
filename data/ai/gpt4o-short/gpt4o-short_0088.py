import random
import os

# Constants
ROWS = 6
COLUMNS = 7
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']  # Symbols for players

# Initialize board
def create_board():
    return [[' ' for _ in range(COLUMNS)] for _ in range(ROWS)]

# Display board
def print_board(board):
    os.system('clear')  # Use 'cls' if you're on Windows
    print("  A   B   C   D   E   F   G")
    for row in board:
        print('| ' + ' | '.join(row) + ' |')
    print("\n")

# Check for valid input
def is_valid_column(board, column):
    return (0 <= column < COLUMNS) and (board[0][column] == ' ')

# Get next open row in column
def get_next_open_row(board, column):
    for row in range(ROWS-1, -1, -1):
        if board[row][column] == ' ':
            return row
    return None

# Place piece
def place_piece(board, row, column, piece):
    board[row][column] = piece

# Check for win
def check_win(board, piece):
    # Horizontal Check
    for c in range(COLUMNS-3):
        for r in range(ROWS):
            if all(board[r][c+i] == piece for i in range(4)):
                return True

    # Vertical Check
    for c in range(COLUMNS):
        for r in range(ROWS-3):
            if all(board[r+i][c] == piece for i in range(4)):
                return True

    # Positive Diagonal
    for c in range(COLUMNS-3):
        for r in range(ROWS-3):
            if all(board[r+i][c+i] == piece for i in range(4)):
                return True

    # Negative Diagonal
    for c in range(COLUMNS-3):
        for r in range(3, ROWS):
            if all(board[r-i][c+i] == piece for i in range(4)):
                return True

    return False

# Check for draw
def check_draw(board):
    return all(board[0][c] != ' ' for c in range(COLUMNS))

# Main game execution
def play_game(num_players):
    # Ensure number of players is valid
    if not (2 <= num_players <= 5):
        print("Number of players must be between 2 and 5.")
        return

    # Initialize game
    board = create_board()
    game_over = False
    turn = random.randint(0, num_players - 1)  # Choose random starting player

    # Game loop
    while not game_over:
        print_board(board)
        player_symbol = PLAYER_SYMBOLS[turn]
        print(f"Player {player_symbol}'s turn!")

        # Get input from player
        try:
            move = input("Choose a column (A-G): ").upper()
            column = ord(move) - ord('A')
            if is_valid_column(board, column):
                row = get_next_open_row(board, column)
                place_piece(board, row, column, player_symbol)

                if check_win(board, player_symbol):
                    print_board(board)
                    print(f"Player {player_symbol} wins!")
                    game_over = True
                elif check_draw(board):
                    print_board(board)
                    print("It's a draw!")
                    game_over = True
                else:
                    turn = (turn + 1) % num_players
            else:
                print("Invalid column. Please try again.")
        except Exception as e:
            print(f"Invalid input: {e}. Please try again.")

if __name__ == "__main__":
    play_game(3)  # Change this number to set the number of players
