import os
import random

# Constants
ROWS = 6
COLS = 7
MAX_PLAYERS = 5
WIN_COUNT = 4

# Players and their checkers
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    board = []
    for _ in range(rows):
        board.append([' '] * cols)
    return board

def print_board(board):
    clear_screen()
    # Print column labels
    labels = [chr(ord('A') + i) for i in range(len(board[0]))]
    print('  ' + '   '.join(labels))
    # Print the board rows and separators
    for row in board:
        print('+' + '---+' * len(board[0]))
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
    print('+' + '---+' * len(board[0]))

def is_valid_column(col_input, cols):
    if len(col_input) != 1:
        return False
    if not col_input.isalpha():
        return False
    col = ord(col_input.upper()) - ord('A')
    if col < 0 or col >= cols:
        return False
    return True

def column_full(board, col):
    # Check if top row in column is occupied
    return board[0][col] != ' '

def place_checker(board, col, checker):
    # Place checker in the lowest empty row in the column
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = checker
            return row
    return -1  # Column full

def check_winner(board, row, col, checker):
    # Check all directions for 4 in a row
    directions = [
        (0, 1),  # Horizontal right
        (1, 0),  # Vertical down
        (1, 1),  # Diagonal down-right
        (1, -1)  # Diagonal down-left
    ]
    for dr, dc in directions:
        count = 1
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

def board_full(board):
    # If any top cell is empty, board is not full
    for col in range(COLS):
        if board[0][col] == ' ':
            return False
    return True

def main():
    board = create_board(ROWS, COLS)
    num_players = PLAYERS
    players = CHECKERS[:num_players]

    current_player_index = random.randint(0, num_players - 1)

    print_board(board)
    print(f"Player {players[current_player_index]} starts first!")

    while True:
        player = players[current_player_index]
        valid_input = False
        while not valid_input:
            col_input = input(f"Player {player}, please enter a column: ").strip().upper()
            if not is_valid_column(col_input, COLS):
                continue
            col = ord(col_input) - ord('A')
            if column_full(board, col):
                # Player loses the turn if column full
                valid_input = True
                placed_row = -1
            else:
                placed_row = place_checker(board, col, player)
                valid_input = True

        if placed_row == -1:
            # Column full, player loses turn: do nothing to board
            print_board(board)
            print(f"Column {col_input} is full. Player {player} loses the turn.")
        else:
            print_board(board)
            # Check win
            if check_winner(board, placed_row, col, player):
                print(f"Player {player} won!")
                break
            # Check draw
            if board_full(board):
                print("The game is a draw.")
                break

        current_player_index = (current_player_index + 1) % num_players

if __name__ == "__main__":
    main()
