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
    board = [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]
    return board

def print_board(board):
    clear_screen()
    # Print column headers
    header = "  "
    for i in range(COLUMNS):
        header += chr(ord('A') + i) + "   "
    print(header)
    
    # Print board rows
    for r in range(ROWS):
        print("+---" * COLUMNS + "+")
        row_str = "|"
        for c in range(COLUMNS):
            row_str += " " + board[r][c] + " |"
        print(row_str)
    print("+---" * COLUMNS + "+")

def is_valid_column(col_char):
    if len(col_char) != 1:
        return False
    if not ('A' <= col_char <= chr(ord('A') + COLUMNS -1)):
        return False
    return True

def column_to_index(col_char):
    return ord(col_char) - ord('A')

def place_checker(board, col_index, checker):
    # Start from bottom row and go up
    for row in range(ROWS-1, -1, -1):
        if board[row][col_index] == " ":
            board[row][col_index] = checker
            return row, col_index
    return None  # Column full

def check_winner(board, checker, row, col):
    # Check horizontal, vertical, and two diagonal directions
    directions = [
        (0,1),  # horizontal right
        (1,0),  # vertical down
        (1,1),  # diagonal down-right
        (1,-1)  # diagonal down-left
    ]
    for dr, dc in directions:
        count = 1
        # Check forward direction
        r, c = row+dr, col+dc
        while 0 <= r < ROWS and 0 <= c < COLUMNS and board[r][c] == checker:
            count += 1
            r += dr
            c += dc
        # Check backward direction
        r, c = row-dr, col-dc
        while 0 <= r < ROWS and 0 <= c < COLUMNS and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc
        if count >= WIN_COUNT:
            return True
    return False

def board_full(board):
    for c in range(COLUMNS):
        if board[0][c] == " ":
            return False
    return True

def main():
    board = create_board()
    players = CHECKERS[:PLAYERS]
    # Choose random starting player index
    current_player_index = random.randint(0, PLAYERS - 1)
    
    print_board(board)
    
    while True:
        current_checker = players[current_player_index]
        print(f"Player {current_checker}, please enter a column:")
        user_input = input().strip().upper()
        
        if not is_valid_column(user_input):
            # Invalid input, ask again without losing turn
            continue
        
        col = column_to_index(user_input)
        pos = place_checker(board, col, current_checker)
        if pos is None:
            # Column full, player loses turn, move to next player
            current_player_index = (current_player_index + 1) % PLAYERS
            print_board(board)
            continue
        
        print_board(board)
        
        row, col = pos
        if check_winner(board, current_checker, row, col):
            print(f"Player {current_checker} won!")
            break
        if board_full(board):
            print("The game is a draw!")
            break
        
        current_player_index = (current_player_index + 1) % PLAYERS

if __name__ == "__main__":
    main()
