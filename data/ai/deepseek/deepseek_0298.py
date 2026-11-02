import os
import random

# Constants
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2

def create_board(rows, cols):
    """Create and initialize a Connect 4 board with given dimensions."""
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """Print the Connect 4 board with column labels."""
    # Clear the screen before printing the updated board
    os.system('clear')
    
    # Print column headers (A, B, C, ...)
    header = "  " + "   ".join([chr(ord('A') + i) for i in range(len(board[0]))])
    print(header)
    
    # Print each row of the board
    for row in board:
        print("+---" * len(row) + "+")
        print("| " + " | ".join(row) + " |")
    
    print("+---" * len(row) + "+")

def is_valid_column(col, num_cols):
    """Check if the column input is valid (within bounds and a letter)."""
    if len(col) != 1:
        return False
    char = col.upper()
    return 'A' <= char <= chr(ord('A') + num_cols - 1)

def column_to_index(col):
    """Convert a column letter (A, B, ...) to a zero-based index."""
    return ord(col.upper()) - ord('A')

def get_next_open_row(board, col_idx):
    """Find the next available row in a column for placing a checker."""
    for row_idx in range(len(board) - 1, -1, -1):
        if board[row_idx][col_idx] == " ":
            return row_idx
    return -1  # Column is full

def place_checker(board, row, col, player):
    """Place the player's checker on the board at the specified position."""
    board[row][col] = player

def check_win(board, player):
    """Check if the current player has won the game."""
    # Directions: horizontal, vertical, diagonal down, diagonal up
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
    
    for row in range(len(board)):
        for col in range(len(board[0])):
            if board[row][col] != player:
                continue
            for dr, dc in directions:
                count = 1
                for i in range(1, 4):
                    r, c = row + dr * i, col + dc * i
                    if (0 <= r < len(board) and 0 <= c < len(board[0]) and
                        board[r][c] == player):
                        count += 1
                    else:
                        break
                if count >= 4:
                    return True
    return False

def is_draw(board):
    """Check if the game is a draw (no more valid moves)."""
    for row in board:
        if " " in row:
            return False
    return True

def get_player_checkers(num_players):
    """Return a list of player checkers based on the number of players."""
    checkers = ["X", "O", "V", "H", "M"]
    return checkers[:num_players]

def main():
    """Main function to run the Connect 4 game."""
    board = create_board(NUM_ROWS, NUM_COLS)
    players = get_player_checkers(NUM_PLAYERS)
    current_player = random.choice(players)
    
    print("Welcome to Connect 4!")
    print(f"Player {current_player} goes first.")
    
    while True:
        print_board(board)
        print(f"Player {current_player}, please enter a column: ")
        col_input = input().strip()
        
        if not is_valid_column(col_input, NUM_COLS):
            print("Invalid input. Please enter a valid column letter (A-G).")
            continue
        
        col_idx = column_to_index(col_input)
        row_idx = get_next_open_row(board, col_idx)
        
        if row_idx == -1:
            print("Column is full. Please choose another column.")
            continue
        
        place_checker(board, row_idx, col_idx, current_player)
        
        if check_win(board, current_player):
            print_board(board)
            print(f"Player {current_player} won!")
            break
        
        if is_draw(board):
            print_board(board)
            print("Game is a draw!")
            break
        
        # Switch to the next player
        current_player = players[(players.index(current_player) + 1) % NUM_PLAYERS]

if __name__ == "__main__":
    main()
