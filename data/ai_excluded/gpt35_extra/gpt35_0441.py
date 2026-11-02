import os
import random

# Constants for board size and players
ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    # Print column headers
    headers = [chr(ord('A') + i) for i in range(len(board[0]))]
    print("  " + "   ".join(headers))
    # Print rows
    for row in board:
        print("+---" * len(row) + "+")
        print("| " + " | ".join(row) + " |")
    print("+---" * len(board[0]) + "+")

def get_column_index(user_input, cols):
    if len(user_input) != 1:
        return -1
    letter = user_input.upper()
    idx = ord(letter) - ord('A')
    if 0 <= idx < cols:
        return idx
    return -1

def place_checker(board, col, checker):
    # Place the checker in the lowest available row in the given column
    # Return True if placement was successful, False if column full
    for row in range(ROWS-1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return True
    return False  # Column full

def check_four_in_a_row(line, checker):
    count = 0
    for cell in line:
        if cell == checker:
            count += 1
            if count == 4:
                return True
        else:
            count = 0
    return False

def check_win(board, checker):
    rows = len(board)
    cols = len(board[0])

    # Check horizontal
    for r in range(rows):
        if check_four_in_a_row(board[r], checker):
            return True

    # Check vertical
    for c in range(cols):
        col_cells = [board[r][c] for r in range(rows)]
        if check_four_in_a_row(col_cells, checker):
            return True

    # Check diagonal (top-left to bottom-right)
    for r in range(rows - 3):
        for c in range(cols - 3):
            diagonal = [board[r+i][c+i] for i in range(4)]
            if all(cell == checker for cell in diagonal):
                return True

    # Check diagonal (bottom-left to top-right)
    for r in range(3, rows):
        for c in range(cols - 3):
            diagonal = [board[r-i][c+i] for i in range(4)]
            if all(cell == checker for cell in diagonal):
                return True

    return False

def check_draw(board):
    for row in board:
        if " " in row:
            return False
    return True

def main():
    board = create_board(ROWS, COLS)
    players = CHECKERS[:PLAYERS]
    current_player_index = random.randint(0, PLAYERS -1)

    print_board(board)

    while True:
        checker = players[current_player_index]
        prompt = f"Player {checker}, please enter a column: "
        while True:
            user_input = input(prompt).strip()
            col = get_column_index(user_input, COLS)
            if col == -1:
                print("Invalid input. Please enter a valid column letter (A to {}).".format(chr(ord('A') + COLS -1)))
                continue

            if not place_checker(board, col, checker):
                # Column full, player loses turn
                print("Column {} is full. You lose your turn.".format(user_input.upper()))
                break
            else:
                break

        print_board(board)

        # Only check for win/draw if a checker was placed
        if col != -1 and board[0][col] != " ":
            if check_win(board, checker):
                print(f"Player {checker} won!")
                break
            if check_draw(board):
                print("The game is a draw!")
                break

        current_player_index = (current_player_index + 1) % PLAYERS

if __name__ == "__main__":
    main()
