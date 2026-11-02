import os
import random

# Constants
ROWS = 6
COLS = 7
COLUMN_LABELS = 'ABCDEFG'
PLAYER_TOKENS = ['X', 'O', 'V', 'H', 'M']  # support 2 to 5 players

def clear_screen():
    os.system('clear')  # For Windows, use 'cls'

def create_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    print("  " + " ".join(COLUMN_LABELS))
    for row in board:
        print("|" + "|".join(row) + "|")
    print("-" * (COLS * 2 + 1))

def get_player_count():
    while True:
        try:
            count = int(input("Enter number of players (2-5): "))
            if 2 <= count <= 5:
                return count
            else:
                print("Please enter a number between 2 and 5.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def get_move(player_token):
    while True:
        move = input(f"Player {player_token}, choose a column (A-G): ").upper()
        if move in COLUMN_LABELS:
            return COLUMN_LABELS.index(move)
        else:
            print("Invalid column. Please select a column between A and G.")

def make_move(board, col, player_token):
    for row in reversed(range(ROWS)):
        if board[row][col] == ' ':
            board[row][col] = player_token
            return row, col
    return None  # Column full

def is_winning_move(board, row, col, player_token):
    # Directions: horizontal, vertical, diag1, diag2
    directions = [
        (0, 1), (1, 0), (1, 1), (1, -1)
    ]

    for dr, dc in directions:
        count = 1
        # Check forward
        r, c = row + dr, col + dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == player_token:
            count += 1
            r += dr
            c += dc
        # Check backward
        r, c = row - dr, col - dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == player_token:
            count += 1
            r -= dr
            c -= dc
        if count >= 4:
            return True
    return False

def is_draw(board):
    return all(board[0][col] != ' ' for col in range(COLS))

def main():
    clear_screen()
    print("Welcome to Connect 4!")

    player_count = get_player_count()
    players = PLAYER_TOKENS[:player_count]

    board = create_board()
    current_player_idx = random.randint(0, player_count - 1)

    while True:
        clear_screen()
        print_board(board)
        current_player = players[current_player_idx]
        print(f"Player {current_player}'s turn.")

        col = get_move(current_player)
        move_pos = make_move(board, col, current_player)

        if move_pos is None:
            print("That column is full. Try again.")
            input("Press Enter to continue...")
            continue

        row, col = move_pos

        if is_winning_move(board, row, col, current_player):
            clear_screen()
            print_board(board)
            print(f"Player {current_player} wins! Congratulations!")
            break

        if is_draw(board):
            clear_screen()
            print_board(board)
            print("It's a draw!")
            break

        current_player_idx = (current_player_idx + 1) % player_count

if __name__ == "__main__":
    main()
