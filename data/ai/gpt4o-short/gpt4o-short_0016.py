import random
import os

# Constants
ROWS = 6
COLUMNS = 7
PLAYER_TOKENS = ['X', 'O', 'V', 'H', 'M']
PLAYER_COUNT = 3  # Change this to 2, 3, 4, or 5 to set the number of players

# Ensure PLAYER_COUNT is not greater than the available tokens
PLAYER_COUNT = min(PLAYER_COUNT, len(PLAYER_TOKENS))

# Board initialization
def create_board():
    return [[' ' for _ in range(COLUMNS)] for _ in range(ROWS)]

# Print the board
def print_board(board):
    os.system('clear')  # Clear terminal screen
    print(' ' + ' '.join(['A', 'B', 'C', 'D', 'E', 'F', 'G']))
    for row in board:
        print('|'.join(row))
        print('-' * (2 * COLUMNS - 1))
    print()

# Check if a move is valid
def is_valid_move(board, column):
    return board[0][column] == ' '

# Place a token in the chosen column
def drop_token(board, column, token):
    for row in reversed(board):
        if row[column] == ' ':
            row[column] = token
            break

# Check for a win
def check_win(board, token):
    # Check horizontal, vertical, and diagonal locations for a win
    for row in range(ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row][col + i] == token for i in range(4)):
                return True

    for row in range(ROWS - 3):
        for col in range(COLUMNS):
            if all(board[row + i][col] == token for i in range(4)):
                return True

    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if all(board[row + i][col + i] == token for i in range(4)):
                return True

    for row in range(3, ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row - i][col + i] == token for i in range(4)):
                return True
                
    return False

# Check for a draw (no empty spaces left)
def check_draw(board):
    return all(board[0][col] != ' ' for col in range(COLUMNS))

# Main game function
def play_game():
    board = create_board()
    current_player = random.choice(range(PLAYER_COUNT))
    game_over = False

    while not game_over:
        print_board(board)
        print(f"Player {PLAYER_TOKENS[current_player]}'s turn")
        
        # Get a valid move from the user
        valid_move = False
        while not valid_move:
            move = input('Choose a column (A-G): ').strip().upper()
            if move in 'ABCDEFG' and len(move) == 1:
                column = ord(move) - ord('A')
                if is_valid_move(board, column):
                    valid_move = True
                else:
                    print('Column is full. Choose another column.')
            else:
                print('Invalid input. Please choose a column (A-G).')

        # Drop the token and check for win/draw
        drop_token(board, column, PLAYER_TOKENS[current_player])
        
        if check_win(board, PLAYER_TOKENS[current_player]):
            print_board(board)
            print(f"Player {PLAYER_TOKENS[current_player]} wins!")
            game_over = True
        elif check_draw(board):
            print_board(board)
            print("It's a draw!")
            game_over = True
        else:
            current_player = (current_player + 1) % PLAYER_COUNT

if __name__ == '__main__':
    play_game()
