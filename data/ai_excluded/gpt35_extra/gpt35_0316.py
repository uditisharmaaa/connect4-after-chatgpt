import os
import random
import string

# Constants
ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']  # Max 5 players

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    cols = len(board[0])
    rows = len(board)
    # Print column headers
    header = '  ' + '   '.join(string.ascii_uppercase[:cols])
    print(header)
    # Print the board rows with borders
    line = '+' + '---+' * cols
    for r in range(rows):
        print(line)
        print('| ' + ' | '.join(board[r]) + ' |')
    print(line)

def input_valid_column(prompt, board):
    cols = len(board[0])
    valid_letters = string.ascii_uppercase[:cols]
    while True:
        col_input = input(prompt).strip().upper()
        if len(col_input) != 1:
            print(f"Invalid input. Please enter a single column letter A-{valid_letters[-1]}.")
            continue
        if col_input not in valid_letters:
            print(f"Invalid column. Please enter a letter from A to {valid_letters[-1]}.")
            continue
        col_index = valid_letters.index(col_input)
        # Check if column is full
        if board[0][col_index] != ' ':
            # Turn lost if full according to assignment
            print(f"Column {col_input} is full. You lose your turn.")
            return None
        return col_index

def place_checker(board, col, checker):
    """
    Place the checker in the lowest empty row in the given column.
    Assumes that column is not full.
    Returns row where checker was placed.
    """
    rows = len(board)
    for r in reversed(range(rows)):
        if board[r][col] == ' ':
            board[r][col] = checker
            return r
    return None  # Should never reach here if checked before

def check_win(board, row, col, checker):
    """
    Check if placing 'checker' at (row, col) causes a win.
    Need 4 in a row horizontally, vertically or diagonally.
    """
    rows = len(board)
    cols = len(board[0])
    directions = [
        (0, 1),  # horizontal right
        (1, 0),  # vertical down
        (1, 1),  # diagonal down-right
        (1, -1), # diagonal down-left
    ]

    for dr, dc in directions:
        count = 1  # Count the checker itself

        # Check in positive direction
        r, c = row + dr, col + dc
        while 0 <= r < rows and 0 <= c < cols and board[r][c] == checker:
            count += 1
            r += dr
            c += dc

        # Check in negative direction
        r, c = row - dr, col - dc
        while 0 <= r < rows and 0 <= c < cols and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc

        if count >= 4:
            return True
    return False

def board_full(board):
    return all(cell != ' ' for cell in board[0])

def main():
    # Only 2 players and 6x7 board as per submission requirement
    rows = ROWS
    cols = COLS
    players = PLAYERS
    checkers = CHECKERS[:players]

    board = create_board(rows, cols)

    # Randomly select first player
    current = random.randint(0, players - 1)

    print_board(board)

    while True:
        player_checker = checkers[current]
        prompt = f"Player {player_checker}, please enter a column: "
        col = input_valid_column(prompt, board)

        if col is None:
            # Column full - player loses turn
            current = (current + 1) % players
            print_board(board)
            continue

        row = place_checker(board, col, player_checker)
        print_board(board)

        # Check win
        if check_win(board, row, col, player_checker):
            print(f"Player {player_checker} won!")
            break

        # Check draw
        if board_full(board):
            print("The game is a draw!")
            break

        # Next player's turn
        current = (current + 1) % players

if __name__ == "__main__":
    main()
