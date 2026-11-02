import os
import random
import string

# Constants
ROWS = 6
COLUMNS = 7
MAX_COLUMNS = 26
NUM_PLAYERS = 2  # Set to 2 for the assignment
CHECKERS = ['X', 'O', 'V', 'H', 'M']
EMPTY_CELL = ' '

def clear_screen():
    # Clear the terminal screen
    os.system('clear')

def create_board(rows, cols):
    # Create the board as a 2D list
    return [[EMPTY_CELL for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    rows = len(board)
    cols = len(board[0])
    letters = string.ascii_uppercase[:cols]

    print()
    # Print column labels
    print('  ', end='')
    for letter in letters:
        print(f' {letter} ', end=' ')
    print()
    # Print top border
    print('+---'*cols + '+')
    # Print rows
    for row in board:
        print('|', end='')
        for cell in row:
            print(f' {cell} |', end='')
        print()
        print('+---'*cols + '+')
    print()

def get_player_move(board, player_checker):
    rows = len(board)
    cols = len(board[0])
    letters = string.ascii_uppercase[:cols]

    while True:
        move = input(f"Player {player_checker}, please enter a column: ").strip().upper()
        if len(move) != 1 or move not in letters:
            print("Invalid input! Please enter a valid column letter.")
            continue
        col = letters.index(move)
        # Check if the column is full
        if board[0][col] != EMPTY_CELL:
            print(f"Column {move} is full! You lose your turn.")
            return None  # Lost turn
        return col

def place_checker(board, col, player_checker):
    rows = len(board)
    for row in range(rows-1, -1, -1):
        if board[row][col] == EMPTY_CELL:
            board[row][col] = player_checker
            return row, col
    # This point should never be reached due to checks in get_player_move
    return None

def is_winner(board, player_checker, row, col):
    # Check 4 in all directions starting from position (row, col)
    directions = [
        (0, 1),   # Horizontal right
        (1, 0),   # Vertical down
        (1, 1),   # Diagonal down-right
        (1, -1)   # Diagonal down-left
    ]
    rows = len(board)
    cols = len(board[0])

    for dr, dc in directions:
        count = 1
        # Check in the positive direction
        r, c = row + dr, col + dc
        while 0 <= r < rows and 0 <= c < cols and board[r][c] == player_checker:
            count += 1
            r += dr
            c += dc
        # Check in the negative direction
        r, c = row - dr, col - dc
        while 0 <= r < rows and 0 <= c < cols and board[r][c] == player_checker:
            count += 1
            r -= dr
            c -= dc
        if count >= 4:
            return True
    return False

def is_draw(board):
    # Draw if top row has no EMPTY_CELL
    return all(cell != EMPTY_CELL for cell in board[0])

def main():
    # Set up board and players
    if COLUMNS > MAX_COLUMNS:
        print("Maximum columns exceeded. Please lower column count.")
        return

    player_checkers = CHECKERS[:NUM_PLAYERS]
    board = create_board(ROWS, COLUMNS)

    # Randomly choose first player
    current_player = random.randint(0, NUM_PLAYERS - 1)
    clear_screen()
    print_board(board)
    print(f"Player {player_checkers[current_player]} starts!\n")

    while True:
        player_checker = player_checkers[current_player]
        col = get_player_move(board, player_checker)

        if col is None:
            # Player loses turn if column is full
            current_player = (current_player + 1) % NUM_PLAYERS
            input("Press Enter to continue...")
            clear_screen()
            print_board(board)
            continue

        # Place the checker
        row, _ = place_checker(board, col, player_checker)

        clear_screen()
        print_board(board)

        # Check for win
        if is_winner(board, player_checker, row, col):
            print(f"Player {player_checker} won!")
            break

        # Check for draw
        if is_draw(board):
            print("The game is a draw.")
            break

        # Switch to next player
        current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == '__main__':
    main()
