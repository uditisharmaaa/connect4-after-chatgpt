import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def create_board():
    """Create a 2D board with whitespaces."""
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Print the current state of the board."""
    print('  A   B   C   D   E   F   G')
    for row in board:
        print('+---+' * COLS)
        print('|   ' + ' | '.join(row) + ' |')
    print('+---+' * COLS)

def validate_input(input_str):
    """Check if the input is a valid column letter."""
    return input_str.upper() in 'ABCDEFG'

def get_column(input_str):
    """Convert the input letter to a column index."""
    return ord(input_str.upper()) - ord('A')

def is_valid_move(board, column):
    """Check if the column is not full."""
    return board[0][column] == ' '

def make_move(board, player, column):
    """Place the player's checker in the specified column."""
    for row in reversed(board):
        if row[column] == ' ':
            row[column] = player
            break

def check_win(board):
    """Check for a win condition."""
    for row in range(ROWS):
        for col in range(COLS):
            # Check horizontal
            if col < COLS - 3 and board[row][col]!= ' ':
                if board[row][col] == board[row][col+1] == board[row][col+2] == board[row][col+3]:
                    return board[row][col]
            # Check vertical
            if row < ROWS - 3 and board[row][col]!= ' ':
                if board[row][col] == board[row+1][col] == board[row+2][col] == board[row+3][col]:
                    return board[row][col]
            # Check diagonal (top-left to bottom-right)
            if row < ROWS - 3 and col < COLS - 3 and board[row][col]!= ' ':
                if board[row][col] == board[row+1][col+1] == board[row+2][col+2] == board[row+3][col+3]:
                    return board[row][col]
            # Check diagonal (bottom-left to top-right)
            if row > 2 and col < COLS - 3 and board[row][col]!= ' ':
                if board[row][col] == board[row-1][col+1] == board[row-2][col+2] == board[row-3][col+3]:
                    return board[row][col]
    return None

def check_draw(board):
    """Check if the board is full."""
    return all(cell!= ' ' for row in board for cell in row)

def main():
    os.system('clear')
    board = create_board()
    players = CHECKERS[:PLAYERS]
    current_player = random.choice(players)

    while True:
        print_board(board)
        print(f"Player {current_player}, please enter a column:")
        input_str = input()
        if not validate_input(input_str):
            print("Invalid input. Please enter a letter between A and G.")
            continue
        column = get_column(input_str)
        if not is_valid_move(board, column):
            print("Column is full. Please choose another column.")
            continue
        make_move(board, current_player, column)
        winner = check_win(board)
        if winner:
            print_board(board)
            print(f"Player {winner} won!")
            break
        if check_draw(board):
            print_board(board)
            print("It's a draw!")
            break
        current_player = players[(players.index(current_player) + 1) % PLAYERS]

if __name__ == "__main__":
    main()
