import os
import random
import string

# --- Constants ---
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2
PLAYER_TOKENS = ["X", "O", "V", "H", "M"]
WIN_CONDITION = 4  # Number of checkers in a row to win

# --- Global Variables ---
board = []
current_player_index = 0
players = []

# --- Functions ---

def create_board():
    """
    Initializes the game board with empty spaces.
    """
    global board
    board = [[" " for _ in range(NUM_COLS)] for _ in range(NUM_ROWS)]

def print_board():
    """
    Prints the current state of the game board.
    """
    os.system('clear')  # Clear the screen

    # Print column labels (A, B, C, ...)
    print("  " + "   ".join(string.ascii_uppercase[:NUM_COLS]))

    # Print board rows
    for r in range(NUM_ROWS):
        print("+---" * NUM_COLS + "+")
        row_str = "|"
        for c in range(NUM_COLS):
            row_str += f" {board[r][c]} |"
        print(row_str)
    print("+---" * NUM_COLS + "+")

def get_column_input():
    """
    Prompts the current player for a column input and validates it.
    Returns the 0-indexed column number if valid, otherwise continues prompting.
    """
    while True:
        player_token = players[current_player_index]
        column_char = input(f"Player {player_token}, please enter a column: ").upper()

        if not column_char:
            print("Invalid input. Please enter a column letter.")
            continue

        if len(column_char) != 1 or column_char not in string.ascii_uppercase[:NUM_COLS]:
            print("Invalid input. Please enter a single uppercase letter corresponding to a column.")
            continue

        col_index = ord(column_char) - ord('A')

        if not (0 <= col_index < NUM_COLS):
            print("Invalid column. Column is out of board range.")
            continue

        # Check if the column is full
        if board[0][col_index] != " ":
            print("That column is full. Please choose another column.")
            continue

        return col_index

def drop_checker(col_index):
    """
    Drops the current player's checker into the specified column.
    Returns True if the checker was placed, False if the column is full.
    """
    for r in range(NUM_ROWS - 1, -1, -1):
        if board[r][col_index] == " ":
            board[r][col_index] = players[current_player_index]
            return True
    return False # Should not be reached if column full check is done earlier

def check_win(row, col):
    """
    Checks if the last placed checker at (row, col) results in a win.
    """
    checker = board[row][col]

    # Check horizontal
    count = 0
    for c in range(NUM_COLS):
        if board[row][c] == checker:
            count += 1
        else:
            count = 0
        if count >= WIN_CONDITION:
            return True

    # Check vertical
    count = 0
    for r in range(NUM_ROWS):
        if board[r][col] == checker:
            count += 1
        else:
            count = 0
        if count >= WIN_CONDITION:
            return True

    # Check diagonal (top-left to bottom-right)
    count = 0
    # Start from the leftmost possible point for this diagonal
    start_row = row - min(row, col)
    start_col = col - min(row, col)
    for i in range(min(NUM_ROWS - start_row, NUM_COLS - start_col)):
        if board[start_row + i][start_col + i] == checker:
            count += 1
        else:
            count = 0
        if count >= WIN_CONDITION:
            return True

    # Check diagonal (top-right to bottom-left)
    count = 0
    # Start from the rightmost possible point for this diagonal
    start_row = row - min(row, NUM_COLS - 1 - col)
    start_col = col + min(row, NUM_COLS - 1 - col)
    for i in range(min(NUM_ROWS - start_row, start_col + 1)):
        if board[start_row + i][start_col - i] == checker:
            count += 1
        else:
            count = 0
        if count >= WIN_CONDITION:
            return True

    return False

def check_draw():
    """
    Checks if the board is completely full, indicating a draw.
    """
    for r in range(NUM_ROWS):
        for c in range(NUM_COLS):
            if board[r][c] == " ":
                return False  # Found an empty space, not a draw yet
    return True # No empty spaces found, it's a draw

def setup_players():
    """
    Initializes the list of player tokens based on NUM_PLAYERS.
    """
    global players
    players = PLAYER_TOKENS[:NUM_PLAYERS]

def switch_player():
    """
    Switches the current player to the next in line.
    """
    global current_player_index
    current_player_index = (current_player_index + 1) % NUM_PLAYERS

def main():
    global current_player_index

    setup_players()
    create_board()

    # Randomly choose the first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)

    game_over = False
    winning_player = None

    while not game_over:
        print_board()

        col_index = get_column_input()

        # Find the actual row where the checker lands
        landed_row = -1
        for r in range(NUM_ROWS - 1, -1, -1):
            if board[r][col_index] == " ":
                landed_row = r
                break
        
        # This condition should always be true due to get_column_input validation
        if landed_row != -1:
            drop_checker(col_index) # Drop the checker
        else:
            # This case should ideally not be reached if get_column_input is robust
            # and checks for full columns. If it does, the player's turn is essentially lost.
            # For robustness, we'll just switch players if somehow a full column was selected.
            print("Error: Column was full after input. Losing turn.")
            switch_player()
            continue
            
        print_board() # Print board after checker drop

        # Check for win
        if check_win(landed_row, col_index):
            winning_player = players[current_player_index]
            game_over = True
            print(f"Player {winning_player} won!")
            break # Exit the game loop

        # Check for draw
        if check_draw():
            game_over = True
            print("The game is a draw!")
            break # Exit the game loop

        switch_player()

if __name__ == "__main__":
    main()
