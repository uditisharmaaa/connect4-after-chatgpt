import os
import random

# Constants
ROWS = 6         # Number of rows
COLS = 7         # Number of columns (max 26)
PLAYERS = 2      # Number of players (2 to 5)
WIN_COUNT = 4    # Number in a row needed to win
CHECKERS = ['X', 'O', 'V', 'H', 'M']  # Player checkers

def clear_screen():
    os.system('clear')

def create_board():
    board = []
    for _ in range(ROWS):
        board.append([" "] * COLS)
    return board

def print_board(board):
    clear_screen()
    # Print column letters
    letters = [chr(ord('A') + i) for i in range(COLS)]
    print("  " + "   ".join(letters))
    # Print top border
    print("+" + "---+" * COLS)
    # Print rows (no labels)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * COLS)

def convert_col_letter_to_index(letter):
    letter = letter.upper()
    if len(letter) != 1:
        return -1
    index = ord(letter) - ord('A')
    if 0 <= index < COLS:
        return index
    return -1

def is_valid_column(col, board):
    if 0 <= col < COLS:
        # Check if column is not full (top row empty)
        return board[0][col] == " "
    return False

def place_checker(board, col, checker):
    # Place checker in the lowest empty spot in column
    for row in range(ROWS-1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return row, col
    return -1, -1  # Column full

def check_direction(board, start_row, start_col, delta_row, delta_col, checker):
    count = 0
    r, c = start_row, start_col
    while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == checker:
        count += 1
        r += delta_row
        c += delta_col
    return count

def check_for_win(board, row, col, checker):
    # Check all directions for 4 in a row
    directions = [
        ((0, 1), (0, -1)),   # Horizontal: right and left
        ((1, 0), (-1, 0)),   # Vertical: down and up
        ((1, 1), (-1, -1)),  # Diagonal down-right and up-left
        ((1, -1), (-1, 1))   # Diagonal down-left and up-right
    ]

    for dir1, dir2 in directions:
        count = 1  # Count the placed checker itself
        count += check_direction(board, row + dir1[0], col + dir1[1], dir1[0], dir1[1], checker)
        count += check_direction(board, row + dir2[0], col + dir2[1], dir2[0], dir2[1], checker)
        if count >= WIN_COUNT:
            return True
    return False

def is_board_full(board):
    for col in range(COLS):
        if board[0][col] == " ":
            return False
    return True

def get_player_input(player_checker, board):
    while True:
        col_letter = input(f"Player {player_checker}, please enter a column: ").strip()
        col_index = convert_col_letter_to_index(col_letter)
        if col_index == -1:
            print("Invalid input. Please enter a letter between A and {}.".format(chr(ord('A') + COLS - 1)))
            continue
        if not is_valid_column(col_index, board):
            # The assignment says if column is full, player loses the turn
            print("Column {} is full. You lose your turn.".format(col_letter.upper()))
            return -1
        return col_index

def main():
    board = create_board()
    player_indices = list(range(PLAYERS))
    first_player = random.choice(player_indices)
    current_player_idx = first_player

    print_board(board)

    while True:
        player_checker = CHECKERS[current_player_idx]
        col = get_player_input(player_checker, board)

        # If player loses turn due to full column
        if col == -1:
            current_player_idx = (current_player_idx + 1) % PLAYERS
            print_board(board)
            continue

        row, col_placed = place_checker(board, col, player_checker)
        print_board(board)

        # Check for win
        if check_for_win(board, row, col_placed, player_checker):
            print(f"Player {player_checker} won!")
            break

        # Check for draw
        if is_board_full(board):
            print("The game is a draw.")
            break

        # Next player's turn
        current_player_idx = (current_player_idx + 1) % PLAYERS

if __name__ == "__main__":
    main()
