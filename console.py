<<<<<<< HEAD
#!/usr/bin/python
"""
Module for console
"""
import cmd
import re
import shlex
import ast
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from models.state import State
from models.city import City


def split_curly_braces(e_arg):
    """
    Splits the curly braces for the update method
    """
    curly_braces = re.search(r"\{(.*?)\}", e_arg)

    if curly_braces:
        id_with_comma = shlex.split(e_arg[:curly_braces.span()[0]])
        id = [i.strip(",") for i in id_with_comma][0]

        str_data = curly_braces.group(1)
        try:
            arg_dict = ast.literal_eval("{" + str_data + "}")
        except Exception:
            print("**  invalid dictionary format **")
            return
        return id, arg_dict
    else:
        commands = e_arg.split(",")
        if commands:
            try:
                id = commands[0]
            except Exception:
                return "", ""
            try:
                attr_name = commands[1]
            except Exception:
                return id, ""
            try:
                attr_value = commands[2]
            except Exception:
                return id, attr_name
            return f"{id}", f"{attr_name} {attr_value}"


class HBNBCommand(cmd.Cmd):
    """
    HBNBCommand console class
    """
    prompt = "(hbnb) "
    valid_classes = ["BaseModel", "User", "Amenity",
                     "Place", "Review", "State", "City"]

    def emptyline(self):
        """
        Do nothing when an empty line is entered.
        """
        pass

    def do_EOF(self, arg):
        """
        EOF (Ctrl+D) signal to exit the program.
        """
        return True

    def do_quit(self, arg):
        """
        Quit command to exit the program.
        """
        return True

    def do_create(self, arg):
        """
        Create a new instance of BaseModel and save it to the JSON file.
        Usage: create <class_name>
        """
        commands = shlex.split(arg)

        if len(commands) == 0:
            print("** class name missing **")
        elif commands[0] not in self.valid_classes:
            print("** class doesn't exist **")
        else:
            new_instance = eval(f"{commands[0]}()")
            storage.save()
            print(new_instance.id)

    def do_show(self, arg):
        """
        Show the string representation of an instance.
        Usage: show <class_name> <id>
        """
        commands = shlex.split(arg)

        if len(commands) == 0:
            print("** class name missing **")
        elif commands[0] not in self.valid_classes:
            print("** class doesn't exist **")
        elif len(commands) < 2:
            print("** instance id missing **")
        else:
            objects = storage.all()

            key = "{}.{}".format(commands[0], commands[1])
            if key in objects:
                print(objects[key])
            else:
                print("** no instance found **")

    def do_destroy(self, arg):
        """
        Delete an instance based on the class name and id.
        Usage: destroy <class_name> <id>
        """
        commands = shlex.split(arg)

        if len(commands) == 0:
            print("** class name missing **")
        elif commands[0] not in self.valid_classes:
            print("** class doesn't exist **")
        elif len(commands) < 2:
            print("** instance id missing **")
        else:
            objects = storage.all()
            key = "{}.{}".format(commands[0], commands[1])
            if key in objects:
                del objects[key]
                storage.save()
            else:
                print("** no instance found **")

    def do_all(self, arg):
        """
        Print the string representation of all instances or a specific class.
        Usage: <User>.all()
                <User>.show()
        """
        objects = storage.all()

        commands = shlex.split(arg)

        if len(commands) == 0:
            for key, value in objects.items():
                print(str(value))
        elif commands[0] not in self.valid_classes:
            print("** class doesn't exist **")
        else:
            for key, value in objects.items():
                if key.split('.')[0] == commands[0]:
                    print(str(value))

    def do_count(self, arg):
        """
        Counts and retrieves the number of instances of a class
        usage: <class name>.count()
        """
        objects = storage.all()

        commands = shlex.split(arg)

        if arg:
            cls_nm = commands[0]

        count = 0

        if commands:
            if cls_nm in self.valid_classes:
                for obj in objects.values():
                    if obj.__class__.__name__ == cls_nm:
                        count += 1
                print(count)
            else:
                print("** invalid class name **")
        else:
            print("** class name missing **")

    def do_update(self, arg):
        """
        Update an instance by adding or updating an attribute.
        Usage: update <class_name> <id> <attribute_name> "<attribute_value>"
        """
        commands = shlex.split(arg)

        if len(commands) == 0:
            print("** class name missing **")
        elif commands[0] not in self.valid_classes:
            print("** class doesn't exist **")
        elif len(commands) < 2:
            print("** instance id missing **")
        else:
            objects = storage.all()

            key = "{}.{}".format(commands[0], commands[1])
            if key not in objects:
                print("** no instance found **")
            elif len(commands) < 3:
                print("** attribute name missing **")
            elif len(commands) < 4:
                print("** value missing **")
            else:
                obj = objects[key]
                curly_braces = re.search(r"\{(.*?)\}", arg)

                if curly_braces:
                    try:
                        str_data = curly_braces.group(1)

                        arg_dict = ast.literal_eval("{" + str_data + "}")

                        attribute_names = list(arg_dict.keys())
                        attribute_values = list(arg_dict.values())
                        try:
                            attr_name1 = attribute_names[0]
                            attr_value1 = attribute_values[0]
                            setattr(obj, attr_name1, attr_value1)
                        except Exception:
                            pass
                        try:
                            attr_name2 = attribute_names[1]
                            attr_value2 = attribute_values[1]
                            setattr(obj, attr_name2, attr_value2)
                        except Exception:
                            pass
                    except Exception:
                        pass
                else:

                    attr_name = commands[2]
                    attr_value = commands[3]

                    try:
                        attr_value = eval(attr_value)
                    except Exception:
                        pass
                    setattr(obj, attr_name, attr_value)

                obj.save()

    def default(self, arg):
        """
        Default behavior for cmd module when input is invalid
        """
        arg_list = arg.split('.')

        cls_nm = arg_list[0]  # incoming class name

        command = arg_list[1].split('(')

        cmd_met = command[0]  # incoming command method

        e_arg = command[1].split(')')[0]  # extra arguments

        method_dict = {
                'all': self.do_all,
                'show': self.do_show,
                'destroy': self.do_destroy,
                'update': self.do_update,
                'count': self.do_count
                }

        if cmd_met in method_dict.keys():
            if cmd_met != "update":
                return method_dict[cmd_met]("{} {}".format(cls_nm, e_arg))
            else:
                if not cls_nm:
                    print("** class name missing **")
                    return
                try:
                    obj_id, arg_dict = split_curly_braces(e_arg)
                except Exception:
                    pass
                try:
                    call = method_dict[cmd_met]
                    return call("{} {} {}".format(cls_nm, obj_id, arg_dict))
                except Exception:
                    pass
        else:
            print("*** Unknown syntax: {}".format(arg))
            return False


