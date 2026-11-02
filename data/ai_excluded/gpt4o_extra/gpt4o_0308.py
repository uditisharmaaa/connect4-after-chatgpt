import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def clear_screen():
    os.system('clear')

def create_board():
    return [[' ' for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    clear_screen()
    print('  ' + '   '.join(chr(ord('A') + i) for i in range(COLUMNS)))
    print('+---' * COLUMNS + '+')
    for row in board:
        print('|' + '|'.join(' ' + cell + ' ' for cell in row) + '|')
        print('+---' * COLUMNS + '+')

def is_valid_column(column, board):
    if column < 0 or column >= COLUMNS:
        return False
    if board[0][column] != ' ':
        return False
    return True

def drop_checker(column, player_checker, board):
    for row in range(ROWS - 1, -1, -1):
        if board[row][column] == ' ':
            board[row][column] = player_checker
            return

def check_winner(board, player_checker):
    # Horizontal
    for row in range(ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row][col + i] == player_checker for i in range(4)):
                return True
            
    # Vertical
    for col in range(COLUMNS):
        for row in range(ROWS - 3):
            if all(board[row + i][col] == player_checker for i in range(4)):
                return True

    # Diagonal (bottom left to top right)
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if all(board[row + i][col + i] == player_checker for i in range(4)):
                return True

    # Diagonal (top left to bottom right)
    for row in range(3, ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row - i][col + i] == player_checker for i in range(4)):
                return True

    return False

def is_draw(board):
    return all(board[0][col] != ' ' for col in range(COLUMNS))

def main():
    board = create_board()
    current_player = random.randint(0, PLAYERS - 1)
    print_board(board)
    
    while True:
        player_checker = CHECKERS[current_player]
        player_input = input(f"Player {player_checker}, please enter a column: ").strip().upper()

        if len(player_input) != 1 or not player_input.isalpha():
            print("Invalid input. Please enter a valid column letter.")
            continue

        column = ord(player_input) - ord('A')

        if not is_valid_column(column, board):
            print("Invalid column. Please choose a different column.")
            continue

        drop_checker(column, player_checker, board)
        print_board(board)

        if check_winner(board, player_checker):
            print(f"Player {player_checker} won!")
            break

        if is_draw(board):
            print("The game is a draw!")
            break

        current_player = (current_player + 1) % PLAYERS

if __name__ == "__main__":
    main()
