import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = 2

CHECKERS = ['X', 'O', 'V', 'H', 'M']  # Up to 5 players
WIN_COUNT = 4

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    cols = len(board[0])
    rows = len(board)
    # Column labels
    labels = [chr(ord('A') + i) for i in range(cols)]
    print('  ' + '   '.join(labels))
    print('+' + '---+' * cols)
    for r in range(rows):
        print('|' + '|'.join(f' {board[r][c]} ' for c in range(cols)) + '|')
        print('+' + '---+' * cols)

def is_valid_input(inp, board):
    if len(inp) != 1 or not inp.isalpha():
        return False
    col_idx = ord(inp) - ord('A')
    if col_idx < 0 or col_idx >= len(board[0]):
        return False
    if board[0][col_idx] != ' ':
        # top cell taken → column full
        return False
    return True

def get_col_index(inp):
    return ord(inp) - ord('A')

def place_checker(board, col, checker):
    # place checker in lowest empty cell of the column
    # return True if placed, False if column full (should not happen if validated before)
    rows = len(board)
    for r in range(rows - 1, -1, -1):
        if board[r][col] == ' ':
            board[r][col] = checker
            return True
    return False

def check_winner(board, checker):
    rows = len(board)
    cols = len(board[0])

    # horizontal check
    for r in range(rows):
        count = 0
        for c in range(cols):
            if board[r][c] == checker:
                count += 1
                if count == WIN_COUNT:
                    return True
            else:
                count = 0

    # vertical check
    for c in range(cols):
        count = 0
        for r in range(rows):
            if board[r][c] == checker:
                count += 1
                if count == WIN_COUNT:
                    return True
            else:
                count = 0

    # diagonal check (top-left to bottom-right)
    for r in range(rows - WIN_COUNT + 1):
        for c in range(cols - WIN_COUNT + 1):
            if all(board[r + i][c + i] == checker for i in range(WIN_COUNT)):
                return True

    # diagonal check (bottom-left to top-right)
    for r in range(WIN_COUNT - 1, rows):
        for c in range(cols - WIN_COUNT + 1):
            if all(board[r - i][c + i] == checker for i in range(WIN_COUNT)):
                return True

    return False

def board_full(board):
    # If top row has any empty space, board is not full
    return all(cell != ' ' for cell in board[0])

def main():
    board = create_board(ROWS, COLS)
    checkers = CHECKERS[:PLAYERS]
    current_player_idx = random.randint(0, PLAYERS - 1)
    print_board(board)

    while True:
        checker = checkers[current_player_idx]
        print(f"Player {checker}, please enter a column:")
        while True:
            user_input = input().strip().upper()
            if user_input == '':
                # Treat empty as invalid
                print(f"Invalid input. Player {checker}, please enter a column:")
                continue
            if not is_valid_input(user_input, board):
                # If the column is full, the turn is lost (optional but assignment says so)
                col_idx = get_col_index(user_input) if len(user_input) == 1 and user_input.isalpha() else None
                if col_idx is not None and 0 <= col_idx < COLS and board[0][col_idx] != ' ':
                    # Column full → turn lost
                    print_board(board)
                    current_player_idx = (current_player_idx + 1) % PLAYERS
                    break
                else:
                    print(f"Invalid input. Player {checker}, please enter a column:")
                continue
            # valid input and column not full → place checker
            col_idx = get_col_index(user_input)
            placed = place_checker(board, col_idx, checker)
            print_board(board)
            if placed:
                # Check win
                if check_winner(board, checker):
                    print(f"Player {checker} won!")
                    return
                # Check draw
                if board_full(board):
                    print("Game is a draw!")
                    return
                # Next player's turn
                current_player_idx = (current_player_idx + 1) % PLAYERS
            else:
                # Column is full → turn lost
                current_player_idx = (current_player_idx + 1) % PLAYERS
            break

if __name__ == '__main__':
    main()
