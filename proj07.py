###################################################################################################
#
#   CSE 231 Project 7
#       Mini-Crossword Project
#           Load a CSV file with all information of the crossword
#           Generate a crossword object which can be printed
#           User input options include:
#               Display puzzle, printing the crossword object
#               Make a Guess, editing the crossword object with a user input
#               Reveal Answer, editing the crossword with the clue answer
#               Display Hint, finding first disimilarity between user input and clue answer
#               Help Menu, printing the options
#               Restart Puzzle, prompting for a new file
#               Quit,
#
###################################################################################################

from crossword import Crossword
import sys


HELP_MENU = "\nCrossword Puzzler -- Press H at any time to bring up this menu" \
                "\nC n - Display n of the current puzzle's down and across clues" \
                "\nG i j A/D - Make a guess for the clue starting at row i, column j" \
                "\nR i j A/D - Reveal the answer for the clue starting at row i, column j" \
                "\nT i j A/D - Gives a hint (first wrong letter) for the clue starting at row i, column j" \
                "\nH - Display the menu" \
                "\nS - Restart the game" \
                "\nQ - Quit the program"


OPTION_PROMPT = "\nEnter option: "
PUZZLE_PROMPT = "Enter the filename of the puzzle you want to play: "
PUZZLE_FILE_ERROR = "No puzzle found with that filename. Try Again.\n"



ENTER_GUESS = "Enter your guess (use _ for blanks): "
"This clue is already correct!"


def input( prompt=None ):
    """
        DO NOT MODIFY: Uncomment this function when submitting to Codio
        or when using the run_file.py to test your code.
        This function is needed for testing in Codio to echo the input to the output
        Function to get user input from the standard input (stdin) with an optional prompt.
        Args:
            prompt (str, optional): A prompt to display before waiting for input. Defaults to None.
        Returns:
            str: The user input received from stdin.
    """

    if prompt:
        print( prompt, end="" )
    aaa_str = sys.stdin.readline()
    aaa_str = aaa_str.rstrip( "\n" )
    print( aaa_str )
    return aaa_str



def open_puzzle(filename):
    '''
    Read a CSV file into a Crossword
    :param filename:
    :return: Crossword object
    '''
    try:
        obj = Crossword(filename)
        return obj
    except:
        print(PUZZLE_FILE_ERROR)


def display_clues(puzzle, integer=0):
    '''
    Prints out the clues involved in the puzzle
    :param puzzle: name of the crossword object
    :param integer: Number of clues to display
    :return: Clues
    '''
    across_lst = []
    down_lst = []
    for key in puzzle.clues:
        if key[2] == 'A':
            across_lst.append(puzzle.clues[key])
        else:
            down_lst.append(puzzle.clues[key])

    across_lst.sort()
    down_lst.sort()

    # All clues are printed out
    if integer == 0:
        integer = max(len(across_lst), len(down_lst))

    i = 0
    print('\nAcross')
    while i < integer:
        try:
            print(across_lst[i])
        except:
            break
        i += 1

    i = 0
    print('\nDown')
    while i < integer:
        try:
            print(down_lst[i])
        except:
            break
        i += 1
    return


def validate(puzzle, input):
    '''
    assures that the user's input is valid and will result in desired program
    :param puzzle: Crossword Object
    :param input: User's prompt
    :return: Boolean of whether the data entered is valid
    '''
    if len(input) == 0:
        return False

    if input[0] in ['H', 'S', 'Q']:
        if len(input) > 1:
            return False
        else:
            return True
    elif input[0] == 'C':
        if len(input) != 2:
            return False

        else:
            return True

    elif input[0] == 'G' or input[0] == 'R' or input[0] == 'T':
        try:
            variable = puzzle.clues[tuple([int(input[1]), int(input[2]), input[3]])]
            return True
        except:
            return False

    else:
        return False


def main():
    # Attempts to read puzzle
    while True:
        filename = input(PUZZLE_PROMPT)
        puzzle = open_puzzle(filename)
        if puzzle != None:
            break

    display_clues(puzzle)

    print(puzzle)
    print(HELP_MENU)

    while True:
        # Separates all parts of the user input
        option_lst = input(OPTION_PROMPT).strip().split()
        t_f = validate(puzzle, option_lst)

        if t_f is True:
            # Display Puzzle
            if option_lst[0] == 'C':
                try:
                    display_clues(puzzle, int(option_lst[1]))
                except:
                    display_clues(puzzle)

            # User Guess
            elif option_lst[0] == 'G':
                while True:
                    guess = input(ENTER_GUESS).upper()
                    key = (tuple(map(int, (option_lst[1], option_lst[2])))) + (option_lst[3],)

                    try:
                        puzzle.change_guess(puzzle.clues[key], guess)
                        print(puzzle)
                        break

                    except RuntimeError as message:
                        print(message)
                        continue


            # Reveal Answer
            elif option_lst[0] == 'R':
                key = (tuple(map(int, (option_lst[1], option_lst[2])))) + (option_lst[3],)
                puzzle.reveal_answer(puzzle.clues[key])
                print(puzzle)

            # Hint System
            elif option_lst[0] == 'T':
                key = (tuple(map(int, (option_lst[1], option_lst[2])))) + (option_lst[3],)
                i = puzzle.find_wrong_letter(puzzle.clues[key])
                if i != -1:
                    print(f"Letter {i+1} is wrong, it should be {puzzle.clues[key].answer[i]}")
                else:
                    print("This clue is already correct!")

            # Help Menu
            elif option_lst[0] == 'H':
                print(HELP_MENU)

            # Restart a Puzzle
            elif option_lst[0] == 'S':
                while True:
                    filename = input(PUZZLE_PROMPT)
                    puzzle = open_puzzle(filename)
                    if puzzle != None:
                        break

                display_clues(puzzle, 0)
                print(puzzle)
                print(HELP_MENU)

            # Quit Function
            elif option_lst[0] == 'Q':
                break

            solved = puzzle.is_solved()
            if solved is True:
                print("\nPuzzle solved! Congratulations!")
                break
        else:
            print("Invalid option/arguments. Type 'H' for help.")

    pass


if __name__ == "__main__":
    main()
