import os
import random
import string

# ==== CONSTANT VARIABLES ====
NUM_ROWS = 6
NUM_COLS = 7
NUM_TO_WIN = 4
NUM_PLAYERS = 2  # Change to 2-5 players as needed
PLAYER_CHECKERS = ['X', 'O', 'V', 'H', 'M'][:NUM_PLAYERS]
COLUMN_LABELS = [string.ascii_uppercase[i] for i in range(NUM_COLS)]

# ==== FUNCTIONS ====

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    board = [[' ' for _ in range(cols)] for _ in range(rows)]
    return board

def print_board(board):
    clear_screen()
    # Print column headers
    print('  ' + '   '.join(COLUMN_LABELS))
    print('+' + '---+' * NUM_COLS)
    for row in board:
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
        print('+' + '---+' * NUM_COLS)

def get_valid_move(board):
    while True:
        move = input(f"Player {current_checker}, please enter a column: ")
        if len(move) != 1 or move not in COLUMN_LABELS:
            print("Invalid input. Please enter a single, valid column letter.")
            continue
        col = COLUMN_LABELS.index(move)
        # Check if column is full
        if board[0][col] != ' ':
            print("Column is full. You lose your turn!")
            return None
        return col

def place_checker(board, col, checker):
    # Place checker in lowest available row
    for row in reversed(range(NUM_ROWS)):
        if board[row][col] == ' ':
            board[row][col] = checker
            return row, col
    # Should not reach here if validated properly
    return None, None

def check_win(board, checker):
    # Check horizontal, vertical, diag /
    for r in range(NUM_ROWS):
        for c in range(NUM_COLS):
            # Horizontal
            if c + NUM_TO_WIN <= NUM_COLS and all(board[r][c + i] == checker for i in range(NUM_TO_WIN)):
                return True
            # Vertical
            if r + NUM_TO_WIN <= NUM_ROWS and all(board[r + i][c] == checker for i in range(NUM_TO_WIN)):
                return True
            # Diagonal down-right
            if c + NUM_TO_WIN <= NUM_COLS and r + NUM_TO_WIN <= NUM_ROWS and all(board[r + i][c + i] == checker for i in range(NUM_TO_WIN)):
                return True
            # Diagonal up-right
            if c + NUM_TO_WIN <= NUM_COLS and r - NUM_TO_WIN + 1 >= 0 and all(board[r - i][c + i] == checker for i in range(NUM_TO_WIN)):
                return True
    return False

def board_full(board):
    return all(cell != ' ' for cell in board[0])

def next_player(current):
    return (current + 1) % NUM_PLAYERS

# ==== MAIN GAME ====
def main():
    global current_checker
    board = create_board(NUM_ROWS, NUM_COLS)
    first_player = random.randint(0, NUM_PLAYERS - 1)
    current_player = first_player

    print_board(board)
    print(f"Player {PLAYER_CHECKERS[current_player]} starts!")
    input("Press Enter to begin...")

    while True:
        print_board(board)
        current_checker = PLAYER_CHECKERS[current_player]

        col = get_valid_move(board)
        # If column is full, the player loses their turn
        if col is None:
            current_player = next_player(current_player)
            continue

        row, col_placed = place_checker(board, col, current_checker)
        print_board(board)
        # Win check
        if check_win(board, current_checker):
            print(f"Player {current_checker} won!")
            break
        # Draw check
        if board_full(board):
            print("The game is a draw!")
            break
        # Next player's turn
        current_player = next_player(current_player)

if __name__ == "__main__":
    main()
