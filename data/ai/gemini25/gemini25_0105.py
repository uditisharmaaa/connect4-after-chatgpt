import os
import random

# --- Constants ---
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2  # Set to 2 for submission
WIN_CONDITION = 4
CHECKERS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]

# --- Board Functions ---

def create_board(rows, cols):
    """
    Creates an empty Connect 4 board.
    """
    board = []
    for _ in range(rows):
        board.append([" "] * cols)
    return board

def print_board(board):
    """
    Prints the Connect 4 board with column labels.
    """
    os.system('clear')  # Clear screen before printing
    num_cols = len(board[0])

    # Print column labels (A, B, C, ...)
    print(" ", end="")
    for col_index in range(num_cols):
        print(f" {chr(ord('A') + col_index)} ", end="")
    print()

    # Print the board
    for row in board:
        print("+", end="")
        for _ in range(num_cols):
            print("---+", end="")
        print()
        print("|", end="")
        for cell in row:
            print(f" {cell} |", end="")
        print()
    
    # Print the bottom border
    print("+", end="")
    for _ in range(num_cols):
        print("---+", end="")
    print()

def get_column_from_input(prompt, num_cols):
    """
    Prompts the user for a column input and validates it.
    Returns the 0-indexed column number.
    """
    while True:
        user_input = input(prompt).strip().upper()
        if len(user_input) == 1 and 'A' <= user_input <= chr(ord('A') + num_cols - 1):
            return ord(user_input) - ord('A')
        else:
            print("Invalid input. Please enter a single uppercase letter corresponding to a column (e.g., A, B, C).")

def place_checker(board, col, checker):
    """
    Places a checker in the specified column.
    Returns True if successful, False if the column is full.
    """
    num_rows = len(board)
    for row in range(num_rows - 1, -1, -1):  # Start from bottom row
        if board[row][col] == " ":
            board[row][col] = checker
            return True
    return False # Column is full

# --- Win Condition Checks ---

def check_win(board, checker):
    """
    Checks if the current player has won horizontally, vertically, or diagonally.
    """
    num_rows = len(board)
    num_cols = len(board[0])

    # Check horizontal
    for r in range(num_rows):
        for c in range(num_cols - WIN_CONDITION + 1):
            if all(board[r][c + i] == checker for i in range(WIN_CONDITION)):
                return True

    # Check vertical
    for r in range(num_rows - WIN_CONDITION + 1):
        for c in range(num_cols):
            if all(board[r + i][c] == checker for i in range(WIN_CONDITION)):
                return True

    # Check diagonal (top-left to bottom-right)
    for r in range(num_rows - WIN_CONDITION + 1):
        for c in range(num_cols - WIN_CONDITION + 1):
            if all(board[r + i][c + i] == checker for i in range(WIN_CONDITION)):
                return True

    # Check diagonal (bottom-left to top-right)
    for r in range(WIN_CONDITION - 1, num_rows):
        for c in range(num_cols - WIN_CONDITION + 1):
            if all(board[r - i][c + i] == checker for i in range(WIN_CONDITION)):
                return True

    return False

def check_draw(board):
    """
    Checks if the board is full, resulting in a draw.
    """
    num_rows = len(board)
    num_cols = len(board[0])
    for r in range(num_rows):
        for c in range(num_cols):
            if board[r][c] == " ":
                return False  # Still empty spaces
    return True # Board is full

# --- Main Game Logic ---

def main():
    board = create_board(NUM_ROWS, NUM_COLS)
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    game_over = False
    winner = None

    while not game_over:
        print_board(board)
        
        current_checker = CHECKERS[current_player_index]
        print(f"Player {current_checker}, please enter a column:")

        chosen_col_index = get_column_from_input(f"Player {current_checker}, your turn: ", NUM_COLS)
        
        if place_checker(board, chosen_col_index, current_checker):
            if check_win(board, current_checker):
                print_board(board)
                winner = current_checker
                game_over = True
            elif check_draw(board):
                print_board(board)
                game_over = True
            else:
                # Switch to next player
                current_player_index = (current_player_index + 1) % NUM_PLAYERS
        else:
            print(f"Column {chr(ord('A') + chosen_col_index)} is full. Please choose another column.")
            # Player does not lose turn, will be asked again in the next loop iteration

    # Game over message
    if winner:
        print(f"Player {winner} won!")
    else:
        print("It's a draw!")

if __name__ == "__main__":
    main()
