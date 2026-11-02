import os
import random

# Constants
ROWS = 6
COLUMNS = 7
MAX_PLAYERS = 5
MIN_PLAYERS = 2
PLAYERS = 2  # For submission, set to 2 players

CHECKERS = ["X", "O", "V", "H", "M"]  # Max 5 players supported
WIN_COUNT = 4

def clear_screen():
    os.system('clear')

def create_board(rows, columns):
    return [[" " for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    # Print column labels
    labels = [chr(ord('A') + i) for i in range(len(board[0]))]
    print("  " + "   ".join(labels))
    separator = "+" + "---+" * len(board[0])
    for row in board:
        print(separator)
        row_str = "| " + " | ".join(row) + " |"
        print(row_str)
    print(separator)

def is_valid_column(col, columns):
    if len(col) != 1:
        return False
    col = col.upper()
    return 'A' <= col < chr(ord('A') + columns)

def column_index(col):
    return ord(col.upper()) - ord('A')

def can_place(board, col_idx):
    return board[0][col_idx] == " "

def place_checker(board, col_idx, checker):
    # Place checker in lowest empty spot of the column
    for row in range(len(board)-1, -1, -1):
        if board[row][col_idx] == " ":
            board[row][col_idx] = checker
            return row, col_idx
    return None  # Should not happen if checked before

def check_win(board, checker, row, col):
    # Check all directions for 4 in a row
    
    directions = [
        (0, 1),   # horizontal right
        (1, 0),   # vertical down
        (1, 1),   # diagonal down-right
        (1, -1),  # diagonal down-left
    ]
    
    rows = len(board)
    cols = len(board[0])
    
    for dr, dc in directions:
        count = 1
        
        # Check forward direction
        r, c = row + dr, col + dc
        while 0 <= r < rows and 0 <= c < cols and board[r][c] == checker:
            count += 1
            r += dr
            c += dc
            
        # Check backward direction
        r, c = row - dr, col - dc
        while 0 <= r < rows and 0 <= c < cols and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc
        
        if count >= WIN_COUNT:
            return True
    return False

def board_full(board):
    # If top row has no empty spaces, board is full
    return all(cell != " " for cell in board[0])

def next_player(current):
    # Cycle through players in order
    return (current + 1) % PLAYERS

def main():
    if PLAYERS < MIN_PLAYERS or PLAYERS > MAX_PLAYERS:
        print("Number of players must be between 2 and 5.")
        return
    
    board = create_board(ROWS, COLUMNS)
    players_checkers = CHECKERS[:PLAYERS]
    
    # Random first player
    current_player = random.randint(0, PLAYERS -1)
    
    # Print initial board
    print_board(board)
    
    while True:
        checker = players_checkers[current_player]
        print(f"Player {checker}, please enter a column:")
        
        valid_input = False
        while not valid_input:
            user_input = input().strip().upper()
            
            if not is_valid_column(user_input, COLUMNS):
                print("Invalid input, please enter a valid column letter:")
                continue
            
            col_idx = column_index(user_input)
            
            if not can_place(board, col_idx):
                # Turn is lost if column full
                print(f"Column {user_input} is full. You lose your turn.")
                valid_input = True  # Accept to lose turn
                col_idx = None
            else:
                valid_input = True
        
        if col_idx is not None:
            row, col = place_checker(board, col_idx, checker)
            print_board(board)
            
            if check_win(board, checker, row, col):
                print(f"Player {checker} won!")
                break
            
            if board_full(board):
                print("The game is a draw.")
                break
        else:
            # Column full, turn lost, print updated board anyway
            print_board(board)
        
        # Next player's turn
        current_player = next_player(current_player)

if __name__ == "__main__":
    main()
