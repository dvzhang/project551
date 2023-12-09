import cmd
import os
from queryparse import parse_query

current_file_path = os.path.abspath(__file__)
current_dir = os.path.dirname(current_file_path)

class CLI(cmd.Cmd):
    intro = """\nWelcome to Frank Data Base (FRDB) \n"""
    prompt = 'FRDB > '
    
    def __init__(self, current_db=None):
        super(CLI, self).__init__()
        self.current_db = current_db

    def onecmd(self, line):
            cmd, arg, line = self.parseline(line)
            if not line:
                return self.emptyline()
            if cmd is None:
                return self.default(line)
            self.lastcmd = line
            if line == 'EOF' :
                self.lastcmd = ''
            if cmd == '':
                return self.default(line)
            else:
                try:
                    func = getattr(self, 'do_' + cmd)
                except AttributeError:
                    try:
                        func = getattr(self, 'do_' + cmd.lower())
                    except AttributeError:
                        return self.default(line)
                return func(arg)

    def do_makedb(self, user_input_query):
        user_input_query = user_input_query.strip().split(" ")
        if self.current_db is not None:
            os.chdir(current_dir)
        if os.path.exists(user_input_query[0]):
            print("DB name already exists! Please use the existing DB or make a DB with a different name.")
        else:
            os.mkdir("./" + user_input_query[0])
            print("Created DB ", user_input_query[0])
        
    def do_usedb(self, user_input_query):
        user_input_query = user_input_query.strip().split(" ")
        if self.current_db is not None:
            os.chdir(current_dir)
            if not os.path.exists(user_input_query[0]):
                print("DB does not exist!")
            else:
                os.chdir(current_dir + "/" + user_input_query[0])
                
        else:
            # os.chdir("./" + user_input_query[0])
            os.chdir(current_dir + "/" + user_input_query[0])
            
        self.current_db = user_input_query[0]
        print("Using DB " + user_input_query[0])

    def do_dropdb(self, user_input_query):
        user_input_query = user_input_query.strip().split(" ")

        if self.current_db is not None:
            os.chdir(current_dir)
        
        if user_input_query[0] not in os.listdir('.'):
            print("DB does not exist!")
            return
        else:
            os.rmdir("./" + user_input_query[0])
            print("Dropped DB", user_input_query[0])

    def do_showdb(self, user_input_query):
        for filename in os.listdir(current_dir):
            if os.path.isdir(current_dir +"/" + filename) and not filename.startswith("_") and not filename.startswith("."):
                print(filename)

    def do_make(self, user_input_query):
        user_input_query = "MAKE " + user_input_query
        return parse_query(user_input_query, self.current_db)
        
    def do_edit(self, user_input_query):
        user_input_query = "EDIT " + user_input_query
        return parse_query(user_input_query, self.current_db)
        
    
    def do_from(self, user_input_query): 
        user_input_query = "FROM " + user_input_query
        return parse_query(user_input_query, self.current_db)
        
    def do_drop(self, user_input_query): 
        user_input_query = "DROP " + user_input_query
        return parse_query(user_input_query, self.current_db)
    
    def do_show(self, user_input_query):
        for filename in os.listdir("./table"):
            print("       ", filename[:-4])

    def do_exit(self, *args):
        print("\nSee you ~\n")
        return True

if __name__ == "__main__": 
    CLI().cmdloop()