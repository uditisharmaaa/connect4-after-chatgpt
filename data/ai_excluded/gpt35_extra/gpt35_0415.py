import os
import random
import string

# Constants - dimensions and players
ROWS = 6
COLUMNS = 7
NUM_PLAYERS = 2  # Changeable up to 5 as per requirements (2-5)
CHECKERS = ['X', 'O', 'V', 'H', 'M']  # Assigned in order for players

EMPTY_CELL = ' '

def clear_screen():
    os.system('clear')

def create_board(rows, columns):
    return [[EMPTY_CELL for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    # Print column labels
    col_labels = [string.ascii_uppercase[i] for i in range(len(board[0]))]
    print('  ' + '   '.join(col_labels))
    # Print top border
    print('+---' * len(board[0]) + '+')
    for row in board:
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
        print('+---' * len(board[0]) + '+')

def valid_column_input(inp, columns):
    if len(inp) != 1:
        return False
    if inp not in string.ascii_uppercase[:columns]:
        return False
    return True

def get_lowest_empty_row(board, col):
    # From bottom to top, find first EMPTY_CELL
    for r in range(len(board) - 1, -1, -1):
        if board[r][col] == EMPTY_CELL:
            return r
    return None  # Column full

def place_checker(board, col, checker):
    row = get_lowest_empty_row(board, col)
    if row is None:
        return False  # Column full
    board[row][col] = checker
    return True

def check_win(board, player_checker):
    rows = len(board)
    cols = len(board[0])
    # Check horizontal
    for r in range(rows):
        for c in range(cols - 3):
            if all(board[r][c + offset] == player_checker for offset in range(4)):
                return True
    # Check vertical
    for c in range(cols):
        for r in range(rows - 3):
            if all(board[r + offset][c] == player_checker for offset in range(4)):
                return True
    # Check diagonal (down-right)
    for r in range(rows - 3):
        for c in range(cols - 3):
            if all(board[r + offset][c + offset] == player_checker for offset in range(4)):
                return True
    # Check diagonal (up-right)
    for r in range(3, rows):
        for c in range(cols - 3):
            if all(board[r - offset][c + offset] == player_checker for offset in range(4)):
                return True
    return False

def check_draw(board):
    # Draw if no empty cells anywhere
    for row in board:
        if EMPTY_CELL in row:
            return False
    return True

def next_player_index(current_index, num_players):
    return (current_index + 1) % num_players

def main():
    # Initialize board and variables
    board = create_board(ROWS, COLUMNS)
    players = CHECKERS[:NUM_PLAYERS]

    # Randomly select first player
    current_player_idx = random.randint(0, NUM_PLAYERS - 1)

    # Print initial board
    print_board(board)

    while True:
        checker = players[current_player_idx]
        prompt = f"Player {checker}, please enter a column: "
        while True:
            inp = input(prompt).strip().upper()
            if not valid_column_input(inp, COLUMNS):
                # invalid input (wrong length or out of bounds)
                continue
            col = string.ascii_uppercase.index(inp)
            # Check if column full - if full player loses turn
            if get_lowest_empty_row(board, col) is None:
                # Player loses turn -> break input loop and end turn
                break
            else:
                # Valid input and column has space
                success = place_checker(board, col, checker)
                if success:
                    break
                else:
                    # Should not occur because get_lowest_empty_row was checked
                    continue
        
        print_board(board)

        # If move was invalid because column full, no checker placed
        if get_lowest_empty_row(board, col) is None and board[-1][col] != EMPTY_CELL:
            # We attempted this column, but it was full, so turn lost
            # Just move on to next player
            current_player_idx = next_player_index(current_player_idx, NUM_PLAYERS)
            continue

        # Check win only if checker was placed
        if check_win(board, checker):
            print(f"Player {checker} won!")
            break

        # Check draw
        if check_draw(board):
            print("Game is a draw!")
            break

        # Next player's turn
        current_player_idx = next_player_index(current_player_idx, NUM_PLAYERS)

if __name__ == "__main__":
    main()
