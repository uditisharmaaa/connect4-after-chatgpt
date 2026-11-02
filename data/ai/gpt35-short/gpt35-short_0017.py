import os
import random

ROWS = 6
COLS = 7
COLUMNS_LABELS = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
PLAYERS = ['X', 'O', 'V', 'H', 'M']

def clear_screen():
    os.system('clear')

def create_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    print(" " + " ".join(COLUMNS_LABELS))
    for row in board:
        print("|" + "|".join(row) + "|")
    print("-" * (COLS * 2 + 1))

def get_num_players():
    while True:
        try:
            n = int(input(f"Enter number of players (2-5): "))
            if 2 <= n <= 5:
                return n
            else:
                print("Please enter a number between 2 and 5.")
        except ValueError:
            print("That's not a number!")

def get_column_choice(board, current_player):
    while True:
        choice = input(f"Player {current_player}, choose a column (A-G): ").upper()
        if choice in COLUMNS_LABELS:
            col = COLUMNS_LABELS.index(choice)
            # Check if column is full
            if board[0][col] == ' ':
                return col
            else:
                print("That column is full. Try again.")
        else:
            print("Invalid column. Please choose A-G.")

def place_piece(board, col, player):
    for row in reversed(range(ROWS)):
        if board[row][col] == ' ':
            board[row][col] = player
            return row, col

def check_win(board, player):
    # Check horizontal
    for r in range(ROWS):
        for c in range(COLS - 3):
            if all(board[r][c+i] == player for i in range(4)):
                return True
    # Check vertical
    for c in range(COLS):
        for r in range(ROWS - 3):
            if all(board[r+i][c] == player for i in range(4)):
                return True
    # Check diagonal /
    for r in range(3, ROWS):
        for c in range(COLS - 3):
            if all(board[r - i][c + i] == player for i in range(4)):
                return True
    # Check diagonal \
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            if all(board[r + i][c + i] == player for i in range(4)):
                return True
    return False

def check_draw(board):
    return all(board[0][c] != ' ' for c in range(COLS))

def main():
    clear_screen()
    num_players = get_num_players()
    players = PLAYERS[:num_players]

    current_player_index = random.randint(0, num_players - 1)
    board = create_board()

    while True:
        clear_screen()
        print_board(board)
        current_player = players[current_player_index]

        col = get_column_choice(board, current_player)
        place_piece(board, col, current_player)

        if check_win(board, current_player):
            clear_screen()
            print_board(board)
            print(f"Player {current_player} wins!")
            break

        if check_draw(board):
            clear_screen()
            print_board(board)
            print("It's a draw!")
            break

        current_player_index = (current_player_index + 1) % num_players

if __name__ == "__main__":
    main()
