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
    board = [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]
    return board

def print_board(board):
    clear_screen()
    # Print column labels
    labels = [chr(ord('A') + i) for i in range(COLUMNS)]
    print("  " + "   ".join(labels))
    print("+" + "---+" * COLUMNS)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * COLUMNS)

def get_player_input(player_checker):
    while True:
        col = input(f"Player {player_checker}, please enter a column: ").strip().upper()
        if len(col) != 1:
            print("Invalid input. Please enter a single letter.")
            continue
        if not ('A' <= col <= chr(ord('A') + COLUMNS -1)):
            print("Invalid column letter. Please enter a valid column.")
            continue
        col_index = ord(col) - ord('A')
        return col_index

def place_checker(board, col_index, checker):
    # place checker in lowest empty row in that column
    for row in range(ROWS-1, -1, -1):
        if board[row][col_index] == " ":
            board[row][col_index] = checker
            return True
    # column full
    return False

def check_win(board, checker):
    # Horizontal check
    for row in range(ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row][col + i] == checker for i in range(4)):
                return True
    # Vertical check
    for col in range(COLUMNS):
        for row in range(ROWS - 3):
            if all(board[row + i][col] == checker for i in range(4)):
                return True
    # Diagonal (bottom-left to top-right)
    for row in range(3, ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row - i][col + i] == checker for i in range(4)):
                return True
    # Diagonal (top-left to bottom-right)
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if all(board[row + i][col + i] == checker for i in range(4)):
                return True
    return False

def check_draw(board):
    for row in board:
        if " " in row:
            return False
    return True

def main():
    board = create_board()
    players = CHECKERS[:PLAYERS]

    current_player_index = random.randint(0, PLAYERS - 1)
    print_board(board)

    while True:
        checker = players[current_player_index]
        col_index = get_player_input(checker)

        placed = place_checker(board, col_index, checker)
        if not placed:
            # Turn lost
            print(f"Column {chr(ord('A') + col_index)} is full. Player {checker} loses the turn.")
            current_player_index = (current_player_index + 1) % PLAYERS
            print_board(board)
            continue

        print_board(board)

        if check_win(board, checker):
            print(f"Player {checker} won!")
            break

        if check_draw(board):
            print("The game is a draw!")
            break

        current_player_index = (current_player_index + 1) % PLAYERS

if __name__ == "__main__":
    main()
