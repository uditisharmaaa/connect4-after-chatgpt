import os
import random
import string

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    cols = len(board[0])
    # Print column labels
    labels = [string.ascii_uppercase[i] for i in range(cols)]
    print("  " + "   ".join(labels))
    # Print board with horizontal lines
    row_line = "+" + "---+" * cols
    for row in range(len(board)):
        print(row_line)
        row_str = "|"
        for col in range(cols):
            row_str += " " + board[row][col] + " |"
        print(row_str)
    print(row_line)

def select_random_player(num_players):
    return random.randint(0, num_players - 1)

def is_valid_column_input(user_input, cols):
    if len(user_input) != 1:
        return False
    if user_input not in string.ascii_uppercase[:cols]:
        return False
    return True

def place_checker(board, col, checker):
    # Place checker in lowest empty spot in the column
    for row in reversed(range(len(board))):
        if board[row][col] == " ":
            board[row][col] = checker
            return True
    return False  # Column full

def check_win(board, checker):
    rows = len(board)
    cols = len(board[0])
    # Check horizontal
    for r in range(rows):
        for c in range(cols - 3):
            if all(board[r][c + offset] == checker for offset in range(4)):
                return True
    # Check vertical
    for r in range(rows - 3):
        for c in range(cols):
            if all(board[r + offset][c] == checker for offset in range(4)):
                return True
    # Check diagonal down-right
    for r in range(rows - 3):
        for c in range(cols - 3):
            if all(board[r + offset][c + offset] == checker for offset in range(4)):
                return True
    # Check diagonal down-left
    for r in range(rows - 3):
        for c in range(3, cols):
            if all(board[r + offset][c - offset] == checker for offset in range(4)):
                return True
    return False

def is_draw(board):
    return all(cell != " " for row in board for cell in row)

def next_player(current, num_players):
    return (current + 1) % num_players

def prompt_player(player_checker, cols):
    prompt = f"Player {player_checker}, please enter a column: "
    while True:
        user_input = input(prompt).strip().upper()
        if not is_valid_column_input(user_input, cols):
            continue
        col = string.ascii_uppercase.index(user_input)
        if col >= cols:
            continue
        return col

def main():
    board = create_board(ROWS, COLS)
    num_players = NUM_PLAYERS
    checkers = CHECKERS[:num_players]

    current_player = select_random_player(num_players)
    print_board(board)

    while True:
        player_checker = checkers[current_player]
        col = prompt_player(player_checker, COLS)

        placed = place_checker(board, col, player_checker)
        if not placed:
            # Column full -> player loses turn
            current_player = next_player(current_player, num_players)
            print_board(board)
            continue

        print_board(board)
        if check_win(board, player_checker):
            print(f"Player {player_checker} won!")
            break
        if is_draw(board):
            print("The game is a draw!")
            break
        current_player = next_player(current_player, num_players)

if __name__ == "__main__":
    main()
