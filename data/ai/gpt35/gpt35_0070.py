import os
import random

# Constants
ROWS = 6
COLUMNS = 7
MAX_COLUMNS = 26
MIN_PLAYERS = 2
MAX_PLAYERS = 5
WIN_COUNT = 4

PLAYERS = ["X", "O", "V", "H", "M"]  # Support up to 5 players

def clear_screen():
    os.system('clear')

def create_board(rows, columns):
    return [[" " for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    columns = len(board[0])
    # Print column labels
    labels = [chr(ord('A') + i) for i in range(columns)]
    print("  " + "   ".join(labels))
    # Print board with separators
    line = "+---" * columns + "+"
    for row in board:
        print(line)
        print("| " + " | ".join(row) + " |")
    print(line)

def is_valid_column_input(user_input, columns):
    if len(user_input) != 1:
        return False
    ch = user_input.upper()
    if 'A' <= ch < chr(ord('A') + columns):
        return True
    return False

def column_to_index(ch):
    return ord(ch.upper()) - ord('A')

def can_place_in_column(board, col_idx):
    return board[0][col_idx] == " "

def place_checker(board, col_idx, checker):
    # Place checker in the lowest empty position of the column
    for row_idx in range(len(board)-1, -1, -1):
        if board[row_idx][col_idx] == " ":
            board[row_idx][col_idx] = checker
            return row_idx, col_idx
    # Column full, return None if cannot place
    return None

def check_win(board, checker):
    rows = len(board)
    cols = len(board[0])

    # Horizontal check
    for r in range(rows):
        count = 0
        for c in range(cols):
            if board[r][c] == checker:
                count += 1
                if count == WIN_COUNT:
                    return True
            else:
                count = 0

    # Vertical check
    for c in range(cols):
        count = 0
        for r in range(rows):
            if board[r][c] == checker:
                count += 1
                if count == WIN_COUNT:
                    return True
            else:
                count = 0

    # Diagonal down-right (\) check
    for r in range(rows - WIN_COUNT + 1):
        for c in range(cols - WIN_COUNT + 1):
            win = True
            for i in range(WIN_COUNT):
                if board[r+i][c+i] != checker:
                    win = False
                    break
            if win:
                return True

    # Diagonal up-right (/) check
    for r in range(WIN_COUNT - 1, rows):
        for c in range(cols - WIN_COUNT + 1):
            win = True
            for i in range(WIN_COUNT):
                if board[r - i][c + i] != checker:
                    win = False
                    break
            if win:
                return True

    return False

def check_draw(board):
    # Draw if no empty cells in top row (no valid moves)
    for c in range(len(board[0])):
        if board[0][c] == " ":
            return False
    return True

def main():
    # Set dimensions and players for submission requirement
    rows = ROWS
    columns = COLUMNS
    num_players = 2
    players = PLAYERS[:num_players]

    board = create_board(rows, columns)
    current_player_idx = random.randint(0, num_players - 1)

    print_board(board)

    while True:
        player_checker = players[current_player_idx]
        prompt = f"Player {player_checker}, please enter a column: "
        user_input = input(prompt).strip().upper()

        if not is_valid_column_input(user_input, columns):
            continue  # Invalid input, ask again

        col_idx = column_to_index(user_input)

        if not can_place_in_column(board, col_idx):
            # Column full, player loses turn
            current_player_idx = (current_player_idx + 1) % num_players
            continue

        place_checker(board, col_idx, player_checker)

        print_board(board)

        if check_win(board, player_checker):
            print(f"Player {player_checker} won!")
            break

        if check_draw(board):
            print("Game is a draw.")
            break

        current_player_idx = (current_player_idx + 1) % num_players

if __name__ == "__main__":
    main()
