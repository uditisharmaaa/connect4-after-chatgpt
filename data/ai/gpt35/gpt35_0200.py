import os
import random

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]  # Up to 5 players
WIN_COUNT = 4

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    cols = len(board[0])
    rows = len(board)
    # Print column labels A, B, C, ...
    col_labels = [chr(ord('A') + i) for i in range(cols)]
    print("  " + "   ".join(col_labels))
    # Print the board
    sep = "+" + "---+" * cols
    for r in range(rows):
        print(sep)
        print("| " + " | ".join(board[r]) + " |")
    print(sep)

def is_valid_column(col_char, board):
    if len(col_char) != 1 or not ('A' <= col_char <= chr(ord('A') + len(board[0]) - 1)):
        return False
    col_idx = ord(col_char) - ord('A')
    # Check if there is space left in column (top row must be empty)
    return board[0][col_idx] == " "

def place_checker(board, col_char, checker):
    col = ord(col_char) - ord('A')
    rows = len(board)
    # Place checker in the lowest available space in column
    for r in range(rows - 1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = checker
            return True
    # Column full, turn lost
    return False

def check_win(board, checker):
    rows, cols = len(board), len(board[0])

    # Directions to check: horizontal, vertical, / diagonal, \ diagonal
    directions = [(0,1), (1,0), (1,1), (1,-1)]

    for r in range(rows):
        for c in range(cols):
            if board[r][c] != checker:
                continue
            for dr, dc in directions:
                count = 1
                nr, nc = r + dr, c + dc
                while 0 <= nr < rows and 0 <= nc < cols and board[nr][nc] == checker:
                    count += 1
                    if count == WIN_COUNT:
                        return True
                    nr += dr
                    nc += dc
    return False

def board_full(board):
    return all(cell != " " for cell in board[0])

def main():
    board = create_board(ROWS, COLS)
    players = CHECKERS[:NUM_PLAYERS]
    current_player_idx = random.randrange(NUM_PLAYERS)

    print_board(board)

    while True:
        checker = players[current_player_idx]
        prompt = f"Player {checker}, please enter a column: "
        # Validate input
        while True:
            col_choice = input(prompt).strip().upper()
            if not is_valid_column(col_choice, board):
                print("Invalid input. Please enter a valid column letter that is not full.")
                continue
            break

        # Place checker
        success = place_checker(board, col_choice, checker)
        if not success:
            # Column full, turn lost
            print(f"Column {col_choice} is full. Player {checker} loses turn.")
        else:
            print_board(board)

            # Check win
            if check_win(board, checker):
                print(f"Player {checker} won!")
                break

            # Check draw
            if board_full(board):
                print("The game is a draw!")
                break

        # Next player
        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
