import random
import os

ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def create_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')
    print('  ' + '   '.join(chr(65 + i) for i in range(COLS)))
    for row in board:
        print('+---' * COLS + '+')
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
    print('+---' * COLS + '+')

def drop_checker(board, checker, col):
    for i in reversed(range(ROWS)):
        if board[i][col] == ' ':
            board[i][col] = checker
            return True
    return False

def check_winner(board, checker):
    for row in range(ROWS):
        for col in range(COLS):
            if col <= COLS - 4 and all(board[row][c] == checker for c in range(col, col+4)):
                return True
            if row <= ROWS - 4 and all(board[r][col] == checker for r in range(row, row+4)):
                return True
            if col <= COLS - 4 and row <= ROWS - 4 and all(board[row+i][col+i] == checker for i in range(4)):
                return True
            if col >= 3 and row <= ROWS - 4 and all(board[row+i][col-i] == checker for i in range(4)):
                return True
    return False

def check_draw(board):
    return all(board[0][col] != ' ' for col in range(COLS))

def main():
    board = create_board()
    checkers = CHECKERS[:PLAYERS]
    current_player = random.randint(0, PLAYERS - 1)
    
    print_board(board)
    while True:
        current_checker = checkers[current_player]
        move = input(f'Player {current_checker}, please enter a column: ')
        
        if len(move) == 1 and 'A' <= move <= chr(65 + COLS - 1):
            col = ord(move) - 65
            if drop_checker(board, current_checker, col):
                print_board(board)
                if check_winner(board, current_checker):
                    print(f'Player {current_checker} won!')
                    break
                if check_draw(board):
                    print('The game is a draw!')
                    break
                current_player = (current_player + 1) % PLAYERS
            else:
                print("Column is full! You lose your turn.")
        else:
            print("Invalid input. Try again.")

if __name__ == '__main__':
    main()
