import os
import random

# Constants
NUM_ROWS = 6
NUM_COLS = 7
MAX_PLAYERS = 2
PLAYERS = ['X', 'O', 'V', 'H', 'M']

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    letters = [chr(i + ord('A')) for i in range(len(board[0]))]
    print('  ' + '   '.join(letters))
    print('+---' * len(board[0]) + '+')
    for row in board:
        print('|' + ' | '.join(row) + '|')
        print('+---' * len(board[0]) + '+')

def check_win(board, player):
    # Check horizontal, vertical, and diagonal wins
    for row in range(NUM_ROWS):
        for col in range(NUM_COLS):
            # Horizontal check
            if col <= NUM_COLS - 4 and all(board[row][col+i] == player for i in range(4)):
                return True
            # Vertical check
            if row <= NUM_ROWS - 4 and all(board[row+i][col] == player for i in range(4)):
                return True
            # Diagonal (top-left to bottom-right)
            if row <= NUM_ROWS - 4 and col <= NUM_COLS - 4 and all(board[row+i][col+i] == player for i in range(4)):
                return True
            # Diagonal (bottom-left to top-right)
            if row >= 3 and col <= NUM_COLS - 4 and all(board[row-i][col+i] == player for i in range(4)):
                return True
    return False

def check_draw(board):
    return all(board[0][col] != ' ' for col in range(NUM_COLS))

def get_column_index(column_letter):
    return ord(column_letter.upper()) - ord('A')

def is_valid_input(input_str):
    return len(input_str) == 1 and input_str.isalpha() and 'A' <= input_str.upper() <= 'G'

def drop_checker(board, col, player):
    for row in reversed(range(NUM_ROWS)):
        if board[row][col] == ' ':
            board[row][col] = player
            return True
    return False

def main():
    board = create_board(NUM_ROWS, NUM_COLS)
    current_player_idx = random.randint(0, MAX_PLAYERS-1)
    print_board(board)

    while True:
        current_player = PLAYERS[current_player_idx]
        user_input = input(f"Player {current_player}, please enter a column: ").strip()
        
        while not is_valid_input(user_input):
            print("Invalid input. Please enter a valid column letter.")
            user_input = input(f"Player {current_player}, please enter a column: ").strip()

        column_idx = get_column_index(user_input)
        
        if not drop_checker(board, column_idx, current_player):
            print("Column is full. Turn is lost.")
        else:
            print_board(board)
            if check_win(board, current_player):
                print(f"Player {current_player} won!")
                break
            if check_draw(board):
                print("The game is a draw!")
                break
        
        current_player_idx = (current_player_idx + 1) % MAX_PLAYERS

if __name__ == "__main__":
    main()
