import os
import random
import string

# ----- CONSTANTS -----
ROWS = 6                     # Number of rows
COLS = 7                     # Number of columns (max 26)
NUM_PLAYERS = 2              # Number of players (between 2 and 5)
PLAYER_CHECKERS = ['X', 'O', 'V', 'H', 'M'][:NUM_PLAYERS]
WIN_COUNT = 4                # Number in a row needed to win

def clear_screen():
    os.system('clear')

def create_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    clear_screen()
    # Print column headers
    header = '  ' + '   '.join(string.ascii_uppercase[:COLS])
    print(header)
    print('+' + '---+' * COLS)
    # Print each row
    for row in board:
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
        print('+' + '---+' * COLS)

def get_valid_column_input(board, player_checker):
    while True:
        inp = input(f"Player {player_checker}, please enter a column: ").strip().upper()
        # Check for single character, is alpha, and in columns range
        if len(inp) == 1 and inp.isalpha():
            col_index = ord(inp) - ord('A')
            if 0 <= col_index < COLS:
                # Check if column is full
                if board[0][col_index] == ' ':
                    return col_index
                else:
                    print("This column is full. You lose your turn!")
                    return None  # Lose the turn if column is full
            else:
                print("Invalid column. Please enter a valid column letter.")
        else:
            print("Invalid input. Please enter a single column letter.")

def place_checker(board, col, checker):
    for row in reversed(range(ROWS)):
        if board[row][col] == ' ':
            board[row][col] = checker
            return row, col
    return None  # Should not get here if checked before

def check_win(board, row, col, checker):
    # Directions: (row_delta, col_delta)
    directions = [
        (0, 1),    # Horizontal
        (1, 0),    # Vertical
        (1, 1),    # Diagonal down-right
        (1, -1),   # Diagonal down-left
    ]
    for dr, dc in directions:
        count = 1  # Count the placed checker
        # Check forward direction
        r, c = row + dr, col + dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == checker:
            count += 1
            r += dr
            c += dc
        # Check backward direction
        r, c = row - dr, col - dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc
        if count >= WIN_COUNT:
            return True
    return False

def check_draw(board):
    # If any top row cell is empty, not draw
    for cell in board[0]:
        if cell == ' ':
            return False
    return True

def main():
    board = create_board()
    print_board(board)
    # Choose random player
    current_player = random.randint(0, NUM_PLAYERS - 1)
    game_over = False

    while not game_over:
        print_board(board)
        col = get_valid_column_input(board, PLAYER_CHECKERS[current_player])
        if col is None:
            # Lose turn if column is full
            current_player = (current_player + 1) % NUM_PLAYERS
            continue
        move = place_checker(board, col, PLAYER_CHECKERS[current_player])
        row, col = move
        # Check for win
        if check_win(board, row, col, PLAYER_CHECKERS[current_player]):
            print_board(board)
            print(f"Player {PLAYER_CHECKERS[current_player]} won!")
            game_over = True
        elif check_draw(board):
            print_board(board)
            print("It's a draw!")
            game_over = True
        else:
            # Next player's turn
            current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == '__main__':
    main()
