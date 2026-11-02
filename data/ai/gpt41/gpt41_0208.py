import random
import os
import sys

# Constants - customize as needed
ROWS = 6
COLS = 7
MAX_COLS = 26  # Maximum of 26 columns (A-Z)
PLAYERS = 2    # Between 2 and 5

CHECKERS = ['X', 'O', 'V', 'H', 'M']

def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    cols = len(board[0])
    header = "  " + "   ".join(chr(ord('A') + c) for c in range(cols))
    sep = "+" + "+".join(['---'] * cols) + "+"
    print(header)
    for row in board:
        print(sep)
        print("| " + " | ".join(row) + " |")
    print(sep)

def get_valid_columns(board):
    return [c for c in range(len(board[0])) if board[0][c] == " "]

def col_from_letter(letter):
    if len(letter) == 1 and letter.isalpha():
        col = ord(letter.upper()) - ord('A')
        return col
    return -1

def is_valid_input(input_str, board):
    if len(input_str) != 1:
        return False
    col = col_from_letter(input_str)
    if 0 <= col < len(board[0]):
        if board[0][col] == " ":
            return True
    return False

def drop_checker(board, col, checker):
    for r in range(len(board)-1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = checker
            return r, col
    return None, None  # Column is full

def check_winner(board, row, col, checker):
    # Directions:  [(dr, dc)]
    directions = [
        (0, 1),    # horizontal
        (1, 0),    # vertical
        (1, 1),    # diagonal /
        (1, -1)    # diagonal \
    ]
    for dr, dc in directions:
        count = 1  # count includes the checker we just put
        # Check one way
        r, c = row + dr, col + dc
        while 0 <= r < len(board) and 0 <= c < len(board[0]) and board[r][c] == checker:
            count += 1
            r += dr
            c += dc
        # Check the other way
        r, c = row - dr, col - dc
        while 0 <= r < len(board) and 0 <= c < len(board[0]) and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc
        if count >= 4:
            return True
    return False

def is_draw(board):
    return all(cell != " " for cell in board[0])

def main():
    # --- Set up variables ---
    rows = ROWS
    cols = COLS
    num_players = PLAYERS
    if cols > MAX_COLS or cols < 1 or rows < 1:
        print("Invalid board dimensions.")
        sys.exit(1)
    if num_players < 2 or num_players > 5:
        print("Invalid number of players.")
        sys.exit(1)
    player_checkers = CHECKERS[:num_players]
    player_names = [f"Player {checker}" for checker in player_checkers]

    board = create_board(rows, cols)
    
    # Randomly select first player
    cur_player = random.randint(0, num_players-1)
    
    # Initial print of board
    clear_screen()
    print_board(board)
    
    winner = None
    while True:
        # Player's turn
        checker = player_checkers[cur_player]
        name = player_names[cur_player]
        move = ""
        valid_move = False
        print(f"{name} ({checker}), please enter a column:", end=" ")
        while not valid_move:
            move = input().strip().upper()
            if move == '':
                print("Please enter a column letter (A-G). Try again:", end=" ")
                continue
            col = col_from_letter(move)
            if col == -1 or col < 0 or col >= cols:
                print("Invalid column letter. Try again:", end=" ")
                continue
            if board[0][col] != " ":
                print("Column is full. Try another column:", end=" ")
                continue
            valid_move = True
        
        # Place checker
        row, col = drop_checker(board, col, checker)
        clear_screen()
        print_board(board)
        
        # Check for win
        if check_winner(board, row, col, checker):
            print(f"{name} won!")
            break
        # Check draw
        if is_draw(board):
            print("The game is a draw!")
            break
        # Next player's turn
        cur_player = (cur_player + 1) % num_players

if __name__ == "__main__":
    main()
