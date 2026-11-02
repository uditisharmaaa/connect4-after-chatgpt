import os
import random

# Constants
ROWS = 6
COLUMNS = 7
MAX_PLAYERS = 5
PLAYER_TOKENS = ["X", "O", "V", "H", "M"]

def clear_screen():
    """Clears the terminal screen."""
    os.system('clear')

def create_board(rows, columns):
    """Creates the game board and initializes it with spaces."""
    return [[" " for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    """Prints the current state of the board."""
    clear_screen()
    column_labels = "   ".join(chr(65 + i) for i in range(len(board[0])))
    border = "+---" * len(board[0]) + "+"
    
    print(f"  {column_labels}")
    for row in board:
        print(border)
        print("| " + " | ".join(row) + " |")
    print(border)

def get_valid_columns(board):
    """Returns a list of columns that are not full."""
    return [i for i in range(len(board[0])) if board[0][i] == " "]

def get_column_index(input_col, num_columns):
    """Converts column input (A, B, etc.) to index if valid."""
    if len(input_col) == 1 and input_col.isalpha():
        index = ord(input_col.upper()) - 65
        if 0 <= index < num_columns:
            return index
    return None

def place_checker(board, col, token):
    """Places a checker in the specified column."""
    for row in range(len(board) - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = token
            return row, col
    return None

def check_for_win(board, row, col, token):
    """Checks if the last move results in a win."""
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]  # Horizontal, Vertical, Diagonal1, Diagonal2
    
    for dr, dc in directions:
        count = 1
        for step in [-1, 1]:  # Check both directions
            r, c = row, col
            while True:
                r += dr * step
                c += dc * step
                if 0 <= r < len(board) and 0 <= c < len(board[0]) and board[r][c] == token:
                    count += 1
                else:
                    break
        if count >= 4:
            return True
    return False

def is_draw(board):
    """Checks if the game is a draw."""
    return all(cell != " " for row in board for cell in row)

def main():
    # Initialize game variables
    board = create_board(ROWS, COLUMNS)
    num_players = 2  # Fixed for the assignment
    players = PLAYER_TOKENS[:num_players]
    current_player = random.choice(players)
    
    print_board(board)
    print(f"Player {current_player} starts!")

    while True:
        # Get and validate column input
        valid_columns = get_valid_columns(board)
        if not valid_columns:
            print("The game is a draw!")
            break
        
        while True:
            player_input = input(f"Player {current_player}, please enter a column: ").strip()
            col_index = get_column_index(player_input, COLUMNS)
            if col_index is not None and col_index in valid_columns:
                break
            print("Invalid input. Please try again.")

        # Place the checker
        row, col = place_checker(board, col_index, current_player)
        print_board(board)

        # Check for win or draw
        if check_for_win(board, row, col, current_player):
            print(f"Player {current_player} won!")
            break
        elif is_draw(board):
            print("The game is a draw!")
            break

        # Switch player
        current_idx = players.index(current_player)
        current_player = players[(current_idx + 1) % num_players]

if __name__ == "__main__":
    main()
