import os
import random

# Global constants for board dimension and number of players
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M'][:PLAYERS]

def clear_screen():
    os.system('clear')

def create_board():
    return [[' ']*COLUMNS for _ in range(ROWS)]

def print_board(board):
    clear_screen()
    print('  ' + '   '.join(chr(65 + i) for i in range(COLUMNS)))
    print('+' + '---+'*COLUMNS)
    for row in board:
        print('| ' + ' | '.join(row) + ' |')
        print('+' + '---+'*COLUMNS)

def is_valid_move(board, column):
    return board[0][column] == ' '

def get_valid_move(board):
    while True:
        move = input("Please enter a column: ").upper()
        if len(move) == 1 and 'A' <= move <= chr(65 + COLUMNS - 1):
            column = ord(move) - 65
            if is_valid_move(board, column):
                return column
            else:
                print("Column is full.")
        else:
            print("Invalid input.")

def place_checker(board, column, checker):
    for row in reversed(board):
        if row[column] == ' ':
            row[column] = checker
            break

def check_for_win(board, checker):
    def check_direction(dr, dc, r, c):
        count = 0
        for _ in range(4):
            if (0 <= r < ROWS) and (0 <= c < COLUMNS) and board[r][c] == checker:
                count += 1
                r += dr
                c += dc
            else:
                break
        return count == 4
    
    for r in range(ROWS):
        for c in range(COLUMNS):
            if board[r][c] == checker:
                if (check_direction(0, 1, r, c) or  # Horizontal
                    check_direction(1, 0, r, c) or  # Vertical
                    check_direction(1, 1, r, c) or  # Diagonal /
                    check_direction(1, -1, r, c)): # Diagonal \
                    return True
    return False

def is_draw(board):
    return all(board[0][c] != ' ' for c in range(COLUMNS))

def connect4():
    board = create_board()
    print_board(board)
    
    current_player_index = random.randint(0, PLAYERS - 1)
    
    while True:
        print_board(board)
        print(f"Player {CHECKERS[current_player_index]}'s turn.")
        column = get_valid_move(board)
        place_checker(board, column, CHECKERS[current_player_index])
        
        if check_for_win(board, CHECKERS[current_player_index]):
            print_board(board)
            print(f"Player {CHECKERS[current_player_index]} won!")
            break
        
        if is_draw(board):
            print_board(board)
            print("The game is a draw!")
            break
        
        current_player_index = (current_player_index + 1) % PLAYERS

if __name__ == "__main__":
    connect4()
