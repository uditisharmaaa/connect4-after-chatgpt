import os
import random

# Constant variables
BOARD_ROWS = 6
BOARD_COLS = 7
MAX_PLAYERS = 5
PLAYERS = ['X', 'O', 'V', 'H', 'M']

def create_board():
    """
    Create a 2D board with all elements initialized to whitespaces.
    """
    return [[' ' for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]

def print_board(board, player_turn):
    """
    Print the current state of the board.
    """
    os.system('clear')
    print('  A   B   C   D   E   F   G')
    for row in board:
        print('+---+---+---+---+---+---+---+')
        print('| ' + ' | '.join(row) + ' |')
    print('+---+---+---+---+---+---+---+')
    print(f"Player {PLAYERS[player_turn]}, please enter a column:")

def validate_input(col):
    """
    Check if the input is a valid column letter.
    """
    if not col.isalpha():
        return False
    if col.upper() < 'A' or col.upper() > chr(64 + BOARD_COLS):
        return False
    return True

def place_checker(board, col, player):
    """
    Place a checker in the lowest available space within the column.
    """
    for row in reversed(board):
        if row[col] == ' ':
            row[col] = PLAYERS[player]
            return

def check_win(board, player):
    """
    Check for a win by checking all possible winning combinations.
    """
    # Check horizontal locations for win
    for c in range(BOARD_COLS-3):
        for r in range(BOARD_ROWS):
            if board[r][c] == PLAYERS[player] and board[r][c+1] == PLAYERS[player] and board[r][c+2] == PLAYERS[player] and board[r][c+3] == PLAYERS[player]:
                return True

    # Check vertical locations for win
    for c in range(BOARD_COLS):
        for r in range(BOARD_ROWS-3):
            if board[r][c] == PLAYERS[player] and board[r+1][c] == PLAYERS[player] and board[r+2][c] == PLAYERS[player] and board[r+3][c] == PLAYERS[player]:
                return True

    # Check positively sloped diagonals
    for c in range(BOARD_COLS-3):
        for r in range(BOARD_ROWS-3):
            if board[r][c] == PLAYERS[player] and board[r+1][c+1] == PLAYERS[player] and board[r+2][c+2] == PLAYERS[player] and board[r+3][c+3] == PLAYERS[player]:
                return True

    # Check negatively sloped diagonals
    for c in range(BOARD_COLS-3):
        for r in range(3, BOARD_ROWS):
            if board[r][c] == PLAYERS[player] and board[r-1][c+1] == PLAYERS[player] and board[r-2][c+2] == PLAYERS[player] and board[r-3][c+3] == PLAYERS[player]:
                return True

def check_draw(board):
    """
    Check if the board is full (i.e., a draw).
    """
    for row in board:
        if ' ' in row:
            return False
    return True

def main():
    num_players = 2
    board = create_board()
    player_turn = random.randint(0, num_players-1)

    while True:
        print_board(board, player_turn)
        col = input().upper()
        if not validate_input(col):
            print("Invalid input. Please try again.")
            continue
        col = ord(col) - 65
        place_checker(board, col, player_turn)
        if check_win(board, player_turn):
            print_board(board, player_turn)
            print(f"Player {PLAYERS[player_turn]} won!")
            break
        if check_draw(board):
            print_board(board, player_turn)
            print("It's a draw!")
            break
        player_turn = (player_turn + 1) % num_players

if __name__ == "__main__":
    main()
