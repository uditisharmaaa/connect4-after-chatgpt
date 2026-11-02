import os
import random

ROWS = 6
COLS = 7
COLUMN_LABELS = ['A', 'B', 'C', 'D', 'E', 'F', 'G']

# Player tokens
PLAYER_TOKENS = ['X', 'O', 'V', 'H', 'M']


def clear_screen():
    os.system('clear')


def create_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]


def print_board(board):
    print("  " + " ".join(COLUMN_LABELS))
    for row in board:
        print("|" + "|".join(row) + "|")
    print("-" * (2 * COLS + 1))


def get_player_count():
    while True:
        try:
            count = int(input(f"Enter number of players (2-{len(PLAYER_TOKENS)}): "))
            if 2 <= count <= len(PLAYER_TOKENS):
                return count
            else:
                print(f"Please enter a number between 2 and {len(PLAYER_TOKENS)}.")
        except ValueError:
            print("Invalid input. Please enter a number.")


def get_move(player_token):
    while True:
        move = input(f"Player {player_token}, choose a column ({'/'.join(COLUMN_LABELS)}): ").upper()
        if move in COLUMN_LABELS:
            return COLUMN_LABELS.index(move)
        else:
            print(f"Invalid column. Please choose from {', '.join(COLUMN_LABELS)}.")


def is_valid_move(board, col):
    return board[0][col] == ' '  # Top cell empty means column not full


def make_move(board, col, token):
    for row in reversed(range(ROWS)):
        if board[row][col] == ' ':
            board[row][col] = token
            return row, col


def check_win(board, token, row, col):
    directions = [
        [(0, 1), (0, -1)],    # Horizontal
        [(1, 0), (-1, 0)],    # Vertical
        [(1, 1), (-1, -1)],   # Diagonal /
        [(1, -1), (-1, 1)]    # Diagonal \
    ]

    for direction in directions:
        count = 1
        for dr, dc in direction:
            r, c = row, col
            while True:
                r += dr
                c += dc
                if 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == token:
                    count += 1
                else:
                    break
        if count >= 4:
            return True
    return False


def check_draw(board):
    return all(board[0][col] != ' ' for col in range(COLS))


def main():
    clear_screen()
    print("Welcome to Connect 4!")
    player_count = get_player_count()
    players = PLAYER_TOKENS[:player_count]
    current_player = random.choice(players)

    board = create_board()
    game_over = False

    while not game_over:
        clear_screen()
        print_board(board)
        print(f"Current player: {current_player}")

        col = get_move(current_player)
        if not is_valid_move(board, col):
            print(f"Column {COLUMN_LABELS[col]} is full. Try another column.")
            input("Press Enter to continue...")
            continue

        row, _ = make_move(board, col, current_player)
        if check_win(board, current_player, row, col):
            clear_screen()
            print_board(board)
            print(f"Player {current_player} wins! Congratulations!")
            game_over = True
        elif check_draw(board):
            clear_screen()
            print_board(board)
            print("Game is a draw!")
            game_over = True
        else:
            # Next player's turn
            current_index = players.index(current_player)
            current_player = players[(current_index + 1) % player_count]

    print("Thanks for playing!")


if __name__ == "__main__":
    main()
