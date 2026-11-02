import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    board = [[' ' for _ in range(cols)] for _ in range(rows)]
    return board

def print_board(board):
    clear_screen()
    # Print column labels
    labels = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    print('  ' + '   '.join(labels[:len(board[0])]))
    print('+' + '---+' * len(board[0]))
    for row in board:
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
        print('+' + '---+' * len(board[0]))

def valid_input(inp, cols):
    labels = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    if len(inp) != 1:
        return False
    if inp < 'A' or inp >= chr(ord('A') + cols):
        return False
    return True

def get_column_index(inp):
    return ord(inp) - ord('A')

def place_checker(board, col, checker):
    # Place checker in the lowest available spot in column col
    for row in reversed(range(len(board))):
        if board[row][col] == ' ':
            board[row][col] = checker
            return True
    return False  # Column full

def check_win(board, checker):
    rows = len(board)
    cols = len(board[0])
    # Horizontal
    for r in range(rows):
        for c in range(cols - 3):
            if all(board[r][c+i] == checker for i in range(4)):
                return True
    # Vertical
    for c in range(cols):
        for r in range(rows - 3):
            if all(board[r+i][c] == checker for i in range(4)):
                return True
    # Diagonal (\)
    for r in range(rows - 3):
        for c in range(cols - 3):
            if all(board[r+i][c+i] == checker for i in range(4)):
                return True
    # Diagonal (/)
    for r in range(3, rows):
        for c in range(cols - 3):
            if all(board[r-i][c+i] == checker for i in range(4)):
                return True
    return False

def check_draw(board):
    for row in board:
        if ' ' in row:
            return False
    return True

def main():
    board = create_board(ROWS, COLS)
    players = CHECKERS[:PLAYERS]
    current_player_index = random.randint(0, PLAYERS -1)

    print_board(board)

    while True:
        current_checker = players[current_player_index]
        print(f"Player {current_checker}, please enter a column:")
        user_input = input().strip().upper()

        if not valid_input(user_input, COLS):
            # Invalid input, ask again
            continue

        col = get_column_index(user_input)

        placed = place_checker(board, col, current_checker)
        if not placed:
            # Column full, player loses turn (do not ask again)
            current_player_index = (current_player_index + 1) % PLAYERS
            print_board(board)
            continue

        print_board(board)

        if check_win(board, current_checker):
            print(f"Player {current_checker} won!")
            break

        if check_draw(board):
            print("The game is a draw!")
            break

        current_player_index = (current_player_index + 1) % PLAYERS

if __name__ == "__main__":
    main()
