import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M'][:PLAYERS]

# Initialize board
def create_board():
    return [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]

# Print board
def print_board(board):
    os.system('clear')
    print("  " + "   ".join(chr(i) for i in range(65, 65 + COLUMNS)))
    for row in board:
        print("+---" * COLUMNS + "+")
        print("| " + " | ".join(row) + " |")
    print("+---" * COLUMNS + "+")

# Check for win
def check_win(board, player_checker):
    def check_direction(r, c, dr, dc):
        count = 0
        for _ in range(4):
            if 0 <= r < ROWS and 0 <= c < COLUMNS and board[r][c] == player_checker:
                count += 1
            else:
                break
            r, c = r + dr, c + dc
        return count == 4

    for r in range(ROWS):
        for c in range(COLUMNS):
            if (check_direction(r, c, 0, 1) or   # Horizontal
                check_direction(r, c, 1, 0) or   # Vertical
                check_direction(r, c, 1, 1) or   # Diagonal /
                check_direction(r, c, 1, -1)):   # Diagonal \
                return True
    return False

# Check for draw
def check_draw(board):
    return all(cell != " " for row in board for cell in row)

# Play move
def play_move(board, col, checker):
    for r in reversed(range(ROWS)):
        if board[r][col] == " ":
            board[r][col] = checker
            return True
    return False

# Get valid input
def get_valid_input(board):
    while True:
        col = input("Enter a column: ").strip().upper()
        if len(col) == 1 and 'A' <= col <= chr(65 + COLUMNS - 1):
            col_idx = ord(col) - 65
            if board[0][col_idx] == " ":
                return col_idx
        print("Invalid input. Try again.")

def main():
    board = create_board()
    current_player = random.randint(0, PLAYERS - 1)
    print_board(board)

    while True:
        print(f"Player {CHECKERS[current_player]}, it's your turn.")
        col = get_valid_input(board)
        play_move(board, col, CHECKERS[current_player])
        print_board(board)

        if check_win(board, CHECKERS[current_player]):
            print(f"Player {CHECKERS[current_player]} won!")
            break

        if check_draw(board):
            print("It's a draw!")
            break

        current_player = (current_player + 1) % PLAYERS

if __name__ == "__main__":
    main()
