import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

def clear_screen():
    """Clear the console screen."""
    os.system('clear')

def initialize_board():
    """Initialize the game board with empty spaces."""
    return [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    """Print the game board."""
    clear_screen()
    print("  " + "   ".join(chr(ord('A') + i) for i in range(COLUMNS)))
    print("+---" * COLUMNS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLUMNS + "+")

def get_input(player):
    """Get valid column input from the player."""
    while True:
        choice = input(f"Player {player}, please enter a column: ").strip().upper()
        if len(choice) != 1 or not choice.isalpha():
            print("Invalid input. Please enter a letter corresponding to a column.")
            continue
        column = ord(choice) - ord('A')
        if column < 0 or column >= COLUMNS:
            print("Invalid column. Please enter a valid column letter.")
            continue
        return column

def drop_checker(board, column, checker):
    """Drop the checker into the chosen column."""
    for row in range(ROWS - 1, -1, -1):
        if board[row][column] == " ":
            board[row][column] = checker
            return row, column
    return None

def check_win(board, row, column):
    """Check if the current player has won."""
    def check_direction(dx, dy):
        count = 0
        x, y = row, column
        for _ in range(4):
            if 0 <= x < ROWS and 0 <= y < COLUMNS and board[x][y] == board[row][column]:
                count += 1
                x += dx
                y += dy
            else:
                break
        return count

    # Check all four directions: (horizontal, vertical, diagonal 1, diagonal 2)
    return (check_direction(0, 1) + check_direction(0, -1) - 1 >= 4 or
            check_direction(1, 0) + check_direction(-1, 0) - 1 >= 4 or
            check_direction(1, 1) + check_direction(-1, -1) - 1 >= 4 or
            check_direction(1, -1) + check_direction(-1, 1) - 1 >= 4)

def check_draw(board):
    """Check if the board is completely filled without a winner."""
    return all(cell != " " for row in board for cell in row)

def main():
    """Main function to run the Connect 4 game."""
    board = initialize_board()
    players = CHECKERS[:PLAYERS]
    current_player_index = random.randint(0, PLAYERS - 1)
    clear_screen()
    print_board(board)

    while True:
        current_player = players[current_player_index]
        column = get_input(current_player)

        if not any(board[row][column] == " " for row in range(ROWS)):
            print(f"Column {chr(ord('A') + column)} is full. Please choose another column.")
            continue

        row, col = drop_checker(board, column, current_player)
        print_board(board)

        if check_win(board, row, col):
            print(f"Player {current_player} won!")
            break
        if check_draw(board):
            print("It's a draw!")
            break

        current_player_index = (current_player_index + 1) % PLAYERS

if __name__ == "__main__":
    main()
