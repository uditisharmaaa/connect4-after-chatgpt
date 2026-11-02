import os
import random

# Constants for the board dimensions and players
BOARD_ROWS = 6
BOARD_COLS = 7
MAX_PLAYERS = 5
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def create_board(rows, cols):
    """
    Creates a 2D board with the specified dimensions.
    """
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """
    Prints the current state of the board.
    """
    print('  A   B   C   D   E   F   G')
    for row in board:
        print('+---+---+---+---+---+---+---+')
        print('| ' + ' | '.join(row) + ' |')
    print('+---+---+---+---+---+---+---+')

def validate_input(input_str, board):
    """
    Validates the user input.
    """
    if not input_str.isalpha():
        print("Invalid input. Please enter a letter.")
        return False
    col = ord(input_str.upper()) - ord('A')
    if col < 0 or col >= BOARD_COLS:
        print("Invalid input. Column out of range.")
        return False
    for row in range(BOARD_ROWS - 1, -1, -1):
        if board[row][col] == ' ':
            return True
    print("Invalid input. Column is full.")
    return False

def place_checker(board, col, checker):
    """
    Places the checker at the correct location.
    """
    for row in range(BOARD_ROWS - 1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = checker
            break

def check_win(board, checker):
    """
    Checks for a win.
    """
    # Check horizontal locations for win
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS - 3):
            if board[row][col] == checker and board[row][col + 1] == checker and board[row][col + 2] == checker and board[row][col + 3] == checker:
                return True

    # Check vertical locations for win
    for col in range(BOARD_COLS):
        for row in range(BOARD_ROWS - 3):
            if board[row][col] == checker and board[row + 1][col] == checker and board[row + 2][col] == checker and board[row + 3][col] == checker:
                return True

    # Check positively sloped diagonals
    for row in range(BOARD_ROWS - 3):
        for col in range(BOARD_COLS - 3):
            if board[row][col] == checker and board[row + 1][col + 1] == checker and board[row + 2][col + 2] == checker and board[row + 3][col + 3] == checker:
                return True

    # Check negatively sloped diagonals
    for row in range(3, BOARD_ROWS):
        for col in range(BOARD_COLS - 3):
            if board[row][col] == checker and board[row - 1][col + 1] == checker and board[row - 2][col + 2] == checker and board[row - 3][col + 3] == checker:
                return True

    return False

def check_draw(board):
    """
    Checks for a draw.
    """
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == ' ':
                return False
    return True

def main():
    board = create_board(BOARD_ROWS, BOARD_COLS)
    num_players = 2
    players = CHECKERS[:num_players]
    current_player_index = random.randint(0, num_players - 1)
    os.system('clear')
    print_board(board)

    while True:
        current_player = players[current_player_index]
        print(f"Player {current_player}, please enter a column:")
        input_str = input().strip()
        if validate_input(input_str, board):
            col = ord(input_str.upper()) - ord('A')
            place_checker(board, col, current_player)
            os.system('clear')
            print_board(board)
            if check_win(board, current_player):
                print(f"Player {current_player} won!")
                break
            elif check_draw(board):
                print("It's a draw!")
                break
            current_player_index = (current_player_index + 1) % num_players

if __name__ == "__main__":
    main()
