import os
import random

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']

def initialize_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')
    # Print column letters
    print('  ' + '   '.join(chr(65 + i) for i in range(COLS)))
    # Print top border
    print('+' + '---+' * COLS)
    for row in board:
        # Print row content
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
        # Print row border
        print('+' + '---+' * COLS)

def get_valid_column(board, player):
    while True:
        col_input = input(f"Player {player}, please enter a column: ").upper()
        if len(col_input) != 1 or not col_input.isalpha():
            print("Invalid input. Please enter a single letter from A to", chr(65 + COLS - 1))
            continue
        col = ord(col_input) - ord('A')
        if col < 0 or col >= COLS:
            print("Column out of range. Please enter a letter from A to", chr(65 + COLS - 1))
            continue
        if board[0][col] != ' ':
            print("Column is full. Please choose another column.")
            continue
        return col

def place_checker(board, col, player):
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = player
            return row
    return -1

def check_win(board, row, col, player):
    # Check horizontal
    count = 0
    for c in range(max(0, col - 3), min(COLS, col + 4)):
        if board[row][c] == player:
            count += 1
            if count == 4:
                return True
        else:
            count = 0

    # Check vertical
    count = 0
    for r in range(max(0, row - 3), min(ROWS, row + 4)):
        if board[r][col] == player:
            count += 1
            if count == 4:
                return True
        else:
            count = 0

    # Check diagonal (top-left to bottom-right)
    count = 0
    for i in range(-3, 4):
        r = row + i
        c = col + i
        if 0 <= r < ROWS and 0 <= c < COLS:
            if board[r][c] == player:
                count += 1
                if count == 4:
                    return True
            else:
                count = 0

    # Check diagonal (top-right to bottom-left)
    count = 0
    for i in range(-3, 4):
        r = row + i
        c = col - i
        if 0 <= r < ROWS and 0 <= c < COLS:
            if board[r][c] == player:
                count += 1
                if count == 4:
                    return True
            else:
                count = 0

    return False

def is_draw(board):
    return all(cell != ' ' for cell in board[0])

def main():
    board = initialize_board()
    players = PLAYER_SYMBOLS[:NUM_PLAYERS]
    current_player = random.choice(players)
    
    while True:
        print_board(board)
        col = get_valid_column(board, current_player)
        row = place_checker(board, col, current_player)
        
        if check_win(board, row, col, current_player):
            print_board(board)
            print(f"Player {current_player} won!")
            break
        
        if is_draw(board):
            print_board(board)
            print("Game ended in a draw!")
            break
        
        # Switch to next player
        current_player = players[(players.index(current_player) + 1) % NUM_PLAYERS]

if __name__ == "__main__":
    main()
