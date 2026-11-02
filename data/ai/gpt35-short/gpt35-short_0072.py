import os
import random

# Constants
ROWS = 6
COLS = 7
COLUMNS_LABELS = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
TOKENS = ['X', 'O', 'V', 'H', 'M']  # Up to 5 players

def clear_screen():
    os.system('clear')

def create_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    clear_screen()
    print("  " + " ".join(COLUMNS_LABELS))
    for row in board:
        print("|" + "|".join(row) + "|")
    print("-" * (COLS * 2 + 1))

def get_valid_columns(board):
    valid_cols = []
    for c in range(COLS):
        if board[0][c] == ' ':
            valid_cols.append(COLUMNS_LABELS[c])
    return valid_cols

def column_to_index(char):
    char = char.upper()
    if char in COLUMNS_LABELS:
        return COLUMNS_LABELS.index(char)
    return -1

def drop_token(board, col, token):
    for row in range(ROWS-1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = token
            return row, col
    return -1, -1  # Should not happen if validated

def check_win(board, row, col, token):
    directions = [
        (0, 1),   # horizontal
        (1, 0),   # vertical
        (1, 1),   # diagonal down-right
        (1, -1),  # diagonal down-left
    ]
    for dr, dc in directions:
        count = 1
        # Check in positive direction
        r, c = row + dr, col + dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == token:
            count += 1
            r += dr
            c += dc
        # Check in negative direction
        r, c = row - dr, col - dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == token:
            count += 1
            r -= dr
            c -= dc
        if count >= 4:
            return True
    return False

def check_draw(board):
    for c in range(COLS):
        if board[0][c] == ' ':
            return False
    return True

def get_num_players():
    while True:
        try:
            n = int(input("Enter number of players (2-5): "))
            if 2 <= n <= 5:
                return n
            print("Number of players must be between 2 and 5.")
        except ValueError:
            print("Please enter a valid integer.")

def main():
    num_players = get_num_players()
    players = TOKENS[:num_players]
    board = create_board()
    current_idx = random.randint(0, num_players - 1)

    while True:
        print_board(board)
        current_player = players[current_idx]
        valid_cols = get_valid_columns(board)

        print(f"Players: {', '.join(players)}")
        print(f"Current player: {current_player}")
        print(f"Valid columns: {', '.join(valid_cols)}")

        move = input(f"Player {current_player}, choose column (A-G): ").strip().upper()
        if move not in valid_cols:
            print("Invalid column or column full. Try again.")
            continue

        col = column_to_index(move)
        row, col = drop_token(board, col, current_player)

        if check_win(board, row, col, current_player):
            print_board(board)
            print(f"Player {current_player} wins!")
            break

        if check_draw(board):
            print_board(board)
            print("Game ends in a draw.")
            break

        current_idx = (current_idx + 1) % num_players

if __name__ == "__main__":
    main()
