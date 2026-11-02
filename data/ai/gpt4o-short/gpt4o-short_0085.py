import os
import random

ROWS = 6
COLUMNS = 7
PLAYER_TOKENS = ['X', 'O', 'V', 'H', 'M']
NUM_PLAYERS = 4  # Change this to set between 2 to 5 players

def create_board():
    return [[' ' for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')
    print('  A B C D E F G')
    for row in board:
        print('|'.join([' '] + row + [' ']))
    print('+' + '-+' * COLUMNS)

def drop_piece(board, col, token):
    for row in reversed(board):
        if row[col] == ' ':
            row[col] = token
            return True
    return False

def is_valid_input(col, board):
    return col in range(COLUMNS) and board[0][col] == ' '

def check_win(board, token):
    for c in range(COLUMNS - 3):
        for r in range(ROWS):
            if all(board[r][c + i] == token for i in range(4)):
                return True
    
    for c in range(COLUMNS):
        for r in range(ROWS - 3):
            if all(board[r + i][c] == token for i in range(4)):
                return True

    for c in range(COLUMNS - 3):
        for r in range(ROWS - 3):
            if all(board[r + i][c + i] == token for i in range(4)):
                return True

    for c in range(COLUMNS - 3):
        for r in range(3, ROWS):
            if all(board[r - i][c + i] == token for i in range(4)):
                return True

    return False

def is_draw(board):
    return all(board[0][col] != ' ' for col in range(COLUMNS))

def get_player_input(current_player):
    try:
        col = input(f"Player {current_player} ({PLAYER_TOKENS[current_player]}), pick a column (A-G): ").upper()
        return ord(col) - ord('A')
    except:
        return -1

def main():
    board = create_board()
    current_player = random.randint(0, NUM_PLAYERS - 1)
    
    while True:
        print_board(board)
        col = get_player_input(current_player)
        
        if is_valid_input(col, board) and drop_piece(board, col, PLAYER_TOKENS[current_player]):
            if check_win(board, PLAYER_TOKENS[current_player]):
                print_board(board)
                print(f"Player {current_player + 1} ({PLAYER_TOKENS[current_player]}) wins!")
                break
            elif is_draw(board):
                print_board(board)
                print("It's a draw!")
                break
            current_player = (current_player + 1) % NUM_PLAYERS
        else:
            print("Invalid move, try again.")

if __name__ == "__main__":
    main()
