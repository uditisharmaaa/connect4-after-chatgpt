import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

def clear_screen():
    os.system('clear')

def create_board():
    board = []
    for _ in range(ROWS):
        row = [" "] * COLUMNS
        board.append(row)
    return board

def print_board(board):
    clear_screen()
    # Print column headers
    letters = [chr(ord('A') + i) for i in range(COLUMNS)]
    print("  " + "   ".join(letters))
    print("+---" * COLUMNS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLUMNS + "+")

def get_player_input(player_checker, board):
    while True:
        user_input = input(f"Player {player_checker}, please enter a column: ").strip().upper()
        if len(user_input) != 1:
            print("Invalid input. Please enter a single letter.")
            continue
        if not ('A' <= user_input <= chr(ord('A') + COLUMNS - 1)):
            print("Invalid column letter. Please enter a valid column.")
            continue
        col = ord(user_input) - ord('A')
        # Check if column is full
        if board[0][col] != " ":
            # Column full, turn lost
            print("Column is full. You lose your turn.")
            return -1
        return col

def place_checker(board, col, checker):
    # Place checker in lowest available row in column
    for row in range(ROWS-1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return row
    return -1  # should not happen if checked before

def check_win(board, checker):
    # Check horizontal
    for r in range(ROWS):
        for c in range(COLUMNS - 3):
            if all(board[r][c + i] == checker for i in range(4)):
                return True
    # Check vertical
    for c in range(COLUMNS):
        for r in range(ROWS - 3):
            if all(board[r + i][c] == checker for i in range(4)):
                return True
    # Check diagonal down-right
    for r in range(ROWS - 3):
        for c in range(COLUMNS - 3):
            if all(board[r + i][c + i] == checker for i in range(4)):
                return True
    # Check diagonal down-left
    for r in range(ROWS - 3):
        for c in range(3, COLUMNS):
            if all(board[r + i][c - i] == checker for i in range(4)):
                return True
    return False

def check_draw(board):
    # If top row is all filled, board is full
    return all(cell != " " for cell in board[0])

def main():
    board = create_board()
    players_checkers = CHECKERS[:PLAYERS]
    current_player_index = random.randint(0, PLAYERS - 1)

    print_board(board)

    while True:
        checker = players_checkers[current_player_index]
        col = get_player_input(checker, board)
        # If invalid column (full), lose turn
        if col == -1:
            current_player_index = (current_player_index + 1) % PLAYERS
            print_board(board)
            continue
        place_checker(board, col, checker)
        print_board(board)
        if check_win(board, checker):
            print(f"Player {checker} won!")
            break
        if check_draw(board):
            print("Game is a draw!")
            break
        current_player_index = (current_player_index + 1) % PLAYERS

if __name__ == "__main__":
    main()
