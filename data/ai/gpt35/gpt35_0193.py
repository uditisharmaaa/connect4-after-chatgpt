import os
import random

# Constants
ROWS = 6
COLS = 7
MAX_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]
WIN_LENGTH = 4

def clear_screen():
    os.system('clear')

def create_board():
    board = [[" " for _ in range(COLS)] for _ in range(ROWS)]
    return board

def print_board(board):
    clear_screen()
    # Print column headers
    headers = [chr(ord('A') + i) for i in range(COLS)]
    print("  " + "   ".join(headers))
    # Print board rows
    for row in board:
        print("+---" * COLS + "+")
        print("| " + " | ".join(row) + " |")
    print("+---" * COLS + "+")

def is_valid_column(col_char):
    if len(col_char) != 1:
        return False
    col_char = col_char.upper()
    if col_char < 'A' or col_char >= chr(ord('A') + COLS):
        return False
    return True

def get_column_index(col_char):
    return ord(col_char.upper()) - ord('A')

def place_checker(board, col, checker):
    # place checker in lowest available spot in column col
    for row in reversed(range(ROWS)):
        if board[row][col] == " ":
            board[row][col] = checker
            return row, col
    # column full
    return None

def check_direction(board, start_row, start_col, delta_row, delta_col, checker):
    count = 0
    row, col = start_row, start_col
    while 0 <= row < ROWS and 0 <= col < COLS and board[row][col] == checker:
        count += 1
        row += delta_row
        col += delta_col
    return count

def check_win(board, checker):
    for row in range(ROWS):
        for col in range(COLS):
            if board[row][col] == checker:
                # Check horizontal right
                if check_direction(board, row, col, 0, 1, checker) >= WIN_LENGTH:
                    return True
                # Check vertical down
                if check_direction(board, row, col, 1, 0, checker) >= WIN_LENGTH:
                    return True
                # Check diagonal down-right
                if check_direction(board, row, col, 1, 1, checker) >= WIN_LENGTH:
                    return True
                # Check diagonal down-left
                if check_direction(board, row, col, 1, -1, checker) >= WIN_LENGTH:
                    return True
    return False

def is_draw(board):
    for row in range(ROWS):
        for col in range(COLS):
            if board[row][col] == " ":
                return False
    return True

def main():
    board = create_board()
    players = CHECKERS[:MAX_PLAYERS]
    current_player_index = random.randint(0, MAX_PLAYERS - 1)
    
    print_board(board)
    
    while True:
        checker = players[current_player_index]
        print(f"Player {checker}, please enter a column:")
        move_input = input().strip()
        
        if not is_valid_column(move_input):
            print("Invalid input. Please enter a valid column letter.")
            continue
        
        col = get_column_index(move_input)
        placed = place_checker(board, col, checker)
        
        if placed is None:
            # Column full - lose the turn
            print(f"Column {move_input.upper()} is full. Turn lost.")
            current_player_index = (current_player_index + 1) % MAX_PLAYERS
            print_board(board)
            continue
        
        print_board(board)
        
        # Check for win
        if check_win(board, checker):
            print(f"Player {checker} won!")
            break
        
        # Check for draw
        if is_draw(board):
            print("Game is a draw!")
            break
        
        # Next player
        current_player_index = (current_player_index + 1) % MAX_PLAYERS


if __name__ == "__main__":
    main()
