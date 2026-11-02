import os
import random

# Constants
ROWS = 6
COLS = 7
COLUMN_LABELS = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
PLAYERS = ['X', 'O', 'V', 'H', 'M']  # Up to 5 players

def clear_screen():
    os.system('clear')

def create_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    print(' ' + ' '.join(COLUMN_LABELS))
    for row in board:
        print('|' + '|'.join(row) + '|')
    print('-' * (COLS * 2 + 1))

def is_valid_column(col_char):
    return col_char in COLUMN_LABELS

def get_column_index(col_char):
    return COLUMN_LABELS.index(col_char)

def is_column_not_full(board, col_idx):
    return board[0][col_idx] == ' '

def drop_piece(board, col_idx, player):
    for row_idx in reversed(range(ROWS)):
        if board[row_idx][col_idx] == ' ':
            board[row_idx][col_idx] = player
            return row_idx
    return -1  # Should not happen if checked before

def is_winning_move(board, row, col, player):
    # Directions: horizontal, vertical, diagonal /, diagonal \
    directions = [
        (0, 1),   # horizontal
        (1, 0),   # vertical
        (1, 1),   # diagonal \
        (1, -1)   # diagonal /
    ]
    
    for dr, dc in directions:
        count = 1
        
        # Check one direction
        r, c = row + dr, col + dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == player:
            count += 1
            r += dr
            c += dc
        
        # Check opposite direction
        r, c = row - dr, col - dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == player:
            count += 1
            r -= dr
            c -= dc
        
        if count >= 4:
            return True
    return False

def is_draw(board):
    return all(board[0][col] != ' ' for col in range(COLS))

def get_number_of_players():
    while True:
        try:
            n = int(input(f"Enter number of players (2-{len(PLAYERS)}): "))
            if 2 <= n <= len(PLAYERS):
                return n
            else:
                print(f"Please enter a number between 2 and {len(PLAYERS)}.")
        except ValueError:
            print("Invalid input. Please enter an integer.")

def get_player_move(current_player):
    while True:
        move = input(f"Player {current_player}'s turn. Choose column ({'/'.join(COLUMN_LABELS)}): ").upper()
        if is_valid_column(move):
            return move
        print(f"Invalid input. Please enter a column letter from {COLUMN_LABELS}.")

def main():
    clear_screen()
    print("Welcome to Connect 4")
    num_players = get_number_of_players()
    players = PLAYERS[:num_players]
    
    board = create_board()
    current_idx = random.randint(0, num_players - 1)
    
    while True:
        clear_screen()
        print_board(board)
        current_player = players[current_idx]
        
        while True:
            col_char = get_player_move(current_player)
            col_idx = get_column_index(col_char)
            if is_column_not_full(board, col_idx):
                break
            else:
                print("Column is full. Choose another column.")
        
        row_idx = drop_piece(board, col_idx, current_player)
        
        if is_winning_move(board, row_idx, col_idx, current_player):
            clear_screen()
            print_board(board)
            print(f"Player {current_player} wins!")
            break
        
        if is_draw(board):
            clear_screen()
            print_board(board)
            print("It's a draw!")
            break
        
        # Next player's turn
        current_idx = (current_idx + 1) % num_players
    
    print("Game over.")

if __name__ == "__main__":
    main()
