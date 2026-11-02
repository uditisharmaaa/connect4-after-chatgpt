import os
import random

# Constants
ROWS = 6
COLS = 7
COLUMN_LABELS = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
PLAYER_TOKENS = ['X', 'O', 'V', 'H', 'M']  # max 5 players

def clear_screen():
    os.system('clear')

def create_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    print("  " + " ".join(COLUMN_LABELS))
    for row in board:
        print("|" + "|".join(row) + "|")
    print("-" * (COLS * 2 + 1))

def is_valid_column(col_char):
    return col_char.upper() in COLUMN_LABELS

def get_column_index(col_char):
    return COLUMN_LABELS.index(col_char.upper())

def make_move(board, col, token):
    # Place token in lowest empty spot in the column
    for row in reversed(range(ROWS)):
        if board[row][col] == ' ':
            board[row][col] = token
            return row, col
    return None  # Column full

def check_win(board, token, last_row, last_col):
    # Check horizontal, vertical, and two diagonal directions for 4 in a row
    directions = [
        (0, 1),  # horizontal right
        (1, 0),  # vertical down
        (1, 1),  # diagonal down-right
        (1, -1), # diagonal down-left
    ]

    for dr, dc in directions:
        count = 1

        # Check in the positive direction
        r, c = last_row + dr, last_col + dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == token:
            count += 1
            r += dr
            c += dc

        # Check in the negative direction
        r, c = last_row - dr, last_col - dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == token:
            count += 1
            r -= dr
            c -= dc

        if count >= 4:
            return True

    return False

def is_draw(board):
    # If top row is full, no more moves
    return all(cell != ' ' for cell in board[0])

def get_number_of_players():
    while True:
        num = input("Enter number of players (2-5): ").strip()
        if num.isdigit() and 2 <= int(num) <= 5:
            return int(num)
        print("Invalid input. Please enter a number between 2 and 5.")

def get_player_move(player_token):
    while True:
        move = input(f"Player {player_token}, choose column (A-G): ").strip().upper()
        if is_valid_column(move):
            return get_column_index(move)
        print("Invalid column! Please enter a letter A-G.")

def main():
    num_players = get_number_of_players()
    players = PLAYER_TOKENS[:num_players]

    board = create_board()
    current_player_idx = random.randint(0, num_players - 1)

    while True:
        clear_screen()
        print_board(board)
        print(f"Players: {', '.join(players)}")
        print(f"Current turn: Player {players[current_player_idx]}")

        col = get_player_move(players[current_player_idx])
        move = make_move(board, col, players[current_player_idx])

        if move is None:
            print("That column is full! Try another.")
            input("Press Enter to continue...")
            continue

        last_row, last_col = move

        if check_win(board, players[current_player_idx], last_row, last_col):
            clear_screen()
            print_board(board)
            print(f"Player {players[current_player_idx]} wins! Congratulations!")
            break

        if is_draw(board):
            clear_screen()
            print_board(board)
            print("It's a draw! No more moves possible.")
            break

        # Next player's turn
        current_player_idx = (current_player_idx + 1) % num_players

    print("Game over.")

if __name__ == "__main__":
    main()
