import random
import os

ROWS = 6
COLS = 7
NUM_PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M'][:NUM_PLAYERS]

def print_board(board):
    os.system('clear')
    print("  " + "   ".join(chr(i + ord('A')) for i in range(COLS)))
    print("+---" * COLS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLS + "+")

def initialize_board(rows, cols):
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def is_valid_move(col, board):
    return col >= 0 and col < COLS and board[0][col] == ' '

def make_move(player, col, board):
    for row in reversed(board):
        if row[col] == ' ':
            row[col] = player
            return

def check_for_win(board, player):
    # Check horizontals
    for row in board:
        for i in range(COLS - 3):
            if all(row[i + j] == player for j in range(4)):
                return True
    # Check verticals
    for col in range(COLS):
        for row in range(ROWS - 3):
            if all(board[row + i][col] == player for i in range(4)):
                return True
    # Check diagonals \
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if all(board[row + i][col + i] == player for i in range(4)):
                return True
    # Check diagonals /
    for row in range(ROWS - 3):
        for col in range(3, COLS):
            if all(board[row + i][col - i] == player for i in range(4)):
                return True
    return False

def is_draw(board):
    return all(cell != ' ' for row in board for cell in row)

def play_game():
    board = initialize_board(ROWS, COLS)
    current_turn = random.randint(0, NUM_PLAYERS - 1)
    while True:
        print_board(board)
        current_player = CHECKERS[current_turn]
        move = input(f"Player {current_player}, please enter a column: ").strip().upper()
        if move.isalpha() and len(move) == 1:
            col = ord(move) - ord('A')
            if is_valid_move(col, board):
                make_move(current_player, col, board)
                if check_for_win(board, current_player):
                    print_board(board)
                    print(f"Player {current_player} won!")
                    break
                elif is_draw(board):
                    print_board(board)
                    print("It's a draw!")
                    break
                current_turn = (current_turn + 1) % NUM_PLAYERS
            else:
                print("Column full, you lose this turn.")
        else:
            print("Invalid input, please enter a valid column letter.")

play_game()
