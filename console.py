#!/usr/bin/python3
"""Command Interpreter Model"""
import cmd


class HBNBCommand(cmd.Cmd):
    """class that contains the entry point of the command interpreter"""
    prompt = "(hbnb) "

    def __init__(self):
        """Initialization"""
        super().__init__()

    def do_help(self, args):
        """Returns information about Class methods"""
        super().do_help(args)

    def emptyline(self):
        """Do nothing"""
        return False 

    def do_quit(self, args):
        """Quit command to exit the program"""
        return True

    def do_EOF(self, args):
        """EOF command to exit the program"""
        return True

if __name__ == '__main__':
    HBNBCommand().cmdloop()
