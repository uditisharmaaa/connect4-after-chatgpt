import os
import random
import string

# === Constants (can be modified for testing multiple dimensions and players) ===
ROWS = 6
COLUMNS = 7
PLAYERS = 2  # Between 2 and 5, typically set to 2 for submission

# Player checker symbols (must match PLAYERS count)
CHECKERS = ['X', 'O', 'V', 'H', 'M']

# Max allowed columns based on alphabet
MAX_COLUMNS = 26

# =================== GAME LOGIC BELOW ===================

def clear_screen():
    os.system('clear')

def create_board(rows, columns):
    return [[' ' for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    columns = len(board[0])
    header_letters = [chr(ord('A') + i) for i in range(columns)]
    # Print header
    print('  ' + '   '.join(header_letters))
    print('+' + '---+' * columns)
    # Print rows
    for row in board:
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
        print('+' + '---+' * columns)

def valid_column_input(user_input, columns):
    if len(user_input) != 1:
        return False
    if user_input not in string.ascii_uppercase[:columns]:
        return False
    return True

def get_lowest_empty_row(board, col):
    # Returns index of lowest available row in given column; or None if full
    for row in range(len(board)-1, -1, -1):
        if board[row][col] == ' ':
            return row
    return None

def is_board_full(board):
    return all(cell != ' ' for cell in board[0])  # If top row has any empties

def check_win(board, row, col, checker):
    directions = [
        (0, 1),   # Horizontal right
        (1, 0),   # Vertical down
        (1, 1),   # Diagonal down-right
        (1, -1)   # Diagonal down-left
    ]
    for dr, dc in directions:
        count = 1  # Include the placed checker
        # Check one direction
        r, c = row+dr, col+dc
        while 0 <= r < len(board) and 0 <= c < len(board[0]) and board[r][c] == checker:
            count += 1
            r += dr
            c += dc
        # Check opposite direction
        r, c = row-dr, col-dc
        while 0 <= r < len(board) and 0 <= c < len(board[0]) and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc
        if count >= 4:
            return True
    return False

def prompt_player_input(current_checker, columns):
    while True:
        user_input = input(f"Player {current_checker}, please enter a column: ").strip().upper()
        if not valid_column_input(user_input, columns):
            print(f"Invalid input. Please enter a letter A-{chr(ord('A')+columns-1)} for column.")
            continue
        col = ord(user_input) - ord('A')
        return col

def main():
    if not (2 <= PLAYERS <= 5):
        print("Error: Number of players must be between 2 and 5.")
        return
    if not (4 <= ROWS and 4 <= COLUMNS <= MAX_COLUMNS):
        print("Error: Board size must be at least 4 rows and between 4 and 26 columns.")
        return

    board = create_board(ROWS, COLUMNS)
    player_symbols = CHECKERS[:PLAYERS]

    # Choose first player randomly
    current_player = random.randint(0, PLAYERS-1)

    clear_screen()
    print_board(board)
    
    while True:
        current_checker = player_symbols[current_player]
        col = prompt_player_input(current_checker, COLUMNS)

        row = get_lowest_empty_row(board, col)
        if row is None:
            print("That column is full. You lose your turn.")
            # Next player's turn
            current_player = (current_player + 1) % PLAYERS
            continue  # Lose turn as per assignment spec

        board[row][col] = current_checker
        clear_screen()
        print_board(board)

        if check_win(board, row, col, current_checker):
            print(f"Player {current_checker} won!")
            break
        elif is_board_full(board):
            print("The game is a draw!")
            break
        else:
            current_player = (current_player + 1) % PLAYERS

if __name__ == "__main__":
    main()
