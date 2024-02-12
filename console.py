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

    def do_create(self, args):
        """Creates a new instance of BaseModel,
	saves it (to the JSON file) and prints the id\n
	"""
        if not args:
            print("** class name missing **")
        elif exist(args[0]):
            print("** class doesn't exist **")
        else:
            bm = BaseModel()
            bm.save()

    def do_show(self, args):
        """Prints the string representation of an instance based
	on the class name and id\n
	"""
        if not args:
            print("** class name missing **")
        elif exist(args[0]):
            print("** class doesn't exist **")
        elif not args[1]:
            print("** instance id missing **")
        else:
            bm = BaseModel()

    def do_destroy(self, args):
        """Deletes an instance based on the class name and id
	(save the change into the JSON file).\n
	"""
        if not args:
            print("** class name missing **")
        elif exist(args[0]):
            print("** class doesn't exist **")
        elif not args[1]:
            print("** instance id missing **")
        else:
            bm = BaseModel()

    def do_all(self, args):
        """Prints all string representation of all instances based
	or not on the class name.\n
	"""
        if exist(args[0]):
            print("** class doesn't exist **")
        else:
            all_objs = storage.all()
            print("-- Reloaded objects --")
            for obj_id in all_objs.keys():
                obj = all_objs[obj_id]
                print(obj)

    def do_update(self, args):
        '''Updates an instance based on the class name and id
	by adding or updating attribute
	(save the change into the JSON file)
	Usage: update <class name> <id> <attribute name> "<attribute value>"
	'''
        if not args:
            print("** class name missing **")
        elif exist(args[0]):
            print("** class doesn't exist **")
        elif not args[1]:
            print("** instance id missing **")
        else:
            bm = BaseModel()

if __name__ == '__main__':
    HBNBCommand().cmdloop()
