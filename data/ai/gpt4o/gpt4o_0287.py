import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = ['X', 'O']  # Additional players can be added

def clear_screen():
    os.system('clear')  # For Unix/Linux systems

def create_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    print('  ' + '   '.join(chr(65 + i) for i in range(COLS)))
    print('+' + '---+' * COLS)
    for row in board:
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
        print('+' + '---+' * COLS)

def is_valid_move(column, board):
    if column < 0 or column >= COLS:
        return False
    return board[0][column] == ' '

def make_move(column, player, board):
    for row in reversed(board):
        if row[column] == ' ':
            row[column] = player
            return

def check_winner(board):
    # Horizontal check
    for row in range(ROWS):
        for col in range(COLS - 3):
            if board[row][col] == board[row][col + 1] == board[row][col + 2] == board[row][col + 3] != ' ':
                return True

    # Vertical check
    for row in range(ROWS - 3):
        for col in range(COLS):
            if board[row][col] == board[row + 1][col] == board[row + 2][col] == board[row + 3][col] != ' ':
                return True

    # Diagonal check (/)
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if board[row][col] == board[row - 1][col + 1] == board[row - 2][col + 2] == board[row - 3][col + 3] != ' ':
                return True

    # Diagonal check (\)
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if board[row][col] == board[row + 1][col + 1] == board[row + 2][col + 2] == board[row + 3][col + 3] != ' ':
                return True

    return False

def check_draw(board):
    for row in board:
        if ' ' in row:
            return False
    return True

def main():
    board = create_board()
    player_count = len(PLAYERS)
    current_player = random.randint(0, player_count - 1)

    while True:
        clear_screen()
        print_board(board)
        current_player_char = PLAYERS[current_player]
        print(f"Player {current_player_char}, please enter a column:")

        while True:
            move = input().strip().upper()
            if len(move) == 1 and 'A' <= move <= chr(65 + COLS - 1):
                col = ord(move) - 65
                if is_valid_move(col, board):
                    make_move(col, current_player_char, board)
                    break
                else:
                    print("Column is full. Try a different column:")
            else:
                print("Invalid input. Please enter a valid column letter:")

        if check_winner(board):
            clear_screen()
            print_board(board)
            print(f"Player {current_player_char} won!")
            break

        if check_draw(board):
            clear_screen()
            print_board(board)
            print("It's a draw!")
            break

        current_player = (current_player + 1) % player_count

if __name__ == "__main__":
    main()
