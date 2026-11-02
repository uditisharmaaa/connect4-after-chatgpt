import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS_COUNT = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M'][:PLAYERS_COUNT]

# Create the board
def create_board(rows, cols):
    board = [[' ' for _ in range(cols)] for _ in range(rows)]
    return board

# Print the board
def print_board(board):
    os.system('clear')
    print("  " + "   ".join([chr(65 + i) for i in range(len(board[0]))]))
    print("+---" * len(board[0]) + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * len(board[0]) + "+")

# Check for win
def check_win(board, player):
    def check_dir(dx, dy):
        for x in range(COLS):
            for y in range(ROWS):
                if all(0 <= x + dx * i < COLS and 0 <= y + dy * i < ROWS and board[y + dy * i][x + dx * i] == player for i in range(4)):
                    return True
        return False

    return check_dir(1, 0) or check_dir(0, 1) or check_dir(1, 1) or check_dir(-1, 1)

# Check for draw
def check_draw(board):
    return all(board[0][c] != ' ' for c in range(COLS))

# Get valid player input
def get_valid_input():
    while True:
        move = input(f"Player {CHECKERS[current_player]}, please enter a column: ")
        if len(move) == 1 and 'A' <= move <= 'G' and board[0][ord(move) - ord('A')] == ' ':
            return ord(move) - ord('A')
        print("Invalid input. Please try again.")

# Play the game
def play_game():
    global current_player
    board = create_board(ROWS, COLS)
    current_player = random.choice(range(PLAYERS_COUNT))
    print_board(board)

    while True:
        col = get_valid_input()
        for row in range(ROWS - 1, -1, -1):
            if board[row][col] == ' ':
                board[row][col] = CHECKERS[current_player]
                break

        print_board(board)

        if check_win(board, CHECKERS[current_player]):
            print(f"Player {CHECKERS[current_player]} won!")
            break

        if check_draw(board):
            print("It's a draw!")
            break

        current_player = (current_player + 1) % PLAYERS_COUNT

play_game()
