import os
import random

# Global constants
BOARD_ROWS = 6
BOARD_COLS = 7
NUM_PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def create_board():
    """Create a 2D board with all elements initialized with whitespaces."""
    board = [[' ' for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]
    return board

def print_board(board):
    """Print the current state of the board."""
    os.system('clear')
    print('  ' + ' '.join([chr(65 + i) for i in range(BOARD_COLS)]))
    print('+' + '+'.join(['---' for _ in range(BOARD_COLS)]) + '+')
    for row in board:
        print('| ' + ' | '.join(row) + ' |')
        print('+' + '+'.join(['---' for _ in range(BOARD_COLS)]) + '+')

def get_player_checker(player_index):
    """Return the checker for the given player."""
    return CHECKERS[player_index % len(CHECKERS)]

def get_player_input(player_checker):
    """Get the column input from the player."""
    while True:
        user_input = input(f"Player {player_checker}, please enter a column: ")
        if len(user_input) == 1 and 'A' <= user_input <= 'A' + BOARD_COLS - 1:
            return ord(user_input) - 65
        print("Invalid input. Please try again.")

def place_checker(board, player_checker, col_index):
    """Place the checker in the given column."""
    for row_index in range(BOARD_ROWS - 1, -1, -1):
        if board[row_index][col_index] == ' ':
            board[row_index][col_index] = player_checker
            return

def check_win(board, player_checker):
    """Check if the given player has won."""
    # Check horizontal wins
    for row_index in range(BOARD_ROWS):
        for col_index in range(BOARD_COLS - 3):
            if all(board[row_index][col_index + i] == player_checker for i in range(4)):
                return True

    # Check vertical wins
    for row_index in range(BOARD_ROWS - 3):
        for col_index in range(BOARD_COLS):
            if all(board[row_index + i][col_index] == player_checker for i in range(4)):
                return True

    # Check diagonal wins (top-left to bottom-right)
    for row_index in range(BOARD_ROWS - 3):
        for col_index in range(BOARD_COLS - 3):
            if all(board[row_index + i][col_index + i] == player_checker for i in range(4)):
                return True

    # Check diagonal wins (bottom-left to top-right)
    for row_index in range(3, BOARD_ROWS):
        for col_index in range(BOARD_COLS - 3):
            if all(board[row_index - i][col_index + i] == player_checker for i in range(4)):
                return True

    return False

def check_draw(board):
    """Check if the game is a draw."""
    return all(cell!= ' ' for row in board for cell in row)

def main():
    board = create_board()
    players = list(range(NUM_PLAYERS))
    random.shuffle(players)
    current_player_index = 0

    while True:
        print_board(board)
        player_checker = get_player_checker(players[current_player_index])
        col_index = get_player_input(player_checker)
        place_checker(board, player_checker, col_index)
        if check_win(board, player_checker):
            print_board(board)
            print(f"Player {player_checker} won!")
            break
        elif check_draw(board):
            print_board(board)
            print("It's a draw!")
            break
        current_player_index = (current_player_index + 1) % len(players)

if __name__ == "__main__":
    main()
