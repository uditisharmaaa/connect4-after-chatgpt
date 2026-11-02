import os
import random

# Constants
ROWS = 6
COLUMNS = 7
NUM_PLAYERS = 2  # can be 2 to 5
CHECKERS = ["X", "O", "V", "H", "M"]


def clear_screen():
    os.system('clear')


def create_board(rows=ROWS, columns=COLUMNS):
    return [[" " for _ in range(columns)] for _ in range(rows)]


def print_board(board):
    columns = len(board[0])
    header = "  " + "   ".join(chr(ord('A') + i) for i in range(columns))
    separator = "+---" * columns + "+"
    print(header)
    for row in board:
        print(separator)
        print("| " + " | ".join(row) + " |")
    print(separator)


def valid_column_input(user_input, columns):
    if len(user_input) != 1:
        return False
    c = user_input.upper()
    if 'A' <= c < chr(ord('A') + columns):
        return True
    return False


def column_index_from_letter(letter):
    return ord(letter.upper()) - ord('A')


def place_checker(board, col_index, checker):
    """
    Places checker in the lowest empty row of the column.
    Returns True if placed, False if column is full.
    """
    for row in reversed(range(len(board))):
        if board[row][col_index] == " ":
            board[row][col_index] = checker
            return True
    return False


def check_horizontal_win(board, checker):
    rows = len(board)
    cols = len(board[0])
    for r in range(rows):
        count = 0
        for c in range(cols):
            if board[r][c] == checker:
                count += 1
                if count == 4:
                    return True
            else:
                count = 0
    return False


def check_vertical_win(board, checker):
    rows = len(board)
    cols = len(board[0])
    for c in range(cols):
        count = 0
        for r in range(rows):
            if board[r][c] == checker:
                count += 1
                if count == 4:
                    return True
            else:
                count = 0
    return False


def check_diagonal_win(board, checker):
    rows = len(board)
    cols = len(board[0])
    # Check \ diagonals
    for r in range(rows - 3):
        for c in range(cols - 3):
            if (board[r][c] == checker and board[r+1][c+1] == checker and
                board[r+2][c+2] == checker and board[r+3][c+3] == checker):
                return True
    # Check / diagonals
    for r in range(3, rows):
        for c in range(cols - 3):
            if (board[r][c] == checker and board[r-1][c+1] == checker and
                board[r-2][c+2] == checker and board[r-3][c+3] == checker):
                return True
    return False


def check_win(board, checker):
    return (check_horizontal_win(board, checker) or
            check_vertical_win(board, checker) or
            check_diagonal_win(board, checker))


def check_draw(board):
    for row in board:
        if " " in row:
            return False
    return True


def get_valid_input(player):
    while True:
        choice = input(f"Player {player}, please enter a column: ").strip().upper()
        if not valid_column_input(choice, COLUMNS):
            continue
        col_index = column_index_from_letter(choice)
        # If column full, turn lost
        if board[0][col_index] != " ":
            # According to the spec: turn is lost
            return col_index, False  # invalid turn, lost the turn
        return col_index, True  # valid turn


# Start of program
board = create_board()
players = CHECKERS[:NUM_PLAYERS]
current_player_index = random.randint(0, NUM_PLAYERS - 1)

clear_screen()
print_board(board)

while True:
    player_checker = players[current_player_index]
    col_index, valid_turn = get_valid_input(player_checker)

    if not valid_turn:
        # turn lost, print board and move on
        clear_screen()
        print_board(board)
        current_player_index = (current_player_index + 1) % NUM_PLAYERS
        continue

    placed = place_checker(board, col_index, player_checker)

    # placed should always be True here because we check for full above,
    # but in case bug or misuse, just skip turn if False
    if not placed:
        # According to spec: turn lost
        clear_screen()
        print_board(board)
        current_player_index = (current_player_index + 1) % NUM_PLAYERS
        continue

    clear_screen()
    print_board(board)

    if check_win(board, player_checker):
        print(f"Player {player_checker} won!")
        break

    if check_draw(board):
        print("The game is a draw!")
        break

    current_player_index = (current_player_index + 1) % NUM_PLAYERS
