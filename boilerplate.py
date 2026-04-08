"""
python boilerplate for scripts
describe the program here
"""

import sys # import sys so we can use the exit function


def main():
    """
    main entry point
    All functions should have a docstring
    """
    print("Hello, world!")
    return 0 # by convention, return 0 for success, non-zero otherwise


if __name__ == "__main__":
    """
    Main guard or module guard. 
    It prevents code from being executed when the script is imported as a module in another Python script.
    """
    # used to exit the program with the exit code returned by the main function
    sys.exit(main())
    # After runnung the script check in the command line the result: echo $?
