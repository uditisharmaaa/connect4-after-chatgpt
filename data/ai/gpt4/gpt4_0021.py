import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"][:PLAYERS]

# Create the board
def create_board():
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

# Print the board
def print_board(board):
    os.system('clear')
    print("  " + "   ".join([chr(65 + i) for i in range(COLS)]))
    for row in board:
        print("+---" * COLS + "+")
        print("| " + " | ".join(row) + " |")
    print("+---" * COLS + "+")

# Check for a win
def check_win(board, player):
    def check_direction(r, c, dr, dc):
        count = 0
        for i in range(4):
            nr, nc = r + dr * i, c + dc * i
            if 0 <= nr < ROWS and 0 <= nc < COLS and board[nr][nc] == player:
                count += 1
            else:
                break
        return count == 4

    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] == player:
                if any(check_direction(r, c, dr, dc) for dr, dc in [(0, 1), (1, 0), (1, 1), (1, -1)]):
                    return True
    return False

# Check for a draw
def check_draw(board):
    return all(board[0][c] != " " for c in range(COLS))

# Place a checker
def place_checker(board, col, player):
    for r in range(ROWS - 1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = player
            return True
    return False

# Main game loop
def play_game():
    board = create_board()
    current_player = random.randint(0, PLAYERS - 1)

    while True:
        print_board(board)
        print(f"Player {CHECKERS[current_player]}, please enter a column:")
        move = input().strip().upper()

        # Validate input
        if len(move) != 1 or not move.isalpha() or not (0 <= ord(move) - 65 < COLS):
            print("Invalid column. Try again.")
            continue

        col = ord(move) - 65
        if not place_checker(board, col, CHECKERS[current_player]):
            print("Column full. Try again.")
            continue

        # Check for win or draw
        if check_win(board, CHECKERS[current_player]):
            print_board(board)
            print(f"Player {CHECKERS[current_player]} won!")
            break
        if check_draw(board):
            print_board(board)
            print("It's a draw!")
            break

        current_player = (current_player + 1) % PLAYERS

# Start the game
if __name__ == "__main__":
    play_game()
