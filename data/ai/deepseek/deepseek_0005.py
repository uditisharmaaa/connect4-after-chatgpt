import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def create_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')
    print('  ' + '   '.join(chr(65 + i) for i in range(COLS)))
    print('+' + '---+' * COLS)
    for row in board:
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
        print('+' + '---+' * COLS)

def is_valid_move(board, col):
    return 0 <= col < COLS and board[0][col] == ' '

def drop_checker(board, col, checker):
    for row in range(ROWS-1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = checker
            return row
    return -1

def check_win(board, row, col, checker):
    directions = [
        (0, 1), (1, 0), (1, 1), (1, -1)
    ]
    for dr, dc in directions:
        count = 1
        for step in range(1, 4):
            r, c = row + dr * step, col + dc * step
            if 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == checker:
                count += 1
            else:
                break
        for step in range(1, 4):
            r, c = row - dr * step, col - dc * step
            if 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == checker:
                count += 1
            else:
                break
        if count >= 4:
            return True
    return False

def is_draw(board):
    return all(cell != ' ' for row in board for cell in row)

def main():
    board = create_board()
    current_player = random.randint(0, PLAYERS - 1)
    checkers = CHECKERS[:PLAYERS]
    
    while True:
        print_board(board)
        print(f"Player {checkers[current_player]}, please enter a column: ")
        
        while True:
            try:
                col = input().upper()
                if len(col) != 1 or not col.isalpha():
                    raise ValueError
                col = ord(col) - ord('A')
                if not is_valid_move(board, col):
                    raise ValueError
                break
            except ValueError:
                print("Invalid input. Please enter a valid column (A-{}): ".format(chr(65 + COLS - 1)))
        
        row = drop_checker(board, col, checkers[current_player])
        if check_win(board, row, col, checkers[current_player]):
            print_board(board)
            print(f"Player {checkers[current_player]} won!")
            break
        if is_draw(board):
            print_board(board)
            print("Game ended in a draw!")
            break
        
        current_player = (current_player + 1) % PLAYERS

if __name__ == "__main__":
    main()
