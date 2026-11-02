import os
import random

# Constants for the game setup
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']

# Initialize the board with empty spaces
def initialize_board(rows, cols):
    return [[' ' for _ in range(cols)] for _ in range(rows)]

# Print the current state of the board
def print_board(board):
    os.system('clear')
    print('  ' + '  '.join(chr(65 + i) for i in range(len(board[0]))))
    print('+---' * len(board[0]) + '+')
    for row in board:
        print('| ' + ' | '.join(row) + ' |')
        print('+---' * len(board[0]) + '+')

# Check if a move is valid
def is_valid_move(board, column):
    if column < 0 or column >= len(board[0]):
        return False
    return board[0][column] == ' '

# Place a checker on the board
def place_checker(board, column, checker):
    for row in reversed(board):
        if row[column] == ' ':
            row[column] = checker
            return True
    return False

# Check for a win condition
def check_win(board, checker):
    rows, cols = len(board), len(board[0])
    
    def check_direction(r_inc, c_inc):
        for r in range(rows):
            for c in range(cols):
                if all((0 <= r + i * r_inc < rows) and (0 <= c + i * c_inc < cols) and board[r + i * r_inc][c + i * c_inc] == checker for i in range(4)):
                    return True
        return False
    
    return any([check_direction(r_inc, c_inc) for r_inc, c_inc in [(0, 1), (1, 0), (1, 1), (1, -1)]])

# Check for draw condition
def check_draw(board):
    return all(space != ' ' for row in board for space in row)

def main():
    board = initialize_board(ROWS, COLUMNS)
    current_player_index = random.randint(0, PLAYERS - 1)
    print_board(board)
    
    while True:
        current_player = CHECKERS[current_player_index]
        print(f"Player {current_player}, please enter a column:")
        
        while True:
            user_input = input().strip().upper()
            if len(user_input) != 1 or not user_input.isalpha():
                print("Invalid input. Enter a letter corresponding to a column.")
                continue
            
            column = ord(user_input) - 65
            
            if is_valid_move(board, column):
                place_checker(board, column, current_player)
                break
            else:
                print("Invalid move. Try a different column.")
        
        print_board(board)
        
        if check_win(board, current_player):
            print(f"Player {current_player} won!")
            break
        
        if check_draw(board):
            print("The game is a draw!")
            break
        
        current_player_index = (current_player_index + 1) % PLAYERS

if __name__ == "__main__":
    main()
