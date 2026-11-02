import os
import random
import string

# --------------------------------------
# CONSTANTS (you can change for testing)
# --------------------------------------
ROWS = 6
COLUMNS = 7  # Max 26 (A-Z)
NUM_PLAYERS = 2  # 2 to 5 supported

# The game tokens for players
PLAYER_CHECKERS = ['X', 'O', 'V', 'H', 'M']

# --------------------------------------
# Helper Functions
# --------------------------------------

def clear_screen():
    """Clears the terminal."""
    os.system('clear')

def create_board(rows, cols):
    """Creates a board initialized with spaces."""
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """Prints the board to the terminal."""
    cols = len(board[0])
    # Print column labels (A, B, C...)
    col_labels = ' '.join(f'  {string.ascii_uppercase[i]}  ' for i in range(cols))
    print()
    print(col_labels)
    print('+' + '---+' * cols)
    for row in board:
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
        print('+' + '---+' * cols)
    print()

def get_available_row(board, col):
    """Given a column index, return the lowest available row index where a token can be placed, or -1 if full."""
    for row in reversed(range(len(board))):
        if board[row][col] == ' ':
            return row
    return -1

def is_valid_column(input_char, board):
    """Check if the input character is a valid column and not full."""
    cols = len(board[0])
    if len(input_char) != 1 or input_char not in string.ascii_uppercase[:cols]:
        return False
    col_idx = string.ascii_uppercase.index(input_char)
    return board[0][col_idx] == ' '  # If top cell is empty, not full

def board_full(board):
    """Check if the board is completely full."""
    for cell in board[0]:
        if cell == ' ':
            return False
    return True

def check_for_win(board, checker):
    """Checks if the specified checker has four in a row (any direction)."""
    rows = len(board)
    cols = len(board[0])
    # Directions: (delta_row, delta_col)
    directions = [
        (0, 1),   # horizontal
        (1, 0),   # vertical
        (1, 1),   # diagonal (down-right)
        (1, -1),  # diagonal (down-left)
    ]
    for r in range(rows):
        for c in range(cols):
            if board[r][c] == checker:
                for dr, dc in directions:
                    count = 1
                    nr, nc = r + dr, c + dc
                    while 0 <= nr < rows and 0 <= nc < cols and board[nr][nc] == checker:
                        count += 1
                        if count >= 4:
                            return True
                        nr += dr
                        nc += dc
    return False

# --------------------------------------
# Main Game Loop
# --------------------------------------

def main():
    # Use global constants defined above. 
    rows, cols, num_players = ROWS, COLUMNS, NUM_PLAYERS
    assert 2 <= num_players <= 5, "Player count must be between 2 and 5"
    assert cols <= 26, "No more than 26 columns are supported (A-Z)"
    assert rows >= 4 and cols >= 4, "Board must be at least 4x4 to enable connect-4"

    checkers = PLAYER_CHECKERS[:num_players]
    board = create_board(rows, cols)

    # Randomly select first player
    current_player = random.randint(0, num_players-1)

    clear_screen()
    print_board(board)
    print(f"Player {checkers[current_player]}, you have been randomly selected to start.\n")

    while True:
        # Print whose turn it is
        player_checker = checkers[current_player]
        print(f"Player {player_checker}, please enter a column:", end=' ')
        
        # Input validation loop
        while True:
            user_input = input().strip().upper()
            if len(user_input) != 1:
                print("Invalid input. Please enter a single letter for a column:", end=' ')
                continue
            if user_input not in string.ascii_uppercase[:cols]:
                print("Invalid input. Column does not exist. Please enter a valid column letter:", end=' ')
                continue
            col_idx = string.ascii_uppercase.index(user_input)
            row_idx = get_available_row(board, col_idx)
            if row_idx == -1:
                print("Selected column is full. Turn lost!")
                break  # Lose the turn
            else:
                # Place the checker
                board[row_idx][col_idx] = player_checker
                break  # Valid move made

        clear_screen()
        print_board(board)

        # If valid move was made, check win/draw (else, player already lost turn)
        if row_idx != -1:
            # Check for win
            if check_for_win(board, player_checker):
                print(f"Player {player_checker} won!")
                break
            elif board_full(board):
                print("The game is a draw!")
                break

        # Next player's turn (cycle)
        current_player = (current_player + 1) % num_players

if __name__ == "__main__":
    main()
