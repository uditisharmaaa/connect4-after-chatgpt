import os
import random

# Constants - Board dimensions and players
ROWS = 6
COLS = 7
MIN_PLAYERS = 2
MAX_PLAYERS = 5

# Players and their checkers in order
CHECKERS = ["X", "O", "V", "H", "M"]

# Number of players for this assignment
NUM_PLAYERS = 2  # Change this between MIN_PLAYERS and MAX_PLAYERS if needed

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    # Create a 2D board filled with " " (spaces)
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    cols = len(board[0])
    # Print Column headers
    headers = [chr(ord('A') + i) for i in range(cols)]
    print(" ", end="  ")
    print("   ".join(headers))
    # Print the board rows with grid lines
    for r in range(len(board)):
        print("+---" * cols + "+")
        print("|", end="")
        for c in range(cols):
            print(f" {board[r][c]} |", end="")
        print()
    print("+---" * cols + "+")

def column_letter_to_index(letter):
    letter = letter.upper()
    if 'A' <= letter <= 'Z':
        return ord(letter) - ord('A')
    return -1

def is_valid_column_choice(choice, cols):
    if len(choice) != 1:
        return False
    idx = column_letter_to_index(choice)
    if idx == -1 or idx >= cols:
        return False
    return True

def get_player_input(player_checker, board):
    cols = len(board[0])
    while True:
        choice = input(f"Player {player_checker}, please enter a column: ").strip().upper()
        if not is_valid_column_choice(choice, cols):
            print("Invalid input. Please enter a valid column letter.")
            continue
        col_idx = column_letter_to_index(choice)
        # Check if column full
        if board[0][col_idx] != " ":
            # Column full - turn lost
            print(f"Column {choice} is full. Player {player_checker} loses turn.")
            return None
        return col_idx

def place_checker(board, col_idx, checker):
    # Place checker in the lowest available space of the column
    for row in reversed(range(len(board))):
        if board[row][col_idx] == " ":
            board[row][col_idx] = checker
            return row, col_idx
    # Should not reach here if called correctly
    return None, None

def check_for_win(board, checker):
    rows = len(board)
    cols = len(board[0])
    win_length = 4

    # Check horizontal
    for r in range(rows):
        for c in range(cols - win_length + 1):
            if all(board[r][c+i] == checker for i in range(win_length)):
                return True

    # Check vertical
    for c in range(cols):
        for r in range(rows - win_length + 1):
            if all(board[r+i][c] == checker for i in range(win_length)):
                return True

    # Check diagonal down-right
    for r in range(rows - win_length + 1):
        for c in range(cols - win_length + 1):
            if all(board[r+i][c+i] == checker for i in range(win_length)):
                return True

    # Check diagonal up-right
    for r in range(win_length - 1, rows):
        for c in range(cols - win_length + 1):
            if all(board[r-i][c+i] == checker for i in range(win_length)):
                return True

    return False

def check_for_draw(board):
    # If no spaces left in top row, board full => draw
    return all(cell != " " for cell in board[0])

def main():
    # Validate NUM_PLAYERS
    num_players = NUM_PLAYERS
    if num_players < MIN_PLAYERS or num_players > MAX_PLAYERS:
        print(f"Number of players must be between {MIN_PLAYERS} and {MAX_PLAYERS}. Exiting.")
        return

    board = create_board(ROWS, COLS)
    players = CHECKERS[:num_players]

    # Randomly select starting player index
    current_player_idx = random.randint(0, num_players - 1)

    print_board(board)

    while True:
        player_checker = players[current_player_idx]
        col_idx = get_player_input(player_checker, board)

        if col_idx is None:
            # Column full => loses turn, move to next player
            current_player_idx = (current_player_idx + 1) % num_players
            print_board(board)
            continue

        place_checker(board, col_idx, player_checker)
        print_board(board)

        if check_for_win(board, player_checker):
            print(f"Player {player_checker} won!")
            break

        if check_for_draw(board):
            print("The game is a draw!")
            break

        current_player_idx = (current_player_idx + 1) % num_players

if __name__ == "__main__":
    main()
