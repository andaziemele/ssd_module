import os
import re


class CLIApp:
    """
    Class to implement app and app methods.
    """
    def list_directory(self):
        """
        List directory contents.
        :return: results of os.listdir
        """
        return os.listdir('')

    def add_numbers(self, num_input):
        """
        Use regex to find numbers and add them
        :param num_input: inputted string with numbers
        :return: sum of first two digits
        """
        numbers = re.findall(r'\d+', num_input)
        if len(numbers) >= 2:
            # convert first two matches to integers and add them
            result = int(numbers[0]) + int(numbers[1])
            return result
        else:
            return ValueError

    def show_help(self):
        """
        Print available commands to the user.
        :return: string of commands
        """
        return "Available commands:\nLIST - List contents of the current directory\nADD <n1> <n2> - Add two numbers\nHELP - Show this help message\nEXIT - Exit the shell"

    def cli(self):
        """
        Implement CLI.
        """
        print("Welcome to the CLI. Type HELP for a list of commands.")
        while True:
            command = input("Enter command: ").strip().upper()
            if command == "LIST":
                print("\n".join(self.list_directory()))
            elif command.startswith("ADD"):
                try:
                    result = self.add_numbers(command)
                    print(f"Result: {result}")
                except ValueError:
                    print("Error: ADD command requires two digits.")
            elif command.upper() == "HELP":
                print(self.show_help())
            elif command.upper() == "EXIT":
                print("Exiting the shell. Goodbye!")
                break
            else:
                print("Unknown command. Type HELP for a list of commands.")


if __name__ == "__main__":
    app = CLIApp()
    app.cli()
