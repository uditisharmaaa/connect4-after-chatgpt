import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']  # Support up to 5 players


def create_board(rows, cols):
    board = []
    for _ in range(rows):
        board.append([' '] * cols)
    return board


def print_board(board):
    os.system('clear')
    cols = len(board[0])
    # Print column labels
    labels = [chr(ord('A') + i) for i in range(cols)]
    print('  ' + '   '.join(labels))
    # Print top border
    print('+' + '---+' * cols)
    for row in board:
        # Print each cell in the row
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
        print('+' + '---+' * cols)


def valid_column_input(user_input, cols):
    if len(user_input) != 1:
        return False
    c = user_input[0]
    if c < 'A' or c >= chr(ord('A') + cols):
        return False
    return True


def column_index(user_input):
    return ord(user_input) - ord('A')


def place_checker(board, col_idx, checker):
    # place checker in the lowest empty row in column col_idx
    for row in range(len(board) - 1, -1, -1):
        if board[row][col_idx] == ' ':
            board[row][col_idx] = checker
            return True
    return False  # column full


def check_win(board, checker):
    rows = len(board)
    cols = len(board[0])
    in_a_row = 4

    # Horizontal check
    for r in range(rows):
        count = 0
        for c in range(cols):
            if board[r][c] == checker:
                count += 1
                if count == in_a_row:
                    return True
            else:
                count = 0

    # Vertical check
    for c in range(cols):
        count = 0
        for r in range(rows):
            if board[r][c] == checker:
                count += 1
                if count == in_a_row:
                    return True
            else:
                count = 0

    # Diagonal (down-right) check
    for r in range(rows - in_a_row + 1):
        for c in range(cols - in_a_row + 1):
            if all(board[r + i][c + i] == checker for i in range(in_a_row)):
                return True

    # Diagonal (up-right) check
    for r in range(in_a_row - 1, rows):
        for c in range(cols - in_a_row + 1):
            if all(board[r - i][c + i] == checker for i in range(in_a_row)):
                return True

    return False


def board_full(board):
    for row in board:
        for cell in row:
            if cell == ' ':
                return False
    return True


def main():
    board = create_board(ROWS, COLS)
    players = CHECKERS[:PLAYERS]

    current_player_idx = random.randint(0, PLAYERS - 1)

    print_board(board)
    print(f"Player {players[current_player_idx]} starts!")

    while True:
        checker = players[current_player_idx]
        # ask for input
        user_input = input(f"Player {checker}, please enter a column: ").strip().upper()
        while not valid_column_input(user_input, COLS):
            user_input = input(f"Invalid input. Player {checker}, please enter a column: ").strip().upper()

        col = column_index(user_input)
        placed = place_checker(board, col, checker)
        if not placed:
            # column full, loses turn
            print("Column is full! You lose your turn.")
        else:
            print_board(board)
            if check_win(board, checker):
                print(f"Player {checker} won!")
                break
            if board_full(board):
                print("Game is a draw!")
                break

        current_player_idx = (current_player_idx + 1) % PLAYERS


if __name__ == "__main__":
    main()
