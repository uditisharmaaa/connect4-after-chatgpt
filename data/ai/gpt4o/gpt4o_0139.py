import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M'][:PLAYERS]

# Initialize the board
def create_board(rows, cols):
    return [[' ' for _ in range(cols)] for _ in range(rows)]

# Print the board
def print_board(board):
    os.system('clear')
    print('  ' + '   '.join([chr(ord('A') + i) for i in range(len(board[0]))]))
    print('+---' * len(board[0]) + '+')
    for row in board:
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
        print('+---' * len(board[0]) + '+')

# Validate column input
def get_valid_column(board, current_player):
    while True:
        column = input(f"Player {CHECKERS[current_player]}, please enter a column: ").upper()
        if len(column) == 1 and 'A' <= column <= chr(ord('A') + len(board[0]) - 1):
            index = ord(column) - ord('A')
            if board[0][index] == ' ':
                return index
            else:
                print("Column is full, try another one.")
        else:
            print("Invalid input, please enter a valid column letter.")

# Place checker on the board
def place_checker(board, column, checker):
    for row in reversed(board):
        if row[column] == ' ':
            row[column] = checker
            break

# Check for win
def check_win(board, checker):
    # Check horizontal locations
    for row in board:
        for col in range(COLUMNS - 3):
            if all(cell == checker for cell in row[col:col + 4]):
                return True
    
    # Check vertical locations
    for col in range(COLUMNS):
        for row in range(ROWS - 3):
            if all(board[row + i][col] == checker for i in range(4)):
                return True
    
    # Check diagonals (bottom-left to top-right)
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if all(board[row + i][col + i] == checker for i in range(4)):
                return True

    # Check diagonals (top-left to bottom-right)
    for row in range(3, ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row - i][col + i] == checker for i in range(4)):
                return True

    return False

# Check for draw
def check_draw(board):
    return all(cell != ' ' for row in board for cell in row)

# Main function
def main():
    board = create_board(ROWS, COLUMNS)
    current_player = random.randint(0, PLAYERS - 1)
    print_board(board)

    while True:
        column = get_valid_column(board, current_player)
        place_checker(board, column, CHECKERS[current_player])
        print_board(board)
        
        if check_win(board, CHECKERS[current_player]):
            print(f"Player {CHECKERS[current_player]} won!")
            break
        
        if check_draw(board):
            print("The game is a draw!")
            break
        
        current_player = (current_player + 1) % PLAYERS

if __name__ == "__main__":
    main()
