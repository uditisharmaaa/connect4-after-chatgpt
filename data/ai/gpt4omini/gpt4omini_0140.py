import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYER_CHECKERS = ['X', 'O', 'V', 'H', 'M']

# Initialize the board
def create_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

# Print the board
def print_board(board):
    os.system('clear')  # Clear the console for better visualization
    print("  " + "   ".join(chr(65 + i) for i in range(COLS)))
    print('+' + '---+' * COLS)
    for row in board:
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
        print('+' + '---+' * COLS)
        
# Get the lowest available row in the selected column
def get_available_row(board, col):
    for row in range(ROWS-1, -1, -1):  # Start checking from the bottom row
        if board[row][col] == ' ':
            return row
    return -1  # Column full

# Check for a win in all directions
def check_win(board, checker):
    # Check horizontal locations for win
    for c in range(COLS - 3):
        for r in range(ROWS):
            if all(board[r][c+i] == checker for i in range(4)):
                return True

    # Check vertical locations for win
    for c in range(COLS):
        for r in range(ROWS - 3):
            if all(board[r+i][c] == checker for i in range(4)):
                return True

    # Check positively sloped diagonals
    for c in range(COLS - 3):
        for r in range(ROWS - 3):
            if all(board[r+i][c+i] == checker for i in range(4)):
                return True

    # Check negatively sloped diagonals
    for c in range(COLS - 3):
        for r in range(3, ROWS):
            if all(board[r-i][c+i] == checker for i in range(4)):
                return True
    
    return False

# Check for a draw
def check_draw(board):
    return all(board[0][c] != ' ' for c in range(COLS))

# Main game function
def play_game():
    board = create_board()
    current_player = random.randint(0, len(PLAYER_CHECKERS) - 1)
    game_over = False

    while not game_over:
        print_board(board)
        checker = PLAYER_CHECKERS[current_player]
        col = input(f"Player {checker}, please enter a column (A-G): ").upper()

        if col not in [chr(65 + i) for i in range(COLS)]:
            print("Invalid column. Please try again.")
            continue
        
        col_index = ord(col) - 65
        row_index = get_available_row(board, col_index)

        if row_index == -1:
            print("Column is full. Please try another column.")
            continue

        board[row_index][col_index] = checker

        if check_win(board, checker):
            print_board(board)
            print(f"Player {checker} won!")
            game_over = True
        elif check_draw(board):
            print_board(board)
            print("The game is a draw!")
            game_over = True
        else:
            current_player = (current_player + 1) % len(PLAYER_CHECKERS)

if __name__ == "__main__":
    play_game()
