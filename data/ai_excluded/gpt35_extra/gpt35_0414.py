import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]  # Support up to 5 players

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    board = [[" " for _ in range(cols)] for _ in range(rows)]
    return board

def print_board(board):
    clear_screen()
    # Print column labels
    labels = [chr(ord('A') + i) for i in range(len(board[0]))]
    print("  " + "   ".join(labels))
    # Print separator line
    sep = "+---" * len(board[0]) + "+"
    for row in board:
        print(sep)
        print("| " + " | ".join(row) + " |")
    print(sep)

def is_valid_column(col_char, cols):
    if len(col_char) != 1:
        return False
    if not ('A' <= col_char <= chr(ord('A') + cols - 1)):
        return False
    return True

def column_index(col_char):
    return ord(col_char) - ord('A')

def place_checker(board, col, checker):
    """
    Place checker in the lowest available row in column col.
    Return True if successfully placed, False if column full.
    """
    for row in reversed(range(len(board))):
        if board[row][col] == " ":
            board[row][col] = checker
            return True
    return False

def check_win(board, checker):
    rows = len(board)
    cols = len(board[0])
    win_count = 4

    # Horizontal check
    for r in range(rows):
        count = 0
        for c in range(cols):
            if board[r][c] == checker:
                count += 1
                if count == win_count:
                    return True
            else:
                count = 0

    # Vertical check
    for c in range(cols):
        count = 0
        for r in range(rows):
            if board[r][c] == checker:
                count += 1
                if count == win_count:
                    return True
            else:
                count = 0

    # Diagonal check (/ direction)
    # from bottom-left to top-right
    for r in range(rows - win_count + 1):
        for c in range(cols - win_count + 1):
            if (board[r][c] == checker and
                board[r+1][c+1] == checker and
                board[r+2][c+2] == checker and
                board[r+3][c+3] == checker):
                return True

    # Diagonal check (\ direction)
    # from top-left to bottom-right
    for r in range(win_count - 1, rows):
        for c in range(cols - win_count + 1):
            if (board[r][c] == checker and
                board[r-1][c+1] == checker and
                board[r-2][c+2] == checker and
                board[r-3][c+3] == checker):
                return True

    return False

def check_draw(board):
    for row in board:
        if " " in row:
            return False
    return True

def main():
    # Prepare game
    board = create_board(ROWS, COLS)
    players = CHECKERS[:PLAYERS]

    current_player = random.choice(range(PLAYERS))

    while True:
        print_board(board)
        print(f"Player {players[current_player]}, please enter a column:")

        valid_input = False
        lose_turn = False

        while not valid_input:
            col_input = input().upper().strip()
            if not is_valid_column(col_input, COLS):
                print("Invalid input. Please enter a column letter from A to " +
                      chr(ord('A') + COLS -1) + ":")
                continue

            col = column_index(col_input)

            if board[0][col] != " ":  # Column full
                # player loses turn
                lose_turn = True
                valid_input = True
            else:
                placed = place_checker(board, col, players[current_player])
                # place_checker should always return True here because we check full above
                valid_input = True

        if lose_turn:
            # nothing to do; move to next player
            current_player = (current_player + 1) % PLAYERS
            continue

        # Check win
        if check_win(board, players[current_player]):
            print_board(board)
            print(f"Player {players[current_player]} won!")
            break

        # Check draw
        if check_draw(board):
            print_board(board)
            print("It's a draw!")
            break

        # Next player
        current_player = (current_player + 1) % PLAYERS


if __name__ == "__main__":
    main()
