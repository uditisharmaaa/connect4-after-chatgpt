import random
import os

ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]  # Supports up to 5 players

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    os.system('clear')
    header = "  " + "   ".join(chr(65 + i) for i in range(len(board[0])))
    print(header)
    print("+---" * len(board[0]) + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * len(row) + "+")

def is_valid_move(col, board):
    return 0 <= col < len(board[0]) and board[0][col] == " "

def place_checker(col, player, board):
    for row in reversed(board):
        if row[col] == " ":
            row[col] = CHECKERS[player]
            break

def check_win(board, player):
    check_lines = (
        [(0, 1), (0, -1)],  # Horizontal
        [(1, 0), (-1, 0)],  # Vertical
        [(1, 1), (-1, -1)], # Diagonal /
        [(1, -1), (-1, 1)]  # Diagonal \
    )

    def count_consecutive(row, col, direction):
        count = 0
        r, c = row, col
        while (
            0 <= r < len(board) and
            0 <= c < len(board[0]) and
            board[r][c] == CHECKERS[player]
        ):
            count += 1
            r += direction[0]
            c += direction[1]
        return count
    
    for r in range(len(board)):
        for c in range(len(board[0])):
            if board[r][c] == CHECKERS[player]:
                for direction in check_lines:
                    total = sum(count_consecutive(r, c, d) for d in direction) - 1
                    if total >= 4:
                        return True
    return False

def is_draw(board):
    return all(square != " " for square in board[0])

def play_game():
    board = create_board(ROWS, COLS)
    current_player = random.randint(0, PLAYERS - 1)
    print_board(board)

    while True:
        col_input = input(f"Player {CHECKERS[current_player]}, please enter a column: ").strip().upper()
        if len(col_input) != 1 or not col_input.isalpha():
            print("Invalid input. Please enter a letter A-G.")
            continue
        
        col = ord(col_input) - 65
        if not is_valid_move(col, board):
            print("Invalid move. Please try again.")
            continue

        place_checker(col, current_player, board)
        print_board(board)

        if check_win(board, current_player):
            print(f"Player {CHECKERS[current_player]} won!")
            break

        if is_draw(board):
            print("The game is a draw!")
            break

        current_player = (current_player + 1) % PLAYERS

play_game()
