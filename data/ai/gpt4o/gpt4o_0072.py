import os
import random

# Constants
ROWS = 6
COLS = 7
MAX_PLAYERS = 5
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    
    # Print column labels
    print('  ' + '   '.join([chr(65 + i) for i in range(COLS)]))
    # Print board
    for row in board:
        print('+---' * COLS + '+')
        print('| ' + ' | '.join(row) + ' |')
    print('+---' * COLS + '+')

def is_valid_input(input_str):
    return len(input_str) == 1 and 'A' <= input_str <= chr(65 + COLS - 1)

def get_lowest_empty_row(board, col):
    for r in range(ROWS - 1, -1, -1):
        if board[r][col] == ' ':
            return r
    return None

def check_for_winner(board, checker):
    # Horizontal check
    for r in range(ROWS):
        for c in range(COLS - 3):
            if all(board[r][c+i] == checker for i in range(4)):
                return True
    
    # Vertical check
    for c in range(COLS):
        for r in range(ROWS - 3):
            if all(board[r+i][c] == checker for i in range(4)):
                return True
    
    # Diagonal checks
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            if all(board[r+i][c+i] == checker for i in range(4)):
                return True
        for c in range(3, COLS):
            if all(board[r+i][c-i] == checker for i in range(4)):
                return True
    
    return False

def check_for_draw(board):
    return all(board[0][c] != ' ' for c in range(COLS))

def play_game(num_players):
    # Initializations
    board = create_board(ROWS, COLS)
    current_player = random.randint(0, num_players - 1)
    player_checkers = CHECKERS[:num_players]
    
    # Main game loop
    while True:
        print_board(board)
        print(f"Player {player_checkers[current_player]}, please enter a column: ")
        
        while True:
            try:
                user_input = input().strip().upper()
                if is_valid_input(user_input):
                    col = ord(user_input) - 65
                    row = get_lowest_empty_row(board, col)
                    if row is not None:
                        board[row][col] = player_checkers[current_player]
                        break
                    else:
                        print(f"Column {user_input} is full. Try another column.")
                else:
                    print("Invalid input. Please enter a valid column letter.")
            except Exception as e:
                print("An error occurred. Please try again.")

        # Check for a winner
        if check_for_winner(board, player_checkers[current_player]):
            print_board(board)
            print(f"Player {player_checkers[current_player]} won!")
            break

        # Check for a draw
        if check_for_draw(board):
            print_board(board)
            print("The game is a draw!")
            break

        # Change turn
        current_player = (current_player + 1) % num_players

if __name__ == "__main__":
    play_game(2)
