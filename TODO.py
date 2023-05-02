from dataclasses import dataclass
from datetime import datetime
import pickle
import sys

PATH = r'C:\USERS\jonathan.santos\Desktop\unisc\SimpleTODO\todos.pkl'
VALID_ARGS = ['new', 'list', 'list all', 'list finished', 'done']
DATE_FORMAT = '%d/%m/%Y'
MEDIA, ALTA ='\033[33m', '\033[31m'
DIAS_PARA_AVERMELHAR = 5
RESET = '\033[0m'

@dataclass
class Todo:
    name_todo: str
    start_date: datetime 
    dead_line: datetime = None
    is_finished: bool = False
    finish_date: datetime = None
    index_of_todo: int = 0

    def __repr__(self) -> str:
        todo_str: str = ""

        if self.dead_line and datetime.now() > self.dead_line:
            day_passed = (datetime.now() - self.dead_line).days
            todo_str += MEDIA if day_passed < DIAS_PARA_AVERMELHAR else ALTA

        todo_str += f'[{"X" if self.is_finished else " "}] ' # [ ]
        todo_str += f'{self.index_of_todo} => '              # 1 => 
        todo_str += f'{self.name_todo} -'                    # name - 
        todo_str += f' S: {format_date(self.start_date)}'    # S: 
        todo_str += f' F: {format_date(self.finish_date)}'   # F:
        todo_str += f' DL: {format_date(self.dead_line)}'    # DL:
        todo_str += RESET
        return todo_str


def main():
    todo_list: list[Todo]
    try:
        todo_list = read_todos()
    except (EOFError, FileNotFoundError):
        todo_list = []

    clear_args(sys.argv)
    args = sys.argv
    len_args = len(args)

    if len_args == 1:
        print('commandos =>', VALID_ARGS)
        return 

    command = args[1]
    match command:
        case 'new':
            try:

                if len_args == 3:
                    todo = Todo(args[2], # name
                                datetime.now(),
                                index_of_todo=len(todo_list)) # start date
                
                elif len_args == 4:
                    todo = Todo(args[2], # name
                                datetime.strptime(args[3], DATE_FORMAT),
                                index_of_todo=len(todo_list)) # start date

                else:                
                        todo = Todo(args[2], # name
                                    datetime.strptime(args[3], DATE_FORMAT), # start date
                                    datetime.strptime(args[4], DATE_FORMAT),
                                    index_of_todo=len(todo_list)) # dead line 

            except ValueError:
                print("Formato => todo new 'nome do todo' 'DD/MM/YYYY' 'DD/MM/YYYY'")
                return 
                    
            todo_list.append(todo)
            write_todo(todo_list)
            print("TODO criado!")

        case 'list':
            if len_args < 3:
                print_todos(todo_list, 'unfinished')

            else:
                print_todos(todo_list, args[2])

        case 'done':
            try:
                done_todo = todo_list[int(args[2])]
                done_todo.is_finished = not done_todo.is_finished
                                
                if done_todo.is_finished:
                    if len_args > 3:
                        done_todo.finish_date = datetime.strptime(args[3], DATE_FORMAT)

                    else:
                        done_todo.finish_date = datetime.now()

                    print(done_todo)
                else:
                    done_todo.finish_date = None
                    print(done_todo)
                
                write_todo(todo_list)
            except IndexError:
                print('Not a valid todo index =>', args[2])
            except ValueError:
                print('Invalid todo index =>', args[2])
                print('Check "todo list all" to get the index', args[2])

        case 'clear':
            if len_args > 2:
                if args[2] == 'all':
                    todo_list = []
                else:
                    print("Invalid clear command =>", args[2])

            else:
                clear_todos(todo_list)
            
            write_todo(todo_list)

        case 'help':
            print('check => https://github.com/djudju12/SimpleTODO')

        case other:
            print('Invalid TODO command =>', command)

def clear_todos(todo_list: list[Todo]):
    contador = 0
    for todo in todo_list.copy():
        if todo.is_finished:
            todo_list.remove(todo)
        else:
            todo.index_of_todo = contador   
            contador +=1

def print_todos(todo_list, m):
    for todo in todo_list:
        match m:
            case 'finished':
                if todo.is_finished:
                    print(todo)

            case 'all':
                print(todo)

            case 'unfinished':
                if not todo.is_finished:
                    print(todo)

            case other:
                print('invalid argument PRINT_TODOS =>', m)

def clear_args(args):
    if '' in args:
        args.remove('')

def read_todos() -> list[str]:
    with open(PATH, 'rb') as f:
        return pickle.load(f)
    
def write_todo(o: list[Todo]) -> list[str]:
    with open(PATH, 'wb') as f:
        pickle.dump(o, f)    

def format_date(date: datetime):
    if date:
        return date.strftime(DATE_FORMAT)
    return "~~/~~/~~~~"

if __name__ == '__main__':
    main()