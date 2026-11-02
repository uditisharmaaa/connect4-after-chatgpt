import os
import random

# Constants
ROWS = 6
COLUMNS = 7
NUM_PLAYERS = 2
PLAYERS = ['X', 'O', 'V', 'H', 'M'][:NUM_PLAYERS]

def initialize_board():
    return [[' ' for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    # Print column headers
    print('  ' + '   '.join([chr(65 + i) for i in range(COLUMNS)]))
    
    # Print the board
    for row in board:
        print('+---+' * COLUMNS)
        print('|' + '|'.join([f' {cell} ' for cell in row]) + '|')
    print('+---+' * COLUMNS)

def is_valid_input(col, board):
    if len(col) != 1 or not col.isupper():
        return False
    column = ord(col) - 65
    if column < 0 or column >= COLUMNS:
        return False
    # Check if column is full
    return board[0][column] == ' '

def place_checker(board, col, player):
    column = ord(col) - 65
    for row in range(ROWS-1, -1, -1):
        if board[row][column] == ' ':
            board[row][column] = player
            return True
    return False

def check_win(board, player):
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
    for row in range(ROWS):
        for col in range(COLUMNS):
            if board[row][col] == player:
                for dr, dc in directions:
                    count = 1
                    for i in range(1, 4):
                        r, c = row + i * dr, col + i * dc
                        if 0 <= r < ROWS and 0 <= c < COLUMNS and board[r][c] == player:
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
    current_player = random.choice(PLAYERS)
    
    while True:
        os.system('clear')
        print_board(board)
        
        if is_draw(board):
            print("Game is a draw!")
            break
        
        col = input(f"Player {current_player}, please enter a column: ").strip().upper()
        if not is_valid_input(col, board):
            print("Invalid input. Please try again.")
            continue
        
        if place_checker(board, col, current_player):
            if check_win(board, current_player):
                os.system('clear')
                print_board(board)
                print(f"Player {current_player} won!")
                break
            # Switch player
            current_player = PLAYERS[(PLAYERS.index(current_player) + 1) % NUM_PLAYERS]

if __name__ == "__main__":
    main()
