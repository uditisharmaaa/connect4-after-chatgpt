import os
import random
import string

# ==== Constants ====
ROWS = 6
COLS = 7
NUM_PLAYERS = 2  # Set to 2 as per submission requirements (can be changed for testing)
PLAYER_CHECKERS = ['X', 'O', 'V', 'H', 'M'][:NUM_PLAYERS]
WIN_COUNT = 4    # Always win at 4 in a row

# ==== Functions ====
def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    """Create the game board as a 2D list filled with spaces."""
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """Display the current state of the board."""
    # Print column headers (A, B, C, ...)
    header = '  ' + '   '.join(string.ascii_uppercase[:len(board[0])])
    print(header)
    print('+' + '---+' * len(board[0]))
    for row in board:
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
        print('+' + '---+' * len(board[0]))

def get_valid_column_input(board):
    """Prompt the player until a valid column is selected."""
    while True:
        col_input = input("Please enter a column: ").strip().upper()
        if len(col_input) != 1 or col_input not in string.ascii_uppercase[:len(board[0])]:
            print("Invalid input. Please enter a valid column letter.")
            continue
        col_idx = ord(col_input) - ord('A')
        if board[0][col_idx] != ' ':
            print("Column is full. You lose your turn.")
            return None  # Lose turn if column full
        return col_idx

def place_checker(board, col, checker):
    """Placed the player's checker into the lowest available row in the selected column."""
    for row in reversed(board):
        if row[col] == ' ':
            row[col] = checker
            return True
    return False  # This shouldn't happen if input checking is correct

def check_win(board, checker):
    """Check for 4 in a row (win) in all directions."""
    rows = len(board)
    cols = len(board[0])
    for r in range(rows):
        for c in range(cols):
            # Only check from positions with the player's checker
            if board[r][c] != checker:
                continue
            # Horizontal
            if c + WIN_COUNT <= cols and all(board[r][c+i] == checker for i in range(WIN_COUNT)):
                return True
            # Vertical
            if r + WIN_COUNT <= rows and all(board[r+i][c] == checker for i in range(WIN_COUNT)):
                return True
            # Diagonal-right
            if c + WIN_COUNT <= cols and r + WIN_COUNT <= rows:
                if all(board[r+i][c+i] == checker for i in range(WIN_COUNT)):
                    return True
            # Diagonal-left
            if c - WIN_COUNT + 1 >= 0 and r + WIN_COUNT <= rows:
                if all(board[r+i][c-i] == checker for i in range(WIN_COUNT)):
                    return True
    return False

def check_draw(board):
    """Check if the board is completely filled."""
    return all(cell != ' ' for cell in board[0])

def main():
    # Randomly select first player
    players = PLAYER_CHECKERS.copy()
    current_player_idx = random.randint(0, NUM_PLAYERS - 1)
    board = create_board(ROWS, COLS)

    clear_screen()
    print_board(board)
    print(f"Player {players[current_player_idx]}'s turn:")

    while True:
        col = get_valid_column_input(board)
        clear_screen()
        if col is None:
            # Skip player's turn if column is full
            print_board(board)
            print(f"Player {players[current_player_idx]}'s turn is skipped.")
        else:
            placed = place_checker(board, col, players[current_player_idx])
            print_board(board)
            if check_win(board, players[current_player_idx]):
                print(f"Player {players[current_player_idx]} won!")
                break
            if check_draw(board):
                print("The game is a draw!")
                break
        # Next player's turn
        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS
        print(f"Player {players[current_player_idx]}'s turn:")

if __name__ == '__main__':
    main()
