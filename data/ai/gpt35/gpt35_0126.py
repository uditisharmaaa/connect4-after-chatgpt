import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]  # Supported checkers, up to 5 players

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    board = [[" " for _ in range(cols)] for _ in range(rows)]
    return board

def print_board(board):
    clear_screen()
    cols = len(board[0])
    rows = len(board)
    # Print column headers
    header = "  "
    for i in range(cols):
        header += " " + chr(ord('A') + i) + "  "
    print(header)
    # Print top border and rows
    for r in range(rows):
        print("+" + "---+" * cols)
        row_str = "|"
        for c in range(cols):
            row_str += " " + board[r][c] + " |"
        print(row_str)
    print("+" + "---+" * cols)

def valid_column_input(user_input, cols):
    if len(user_input) != 1:
        return False
    c = user_input.upper()
    if c < 'A' or c >= chr(ord('A') + cols):
        return False
    return True

def column_index(user_input):
    return ord(user_input.upper()) - ord('A')

def place_checker(board, col, checker):
    # Place checker in the lowest available spot in the column
    rows = len(board)
    for row in range(rows - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return True
    return False  # Column full

def check_winner(board, checker):
    rows = len(board)
    cols = len(board[0])
    # Check horizontal
    for r in range(rows):
        for c in range(cols - 3):
            if board[r][c] == checker and board[r][c+1] == checker and board[r][c+2] == checker and board[r][c+3] == checker:
                return True
    # Check vertical
    for c in range(cols):
        for r in range(rows - 3):
            if board[r][c] == checker and board[r+1][c] == checker and board[r+2][c] == checker and board[r+3][c] == checker:
                return True
    # Check diagonal down-right
    for r in range(rows - 3):
        for c in range(cols - 3):
            if board[r][c] == checker and board[r+1][c+1] == checker and board[r+2][c+2] == checker and board[r+3][c+3] == checker:
                return True
    # Check diagonal down-left
    for r in range(rows - 3):
        for c in range(3, cols):
            if board[r][c] == checker and board[r+1][c-1] == checker and board[r+2][c-2] == checker and board[r+3][c-3] == checker:
                return True
    return False

def board_full(board):
    for row in board:
        for cell in row:
            if cell == " ":
                return False
    return True

def main():
    board = create_board(ROWS, COLS)
    players_checkers = CHECKERS[:PLAYERS]
    current_player = random.randint(0, PLAYERS -1)

    print_board(board)
    print("Game start! Player {} goes first.".format(players_checkers[current_player]))

    while True:
        checker = players_checkers[current_player]
        print("Player {}, please enter a column:".format(checker))
        user_input = input().strip()

        if not valid_column_input(user_input, COLS):
            # Invalid input: ask again
            continue

        col = column_index(user_input)
        placed = place_checker(board, col, checker)
        if not placed:
            # Column full, player loses turn
            current_player = (current_player + 1) % PLAYERS
            print_board(board)
            continue

        print_board(board)

        # Check for win
        if check_winner(board, checker):
            print("Player {} won!".format(checker))
            break

        # Check for draw
        if board_full(board):
            print("The game is a draw.")
            break

        # Next player's turn
        current_player = (current_player + 1) % PLAYERS

if __name__ == "__main__":
    main()
