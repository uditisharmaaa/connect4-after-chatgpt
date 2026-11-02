import os
import random
import string

# Constants
BOARD_COLUMNS = 7
BOARD_ROWS = 6
MIN_PLAYERS = 2
MAX_PLAYERS = 5
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def create_board(columns, rows):
    """Create a 2D board with specified columns and rows."""
    return [[' ' for _ in range(columns)] for _ in range(rows)]

def print_board(board, columns):
    """Print the current state of the board."""
    print('  ' + '   '.join(string.ascii_uppercase[:columns]))
    for row in board:
        print('+---' * columns + '+')
        print('| ' + ' | '.join(row) + ' |')
    print('+---' * columns + '+')

def validate_input(column, columns):
    """Validate user input for column choice."""
    if not column.isalpha() or len(column)!= 1:
        return False
    if column.upper() not in string.ascii_uppercase[:columns]:
        return False
    return True

def get_next_player(current_player, players):
    """Get the next player's index and checker."""
    next_player_index = (current_player + 1) % len(players)
    return next_player_index, players[next_player_index]

def check_win(board, player_checker, columns, rows):
    """Check for a win in all directions."""
    # Check horizontal locations for win
    for c in range(columns - 3):
        for r in range(rows):
            if board[r][c] == player_checker and board[r][c + 1] == player_checker and board[r][c + 2] == player_checker and board[r][c + 3] == player_checker:
                return True

    # Check vertical locations for win
    for c in range(columns):
        for r in range(rows - 3):
            if board[r][c] == player_checker and board[r + 1][c] == player_checker and board[r + 2][c] == player_checker and board[r + 3][c] == player_checker:
                return True

    # Check positively sloped diagonals
    for c in range(columns - 3):
        for r in range(rows - 3):
            if board[r][c] == player_checker and board[r + 1][c + 1] == player_checker and board[r + 2][c + 2] == player_checker and board[r + 3][c + 3] == player_checker:
                return True

    # Check negatively sloped diagonals
    for c in range(columns - 3):
        for r in range(3, rows):
            if board[r][c] == player_checker and board[r - 1][c + 1] == player_checker and board[r - 2][c + 2] == player_checker and board[r - 3][c + 3] == player_checker:
                return True

def check_draw(board):
    """Check if the board is full (draw)."""
    for row in board:
        if ' ' in row:
            return False
    return True

def main():
    num_players = 2
    players = CHECKERS[:num_players]
    board = create_board(BOARD_COLUMNS, BOARD_ROWS)
    current_player_index = random.randint(0, num_players - 1)
    current_player_checker = players[current_player_index]

    while True:
        os.system('clear')
        print_board(board, BOARD_COLUMNS)
        print(f"Player {current_player_checker}, please enter a column (A-{string.ascii_uppercase[BOARD_COLUMNS - 1]}): ")
        column = input().upper()
        if not validate_input(column, BOARD_COLUMNS):
            print("Invalid input. Please try again.")
            input("Press Enter to continue...")
            continue
        column_index = string.ascii_uppercase.index(column)

        # Place checker in lowest available space in column
        for row_index in range(BOARD_ROWS - 1, -1, -1):
            if board[row_index][column_index] == ' ':
                board[row_index][column_index] = current_player_checker
                break
        else:
            print("Column is full. Try again.")
            input("Press Enter to continue...")
            continue

        if check_win(board, current_player_checker, BOARD_COLUMNS, BOARD_ROWS):
            os.system('clear')
            print_board(board, BOARD_COLUMNS)
            print(f"Player {current_player_checker} won!")
            break
        if check_draw(board):
            os.system('clear')
            print_board(board, BOARD_COLUMNS)
            print("It's a draw!")
            break

        current_player_index, current_player_checker = get_next_player(current_player_index, players)

if __name__ == "__main__":
    main()
