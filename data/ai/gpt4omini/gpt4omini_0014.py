import os
import random

# Constants for board dimensions and player symbols
ROWS = 6
COLS = 7
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']

# Initialize the board
def create_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

# Print the board
def print_board(board):
    os.system('clear')  # Clear the console screen
    print("  " + "   ".join(chr(65 + i) for i in range(COLS)))
    print("+---" + "---+" * COLS)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" + "---+" * COLS)

# Get the index of the column from the user's input
def get_column_index(column):
    if 'A' <= column <= chr(65 + COLS - 1):
        return ord(column) - 65  # Convert letter to column index
    return None

# Place the player's checker in the specified column
def place_checker(board, column_index, player_symbol):
    for row in reversed(board):  # Start from the bottom row
        if row[column_index] == ' ':
            row[column_index] = player_symbol
            return True
    return False

# Check for a win in the current board
def check_win(board, player_symbol):
    # Check horizontal, vertical, and diagonal
    return (check_lines(board, player_symbol) or
            check_lines(zip(*board), player_symbol) or  # Vertical check
            check_diagonals(board, player_symbol))

# Check for four in a line in the given lines (rows or columns)
def check_lines(lines, player_symbol):
    for line in lines:
        count = 0
        for cell in line:
            count = count + 1 if cell == player_symbol else 0
            if count >= 4:
                return True
    return False

# Check for diagonal wins
def check_diagonals(board, player_symbol):
    for r in range(ROWS):
        for c in range(COLS):
            # Check for downward diagonals
            if r <= ROWS - 4 and c <= COLS - 4:
                if all(board[r + i][c + i] == player_symbol for i in range(4)):
                    return True
            # Check for upward diagonals
            if r >= 3 and c <= COLS - 4:
                if all(board[r - i][c + i] == player_symbol for i in range(4)):
                    return True
    return False

# Check if the board is full
def is_draw(board):
    return all(cell != ' ' for row in board for cell in row)

# Main game loop
def main():
    board = create_board()
    print_board(board)
    
    current_player = random.randint(0, 1)  # Randomly choose the first player
    while True:
        player_symbol = PLAYER_SYMBOLS[current_player]
        column_choice = input(f"Player {player_symbol}, please enter a column: ").upper()
        
        column_index = get_column_index(column_choice)
        if column_index is None:
            print("Invalid column choice. Please enter a letter from A to G.")
            continue
        
        if not place_checker(board, column_index, player_symbol):
            print("Column is full. Please choose another column.")
            continue

        print_board(board)

        if check_win(board, player_symbol):
            print(f"Player {player_symbol} won!")
            break
        
        if is_draw(board):
            print("The game is a draw!")
            break
        
        current_player = (current_player + 1) % len(PLAYER_SYMBOLS)

if __name__ == "__main__":
    main()
