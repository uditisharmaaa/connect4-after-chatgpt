import os
import random

# Constants
ROWS = 6
COLS = 7
MAX_PLAYERS = 5
PLAYER_CHECKERS = ["X", "O", "V", "H", "M"]

def clear_screen():
    """Clears the console screen."""
    os.system('clear')

def create_board(rows=ROWS, cols=COLS):
    """Creates and returns an empty game board."""
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """Prints the game board."""
    clear_screen()
    column_labels = "   ".join(chr(65 + i) for i in range(len(board[0])))
    print("  " + column_labels)
    print("+---" * len(board[0]) + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * len(board[0]) + "+")

def is_valid_column(board, col):
    """Checks if the column is valid and has space for a move."""
    return 0 <= col < len(board[0]) and board[0][col] == " "

def get_column_choice(board):
    """Prompts the player for a valid column and returns the column index."""
    while True:
        try:
            column_choice = input("Please enter a column (A-G): ").upper()
            col_index = ord(column_choice) - 65
            if is_valid_column(board, col_index):
                return col_index
            else:
                print("Invalid column. Try again.")
        except (ValueError, IndexError):
            print("Invalid input. Please enter a valid column label.")

def place_checker(board, col, player_checker):
    """Places the player's checker in the chosen column."""
    for row in reversed(board):
        if row[col] == " ":
            row[col] = player_checker
            break

def check_win(board, row, col, checker):
    """Checks for a win starting from the position (row, col)."""
    # Check directions: horizontal, vertical, diagonal /
    directions = [
        ((0, 1), (0, -1)),  # Horizontal
        ((1, 0), (-1, 0)),  # Vertical
        ((1, 1), (-1, -1)), # Diagonal \
        ((1, -1), (-1, 1))  # Diagonal /
    ]
    
    for direction in directions:
        count = 1
        for drow, dcol in direction:
            r, c = row, col
            while 0 <= r + drow < ROWS and 0 <= c + dcol < COLS:
                r += drow
                c += dcol
                if board[r][c] == checker:
                    count += 1
                else:
                    break
            if count >= 4:
                return True
    return False

def is_draw(board):
    """Checks if the game is a draw."""
    return all(cell != " " for cell in board[0])

def main():
    """Main function to run the game."""
    # Configuration
    board = create_board()
    num_players = 2  # Fixed to 2 players for this submission
    player_checkers = PLAYER_CHECKERS[:num_players]

    # Randomly select the starting player
    current_player = random.randint(0, num_players - 1)

    # Game loop
    while True:
        print_board(board)
        print(f"Player {player_checkers[current_player]}'s turn.")
        
        # Get a valid column choice from the player
        col = get_column_choice(board)
        
        # Place the player's checker
        place_checker(board, col, player_checkers[current_player])
        
        # Check if the player has won
        for row_idx in range(ROWS):
            if board[row_idx][col] == player_checkers[current_player]:
                if check_win(board, row_idx, col, player_checkers[current_player]):
                    print_board(board)
                    print(f"Player {player_checkers[current_player]} won!")
                    return
        
        # Check if the game is a draw
        if is_draw(board):
            print_board(board)
            print("The game is a draw!")
            return
        
        # Switch to the next player
        current_player = (current_player + 1) % num_players

if __name__ == "__main__":
    main()
