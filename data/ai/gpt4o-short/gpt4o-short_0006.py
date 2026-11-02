import random
import os

# Constants
ROWS = 6
COLUMNS = 7
COLUMN_LABELS = ["A", "B", "C", "D", "E", "F", "G"]
PLAYER_MARKERS = ["X", "O", "V", "H", "M"]  # Up to 5 players

# Number of players - adjust as needed (min: 2, max: 5)
NUM_PLAYERS = 3

def create_board():
    return [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')  # Clear screen
    print("  " + " ".join(COLUMN_LABELS))
    for row in board:
        print("| " + " | ".join(row) + " |")
    print()

def get_valid_moves(board):
    return [i for i in range(COLUMNS) if board[0][i] == " "]

def make_move(board, column, marker):
    for row in reversed(board):
        if row[column] == " ":
            row[column] = marker
            break

def check_winner(board, marker):
    # Check horizontal, vertical, and diagonal for a win
    for r in range(ROWS):
        for c in range(COLUMNS - 3):
            if all(board[r][c+i] == marker for i in range(4)):
                return True

    for r in range(ROWS - 3):
        for c in range(COLUMNS):
            if all(board[r+i][c] == marker for i in range(4)):
                return True

    for r in range(ROWS - 3):
        for c in range(COLUMNS - 3):
            if all(board[r+i][c+i] == marker for i in range(4)):
                return True
            if all(board[r+3-i][c+i] == marker for i in range(4)):
                return True

    return False

def is_draw(board):
    return all(board[0][i] != " " for i in range(COLUMNS))

def play_game():
    board = create_board()
    player_turns = random.sample(range(NUM_PLAYERS), NUM_PLAYERS)  # Randomize initial order
    markers = [PLAYER_MARKERS[i] for i in player_turns]

    current_player = 0
    print_board(board)

    while True:
        marker = markers[current_player]
        column_labels = COLUMN_LABELS
        valid_moves = get_valid_moves(board)

        print(f"Player {marker}'s turn.")
        move = input(f"Choose a column ({', '.join([column_labels[i] for i in valid_moves])}): ").upper()

        while move not in column_labels or column_labels.index(move) not in valid_moves:
            move = input("Invalid move. Try again: ").upper()

        make_move(board, column_labels.index(move), marker)
        print_board(board)

        if check_winner(board, marker):
            print(f"Player {marker} wins!")
            break
        elif is_draw(board):
            print("It's a draw!")
            break

        current_player = (current_player + 1) % NUM_PLAYERS

play_game()
