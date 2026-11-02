import os
import random

# Constants
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def clear_screen():
    os.system('clear')

def create_board():
    return [[' ' for _ in range(NUM_COLS)] for _ in range(NUM_ROWS)]

def print_board(board):
    clear_screen()
    print('  ' + '   '.join(chr(i) for i in range(65, 65 + NUM_COLS)))
    print('+' + '---+' * NUM_COLS)
    for row in board:
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
        print('+' + '---+' * NUM_COLS)

def is_valid_column(col, board):
    if col < 0 or col >= NUM_COLS:
        return False
    return board[0][col] == ' '

def drop_checker(board, col, checker):
    for row in reversed(board):
        if row[col] == ' ':
            row[col] = checker
            return

def check_win(board, checker):
    # Check horizontal
    for row in range(NUM_ROWS):
        for col in range(NUM_COLS - 3):
            if all(board[row][col + i] == checker for i in range(4)):
                return True

    # Check vertical
    for col in range(NUM_COLS):
        for row in range(NUM_ROWS - 3):
            if all(board[row + i][col] == checker for i in range(4)):
                return True

    # Check diagonal (/)
    for row in range(NUM_ROWS - 3):
        for col in range(NUM_COLS - 3):
            if all(board[row + i][col + i] == checker for i in range(4)):
                return True

    # Check diagonal (\)
    for row in range(3, NUM_ROWS):
        for col in range(NUM_COLS - 3):
            if all(board[row - i][col + i] == checker for i in range(4)):
                return True

    return False

def check_draw(board):
    return all(board[0][col] != ' ' for col in range(NUM_COLS))

def main():
    board = create_board()
    current_player = random.randint(0, NUM_PLAYERS - 1)
    game_over = False

    print_board(board)
    while not game_over:
        player_checker = CHECKERS[current_player]

        print(f"Player {player_checker}, please enter a column:")
        while True:
            try:
                user_input = input().strip().upper()
                col = ord(user_input) - 65  # Convert letter to index (A=0, B=1, etc.)
                if is_valid_column(col, board):
                    break
                print("Invalid column, please try again.")
            except (ValueError, IndexError):
                print("Invalid input, please enter a valid column.")

        drop_checker(board, col, player_checker)
        print_board(board)

        if check_win(board, player_checker):
            print(f"Player {player_checker} won!")
            game_over = True
        elif check_draw(board):
            print("The game is a draw!")
            game_over = True
        else:
            current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
