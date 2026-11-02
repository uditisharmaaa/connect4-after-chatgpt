import os
import random
import string

# Constants
BOARD_ROWS = 6
BOARD_COLS = 7
MIN_PLAYERS = 2
MAX_PLAYERS = 5
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def create_board():
    """Create a 2D board with given dimensions and initialize with whitespaces."""
    board = [[' ' for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]
    return board

def print_board(board, current_player):
    """Print the current state of the board."""
    os.system('clear')
    print('  ' + '   '.join(string.ascii_uppercase[:BOARD_COLS]))
    for row in board:
        print('+---' * BOARD_COLS + '+')
        print('|   ' * BOARD_COLS + '|')
        print('| ' + ' | '.join(row) + ' |')
        print('|   ' * BOARD_COLS + '|')
    print('+---' * BOARD_COLS + '+')
    print(f"Player {current_player}, please enter a column: ")

def validate_input(input_str):
    """Validate the user input."""
    if len(input_str)!= 1 or not input_str.isalpha():
        return False
    if input_str.upper() < 'A' or input_str.upper() > chr(64 + BOARD_COLS):
        return False
    return True

def get_player_move(board, player):
    """Get the player's move and validate the input."""
    while True:
        input_str = input().strip().upper()
        if validate_input(input_str):
            col_idx = ord(input_str) - 65
            if board[0][col_idx]!= ' ':
                print("Column is full, please choose another column.")
                continue
            for row_idx in range(BOARD_ROWS - 1, -1, -1):
                if board[row_idx][col_idx] == ' ':
                    board[row_idx][col_idx] = player
                    break
            break
        else:
            print("Invalid input, please enter a letter between A and", chr(64 + BOARD_COLS))

def check_win(board, player):
    """Check for a win."""
    # Check horizontal locations for win
    for row_idx in range(BOARD_ROWS):
        for col_idx in range(BOARD_COLS - 3):
            if board[row_idx][col_idx] == player and board[row_idx][col_idx + 1] == player and board[row_idx][col_idx + 2] == player and board[row_idx][col_idx + 3] == player:
                return True

    # Check vertical locations for win
    for row_idx in range(BOARD_ROWS - 3):
        for col_idx in range(BOARD_COLS):
            if board[row_idx][col_idx] == player and board[row_idx + 1][col_idx] == player and board[row_idx + 2][col_idx] == player and board[row_idx + 3][col_idx] == player:
                return True

    # Check positively sloped diagonals
    for row_idx in range(BOARD_ROWS - 3):
        for col_idx in range(BOARD_COLS - 3):
            if board[row_idx][col_idx] == player and board[row_idx + 1][col_idx + 1] == player and board[row_idx + 2][col_idx + 2] == player and board[row_idx + 3][col_idx + 3] == player:
                return True

    # Check negatively sloped diagonals
    for row_idx in range(3, BOARD_ROWS):
        for col_idx in range(BOARD_COLS - 3):
            if board[row_idx][col_idx] == player and board[row_idx - 1][col_idx + 1] == player and board[row_idx - 2][col_idx + 2] == player and board[row_idx - 3][col_idx + 3] == player:
                return True

    return False

def check_draw(board):
    """Check for a draw."""
    for row_idx in range(BOARD_ROWS):
        for col_idx in range(BOARD_COLS):
            if board[row_idx][col_idx] == ' ':
                return False
    return True

def main():
    num_players = 2
    players = CHECKERS[:num_players]
    board = create_board()
    current_player_idx = random.randint(0, num_players - 1)
    while True:
        print_board(board, players[current_player_idx])
        get_player_move(board, players[current_player_idx])
        if check_win(board, players[current_player_idx]):
            print_board(board, players[current_player_idx])
            print("Player", players[current_player_idx], "won!")
            break
        if check_draw(board):
            print_board(board, players[current_player_idx])
            print("It's a draw!")
            break
        current_player_idx = (current_player_idx + 1) % num_players

if __name__ == "__main__":
    main()