if __name__ == '__main__':
    HBNBCommand().cmdloop()
=======
#!/usr/bin/python3
"""
This is the console base for the unit
"""
import cmd
from models.base_model import BaseModel
from models import storage
import json
import shlex
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class HBNBCommand(cmd.Cmd):
    """ Holberton command prompt to access models data """
    prompt = '(hbnb) '
    my_dict = {
        "BaseModel": BaseModel,
        "User": User,
        "State": State,
        "City": City,
        "Amenity": Amenity,
        "Place": Place,
        "Review": Review
            }

    def do_nothing(self, arg):
        """ Does nothing """
        pass

    def do_quit(self, arg):
        """ Close program and saves safely data """
        return True

    def do_EOF(self, arg):
        """ Close program and saves safely data, when
        user input is CTRL + D
        """
        print("")
        return True

    def emptyline(self):
        """ Overrides the empty line method """
        pass

    def do_create(self, arg):
        """ Creates a new instance of the basemodel class
        Structure: create [class name]
        """
        if not arg:
            print("** class name missing **")
            return
        my_data = shlex.split(arg)
        if my_data[0] not in HBNBCommand.my_dict.keys():
            print("** class doesn't exist **")
            return
        new_instance = HBNBCommand.my_dict[my_data[0]]()
        new_instance.save()
        print(new_instance.id)

    def do_show(self, arg):
        """
        Prints the string representation of an instance
        based on the class name and id
        Structure: show [class name] [id]
        """
        tokens = shlex.split(arg)
        if len(tokens) == 0:
            print("** class name missing **")
            return
        if tokens[0] not in HBNBCommand.my_dict.keys():
            print("** class doesn't exist **")
            return
        if len(tokens) <= 1:
            print("** instance id missing **")
            return
        storage.reload()
        objs_dict = storage.all()
        key = tokens[0] + "." + tokens[1]
        if key in objs_dict:
            obj_instance = str(objs_dict[key])
            print(obj_instance)
        else:
            print("** no instance found **")

    def do_destroy(self, arg):
        """
        Deletes an instance based on the class name and id
        (saves the changes into the JSON file)
        Structure: destroy [class name] [id]
        """
        tokens = shlex.split(arg)
        if len(tokens) == 0:
            print("** class name missing **")
            return
        if tokens[0] not in HBNBCommand.my_dict.keys():
            print("** class doesn't exist **")
            return
        if len(tokens) <= 1:
            print("** instance id missing **")
            return
        storage.reload()
        objs_dict = storage.all()
        key = tokens[0] + "." + tokens[1]
        if key in objs_dict:
            del objs_dict[key]
            storage.save()
        else:
            print("** no instance found **")

    def do_all(self, arg):
        """
        Prints all string representation of all instances
        based or not on the class name
        Structure: all [class name] or all
        """
        # prints the whole file
        storage.reload()
        my_json = []
        objects_dict = storage.all()
        if not arg:
            for key in objects_dict:
                my_json.append(str(objects_dict[key]))
            print(json.dumps(my_json))
            return
        token = shlex.split(arg)
        if token[0] in HBNBCommand.my_dict.keys():
            for key in objects_dict:
                if token[0] in key:
                    my_json.append(str(objects_dict[key]))
            print(json.dumps(my_json))
        else:
            print("** class doesn't exist **")

    def do_update(self, arg):
        """
        Updates an instance based on the class name and
        id by adding or updating attribute
        (save the change into the JSON file).
        Structure: update [class name] [id] [arg_name] [arg_value]
        """
        if not arg:
            print("** class name missing **")
            return
        my_data = shlex.split(arg)
        storage.reload()
        objs_dict = storage.all()
        if my_data[0] not in HBNBCommand.my_dict.keys():
            print("** class doesn't exist **")
            return
        if (len(my_data) == 1):
            print("** instance id missing **")
            return
        try:
            key = my_data[0] + "." + my_data[1]
            objs_dict[key]
        except KeyError:
            print("** no instance found **")
            return
        if (len(my_data) == 2):
            print("** attribute name missing **")
            return
        if (len(my_data) == 3):
            print("** value missing **")
            return
        my_instance = objs_dict[key]
        if hasattr(my_instance, my_data[2]):
            data_type = type(getattr(my_instance, my_data[2]))
            setattr(my_instance, my_data[2], data_type(my_data[3]))
        else:
            setattr(my_instance, my_data[2], my_data[3])
        storage.save()

    def do_update2(self, arg):
        """
        Updates an instance based on the class name and
        id by adding or updating attribute
        (save the change into the JSON file).
        Structure: update [class name] [id] [dictionary]
        """
        if not arg:
            print("** class name missing **")
            return
        my_dictionary = "{" + arg.split("{")[1]
        my_data = shlex.split(arg)
        storage.reload()
        objs_dict = storage.all()
        if my_data[0] not in HBNBCommand.my_dict.keys():
            print("** class doesn't exist **")
            return
        if (len(my_data) == 1):
            print("** instance id missing **")
            return
        try:
            key = my_data[0] + "." + my_data[1]
            objs_dict[key]
        except KeyError:
            print("** no instance found **")
            return
        if (my_dictionary == "{"):
            print("** attribute name missing **")
            return

        my_dictionary = my_dictionary.replace("\'", "\"")
        my_dictionary = json.loads(my_dictionary)
        my_instance = objs_dict[key]
        for my_key in my_dictionary:
            if hasattr(my_instance, my_key):
                data_type = type(getattr(my_instance, my_key))
                setattr(my_instance, my_key, my_dictionary[my_key])
            else:
                setattr(my_instance, my_key, my_dictionary[my_key])
        storage.save()

    def do_count(self, arg):
        """
        Counts number of instances of a class
        """
        counter = 0
        objects_dict = storage.all()
        for key in objects_dict:
            if (arg in key):
                counter += 1
        print(counter)

    def default(self, arg):
        """ handle new ways of inputing data """
        val_dict = {
            "all": self.do_all,
            "count": self.do_count,
            "show": self.do_show,
            "destroy": self.do_destroy,
            "update": self.do_update
        }
        arg = arg.strip()
        values = arg.split(".")
        if len(values) != 2:
            cmd.Cmd.default(self, arg)
            return
        class_name = values[0]
        command = values[1].split("(")[0]
        line = ""
        if (command == "update" and values[1].split("(")[1][-2] == "}"):
            inputs = values[1].split("(")[1].split(",", 1)
            inputs[0] = shlex.split(inputs[0])[0]
            line = "".join(inputs)[0:-1]
            line = class_name + " " + line
            self.do_update2(line.strip())
            return
        try:
            inputs = values[1].split("(")[1].split(",")
            for num in range(len(inputs)):
                if (num != len(inputs) - 1):
                    line = line + " " + shlex.split(inputs[num])[0]
                else:
                    line = line + " " + shlex.split(inputs[num][0:-1])[0]
        except IndexError:
            inputs = ""
            line = ""
        line = class_name + line
        if (command in val_dict.keys()):
            val_dict[command](line.strip())


if __name__ == '__main__':
    HBNBCommand().cmdloop()
>>>>>>> 26c1e316c2df54f9260000d24368be307ee57555
