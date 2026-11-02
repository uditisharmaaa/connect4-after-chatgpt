import os
import random

# Constants
ROWS = 6
COLS = 7
MAX_PLAYERS = 5
CHECKERS = ["X", "O", "V", "H", "M"]

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    os.system('clear')  # Clear the screen
    col_labels = "  " + "   ".join(chr(65 + i) for i in range(len(board[0])))
    print(col_labels)
    for row in board:
        print("+---" * len(row) + "+")
        print("| " + " | ".join(row) + " |")
    print("+---" * len(board[0]) + "+")

def is_valid_column(column, board):
    return column.isalpha() and len(column) == 1 and ord(column.upper()) in range(65, 65 + len(board[0]))

def is_column_full(board, col_idx):
    return all(row[col_idx] != " " for row in board)

def drop_checker(board, col_idx, checker):
    for row in reversed(board):
        if row[col_idx] == " ":
            row[col_idx] = checker
            return

def check_win(board, checker):
    rows, cols = len(board), len(board[0])

    def check_direction(r, c, dr, dc):
        count = 0
        for _ in range(4):
            if 0 <= r < rows and 0 <= c < cols and board[r][c] == checker:
                count += 1
                r += dr
                c += dc
            else:
                break
        return count == 4

    for r in range(rows):
        for c in range(cols):
            if board[r][c] == checker:
                if (check_direction(r, c, 0, 1) or  # Horizontal
                    check_direction(r, c, 1, 0) or  # Vertical
                    check_direction(r, c, 1, 1) or  # Diagonal /
                    check_direction(r, c, 1, -1)):  # Diagonal \
                    return True
    return False

def is_draw(board):
    return all(row[col] != " " for row in board for col in range(len(row)))

def main():
    # Setup
    board = create_board(ROWS, COLS)
    num_players = 2
    players = CHECKERS[:num_players]
    current_player = random.choice(players)

    print_board(board)

    while True:
        print(f"Player {current_player}, please enter a column: ", end="")
        column = input().strip().upper()

        if not is_valid_column(column, board):
            print("Invalid input. Please enter a valid column (A-G).")
            continue
        
        col_idx = ord(column) - 65

        if is_column_full(board, col_idx):
            print(f"Column {column} is full. Choose another column.")
            continue

        drop_checker(board, col_idx, current_player)
        print_board(board)

        if check_win(board, current_player):
            print(f"Player {current_player} won!")
            break

        if is_draw(board):
            print("The game is a draw!")
            break

        # Switch to the next player
        current_player_idx = players.index(current_player)
        current_player = players[(current_player_idx + 1) % len(players)]

if __name__ == "__main__":
    main()
