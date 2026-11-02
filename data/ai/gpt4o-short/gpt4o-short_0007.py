import random
import os

# Constants
ROWS = 6
COLS = 7
PLAYERS = ['X', 'O', 'V', 'H', 'M']  # Player markers
NUM_PLAYERS = min(max(int(input('Enter number of players [2-5]: ')), 2), 5)  # Validate number of players

def clear_screen():
    os.system('clear')  # Clear the terminal

def create_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    clear_screen()
    print("  " + "   ".join(chr(65 + i) for i in range(COLS)))  # Print column headers A-G
    for row in board:
        print('| ' + ' | '.join(row) + ' |')  # Print board rows
    print('-' * 29)

def select_random_player():
    return random.choice(PLAYERS[:NUM_PLAYERS])

def is_valid_move(board, column):
    if column < 0 or column >= COLS:
        return False
    return board[0][column] == ' '

def get_next_open_row(board, column):
    for r in range(ROWS - 1, -1, -1):
        if board[r][column] == ' ':
            return r
    return None

def drop_piece(board, row, column, piece):
    board[row][column] = piece

def winning_move(board, piece):
    # Horizontal check
    for c in range(COLS - 3):
        for r in range(ROWS):
            if all(board[r][c+i] == piece for i in range(4)):
                return True

    # Vertical check
    for c in range(COLS):
        for r in range(ROWS - 3):
            if all(board[r+i][c] == piece for i in range(4)):
                return True

    # Positive diagonal check
    for c in range(COLS - 3):
        for r in range(ROWS - 3):
            if all(board[r+i][c+i] == piece for i in range(4)):
                return True

    # Negative diagonal check
    for c in range(COLS - 3):
        for r in range(3, ROWS):
            if all(board[r-i][c+i] == piece for i in range(4)):
                return True

    return False

def is_draw(board):
    return all(board[0][c] != ' ' for c in range(COLS))

def play_game():
    board = create_board()
    game_over = False
    turn = 0
    current_player = select_random_player()

    while not game_over:
        print_board(board)
        print(f"Player {current_player}'s turn")

        col_letter = input("Select a column (A-G): ").upper()
        col = ord(col_letter) - ord('A')

        if is_valid_move(board, col):
            row = get_next_open_row(board, col)
            drop_piece(board, row, col, current_player)

            if winning_move(board, current_player):
                print_board(board)
                print(f"Player {current_player} wins!")
                game_over = True
            elif is_draw(board):
                print_board(board)
                print("It's a draw!")
                game_over = True
            else:
                turn += 1
                current_player = PLAYERS[turn % NUM_PLAYERS]
        else:
            print("Invalid move. Try another column.")

if __name__ == "__main__":
    play_game()
