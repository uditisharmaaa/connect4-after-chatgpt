import os
import random

# Constant global variables
BOARD_ROWS = 6
BOARD_COLS = 7
NUM_PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']

# Function to create the board
def create_board():
    board = []
    for _ in range(BOARD_ROWS):
        row = []
        for _ in range(BOARD_COLS):
            row.append(' ')
        board.append(row)
    return board

# Function to print the board
def print_board(board):
    os.system('clear')
    print('  ' + '   '.join(chr(65 + i) for i in range(BOARD_COLS)))
    print('+---' * BOARD_COLS + '+')
    for row in board:
        print('|   ' * BOARD_COLS + '|')
        print('| ' + ' | '.join(row) + ' |')
        print('+---' * BOARD_COLS + '+')
    print('  ' + '   '.join(chr(65 + i) for i in range(BOARD_COLS)))

# Function to get the player's move
def get_player_move(player):
    while True:
        move = input(f'Player {player}, please enter a column: ').upper()
        if len(move)!= 1 or move not in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ' or ord(move) - 65 >= BOARD_COLS:
            print('Invalid input. Please try again.')
        else:
            return ord(move) - 65

# Function to place the checker
def place_checker(board, player, col):
    for row in reversed(board):
        if row[col] == ' ':
            row[col] = CHECKERS[player - 1]
            break
    else:
        print('Column is full. Try again.')
        return False
    return True

# Function to check for a win
def check_win(board, player):
    # Check horizontal locations for win
    for row in board:
        for i in range(len(row) - 3):
            if row[i] == CHECKERS[player - 1] and row[i + 1] == CHECKERS[player - 1] and row[i + 2] == CHECKERS[player - 1] and row[i + 3] == CHECKERS[player - 1]:
                return True

    # Check vertical locations for win
    for col in range(len(board[0])):
        for i in range(len(board) - 3):
            if board[i][col] == CHECKERS[player - 1] and board[i + 1][col] == CHECKERS[player - 1] and board[i + 2][col] == CHECKERS[player - 1] and board[i + 3][col] == CHECKERS[player - 1]:
                return True

    # Check positively sloped diagonals
    for row in range(len(board) - 3):
        for col in range(len(board[0]) - 3):
            if board[row][col] == CHECKERS[player - 1] and board[row + 1][col + 1] == CHECKERS[player - 1] and board[row + 2][col + 2] == CHECKERS[player - 1] and board[row + 3][col + 3] == CHECKERS[player - 1]:
                return True

    # Check negatively sloped diagonals
    for row in range(3, len(board)):
        for col in range(len(board[0]) - 3):
            if board[row][col] == CHECKERS[player - 1] and board[row - 1][col + 1] == CHECKERS[player - 1] and board[row - 2][col + 2] == CHECKERS[player - 1] and board[row - 3][col + 3] == CHECKERS[player - 1]:
                return True

    return False

# Function to check for a draw
def check_draw(board):
    for row in board:
        for col in row:
            if col == ' ':
                return False
    return True

# Main function
def main():
    board = create_board()
    current_player = random.randint(1, NUM_PLAYERS)
    while True:
        print_board(board)
        col = get_player_move(current_player)
        if place_checker(board, current_player, col):
            if check_win(board, current_player):
                print_board(board)
                print(f'Player {CHECKERS[current_player - 1]} won!')
                break
            elif check_draw(board):
                print_board(board)
                print('It\'s a draw!')
                break
            current_player = (current_player % NUM_PLAYERS) + 1

if __name__ == '__main__':
    main()
