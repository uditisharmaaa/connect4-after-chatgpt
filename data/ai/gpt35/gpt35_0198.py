import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]
WIN_COUNT = 4

def clear_screen():
    os.system('clear')

def create_board():
    return [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    clear_screen()
    # Print column headers
    header = "  "
    for i in range(COLUMNS):
        header += "  " + chr(ord('A') + i) + " "
    print(header)
    
    # Print the board
    for row in range(ROWS):
        line = "+"
        for _ in range(COLUMNS):
            line += "---+"
        print(line)
        
        row_line = "|"
        for col in range(COLUMNS):
            row_line += " " + board[row][col] + " |"
        print(row_line)
    print(line)

def is_valid_column(col_char):
    if len(col_char) != 1:
        return False
    if not ('A' <= col_char <= chr(ord('A') + COLUMNS -1)):
        return False
    return True

def get_column_index(col_char):
    return ord(col_char) - ord('A')

def column_full(board, col):
    return board[0][col] != " "

def place_checker(board, col, checker):
    # Place checker in the lowest empty cell in column col
    for row in range(ROWS-1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return row, col
    return None, None  # Column full, no place to put

def check_win(board, checker, row, col):
    # Check horizontal, vertical, diagonal wins
    # Directions: (delta_row, delta_col)
    directions = [
        (0,1),  # horizontal
        (1,0),  # vertical
        (1,1),  # diagonal down-right
        (1,-1)  # diagonal down-left
    ]
    
    for dr, dc in directions:
        count = 1
        
        # Check one direction
        r, c = row + dr, col + dc
        while 0 <= r < ROWS and 0 <= c < COLUMNS and board[r][c] == checker:
            count += 1
            r += dr
            c += dc
        
        # Check opposite direction
        r, c = row - dr, col - dc
        while 0 <= r < ROWS and 0 <= c < COLUMNS and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc
        
        if count >= WIN_COUNT:
            return True
    return False

def check_draw(board):
    # If no empty space in top row, draw
    for col in range(COLUMNS):
        if board[0][col] == " ":
            return False
    return True

def main():
    board = create_board()
    players_checkers = CHECKERS[:PLAYERS]
    current_player_idx = random.randint(0, PLAYERS - 1)
    
    print_board(board)
    while True:
        checker = players_checkers[current_player_idx]
        prompt = f"Player {checker}, please enter a column: "
        col_char = input(prompt).strip().upper()
        
        # Validate input (repeat until valid)
        while True:
            if not is_valid_column(col_char):
                col_char = input(f"Invalid input. Please enter a column (A-{chr(ord('A')+COLUMNS-1)}): ").strip().upper()
                continue
            col_idx = get_column_index(col_char)
            if col_idx < 0 or col_idx >= COLUMNS:
                col_char = input(f"Invalid input. Please enter a column (A-{chr(ord('A')+COLUMNS-1)}): ").strip().upper()
                continue
            break
        
        # Check if column full
        if column_full(board, col_idx):
            # Player loses turn
            print(f"Column {col_char} is full. Player {checker} loses the turn.")
            input("Press Enter to continue...")
            current_player_idx = (current_player_idx + 1) % PLAYERS
            print_board(board)
            continue
        
        # Place checker
        row_placed, col_placed = place_checker(board, col_idx, checker)
        print_board(board)
        
        # Check win
        if check_win(board, checker, row_placed, col_placed):
            print(f"Player {checker} won!")
            break
        
        # Check draw
        if check_draw(board):
            print("The game is a draw!")
            break
        
        # Next player
        current_player_idx = (current_player_idx + 1) % PLAYERS

if __name__ == "__main__":
    main()
