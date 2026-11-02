import os
import random

# Constants
ROWS = 6
COLUMNS = 7
WIN_CONDITION = 4
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]  # Only first PLAYERS elements will be used

def clear_screen():
    os.system('clear')

def create_board():
    return [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    clear_screen()
    # Print column headers
    headers = [chr(ord('A') + i) for i in range(COLUMNS)]
    print("  " + "   ".join(headers))
    # Print rows with separator lines
    line_sep = "+" + "---+" * COLUMNS
    for row in board:
        print(line_sep)
        print("| " + " | ".join(row) + " |")
    print(line_sep)

def is_valid_column_input(s):
    if len(s) != 1:
        return False
    if not ('A' <= s <= chr(ord('A') + COLUMNS - 1)):
        return False
    return True

def get_column_index(column_letter):
    return ord(column_letter) - ord('A')

def place_checker(board, col_idx, checker):
    # Place checker in the lowest empty row in column col_idx
    for row_idx in range(ROWS - 1, -1, -1):
        if board[row_idx][col_idx] == " ":
            board[row_idx][col_idx] = checker
            return row_idx, col_idx
    return None  # Column full

def check_win(board, row, col, checker):
    # Directions: (dx, dy) pairs - horizontal, vertical, diagonal /
    directions = [
        (0, 1),   # horizontal
        (1, 0),   # vertical
        (1, 1),   # diagonal \
        (1, -1)   # diagonal /
    ]
    for dx, dy in directions:
        count = 1
        # Check forward direction
        for step in range(1, WIN_CONDITION):
            r = row + dx * step
            c = col + dy * step
            if 0 <= r < ROWS and 0 <= c < COLUMNS and board[r][c] == checker:
                count += 1
            else:
                break
        # Check backward direction
        for step in range(1, WIN_CONDITION):
            r = row - dx * step
            c = col - dy * step
            if 0 <= r < ROWS and 0 <= c < COLUMNS and board[r][c] == checker:
                count += 1
            else:
                break
        if count >= WIN_CONDITION:
            return True
    return False

def board_full(board):
    for row in board:
        for cell in row:
            if cell == " ":
                return False
    return True

def main():
    board = create_board()
    players = CHECKERS[:PLAYERS]
    
    # Choose first player randomly
    current_player_index = random.randint(0, PLAYERS - 1)
    
    print_board(board)
    
    while True:
        checker = players[current_player_index]
        prompt = f"Player {checker}, please enter a column: "
        
        while True:
            col_input = input(prompt).strip().upper()
            if not is_valid_column_input(col_input):
                # Invalid input, ask again
                continue
            col_idx = get_column_index(col_input)
            placed = place_checker(board, col_idx, checker)
            if placed is None:
                # Column full: turn lost, go to next player
                print_board(board)
                current_player_index = (current_player_index + 1) % PLAYERS
                break
            else:
                print_board(board)
                row_placed, col_placed = placed
                if check_win(board, row_placed, col_placed, checker):
                    print(f"Player {checker} won!")
                    return
                if board_full(board):
                    print("The game is a draw!")
                    return
                # Continue game with next player
                current_player_index = (current_player_index + 1) % PLAYERS
                break

if __name__ == "__main__":
    main()
