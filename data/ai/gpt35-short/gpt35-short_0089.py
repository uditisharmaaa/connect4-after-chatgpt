import os
import random

ROWS = 6
COLS = 7
COLUMNS_LABELS = ['A', 'B', 'C', 'D', 'E', 'F', 'G']

# Players - use only as many as needed
PLAYERS = ['X', 'O', 'V', 'H', 'M']

def clear_screen():
    os.system('clear')

def create_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    print('  ' + ' '.join(COLUMNS_LABELS))
    for row in board:
        print('| ' + ' '.join(row) + ' |')
    print()

def get_column_index():
    while True:
        col = input("Choose a column (A-G): ").upper()
        if col in COLUMNS_LABELS:
            return COLUMNS_LABELS.index(col)
        else:
            print("Invalid column. Please enter a letter from A to G.")

def is_valid_column(board, col):
    return board[0][col] == ' '

def drop_piece(board, col, piece):
    for row in range(ROWS-1, -1, -1):  # from bottom row to top row
        if board[row][col] == ' ':
            board[row][col] = piece
            return row, col

def check_win(board, piece):
    # Check horizontal
    for r in range(ROWS):
        for c in range(COLS - 3):
            if all(board[r][c+i] == piece for i in range(4)):
                return True

    # Check vertical
    for c in range(COLS):
        for r in range(ROWS - 3):
            if all(board[r+i][c] == piece for i in range(4)):
                return True

    # Check diagonal down-right
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            if all(board[r+i][c+i] == piece for i in range(4)):
                return True

    # Check diagonal up-right
    for r in range(3, ROWS):
        for c in range(COLS - 3):
            if all(board[r-i][c+i] == piece for i in range(4)):
                return True
    return False

def board_full(board):
    return all(board[0][c] != ' ' for c in range(COLS))

def main():
    clear_screen()
    print("Welcome to Connect 4!")
    while True:
        try:
            num_players = int(input(f"Enter number of players (2-{len(PLAYERS)}): "))
            if 2 <= num_players <= len(PLAYERS):
                break
            else:
                print(f"Please enter a number between 2 and {len(PLAYERS)}.")
        except ValueError:
            print("That's not a valid number.")

    players = PLAYERS[:num_players]
    current_player_index = random.randint(0, num_players -1)

    board = create_board()

    while True:
        clear_screen()
        print_board(board)
        print(f"Player {players[current_player_index]}'s turn.")
        
        col = get_column_index()

        if not is_valid_column(board, col):
            print("That column is full. Try another one.")
            input("Press Enter to continue...")
            continue

        row, col = drop_piece(board, col, players[current_player_index])

        if check_win(board, players[current_player_index]):
            clear_screen()
            print_board(board)
            print(f"Player {players[current_player_index]} wins! Congratulations!")
            break

        if board_full(board):
            clear_screen()
            print_board(board)
            print("It's a draw!")
            break

        current_player_index = (current_player_index + 1) % num_players

    print("Game over.")

if __name__ == "__main__":
    main()
