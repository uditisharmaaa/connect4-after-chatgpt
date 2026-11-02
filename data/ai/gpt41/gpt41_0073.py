import os
import random

# CONSTANTS
ROWS = 6
COLUMNS = 7    # Max 26
NUM_PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']
COLUMN_LABELS = [chr(i) for i in range(65, 65 + COLUMNS)]  # ['A', 'B', ..., 'G']

def clear_screen():
    os.system('clear')  # use 'cls' for Windows, 'clear' for Unix/Linux

def create_board(rows, columns):
    return [[" " for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    # Print the column labels
    print('  ' + '   '.join(COLUMN_LABELS))
    print('+' + '+'.join(['---'] * COLUMNS) + '+')
    for row in board:
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
        print('+' + '+'.join(['---'] * COLUMNS) + '+')

def get_player_input(player_checker):
    while True:
        col = input(f"Player {player_checker}, please enter a column: ").strip().upper()
        if len(col) != 1 or col not in COLUMN_LABELS:
            print(f"Invalid input! Please enter a column between {COLUMN_LABELS[0]} and {COLUMN_LABELS[-1]}.")
            continue
        col_index = COLUMN_LABELS.index(col)
        return col_index

def place_checker(board, col_index, player_checker):
    for row in reversed(range(ROWS)):
        if board[row][col_index] == " ":
            board[row][col_index] = player_checker
            return row  # Return row index where checker was placed
    return -1  # Column is full

def is_winner(board, row, col, player_checker):
    # Directions: (dr, dc)
    directions = [
        (0, 1),   # horizontal
        (1, 0),   # vertical
        (1, 1),   # diagonal down-right
        (1, -1),  # diagonal down-left
    ]
    for dr, dc in directions:
        count = 1  # Count the checker itself
        # Check in the positive direction
        r, c = row + dr, col + dc
        while 0 <= r < ROWS and 0 <= c < COLUMNS and board[r][c] == player_checker:
            count += 1
            r += dr
            c += dc
        # Check in the negative direction
        r, c = row - dr, col - dc
        while 0 <= r < ROWS and 0 <= c < COLUMNS and board[r][c] == player_checker:
            count += 1
            r -= dr
            c -= dc
        if count >= 4:
            return True
    return False

def is_draw(board):
    for col in range(COLUMNS):
        if board[0][col] == " ":
            return False
    return True

def main():
    board = create_board(ROWS, COLUMNS)
    players = CHECKERS[:NUM_PLAYERS]
    # Randomly select starting player
    current_player = random.randint(0, NUM_PLAYERS - 1)

    clear_screen()
    print_board(board)

    while True:
        player_checker = players[current_player]
        # Get valid input
        col_index = get_player_input(player_checker)

        row_index = place_checker(board, col_index, player_checker)
        if row_index == -1:
            print("Column is full! You lose your turn.")
            current_player = (current_player + 1) % NUM_PLAYERS
            continue

        clear_screen()
        print_board(board)

        # Check for win
        if is_winner(board, row_index, col_index, player_checker):
            print(f"Player {player_checker} won!")
            break

        # Check draw
        if is_draw(board):
            print("Game is a draw!")
            break
        
        # Next player
        current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
