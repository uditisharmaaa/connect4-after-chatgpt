import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = 2

def initialize_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    # Clear the screen
    os.system('clear')
    # Print column headers
    print('  ' + '   '.join([chr(ord('A') + i) for i in range(COLS)]))
    # Print the board
    for row in board:
        print('+---' * COLS + '+')
        print('| ' + ' | '.join(row) + ' |')
    print('+---' * COLS + '+')

def get_player_checkers(num_players):
    checkers = ['X', 'O', 'V', 'H', 'M']
    return checkers[:num_players]

def get_random_first_player(num_players):
    return random.randint(0, num_players - 1)

def is_valid_column(col, board):
    if len(col) != 1:
        return False
    col_letter = col.upper()
    if col_letter < 'A' or col_letter > chr(ord('A') + COLS - 1):
        return False
    col_index = ord(col_letter) - ord('A')
    return board[0][col_index] == ' '

def place_checker(board, col, checker):
    col_index = ord(col.upper()) - ord('A')
    for row in range(ROWS - 1, -1, -1):
        if board[row][col_index] == ' ':
            board[row][col_index] = checker
            return (row, col_index)
    return None

def check_win(board, row, col):
    checker = board[row][col]
    # Check horizontal
    count = 1
    # Left
    for c in range(col - 1, max(-1, col - 4), -1):
        if board[row][c] == checker:
            count += 1
        else:
            break
    # Right
    for c in range(col + 1, min(COLS, col + 4)):
        if board[row][c] == checker:
            count += 1
        else:
            break
    if count >= 4:
        return True

    # Check vertical
    count = 1
    # Up
    for r in range(row - 1, max(-1, row - 4), -1):
        if board[r][col] == checker:
            count += 1
        else:
            break
    # Down
    for r in range(row + 1, min(ROWS, row + 4)):
        if board[r][col] == checker:
            count += 1
        else:
            break
    if count >= 4:
        return True

    # Check diagonal (top-left to bottom-right)
    count = 1
    # Top-left
    r, c = row - 1, col - 1
    while r >= 0 and c >= 0 and abs(r - row) < 4:
        if board[r][c] == checker:
            count += 1
            r -= 1
            c -= 1
        else:
            break
    # Bottom-right
    r, c = row + 1, col + 1
    while r < ROWS and c < COLS and abs(r - row) < 4:
        if board[r][c] == checker:
            count += 1
            r += 1
            c += 1
        else:
            break
    if count >= 4:
        return True

    # Check diagonal (top-right to bottom-left)
    count = 1
    # Top-right
    r, c = row - 1, col + 1
    while r >= 0 and c < COLS and abs(r - row) < 4:
        if board[r][c] == checker:
            count += 1
            r -= 1
            c += 1
        else:
            break
    # Bottom-left
    r, c = row + 1, col - 1
    while r < ROWS and c >= 0 and abs(r - row) < 4:
        if board[r][c] == checker:
            count += 1
            r += 1
            c -= 1
        else:
            break
    if count >= 4:
        return True

    return False

def is_draw(board):
    return all(cell != ' ' for row in board for cell in row)

def play_game():
    board = initialize_board()
    checkers = get_player_checkers(PLAYERS)
    current_player = get_random_first_player(PLAYERS)
    
    while True:
        print_board(board)
        print(f"Player {checkers[current_player]}, please enter a column:")
        
        while True:
            col = input().strip().upper()
            if is_valid_column(col, board):
                break
            print("Invalid column. Please try again:")
        
        position = place_checker(board, col, checkers[current_player])
        if check_win(board, position[0], position[1]):
            print_board(board)
            print(f"Player {checkers[current_player]} won!")
            break
        if is_draw(board):
            print_board(board)
            print("It's a draw!")
            break
        
        current_player = (current_player + 1) % PLAYERS

if __name__ == '__main__':
    play_game()
