import os
import random

# Constants for the game
ROWS = 6
COLUMNS = 7
PLAYERS = ['X', 'O', 'V', 'H', 'M']  # Player symbols
NUM_PLAYERS = 3  # Set number of players (between 2 and 5)
PLAYER_NAMES = PLAYERS[:NUM_PLAYERS]

def clear_screen():
    os.system('clear')  # Use 'cls' for Windows

def create_board():
    return [[' ' for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    print('  '.join('ABCDEFG'))
    for row in board:
        print(' '.join(row))
    print()

def is_valid_column(board, col):
    return board[0][col] == ' '

def drop_piece(board, col, piece):
    for row in reversed(board):
        if row[col] == ' ':
            row[col] = piece
            return

def check_winner(board, piece):
    # Check horizontal locations for win
    for c in range(COLUMNS - 3):
        for r in range(ROWS):
            if board[r][c] == piece and board[r][c + 1] == piece and board[r][c + 2] == piece and board[r][c + 3] == piece:
                return True

    # Check vertical locations for win
    for c in range(COLUMNS):
        for r in range(ROWS - 3):
            if board[r][c] == piece and board[r + 1][c] == piece and board[r + 2][c] == piece and board[r + 3][c] == piece:
                return True

    # Check positively sloped diagonals
    for c in range(COLUMNS - 3):
        for r in range(ROWS - 3):
            if board[r][c] == piece and board[r + 1][c + 1] == piece and board[r + 2][c + 2] == piece and board[r + 3][c + 3] == piece:
                return True

    # Check negatively sloped diagonals
    for c in range(COLUMNS - 3):
        for r in range(3, ROWS):
            if board[r][c] == piece and board[r - 1][c + 1] == piece and board[r - 2][c + 2] == piece and board[r - 3][c + 3] == piece:
                return True

    return False

def is_full(board):
    return all(cell != ' ' for row in board for cell in row)

def play_game():
    board = create_board()
    clear_screen()

    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    game_over = False

    while not game_over:
        print_board(board)
        current_player = PLAYER_NAMES[current_player_index]
        print(f"Player {current_player}'s turn")

        # Input validation
        input_valid = False
        col = None
        while not input_valid:
            try:
                col_input = input("Select a column (A-G): ").upper()
                if col_input not in "ABCDEFG" or len(col_input) != 1:
                    raise ValueError
                col = ord(col_input) - ord('A')
                if not is_valid_column(board, col):
                    raise ValueError
                input_valid = True
            except ValueError:
                print("Invalid input. Please try again.")

        drop_piece(board, col, current_player)

        if check_winner(board, current_player):
            clear_screen()
            print_board(board)
            print(f"Player {current_player} wins!")
            game_over = True
        elif is_full(board):
            clear_screen()
            print_board(board)
            print("The game is a draw!")
            game_over = True

        current_player_index = (current_player_index + 1) % NUM_PLAYERS
        clear_screen()

if __name__ == "__main__":
    play_game()
