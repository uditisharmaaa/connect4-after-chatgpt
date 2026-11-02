import random
import os

# Constants for the game
ROWS = 6
COLUMNS = 7
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']
NUM_PLAYERS = 2 # You can change this to 2, 3, 4, or 5 based on your needs

def clear_screen():
    # Clear the console
    os.system('clear' if os.name == 'posix' else 'cls')

def create_board():
    # Create a 6x7 board initialized with empty strings
    return [[' ' for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    # Print the board with column headers
    print('  ' + ' '.join(list('ABCDEFG')))
    for row in board:
        print('| ' + ' | '.join(row) + ' |')
    print('+---' * COLUMNS + '+')

def is_valid_column(board, col):
    # Check if placing a piece in the column is valid (i.e., it is not full)
    return board[0][col] == ' '

def get_next_open_row(board, col):
    # Get the next open row in a column
    for r in range(ROWS - 1, -1, -1):
        if board[r][col] == ' ':
            return r
    return None

def place_piece(board, row, col, piece):
    # Place a piece in the board at the specified location
    board[row][col] = piece

def check_for_win(board, piece):
    # Check horizontal, vertical, and diagonal for a win
    # Horizontal
    for c in range(COLUMNS - 3):
        for r in range(ROWS):
            if (board[r][c] == piece and board[r][c+1] == piece and
                board[r][c+2] == piece and board[r][c+3] == piece):
                return True
    # Vertical
    for c in range(COLUMNS):
        for r in range(ROWS - 3):
            if (board[r][c] == piece and board[r+1][c] == piece and
                board[r+2][c] == piece and board[r+3][c] == piece):
                return True
    # Positive diagonal
    for c in range(COLUMNS - 3):
        for r in range(ROWS - 3):
            if (board[r][c] == piece and board[r+1][c+1] == piece and
                board[r+2][c+2] == piece and board[r+3][c+3] == piece):
                return True
    # Negative diagonal
    for c in range(COLUMNS - 3):
        for r in range(3, ROWS):
            if (board[r][c] == piece and board[r-1][c+1] == piece and
                board[r-2][c+2] == piece and board[r-3][c+3] == piece):
                return True
    return False

def check_for_draw(board):
    # Check if the board is full, indicating a draw
    for r in range(ROWS):
        for c in range(COLUMNS):
            if board[r][c] == ' ':
                return False
    return True

def select_player_order():
    # Randomize the player order
    players = PLAYER_SYMBOLS[:NUM_PLAYERS]
    random.shuffle(players)
    return players

def get_player_input():
    # Get the player's chosen column
    while True:
        col_input = input("Choose a column (A-G): ").strip().upper()
        if col_input in 'ABCDEFG':
            return ord(col_input) - ord('A')
        else:
            print("Invalid input! Please choose a column labeled A-G.")

def main():
    # Main function to run the game
    board = create_board()
    game_over = False
    turn = 0
    players = select_player_order()

    clear_screen()
    print(f"Players: {players}")
    
    while not game_over:
        current_player = players[turn % NUM_PLAYERS]
        print_board(board)
        print(f"Player {current_player}'s turn")
        
        col = get_player_input()

        if is_valid_column(board, col):
            row = get_next_open_row(board, col)
            place_piece(board, row, col, current_player)
            
            if check_for_win(board, current_player):
                clear_screen()
                print_board(board)
                print(f"Congratulations! Player {current_player} wins!")
                game_over = True
            elif check_for_draw(board):
                clear_screen()
                print_board(board)
                print("The game is a draw!")
                game_over = True
            else:
                turn += 1
        else:
            print("Column is full! Please choose another.")

        # Prepare for the next turn
        if not game_over:
            clear_screen()

if __name__ == "__main__":
    main()
