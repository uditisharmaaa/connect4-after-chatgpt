import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = 2
PLAYER_SYMBOLS = ["X", "O", "V", "H", "M"]

def create_board(rows, cols):
    """Create and initialize the game board with empty spaces."""
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """Print the current game board with column labels."""
    # Print column letters
    header = "  "
    for col in range(len(board[0])):
        header += f" {chr(col + 65)}  "
    print(header)
    
    # Print each row with separators
    for row in board:
        print("+" + "---+" * len(row))
        print("|" + "|".join(f" {cell} " for cell in row) + "|")
    
    # Print bottom separator
    print("+" + "---+" * len(board[0]))

def is_valid_column(col_letter, cols):
    """Check if the column letter is valid."""
    if len(col_letter) != 1:
        return False
    col = ord(col_letter.upper()) - ord('A')
    return 0 <= col < cols

def get_column_index(col_letter):
    """Convert column letter to 0-based index."""
    return ord(col_letter.upper()) - ord('A')

def drop_checker(board, col, player_symbol):
    """Place the checker in the lowest available row of the column."""
    for row in range(len(board) - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = player_symbol
            return row  # Return the row where the checker was placed
    return None  # Column is full

def check_win(board, row, col, player_symbol):
    """Check if the last move resulted in a win."""
    # Directions: (dr, dc) for row, col changes (horizontal, vertical, diagonals)
    directions = [
        (0, 1),   # horizontal
        (1, 0),    # vertical
        (1, 1),    # diagonal down-right
        (1, -1)    # diagonal down-left
    ]
    
    for dr, dc in directions:
        count = 1  # Include the current checker
        
        # Check in the positive direction
        r, c = row + dr, col + dc
        while 0 <= r < len(board) and 0 <= c < len(board[0]) and board[r][c] == player_symbol:
            count += 1
            r += dr
            c += dc
        
        # Check in the negative direction
        r, c = row - dr, col - dc
        while 0 <= r < len(board) and 0 <= c < len(board[0]) and board[r][c] == player_symbol:
            count += 1
            r -= dr
            c -= dc
        
        if count >= 4:
            return True
    return False

def is_board_full(board):
    """Check if the board is full (draw)."""
    return all(cell != " " for row in board for cell in row)

def clear_screen():
    """Clear the terminal screen."""
    os.system('clear' if os.name == 'posix' else 'cls')

def main():
    """Main function to run the Connect 4 game."""
    board = create_board(ROWS, COLS)
    current_player = random.randint(0, PLAYERS - 1)
    symbols = PLAYER_SYMBOLS[:PLAYERS]
    
    clear_screen()
    print(f"Player {symbols[current_player]} starts first!")
    print_board(board)
    
    while True:
        player_symbol = symbols[current_player]
        while True:
            col_letter = input(f"Player {player_symbol}, please enter a column: ").strip().upper()
            if not is_valid_column(col_letter, COLS):
                print("Invalid input. Please enter a valid column letter (A-G).")
                continue
            col = get_column_index(col_letter)
            row = drop_checker(board, col, player_symbol)
            if row is None:
                print("Column is full. Try another column.")
                continue
            break
        
        clear_screen()
        print_board(board)
        
        if check_win(board, row, col, player_symbol):
            print(f"Player {player_symbol} won!")
            break
        
        if is_board_full(board):
            print("Game ended in a draw!")
            break
        
        current_player = (current_player + 1) % PLAYERS

if __name__ == "__main__":
    main()
