import os
import random
import sys

# Constants (for the assignment submission)
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]  # max 5 players

def clear_screen():
    os.system('clear')

def create_board(rows, columns):
    return [[" " for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    # Print column headers
    headers = "  " + "   ".join(chr(ord('A') + i) for i in range(len(board[0])))
    print(headers)
    sep_line = "+" + "---+" * len(board[0])
    for row in board:
        print(sep_line)
        print("| " + " | ".join(row) + " |")
    print(sep_line)

def is_valid_column(col_letter, board):
    if len(col_letter) != 1 or not col_letter.isalpha():
        return False
    col_letter = col_letter.upper()
    col_index = ord(col_letter) - ord('A')
    if 0 <= col_index < len(board[0]):
        return True
    return False

def column_has_space(board, col_index):
    # If topmost cell empty, space remains
    return board[0][col_index] == " "

def place_checker(board, col_index, checker):
    # Place checker in the lowest empty spot in the column
    for row_index in reversed(range(len(board))):
        if board[row_index][col_index] == " ":
            board[row_index][col_index] = checker
            return row_index, col_index
    return None  # column full

def check_winner(board, row, col, checker):
    # Check all four directions for 4 in a row:
    # Horizontal, Vertical, Diagonal /

    directions = [
        (0, 1),   # horizontal right
        (1, 0),   # vertical down
        (1, 1),   # diagonal down-right
        (1, -1)   # diagonal down-left
    ]
    rows = len(board)
    cols = len(board[0])

    for dr, dc in directions:
        count = 1  # Current checker

        # Check positive direction
        r, c = row + dr, col + dc
        while 0 <= r < rows and 0 <= c < cols and board[r][c] == checker:
            count += 1
            r += dr
            c += dc

        # Check negative direction
        r, c = row - dr, col - dc
        while 0 <= r < rows and 0 <= c < cols and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc

        if count >= 4:
            return True
    return False

def board_full(board):
    # If any top cell is empty, board not full
    for c in range(len(board[0])):
        if board[0][c] == " ":
            return False
    return True

def main():
    board = create_board(ROWS, COLUMNS)
    players_checkers = CHECKERS[:PLAYERS]

    # Randomly select starting player
    current_player_idx = random.randint(0, PLAYERS -1)

    print_board(board)

    while True:
        checker = players_checkers[current_player_idx]
        prompt = f"Player {checker}, please enter a column: "
        while True:
            user_input = input(prompt).strip().upper()
            if not is_valid_column(user_input, board):
                # Invalid input (not a letter or out of range)
                continue
            col_index = ord(user_input) - ord('A')
            if not column_has_space(board, col_index):
                # Column full — turn lost per assignment
                # No repeated prompt, break and lose turn
                placed = None
                break
            placed = place_checker(board, col_index, checker)
            break

        print_board(board)
        if placed is None:
            # Turn lost due to full column
            current_player_idx = (current_player_idx + 1) % PLAYERS
            continue

        row, col = placed

        # Check win
        if check_winner(board, row, col, checker):
            print(f"Player {checker} won!")
            break

        # Check draw
        if board_full(board):
            print("The game is a draw!")
            break

        # Next player's turn
        current_player_idx = (current_player_idx + 1) % PLAYERS

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nGame terminated.")
        sys.exit()
