#!/usr/bin/python3
"""Command Interpreter Model"""
import cmd
import re
from shlex import split
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review


def parse(arg):
    """
    Parses a string containing optional curly braces {} and/or brackets [].

    Args:
        arg (str): The string to be parsed.

    Returns:
        list: A list containing the elements of the string, 
                separated and stripped of commas,
                with optional curly braces or brackets included as separate elements.
    """
    curly_braces = re.search(r"\{(.*?)\}", arg)
    brackets = re.search(r"\[(.*?)\]", arg)
    if curly_braces is None:
        if brackets is None:
            return [i.strip(",") for i in split(arg)]
        else:
            lexer = split(arg[:brackets.span()[0]])
            retl = [i.strip(",") for i in lexer]
            retl.append(brackets.group())
            return retl
    else:
        lexer = split(arg[:curly_braces.span()[0]])
        retl = [i.strip(",") for i in lexer]
        retl.append(curly_braces.group())
        return retl


class HBNBCommand(cmd.Cmd):
    """class that contains the entry point of the command interpreter

    Args:
        cmd (str): gives all entry point to the Cmd tool 
    """
    prompt = "(hbnb) "
    __classes = {
        "BaseModel",
        "User",
        "State",
        "City",
        "Place",
        "Amenity",
        "Review"
    }
    
    def do_quit(self, arg):
        """Quit functionality 

        Args:
            arg (str): command give 

        Returns:
            bool: Ends the interpreter
        """
        return True
    
    def do_EOF(self, arg):
        """EOF signal to exit the program.

        Args:
            arg (str): signal to exit the program

        Returns:
            bool: EOF signal to exit the program
        """
        print("")
        return True
    
    def emptyline(self):
        """Do nothing upon receiving an empty line.

        Returns:
            bool: Do nothing upon receiving an empty line.
        """
        return False
    
    def default(self, arg):
        """
        Default behavior for the cmd module when 
            the input command is not recognized.

        Args:
            arg (str): The input command string that is not recognized.

        Returns:
            bool: False if the command is not recognized,
                otherwise the result of executing the recognized
                command.
        """
        argdict = {
            "all": self.do_all,
            "show": self.do_show,
            "destroy": self.do_destroy,
            "count": self.do_count,
            "update": self.do_update
        }
        match = re.search(r"\.", arg)
        if match:
            # Split the command into two parts: command name and arguments
            command_parts = arg.split('.', 1)
            command_name = command_parts[0].strip()
            arguments = command_parts[1].strip()

        # Check if the command name is recognized
        if command_name in argdict:
            # Call the corresponding method with the arguments
            return argdict[command_name](arguments)

        print("*** Unknown syntax: {}".format(arg))
        return False
    
    def do_create(self, line):
        """
        Create a new instance of a specified class with given attributes.

        Usage: create <class> <key1>=<value1> <key2>=<value2> cont

        Args
            line (str): A string containing the command and its arguments.

        Raises:
            SyntaxError: If no class name is provided in the command.
            NameError: If the specified class does not exist.

        Prints:
            str: The id of the newly created instance.
        """
        try:
            if not line:
                raise SyntaxError()
            my_list = line.split(" ")

            kwargs = {}
            for i in range(1, len(my_list)):
                key, value = tuple(my_list[i].split("="))
                if value[0] == '"':
                    value = value.strip('"').replace("_", " ")
                else:
                    try:
                        value = eval(value)
                    except (SyntaxError, NameError):
                        continue
                kwargs[key] = value

            if kwargs == {}:
                obj = eval(my_list[0])()
            else:
                obj = eval(my_list[0])(**kwargs)
                storage.new(obj)
            print(obj.id)
            obj.save()

        except SyntaxError:
            print("** class name missing **")
        except NameError:
            print("** class doesn't exist **")
    
    def do_show(self, arg):
        """
        Display the string representation of a class instance with the given ID.
        Usage:
            show <class> <id> or <class>.show(<id>)
        Args:
            arg (str): A string containing the class name and
                        the ID of the instance,
                        separated by whitespace or a dot,
                        or provided as a method call.
        Prints:
            str: The string representation of the class instance.
        Raises:
            ValueError: If the input command is incomplete or invalid.
        """
        argl = parse(arg)
        objdict = storage.all()
        if len(argl) == 0:
            print("** class name missing **")
        elif argl[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif len(argl) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(argl[0], argl[1]) not in objdict:
            print("** no instance found **")
        else:
            print(objdict["{}.{}".format(argl[0], argl[1])])

    def do_destroy(self, arg):
        """
        Delete a class instance with the specified ID.
        Usage: destroy <class> <id> or <class>.destroy(<id>)
        Args:
            arg (str): A string containing the class name and
                        the ID of the instance,
                        separated by whitespace or a dot,
                        or provided as a method call.
        """
        argl = parse(arg)
        objdict = storage.all()
        if len(argl) == 0:
            print("** class name missing **")
        elif argl[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif len(argl) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(argl[0], argl[1]) not in objdict.keys():
            print("** no instance found **")
        else:
            del objdict["{}.{}".format(argl[0], argl[1])]
            storage.save()

    def do_all(self, arg):
        """Display string representations of instances.

        Usage: 
            - all: Display string representations of all instantiated objects.
            - all <class>: Display string representations of instances of a given class.
            - <class>.all(): Alternate syntax for displaying instances of a given class.

        Args:
            arg (str): A string containing the class name or a method call.

        Notes:
            If a class is specified, only instances of that class are displayed.
            If no class is specified, all instantiated objects are displayed.
        """
        argl = parse(arg)
        if len(argl) > 0 and argl[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        else:
            objl = []
            for obj in storage.all().values():
                if len(argl) > 0 and argl[0] == obj.__class__.__name__:
                    objl.append(obj.__str__())
                elif len(argl) == 0:
                    objl.append(obj.__str__())
            print(objl)

    def do_count(self, arg):
        """Retrieve the number of instances of a given class.
        Usage: 
            - count <class>: Retrieve the number of instances of the specified class.
            - <class>.count(): Alternate syntax for retrieving the number of instances of a class.
        Args:
            arg (str): A string containing the class name or a method call.
        """
        argl = parse(arg)
        count = 0
        for obj in storage.all().values():
            if argl[0] == obj.__class__.__name__:
                count += 1
        print(count)

    def do_update(self, arg):
        """
        Update a class instance with the specified ID by adding or updating 
                    attribute key/value pairs or a dictionary.

        Usage:
            - update <class> <id> <attribute_name> <attribute_value>: 
                            Update a specific attribute of an instance.
                            
            - <class>.update(<id>, <attribute_name>, <attribute_value>): 
                            Alternate syntax for updating a specific attribute.
                            
            - <class>.update(<id>, <dictionary>): 
                            Update multiple attributes of an instance using a dictionary.

        Args:
            arg (str): A string containing the class name, ID, attribute name/value, or a dictionary.

        Returns:
            bool: True if the update was successful, False otherwise.
        """
        argl = parse(arg)
        objdict = storage.all()

        if len(argl) == 0:
            print("** class name missing **")
            return False
        if argl[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
            return False
        if len(argl) == 1:
            print("** instance id missing **")
            return False
        if "{}.{}".format(argl[0], argl[1]) not in objdict.keys():
            print("** no instance found **")
            return False
        if len(argl) == 2:
            print("** attribute name missing **")
            return False
        if len(argl) == 3:
            try:
                type(eval(argl[2])) != dict
            except NameError:
                print("** value missing **")
                return False

        if len(argl) == 4:
            obj = objdict["{}.{}".format(argl[0], argl[1])]
            if argl[2] in obj.__class__.__dict__.keys():
                valtype = type(obj.__class__.__dict__[argl[2]])
                obj.__dict__[argl[2]] = valtype(argl[3])
            else:
                obj.__dict__[argl[2]] = argl[3]
        elif type(eval(argl[2])) == dict:
            obj = objdict["{}.{}".format(argl[0], argl[1])]
            for k, v in eval(argl[2]).items():
                if (k in obj.__class__.__dict__.keys() and
                        type(obj.__class__.__dict__[k]) in {str, int, float}):
                    valtype = type(obj.__class__.__dict__[k])
                    obj.__dict__[k] = valtype(v)
                else:
                    obj.__dict__[k] = v
        storage.save()


if __name__ == "__main__":
    HBNBCommand().cmdloop()
