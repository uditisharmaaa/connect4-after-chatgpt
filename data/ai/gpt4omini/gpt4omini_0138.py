import os
import random

# Constants for board dimensions and number of players
ROWS = 6
COLUMNS = 7
NUM_PLAYERS = 2
PLAYERS = ['X', 'O', 'V', 'H', 'M']  # Up to 5 players

# Initialize the game board
def create_board():
    return [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]

# Print the game board
def print_board(board):
    os.system('clear')  # Clear the terminal screen
    # Print column labels
    print("  " + "   ".join([chr(i) for i in range(65, 65 + COLUMNS)]))
    print("+" + "---+" * COLUMNS)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * COLUMNS)

# Check if a move is valid
def is_valid_move(board, col):
    return board[0][col] == " "

# Place a checker on the board
def place_checker(board, col, checker):
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return True
    return False

# Check for a win
def check_win(board, checker):
    # Check horizontal, vertical and diagonal wins
    for row in range(ROWS):
        for col in range(COLUMNS):
            if (check_horizontal(board, row, col, checker) or
                check_vertical(board, row, col, checker) or
                check_diagonal(board, row, col, checker)):
                return True
    return False

# Check horizontal win
def check_horizontal(board, row, col, checker):
    if col + 3 < COLUMNS:
        return all(board[row][col + i] == checker for i in range(4))
    return False

# Check vertical win
def check_vertical(board, row, col, checker):
    if row + 3 < ROWS:
        return all(board[row + i][col] == checker for i in range(4))
    return False

# Check diagonal win (bottom-left to top-right)
def check_diagonal(board, row, col, checker):
    if row + 3 < ROWS and col - 3 >= 0:
        return all(board[row + i][col - i] == checker for i in range(4))
    # Check diagonal (top-left to bottom-right)
    if row - 3 >= 0 and col - 3 >= 0:
        return all(board[row - i][col - i] == checker for i in range(4))
    return False

# Check for a draw
def check_draw(board):
    return all(board[0][col] != " " for col in range(COLUMNS))

# Main game function
def play_game():
    board = create_board()
    current_player = random.randint(0, NUM_PLAYERS - 1)
    print_board(board)

    while True:
        player_checker = PLAYERS[current_player]
        col = input(f"Player {player_checker}, please enter a column (A-{chr(65 + COLUMNS - 1)}): ").upper()

        if len(col) != 1 or ord(col) < 65 or ord(col) >= 65 + COLUMNS:
            print("Invalid column! Please try again.")
            continue

        col = ord(col) - 65  # Convert letter to index
        if not is_valid_move(board, col):
            print("Column is full! Please try again.")
            continue

        place_checker(board, col, player_checker)
        print_board(board)

        if check_win(board, player_checker):
            print(f"Player {player_checker} won!")
            break
            
        if check_draw(board):
            print("The game is a draw!")
            break
        
        # Alternate to the next player
        current_player = (current_player + 1) % NUM_PLAYERS

# Run the game
if __name__ == "__main__":
    play_game()
