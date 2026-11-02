import os
import random

# Constants for the game
ROWS = 6
COLUMNS = 7
PLAYER_COUNT = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']  # Supports up to 5 players
WIN_LENGTH = 4

assert 2 <= PLAYER_COUNT <= 5
assert 1 <= ROWS and 1 <= COLUMNS <= 26  # Max 26 for column labeling with letters


def clear_screen():
    os.system('clear')


def create_board():
    """Create an empty board with ROWS x COLUMNS filled with ' '."""
    return [[' ' for _ in range(COLUMNS)] for _ in range(ROWS)]


def print_board(board):
    clear_screen()
    # Print column headers A..G (or more, up to COLUMNS)
    header = '  ' + '   '.join(chr(ord('A') + col) for col in range(COLUMNS))
    print(header)
    # Print top border line
    line = '+---' * COLUMNS + '+'
    for row in range(ROWS):
        print(line)
        # Print each cell row
        print('|' + '|'.join(f' {board[row][col]} ' for col in range(COLUMNS)) + '|')
    print(line)


def get_player_input(current_player, board):
    """Prompt current player until a valid move is made or turn is lost due to full column."""
    player_char = CHECKERS[current_player]
    prompt = f"Player {player_char}, please enter a column: "
    while True:
        user_input = input(prompt).strip()
        # Validate length
        if len(user_input) != 1:
            print("Invalid input. Please enter a single uppercase letter corresponding to a column.")
            continue
        col_char = user_input[0]
        # Validate uppercase letter
        if not ('A' <= col_char <= chr(ord('A') + COLUMNS - 1)):
            print(f"Invalid input. Please enter a column between A and {chr(ord('A') + COLUMNS - 1)}.")
            continue
        col_index = ord(col_char) - ord('A')
        # Check if the column is full
        if board[0][col_index] != ' ':
            # Column is full, turn lost
            return col_index, False
        return col_index, True


def place_checker(board, col, checker):
    """Place checker into the lowest empty row of the given column."""
    # Start from bottom row upwards to place checker
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = checker
            return row, col
    # Should never get here if we check for full column beforehand
    return None


def check_win(board, row, col, checker):
    """Check all directions if placing checker at (row, col) causes a win."""
    # Directions represented as (d_row, d_col)
    directions = [
        (0, 1),   # Horizontal right
        (1, 0),   # Vertical down
        (1, 1),   # Diagonal down-right
        (1, -1),  # Diagonal down-left
    ]

    for dr, dc in directions:
        count = 1

        # Check in positive direction
        r, c = row + dr, col + dc
        while 0 <= r < ROWS and 0 <= c < COLUMNS and board[r][c] == checker:
            count += 1
            r += dr
            c += dc

        # Check in negative direction
        r, c = row - dr, col - dc
        while 0 <= r < ROWS and 0 <= c < COLUMNS and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc

        if count >= WIN_LENGTH:
            return True

    return False


def board_full(board):
    """Returns True if the board has no empty spaces in top row, else False."""
    for col in range(COLUMNS):
        if board[0][col] == ' ':
            return False
    return True


def main():
    board = create_board()
    # Randomly choose player to start
    current_player = random.randint(0, PLAYER_COUNT - 1)
    print_board(board)

    while True:
        player_char = CHECKERS[current_player]
        col_index, valid_turn = get_player_input(current_player, board)
        if not valid_turn:
            # Column full - turn lost, move on to next player
            print(f"Column {chr(ord('A') + col_index)} is full. Player {player_char} loses the turn.")
            current_player = (current_player + 1) % PLAYER_COUNT
            print_board(board)
            continue

        row, col = place_checker(board, col_index, player_char)
        print_board(board)

        if check_win(board, row, col, player_char):
            print(f"Player {player_char} won!")
            break

        if board_full(board):
            print("The game is a draw!")
            break

        # Next player's turn
        current_player = (current_player + 1) % PLAYER_COUNT


if __name__ == "__main__":
    main()
