import random
import os

# Constants
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def initialize_board(rows, cols):
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    os.system('clear')  # Adjust for the specific OS if not using Unix/Linux
    cols_labels = ' '.join(chr(65 + i) for i in range(NUM_COLS))
    print('  ' + cols_labels)
    print('+' + '---+' * NUM_COLS)
    for row in board:
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
        print('+' + '---+' * NUM_COLS)

def get_valid_column_input(board):
    while True:
        user_input = input("Please enter a column: ").strip().upper()
        if len(user_input) == 1 and 'A' <= user_input <= chr(65 + NUM_COLS - 1):
            col = ord(user_input) - 65
            if board[0][col] == ' ':  # Check if the column isn't full
                return col
        print("Invalid input. Please try again.")

def place_checker(board, col, checker):
    for row in reversed(board):
        if row[col] == ' ':
            row[col] = checker
            break

def check_winner(board, checker):
    # Check horizontally, vertically, and diagonally
    for row in range(NUM_ROWS):
        for col in range(NUM_COLS):
            if (col + 3 < NUM_COLS and all(board[row][col + i] == checker for i in range(4))) or \
               (row + 3 < NUM_ROWS and all(board[row + i][col] == checker for i in range(4))) or \
               (row + 3 < NUM_ROWS and col + 3 < NUM_COLS and all(board[row + i][col + i] == checker for i in range(4))) or \
               (row - 3 >= 0 and col + 3 < NUM_COLS and all(board[row - i][col + i] == checker for i in range(4))):
                return True
    return False

def check_draw(board):
    return all(cell != ' ' for row in board for cell in row)

def main():
    board = initialize_board(NUM_ROWS, NUM_COLS)
    current_player = random.randint(0, NUM_PLAYERS - 1)
    checkers_for_players = CHECKERS[:NUM_PLAYERS]
    
    print_board(board)
    
    while True:
        print(f"Player {checkers_for_players[current_player]}, it's your turn.")
        col = get_valid_column_input(board)
        place_checker(board, col, checkers_for_players[current_player])
        print_board(board)
        
        if check_winner(board, checkers_for_players[current_player]):
            print(f"Player {checkers_for_players[current_player]} won!")
            break
        if check_draw(board):
            print("The game is a draw!")
            break
        
        # Alternate players
        current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
