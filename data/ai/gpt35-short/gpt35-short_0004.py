import os
import random

ROWS = 6
COLS = 7
COL_LABELS = ['A','B','C','D','E','F','G']
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']  # Max 5 players

def clear_screen():
    os.system('clear')

def create_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    print(' ' + ' '.join(COL_LABELS))
    for row in board:
        print('|' + '|'.join(row) + '|')
    print('-' * (2 * COLS + 1))

def get_num_players():
    while True:
        num = input("Enter number of players (2-5): ")
        if num.isdigit():
            num = int(num)
            if 2 <= num <= 5:
                return num
        print("Invalid input. Please enter a number between 2 and 5.")

def get_player_move(board, player):
    while True:
        col_input = input(f"Player {player}'s turn. Choose column (A-G): ").upper()
        if col_input in COL_LABELS:
            col = COL_LABELS.index(col_input)
            if board[0][col] == ' ':
                return col
            else:
                print("Column is full! Choose another column.")
        else:
            print("Invalid column. Please enter A-G.")

def drop_piece(board, col, piece):
    # Drop piece in the lowest available row at column col
    for row in reversed(range(ROWS)):
        if board[row][col] == ' ':
            board[row][col] = piece
            return row, col

def check_win(board, piece, row, col):
    # Directions: horizontal, vertical, diag down-right, diag up-right
    directions = [(0,1), (1,0), (1,1), (-1,1)]
    for dr, dc in directions:
        count = 1
        # Check in positive direction
        r, c = row + dr, col + dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == piece:
            count += 1
            r += dr
            c += dc

        # Check in negative direction
        r, c = row - dr, col - dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == piece:
            count += 1
            r -= dr
            c -= dc

        if count >= 4:
            return True
    return False

def check_draw(board):
    # Draw if no empty spaces in top row
    return all(cell != ' ' for cell in board[0])

def main():
    clear_screen()
    print("Welcome to Connect 4!")
    num_players = get_num_players()
    players = PLAYER_SYMBOLS[:num_players]
    board = create_board()
    
    current_player_idx = random.randint(0, num_players-1)
    print(f"Randomly selected Player {players[current_player_idx]} to start.")
    
    while True:
        clear_screen()
        print_board(board)
        piece = players[current_player_idx]

        col = get_player_move(board, piece)
        row, _ = drop_piece(board, col, piece)

        if check_win(board, piece, row, col):
            clear_screen()
            print_board(board)
            print(f"Player {piece} wins!")
            break
        if check_draw(board):
            clear_screen()
            print_board(board)
            print("It's a draw!")
            break
        
        current_player_idx = (current_player_idx + 1) % num_players

if __name__ == '__main__':
    main()
