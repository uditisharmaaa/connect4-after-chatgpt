import os
import random

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M'][:NUM_PLAYERS]

def initialize_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')
    print('  ' + '   '.join(chr(65 + i) for i in range(COLS)))
    separator = '+' + ('---+' * COLS)
    print(separator)
    for row in board:
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
        print(separator)

def get_player_move(player):
    while True:
        col = input(f"Player {player}, please enter a column: ").upper()
        if len(col) != 1 or col < 'A' or col >= chr(65 + COLS):
            print(f"Invalid column. Please enter a letter from A to {chr(64 + COLS)}")
            continue
        col_idx = ord(col) - ord('A')
        return col_idx

def place_checker(board, col_idx, player):
    for row_idx in range(ROWS-1, -1, -1):
        if board[row_idx][col_idx] == ' ':
            board[row_idx][col_idx] = player
            return True
    return False

def check_win(board, player):
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
    for row in range(ROWS):
        for col in range(COLS):
            if board[row][col] != player:
                continue
            for dr, dc in directions:
                count = 1
                for i in range(1, 4):
                    r, c = row + i*dr, col + i*dc
                    if 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == player:
                        count += 1
                    else:
                        break
                if count >= 4:
                    return True
    return False

def is_draw(board):
    return all(cell != ' ' for row in board for cell in row)

def main():
    board = initialize_board()
    current_player = random.choice(CHECKERS)
    print_board(board)
    
    while True:
        col_idx = get_player_move(current_player)
        if not place_checker(board, col_idx, current_player):
            print("Column is full. Try another column.")
            continue
        
        print_board(board)
        
        if check_win(board, current_player):
            print(f"Player {current_player} won!")
            break
        
        if is_draw(board):
            print("It's a draw!")
            break
        
        current_player = CHECKERS[(CHECKERS.index(current_player) + 1) % NUM_PLAYERS]

if __name__ == "__main__":
    main()
