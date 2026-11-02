import os
import random

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
PLAYERS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]  # Only take required players

def initialize_board():
    """Initialize an empty board with ROWS x COLS dimensions."""
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Print the board with column labels and borders."""
    # Print column headers (A, B, C, ...)
    header = "  " + "   ".join(chr(65 + i) for i in range(COLS)) + "  "
    print(header)
    
    # Print the top border
    top_border = "+" + ("---+" * COLS)
    print(top_border)
    
    # Print each row
    for row in board:
        row_str = "| " + " | ".join(row) + " |"
        print(row_str)
        print(top_border)

def is_valid_move(board, col):
    """Check if a move is valid (column exists and is not full)."""
    if col < 0 or col >= COLS:
        return False
    return board[0][col] == " "  # At least the top cell is empty

def place_checker(board, col, player):
    """Place the player's checker in the specified column."""
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = player
            return

def check_win(board, player):
    """Check if the player has won (4 in a row horizontally, vertically, or diagonally)."""
    directions = [
        (0, 1),  # Horizontal
        (1, 0),  # Vertical
        (1, 1),  # Diagonal down-right
        (1, -1),  # Diagonal down-left
    ]
    
    for row in range(ROWS):
        for col in range(COLS):
            if board[row][col] == player:
                for dr, dc in directions:
                    count = 1
                    for step in range(1, 4):
                        r = row + dr * step
                        c = col + dc * step
                        if 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == player:
                            count += 1
                        else:
                            break
                    if count == 4:
                        return True
    return False

def is_draw(board):
    """Check if the board is full (draw)."""
    return all(cell != " " for cell in board[0])

def clear_screen():
    """Clear the terminal screen."""
    os.system('clear' if os.name == 'posix' else 'cls')

def main():
    """Main function to run the Connect 4 game."""
    board = initialize_board()
    current_player = random.choice(PLAYERS)
    game_over = False
    
    clear_screen()
    print_board(board)
    
    while not game_over:
        print(f"Player {current_player}, please enter a column: ")
        user_input = input().strip().upper()
        
        # Validate input
        if len(user_input) != 1 or not user_input.isalpha():
            print("Invalid input. Please enter a single letter (A-G).")
            continue
        
        col = ord(user_input) - ord('A')
        if not is_valid_move(board, col):
            print("Invalid move. Column is full or does not exist.")
            continue
        
        # Place checker
        place_checker(board, col, current_player)
        clear_screen()
        print_board(board)
        
        # Check for win
        if check_win(board, current_player):
            print(f"Player {current_player} won!")
            game_over = True
        # Check for draw
        elif is_draw(board):
            print("Game is a draw!")
            game_over = True
        else:
            # Switch players
            current_player = PLAYERS[(PLAYERS.index(current_player) + 1) % NUM_PLAYERS]

if __name__ == "__main__":
    main()
