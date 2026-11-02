import os
import random

# Constants for configuration
ROWS = 6
COLUMNS = 7
MAX_COLUMNS = 26
NUM_PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def clear_screen():
    os.system('clear')

def create_board(rows, columns):
    return [[" " for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    
    # Column labels
    column_labels = "   ".join(chr(65 + col) for col in range(len(board[0])))
    print(f"  {column_labels}")
    
    # Horizontal delimiter
    delimiter = "+---" * len(board[0]) + "+"
    
    # Print rows
    for row in board:
        print(delimiter)
        print("| " + " | ".join(row) + " |")
    print(delimiter)

def is_valid_column(column_label, board):
    if len(column_label) != 1 or not column_label.isalpha():
        return False
    column = ord(column_label.upper()) - 65
    return 0 <= column < len(board[0]) and board[0][column] == " "

def get_empty_row(column, board):
    for row in range(len(board) - 1, -1, -1):
        if board[row][column] == " ":
            return row
    return None

def drop_checker(board, column, checker):
    row = get_empty_row(column, board)
    if row is not None:
        board[row][column] = checker
        return True
    return False

def is_winning_move(board, row, col, checker):
    # Horizontal, vertical, diagonal checks
    directions = [
        [(0, 1), (0, -1)],       # Horizontal
        [(-1, 0), (1, 0)],       # Vertical
        [(-1, -1), (1, 1)],      # Diagonal /
        [(-1, 1), (1, -1)]       # Diagonal \
    ]
    
    for direction in directions:
        count = 1
        for dr, dc in direction:
            r, c = row, col
            while True:
                r += dr
                c += dc
                if 0 <= r < len(board) and 0 <= c < len(board[0]) and board[r][c] == checker:
                    count += 1
                else:
                    break
            if count >= 4:
                return True
    return False

def is_draw(board):
    return all(board[0][col] != " " for col in range(len(board[0])))

def main():
    # Generate board
    board = create_board(ROWS, COLUMNS)
    
    # Player configurations
    players = CHECKERS[:NUM_PLAYERS]
    current_player = random.randint(0, NUM_PLAYERS - 1)
    
    # Start game
    print_board(board)
    
    while True:
        player_checker = players[current_player]
        print(f"Player {player_checker}, it's your turn!")
        
        column_label = input("Please enter a column: ").strip().upper()
        
        if not is_valid_column(column_label, board):
            print("Invalid input. Please try again.")
            continue
        
        column = ord(column_label) - 65
        drop_checker(board, column, player_checker)
        
        print_board(board)
        
        # Check for win
        row = get_empty_row(column, board) + 1  # Last row where checker was placed
        if is_winning_move(board, row, column, player_checker):
            print(f"Player {player_checker} won!")
            break
        
        # Check for draw
        if is_draw(board):
            print("It's a draw!")
            break
        
        # Switch to next player
        current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
