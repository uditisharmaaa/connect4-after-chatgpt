import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']  # supports up to 5 players
WIN_COUNT = 4

def clear_screen():
    os.system('clear')

def create_board():
    return [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    clear_screen()
    # Print column headers
    headers = [chr(ord('A') + i) for i in range(COLUMNS)]
    print("  " + "   ".join(headers))
    # Print each row with the format described
    line = "+---" * COLUMNS + "+"
    for row in board:
        print(line)
        row_str = "| " + " | ".join(row) + " |"
        print(row_str)
    print(line)

def input_column(player):
    while True:
        col = input(f"Player {player}, please enter a column: ").strip().upper()
        if len(col) != 1:
            print("Invalid input. Please enter a single letter corresponding to a column.")
            continue
        if not ('A' <= col <= chr(ord('A') + COLUMNS -1)):
            print("Invalid column letter. Please enter a valid column.")
            continue
        return ord(col) - ord('A')

def place_checker(board, col, checker):
    # Find lowest empty spot in the column
    for row in range(ROWS-1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return row
    return -1  # Column full

def check_win(board, row, col, checker):
    # Directions: horizontal, vertical, diagonal /
    directions = [
        (0, 1),  # horizontal right
        (1, 0),  # vertical down
        (1, 1),  # diagonal down right
        (1, -1), # diagonal down left
    ]

    for dr, dc in directions:
        count = 1  # counting the current checker
        # Check in the positive direction
        r, c = row + dr, col + dc
        while 0 <= r < ROWS and 0 <= c < COLUMNS and board[r][c] == checker:
            count += 1
            r += dr
            c += dc
        # Check in the negative direction
        r, c = row - dr, col - dc
        while 0 <= r < ROWS and 0 <= c < COLUMNS and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc
        if count >= WIN_COUNT:
            return True
    return False

def board_full(board):
    for col in range(COLUMNS):
        if board[0][col] == " ":
            return False
    return True

def main():
    board = create_board()
    player_order = list(range(PLAYERS))
    random_start = random.choice(player_order)
    players_cycle = player_order[random_start:] + player_order[:random_start]
    running = True

    print_board(board)
    current_player_index = 0

    while running:
        player_num = players_cycle[current_player_index]
        checker = CHECKERS[player_num]
        col = input_column(checker)
        placed_row = place_checker(board, col, checker)
        if placed_row == -1:
            # Column full; player loses turn
            print(f"Column {chr(ord('A')+col)} is full. Player {checker} loses the turn.")
            input("Press Enter to continue...")
            current_player_index = (current_player_index + 1) % PLAYERS
            print_board(board)
            continue

        print_board(board)

        if check_win(board, placed_row, col, checker):
            print(f"Player {checker} won!")
            running = False
            break

        if board_full(board):
            print("The game is a draw!")
            running = False
            break

        current_player_index = (current_player_index + 1) % PLAYERS

if __name__ == "__main__":
    main()
