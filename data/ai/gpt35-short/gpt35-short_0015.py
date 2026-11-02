import os
import random

# Constants
ROWS = 6
COLS = 7
COLUMN_LABELS = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
PLAYER_MARKERS = ['X', 'O', 'V', 'H', 'M']  # up to 5 players

def clear_screen():
    os.system('clear')

def create_board():
    # Create empty board (list of lists) filled with spaces
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    # Print column labels
    print('  ' + '   '.join(COLUMN_LABELS))
    # Print board rows from top to bottom
    for row in board:
        print('| ' + ' | '.join(row) + ' |')
    print('-' * (COLS * 4 + 1))  # Bottom border

def get_num_players():
    while True:
        try:
            n = int(input("Enter number of players (2-5): "))
            if 2 <= n <= 5:
                return n
            else:
                print("Please enter a number between 2 and 5.")
        except ValueError:
            print("Invalid input! Please enter an integer.")

def get_player_move(player):
    while True:
        move = input(f"Player {player} ({player_markers[player]}), choose a column ({', '.join(COLUMN_LABELS)}): ").upper()
        if move in COLUMN_LABELS:
            col_idx = COLUMN_LABELS.index(move)
            return col_idx
        else:
            print(f"Invalid column! Please choose from {', '.join(COLUMN_LABELS)}.")

def is_valid_move(board, col):
    # Move is valid if top row in the chosen col is empty
    return board[0][col] == ' '

def make_move(board, col, marker):
    # Place marker in lowest empty spot in the chosen column
    for row in reversed(range(ROWS)):
        if board[row][col] == ' ':
            board[row][col] = marker
            return row, col

def check_win(board, row, col, marker):
    # Directions: horizontal, vertical, diag1 (/), diag2 (\)
    directions = [
        [(0,1), (0,-1)],   # horizontal
        [(1,0), (-1,0)],   # vertical
        [(1,1), (-1,-1)],  # diagonal down-right and up-left
        [(1,-1), (-1,1)]   # diagonal down-left and up-right
    ]

    for direction in directions:
        count = 1  # counts the placed marker itself
        for dr, dc in direction:
            r, c = row, col
            while True:
                r += dr
                c += dc
                if 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == marker:
                    count += 1
                else:
                    break
        if count >= 4:
            return True
    return False

def check_draw(board):
    # If top row is full, the board is full (draw)
    return all(space != ' ' for space in board[0])

def play_game():
    clear_screen()
    print("Welcome to Connect 4!")
    num_players = get_num_players()
    global player_markers
    player_markers = PLAYER_MARKERS[:num_players]

    # Create board
    board = create_board()

    # Randomly select first player index
    current_player = random.randint(0, num_players - 1)

    while True:
        clear_screen()
        print_board(board)
        print(f"Player turn: {player_markers[current_player]}")

        col = get_player_move(current_player)
        if not is_valid_move(board, col):
            print(f"Column {COLUMN_LABELS[col]} is full! Try again.")
            input("Press Enter to continue...")
            continue

        row, col = make_move(board, col, player_markers[current_player])

        # Check for win
        if check_win(board, row, col, player_markers[current_player]):
            clear_screen()
            print_board(board)
            print(f"Player {player_markers[current_player]} wins! Congratulations!")
            break

        # Check for draw
        if check_draw(board):
            clear_screen()
            print_board(board)
            print("The game is a draw! No more valid moves.")
            break

        # Next player's turn
        current_player = (current_player + 1) % num_players

    print("Game over! Thanks for playing.")

if __name__ == "__main__":
    play_game()
