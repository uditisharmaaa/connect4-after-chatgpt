import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]  # Up to 5 players

def clear_screen():
    os.system('clear')

def create_board(rows, columns):
    board = []
    for _ in range(rows):
        board.append([" "] * columns)
    return board

def print_board(board):
    clear_screen()
    # Print column labels
    labels = [chr(ord('A') + i) for i in range(len(board[0]))]
    print("  " + "   ".join(labels))
    print("+---" * len(board[0]) + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * len(board[0]) + "+")

def is_valid_column(input_str, board):
    if len(input_str) != 1:
        return False
    col = ord(input_str) - ord('A')
    if col < 0 or col >= len(board[0]):
        return False
    # Check if column is full
    if board[0][col] != " ":
        return False
    return True

def get_next_open_row(board, col):
    for r in range(len(board)-1, -1, -1):
        if board[r][col] == " ":
            return r
    return None  # Column full

def place_checker(board, row, col, checker):
    board[row][col] = checker

def check_win(board, checker):
    rows = len(board)
    cols = len(board[0])
    needed = 4

    # Check horizontal
    for r in range(rows):
        for c in range(cols - needed + 1):
            if all(board[r][c+i] == checker for i in range(needed)):
                return True

    # Check vertical
    for c in range(cols):
        for r in range(rows - needed + 1):
            if all(board[r+i][c] == checker for i in range(needed)):
                return True

    # Check diagonal (down-right)
    for r in range(rows - needed + 1):
        for c in range(cols - needed + 1):
            if all(board[r+i][c+i] == checker for i in range(needed)):
                return True

    # Check diagonal (down-left)
    for r in range(rows - needed + 1):
        for c in range(needed - 1, cols):
            if all(board[r+i][c-i] == checker for i in range(needed)):
                return True

    return False

def check_draw(board):
    # If top row has any empty spaces, no draw
    return all(cell != " " for cell in board[0])

def main():
    board = create_board(ROWS, COLUMNS)
    players_checkers = CHECKERS[:PLAYERS]

    # Randomly select starting player
    current_player_index = random.randint(0, PLAYERS - 1)

    print_board(board)

    while True:
        player_checker = players_checkers[current_player_index]
        print(f"Player {player_checker}, please enter a column:")

        while True:
            user_input = input().strip().upper()
            if not is_valid_column(user_input, board):
                print("Invalid input. Please enter a valid column letter (A-G) that is not full:")
                continue
            else:
                break

        col = ord(user_input) - ord('A')
        row = get_next_open_row(board, col)
        if row is None:
            # Column full, turn is lost
            current_player_index = (current_player_index + 1) % PLAYERS
            print_board(board)
            continue

        place_checker(board, row, col, player_checker)
        print_board(board)

        if check_win(board, player_checker):
            print(f"Player {player_checker} won!")
            break

        if check_draw(board):
            print("Game is a draw!")
            break

        current_player_index = (current_player_index + 1) % PLAYERS

if __name__ == "__main__":
    main()
