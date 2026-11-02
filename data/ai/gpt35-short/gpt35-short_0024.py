import os
import random

ROWS = 6
COLS = 7
COLUMN_LABELS = "ABCDEFG"
PLAYERS = ['X', 'O', 'V', 'H', 'M']  # Max 5 players
MIN_PLAYERS = 2
MAX_PLAYERS = 5

def clear_screen():
    os.system('clear')

def create_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    print(" " + " ".join(COLUMN_LABELS))
    for row in board:
        print("|" + "|".join(row) + "|")
    print("-" * (COLS * 2 + 1))

def get_valid_column(board):
    while True:
        choice = input("Choose a column (A-G): ").upper()
        if choice not in COLUMN_LABELS:
            print("Invalid column. Please choose a letter A-G.")
            continue

        col = COLUMN_LABELS.index(choice)
        # Check if the column is full
        if board[0][col] != ' ':
            print("That column is full. Choose a different one.")
            continue

        return col

def drop_piece(board, col, player):
    # Start from bottom row and find the first empty spot
    for row in range(ROWS-1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = player
            return row, col

def check_win(board, player, row, col):
    # Directions: horizontal, vertical, diag \, diag /
    directions = [
        [(0,1), (0,-1)],      # horizontal
        [(1,0), (-1,0)],      # vertical
        [(1,1), (-1,-1)],     # diag '\'
        [(1,-1), (-1,1)]      # diag '/'
    ]
    for direction in directions:
        count = 1  # Count the current piece
        for dr, dc in direction:
            r, c = row, col
            while True:
                r += dr
                c += dc
                if 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == player:
                    count += 1
                else:
                    break
        if count >= 4:
            return True
    return False

def board_full(board):
    return all(board[0][c] != ' ' for c in range(COLS))

def choose_number_of_players():
    while True:
        try:
            n = int(input(f"Enter number of players ({MIN_PLAYERS}-{MAX_PLAYERS}): "))
            if MIN_PLAYERS <= n <= MAX_PLAYERS:
                return n
            else:
                print(f"Please enter a number between {MIN_PLAYERS} and {MAX_PLAYERS}.")
        except ValueError:
            print("Invalid input. Enter a number.")

def main():
    clear_screen()
    print("Welcome to Connect 4!")
    
    num_players = choose_number_of_players()
    players = PLAYERS[:num_players]
    random.shuffle(players)  # Shuffle to randomize order
    print(f"Players: {', '.join(players)}")
    print(f"First player: {players[0]}")

    board = create_board()
    current_player_index = 0

    while True:
        clear_screen()
        print_board(board)
        current_player = players[current_player_index]
        print(f"Player {current_player}'s turn.")
        col = get_valid_column(board)
        row, col = drop_piece(board, col, current_player)

        if check_win(board, current_player, row, col):
            clear_screen()
            print_board(board)
            print(f"Player {current_player} wins! Congratulations!")
            break

        if board_full(board):
            clear_screen()
            print_board(board)
            print("The game is a draw! No more moves possible.")
            break

        current_player_index = (current_player_index + 1) % num_players

if __name__ == "__main__":
    main()
