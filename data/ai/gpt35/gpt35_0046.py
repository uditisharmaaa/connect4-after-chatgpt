import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]  # up to 5 players


def clear_screen():
    os.system('clear')


def create_board(rows, cols):
    board = []
    for _ in range(rows):
        board.append([" "] * cols)
    return board


def print_board(board):
    clear_screen()
    # Print column labels
    letters = [chr(ord('A') + i) for i in range(len(board[0]))]
    print("  " + "   ".join(letters))
    # Print board with borders
    for row in range(len(board)):
        print("+" + "---+" * len(board[0]))
        line = "|"
        for col in range(len(board[0])):
            line += " " + board[row][col] + " |"
        print(line)
    print("+" + "---+" * len(board[0]))


def is_valid_column_input(inp, cols):
    if len(inp) != 1:
        return False
    c = inp[0]
    if c < 'A' or c >= chr(ord('A') + cols):
        return False
    return True


def get_column_index(column_letter):
    return ord(column_letter) - ord('A')


def place_checker(board, col_index, checker):
    # place on lowest available row in this column
    # row 0 is top, row ROWS-1 is bottom
    for row in reversed(range(len(board))):
        if board[row][col_index] == " ":
            board[row][col_index] = checker
            return True
    return False  # Column full


def check_horizontal(board, r, c, checker):
    count = 0
    for col in range(len(board[0])):
        if board[r][col] == checker:
            count += 1
            if count == 4:
                return True
        else:
            count = 0
    return False


def check_vertical(board, r, c, checker):
    count = 0
    for row in range(len(board)):
        if board[row][c] == checker:
            count += 1
            if count == 4:
                return True
        else:
            count = 0
    return False


def check_diagonal(board, r, c, checker):
    rows = len(board)
    cols = len(board[0])
    # check / diagonal (bottom-left to top-right)
    for row in range(rows - 3):
        for col in range(cols - 3):
            if (board[row][col] == checker and
                board[row+1][col+1] == checker and
                board[row+2][col+2] == checker and
                board[row+3][col+3] == checker):
                return True

    # check \ diagonal (top-left to bottom-right)
    for row in range(3, rows):
        for col in range(cols - 3):
            if (board[row][col] == checker and
                board[row-1][col+1] == checker and
                board[row-2][col+2] == checker and
                board[row-3][col+3] == checker):
                return True

    return False


def check_win(board, checker):
    rows = len(board)
    cols = len(board[0])
    for r in range(rows):
        for c in range(cols):
            if board[r][c] == checker:
                if (check_horizontal(board, r, c, checker) or
                    check_vertical(board, r, c, checker) or
                    check_diagonal(board, r, c, checker)):
                    return True
    return False


def check_draw(board):
    for row in board:
        for cell in row:
            if cell == " ":
                return False
    return True


def main():
    board = create_board(ROWS, COLUMNS)
    players_checkers = CHECKERS[:PLAYERS]

    # Randomly select starting player index
    current_player_index = random.randint(0, PLAYERS - 1)

    print_board(board)

    while True:
        checker = players_checkers[current_player_index]
        valid_input = False
        while not valid_input:
            user_input = input(f"Player {checker}, please enter a column: ").strip().upper()
            if not is_valid_column_input(user_input, COLUMNS):
                continue
            col_idx = get_column_index(user_input)
            # Try to place checker
            if place_checker(board, col_idx, checker):
                valid_input = True
            else:
                # Column full, turn is lost
                valid_input = True
                # Do not place checker, just lose turn

        print_board(board)

        # Check win (only if checker was placed)
        if board and board[0][col_idx] == checker:
            if check_win(board, checker):
                print(f"Player {checker} won!")
                break

        # Check draw
        if check_draw(board):
            print("The game is a draw!")
            break

        # Next player
        current_player_index = (current_player_index + 1) % PLAYERS


if __name__ == "__main__":
    main()
