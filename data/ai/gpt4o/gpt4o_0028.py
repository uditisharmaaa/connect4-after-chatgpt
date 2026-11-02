import random
import os

# Constants
ROWS = 6
COLUMNS = 7
MAX_PLAYERS = 5
DEFAULT_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

def create_board(rows, columns):
    return [[" " for _ in range(columns)] for _ in range(rows)]

def print_board(board, columns):
    os.system('clear')
    col_labels = "  " + "   ".join(chr(65 + i) for i in range(columns))
    print(col_labels)
    print("+---" * columns + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * columns + "+")

def get_next_open_row(board, col):
    for r in range(ROWS-1, -1, -1):
        if board[r][col] == " ":
            return r
    return None

def is_valid_column(column_input, columns):
    return len(column_input) == 1 and column_input.isalpha() and 0 <= ord(column_input.upper()) - 65 < columns

def check_winner(board, checker):
    # Check horizontal
    for r in range(ROWS):
        for c in range(COLUMNS - 3):
            if all(board[r][c + i] == checker for i in range(4)):
                return True

    # Check vertical
    for r in range(ROWS - 3):
        for c in range(COLUMNS):
            if all(board[r + i][c] == checker for i in range(4)):
                return True

    # Check diagonal (positive slope)
    for r in range(ROWS - 3):
        for c in range(COLUMNS - 3):
            if all(board[r + i][c + i] == checker for i in range(4)):
                return True

    # Check diagonal (negative slope)
    for r in range(3, ROWS):
        for c in range(COLUMNS - 3):
            if all(board[r - i][c + i] == checker for i in range(4)):
                return True

    return False

def is_draw(board):
    return all(all(cell != " " for cell in row) for row in board)

def main():
    board = create_board(ROWS, COLUMNS)
    players = DEFAULT_PLAYERS
    player_checkers = CHECKERS[:players]

    current_player_idx = random.randint(0, players - 1)
    
    while True:
        print_board(board, COLUMNS)
        current_player = player_checkers[current_player_idx]
        print(f"Player {current_player}, please enter a column:")
        column_input = input().strip()

        if not is_valid_column(column_input, COLUMNS):
            print("Invalid input. Please enter a valid column letter.")
            continue

        col = ord(column_input.upper()) - 65
        row = get_next_open_row(board, col)

        if row is None:
            print("Column full. You lose your turn.")
        else:
            board[row][col] = current_player
            if check_winner(board, current_player):
                print_board(board, COLUMNS)
                print(f"Player {current_player} won!")
                break
            if is_draw(board):
                print_board(board, COLUMNS)
                print("The game is a draw!")
                break

        current_player_idx = (current_player_idx + 1) % players

if __name__ == "__main__":
    main()
