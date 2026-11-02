import os
import random

ROWS = 6
COLUMNS = 7
COLUMN_LABELS = 'ABCDEFG'
PLAYERS = ['X', 'O', 'V', 'H', 'M'][:5]  # Adjust number of players here

def create_board():
    return [[' ' for _ in range(COLUMNS)] for _ in range(ROWS)]

def clear_screen():
    os.system('clear')

def print_board(board):
    clear_screen()
    print(' '.join(COLUMN_LABELS))
    for row in board:
        print(' '.join(row))

def drop_piece(board, column, piece):
    for row in reversed(board):
        if row[column] == ' ':
            row[column] = piece
            return

def valid_move(board, column):
    return board[0][column] == ' '

def check_win(board, piece):
    for row in range(ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row][col+i] == piece for i in range(4)):
                return True
    for col in range(COLUMNS):
        for row in range(ROWS - 3):
            if all(board[row+i][col] == piece for i in range(4)):
                return True
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if all(board[row+i][col+i] == piece for i in range(4)):
                return True
            if all(board[row+3-i][col+i] == piece for i in range(4)):
                return True
    return False

def check_draw(board):
    return all(board[0][col] != ' ' for col in range(COLUMNS))

def play_game():
    board = create_board()
    current_player = random.choice(PLAYERS)
    player_index = PLAYERS.index(current_player)
    
    while True:
        print_board(board)
        move = input(f"Player {current_player}, choose a column (A-G): ").strip().upper()
        
        if move not in COLUMN_LABELS:
            print("Invalid column. Try again.")
            continue
        
        column = COLUMN_LABELS.index(move)
        
        if not valid_move(board, column):
            print("Column full. Try another.")
            continue

        drop_piece(board, column, current_player)

        if check_win(board, current_player):
            print_board(board)
            print(f"Player {current_player} wins!")
            break
        if check_draw(board):
            print_board(board)
            print("It's a draw!")
            break
        
        player_index = (player_index + 1) % len(PLAYERS)
        current_player = PLAYERS[player_index]

if __name__ == '__main__':
    play_game()
