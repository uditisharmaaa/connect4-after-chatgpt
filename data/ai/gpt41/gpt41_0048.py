import os
import random
import string

# ==== CONSTANT VARIABLES ====
NUM_ROWS = 6                    # Number of rows in the board
NUM_COLS = 7                    # Number of columns in the board
NUM_PLAYERS = 2                 # Number of players (Set from 2 to 5)
PLAYER_CHECKERS = ['X', 'O', 'V', 'H', 'M'][:NUM_PLAYERS]  # Symbols for players
WIN_COUNT = 4                   # Number of checkers in a row needed to win
MAX_COLS = 26                   # For column labels (A-Z)

assert NUM_COLS <= MAX_COLS, "Too many columns, max 26 supported."

# ==== UTILITY FUNCTIONS ====
def clear_screen():
    os.system('clear')

def create_board(rows=NUM_ROWS, cols=NUM_COLS):
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    cols = len(board[0])
    # Print column labels
    col_labels = '  ' + '   '.join(string.ascii_uppercase[:cols])
    print(col_labels)
    # Print top border
    print('+' + '---+' * cols)
    # Print rows
    for row in board:
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
        print('+' + '---+' * cols)

def get_valid_columns(board):
    # Returns a list of column indices that are not full
    return [c for c in range(len(board[0])) if board[0][c] == ' ']

def get_column_choice(board, player_checker):
    cols = len(board[0])
    valid_columns = get_valid_columns(board)
    valid_labels = [string.ascii_uppercase[c] for c in valid_columns]
    while True:
        choice = input(f"Player {player_checker}, please enter a column: ").strip().upper()
        # Input validation
        if len(choice) != 1 or choice not in string.ascii_uppercase[:cols]:
            print(f"Invalid input. Please enter a letter from {string.ascii_uppercase[0]} to {string.ascii_uppercase[cols-1]}.")
            continue
        col_index = string.ascii_uppercase.index(choice)
        if col_index not in valid_columns:
            if board[0][col_index] != ' ':
                print("Column is full; you lose your turn!")
                return None  # Indicate a lost turn
            else:
                print("Invalid column. Try again.")
                continue
        return col_index

def drop_checker(board, col, checker):
    """
    Drops a checker into the specified column, returns (row, col) placed at.
    """
    for row in reversed(range(len(board))):
        if board[row][col] == ' ':
            board[row][col] = checker
            return row, col

def check_win(board, row, col, checker):
    """
    Checks if placing checker at (row, col) wins the game.
    """
    directions = [
        (0, 1),   # Horizontal right
        (1, 0),   # Vertical down
        (1, 1),   # Diagonal down-right
        (1, -1)   # Diagonal down-left
    ]
    for dr, dc in directions:
        count = 1
        # Check one direction
        r, c = row + dr, col + dc
        while 0 <= r < len(board) and 0 <= c < len(board[0]) and board[r][c] == checker:
            count += 1
            r += dr
            c += dc
        # Check opposite direction
        r, c = row - dr, col - dc
        while 0 <= r < len(board) and 0 <= c < len(board[0]) and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc
        if count >= WIN_COUNT:
            return True
    return False

def check_draw(board):
    return all(cell != ' ' for cell in board[0])

# ==== MAIN GAME LOOP ====

def main():
    board = create_board(NUM_ROWS, NUM_COLS)
    players = PLAYER_CHECKERS[:NUM_PLAYERS]

    # Randomly choose first player
    current_player_idx = random.randint(0, NUM_PLAYERS - 1)
    clear_screen()
    print_board(board)

    while True:
        player_checker = players[current_player_idx]
        valid_columns = get_valid_columns(board)
        if not valid_columns:
            print("It's a draw!")
            break

        col_index = get_column_choice(board, player_checker)
        clear_screen()
        if col_index is not None:
            row, col = drop_checker(board, col_index, player_checker)
            print_board(board)
            if check_win(board, row, col, player_checker):
                print(f"Player {player_checker} won!")
                break
            elif check_draw(board):
                print("It's a draw!")
                break
        else:
            # Turn lost due to full column
            print_board(board)

        # Next player's turn
        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
