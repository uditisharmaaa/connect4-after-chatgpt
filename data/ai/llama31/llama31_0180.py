import os
import random

# Constants
NUM_ROWS = 6
NUM_COLS = 7
MAX_PLAYERS = 5
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def create_board():
    """Create an empty Connect 4 board."""
    board = []
    for _ in range(NUM_ROWS):
        row = [' ']*NUM_COLS
        board.append(row)
    return board

def print_board(board):
    """Print the Connect 4 board."""
    print('  ' + ' '.join([chr(65 + i) for i in range(NUM_COLS)]))
    print('+---'*NUM_COLS + '+')
    for row in board:
        print('| ' + ' | '.join(row) + ' |')
        print('+---'*NUM_COLS + '+')

def get_player_checkers(num_players):
    """Get the checkers for the players."""
    return CHECKERS[:num_players]

def get_first_player(num_players):
    """Randomly select the first player."""
    return random.randint(0, num_players - 1)

def get_valid_move(board, col):
    """Get the row where the checker should be placed."""
    for row in range(NUM_ROWS - 1, -1, -1):
        if board[row][col] == ' ':
            return row
    return -1

def place_checker(board, row, col, checker):
    """Place the checker on the board."""
    board[row][col] = checker

def check_win(board, row, col, checker):
    """Check if the player has won."""
    # Check horizontal
    count = 0
    for c in range(NUM_COLS):
        if board[row][c] == checker:
            count += 1
            if count == 4:
                return True
        else:
            count = 0

    # Check vertical
    count = 0
    for r in range(NUM_ROWS):
        if board[r][col] == checker:
            count += 1
            if count == 4:
                return True
        else:
            count = 0

    # Check diagonal (top-left to bottom-right)
    count = 0
    r = row
    c = col
    while r >= 0 and c >= 0:
        if board[r][c] == checker:
            count += 1
            if count == 4:
                return True
        else:
            count = 0
        r -= 1
        c -= 1
    count = 0
    r = row + 1
    c = col + 1
    while r < NUM_ROWS and c < NUM_COLS:
        if board[r][c] == checker:
            count += 1
            if count == 4:
                return True
        else:
            count = 0
        r += 1
        c += 1

    # Check diagonal (bottom-left to top-right)
    count = 0
    r = row
    c = col
    while r < NUM_ROWS and c >= 0:
        if board[r][c] == checker:
            count += 1
            if count == 4:
                return True
        else:
            count = 0
        r += 1
        c -= 1
    count = 0
    r = row - 1
    c = col + 1
    while r >= 0 and c < NUM_COLS:
        if board[r][c] == checker:
            count += 1
            if count == 4:
                return True
        else:
            count = 0
        r -= 1
        c += 1

    return False

def check_draw(board):
    """Check if the game is a draw."""
    for row in board:
        for col in row:
            if col == ' ':
                return False
    return True

def game():
    """Play the Connect 4 game."""
    num_players = 2
    players = get_player_checkers(num_players)
    current_player = get_first_player(num_players)
    board = create_board()
    os.system('clear')
    print_board(board)

    while True:
        print(f"Player {players[current_player]}, please enter a column:")
        col = input().upper()
        if not col.isalpha() or not 65 <= ord(col) <= 65 + NUM_COLS - 1:
            print("Invalid input. Please enter a letter between A and", chr(65 + NUM_COLS - 1))
            continue

        col = ord(col) - 65
        row = get_valid_move(board, col)
        if row == -1:
            print("Column is full. Please choose another column.")
            continue

        place_checker(board, row, col, players[current_player])
        os.system('clear')
        print_board(board)
        if check_win(board, row, col, players[current_player]):
            print(f"Player {players[current_player]} won!")
            break
        elif check_draw(board):
            print("It's a draw!")
            break
        current_player = (current_player + 1) % num_players

game()
