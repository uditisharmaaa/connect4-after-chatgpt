import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = ['X', 'O', 'V', 'H', 'M'][:5]  # Adjust number of players here (2 to 5)

# Board setup
def create_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')
    print("  A B C D E F G")
    for row in board:
        print("|" + "|".join(row) + "|")
    print("  " + "--" * COLS)

def is_valid_column(column, board):
    return column in range(COLS) and board[0][column] == ' '

def get_column_name(column):
    return chr(ord('A') + column)

def drop_piece(board, column, piece):
    for row in range(ROWS - 1, -1, -1):
        if board[row][column] == ' ':
            board[row][column] = piece
            break

def check_winner(board, piece):
    # Check horizontal, vertical, and diagonal for win
    for row in range(ROWS):
        for col in range(COLS - 3):
            if all(board[row][col + i] == piece for i in range(4)):
                return True

    for row in range(ROWS - 3):
        for col in range(COLS):
            if all(board[row + i][col] == piece for i in range(4)):
                return True

    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if all(board[row + i][col + i] == piece for i in range(4)):
                return True
            if all(board[row + 3 - i][col + i] == piece for i in range(4)):
                return True
                
    return False

def is_draw(board):
    return all(board[0][col] != ' ' for col in range(COLS))

def connect4():
    board = create_board()
    current_player_index = random.randint(0, len(PLAYERS) - 1)
    print_board(board)
    
    while True:
        current_player = PLAYERS[current_player_index]
        valid_move = False
        while not valid_move:
            try:
                move = input(f"Player {current_player}, choose a column (A-G): ").strip().upper()
                column = ord(move) - ord('A')
                if is_valid_column(column, board):
                    valid_move = True
                else:
                    print("Invalid move! Try again.")
            except (IndexError, ValueError):
                print("Invalid column! Please enter A-G.")
        
        drop_piece(board, column, current_player)
        print_board(board)

        if check_winner(board, current_player):
            print(f"Player {current_player} wins!")
            break
        elif is_draw(board):
            print("It's a draw!")
            break
        
        current_player_index = (current_player_index + 1) % len(PLAYERS)

if __name__ == '__main__':
    connect4()
