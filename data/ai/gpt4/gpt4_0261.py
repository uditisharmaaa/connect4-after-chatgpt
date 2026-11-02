import os
import random

# Constants
ROWS = 6
COLS = 7
MAX_PLAYERS = 5
PLAYERS = ["X", "O", "V", "H", "M"][:2]  # Adjust for 2 players

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    os.system('clear')
    header = "  " + "   ".join(chr(65 + i) for i in range(len(board[0])))
    separator = "+---" * len(board[0]) + "+"
    print(header)
    for row in board:
        print(separator)
        print("| " + " | ".join(row) + " |")
    print(separator)

def is_valid_input(col, board):
    if not col.isalpha() or len(col) != 1:
        return False
    idx = ord(col.upper()) - 65
    return 0 <= idx < len(board[0]) and board[0][idx] == " "

def get_column_index(player_input):
    return ord(player_input.upper()) - 65

def drop_checker(board, col, checker):
    for row in reversed(board):
        if row[col] == " ":
            row[col] = checker
            return

def check_winner(board, checker):
    def check_direction(r, c, dr, dc):
        count = 0
        for i in range(4):
            nr, nc = r + dr * i, c + dc * i
            if 0 <= nr < ROWS and 0 <= nc < COLS and board[nr][nc] == checker:
                count += 1
            else:
                break
        return count == 4

    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] == checker:
                if any(check_direction(r, c, dr, dc) for dr, dc in [(0, 1), (1, 0), (1, 1), (1, -1)]):
                    return True
    return False

def board_full(board):
    return all(cell != " " for row in board for cell in row)

def main():
    board = create_board(ROWS, COLS)
    players = PLAYERS
    current_player = random.choice(players)
    print_board(board)

    while True:
        print(f"Player {current_player}, please enter a column: ")
        user_input = input().strip()

        if not is_valid_input(user_input, board):
            print("Invalid input. Try again.")
            continue

        col_idx = get_column_index(user_input)
        drop_checker(board, col_idx, current_player)
        print_board(board)

        if check_winner(board, current_player):
            print(f"Player {current_player} won!")
            break

        if board_full(board):
            print("It's a draw!")
            break

        current_player = players[(players.index(current_player) + 1) % len(players)]

if __name__ == "__main__":
    main()
