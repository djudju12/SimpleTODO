from dataclasses import dataclass
from datetime import datetime, timedelta
import pickle
import sys

PATH = 'todos.pkl'
VALID_ARGS = ['new', 'list', 'list all', 'list finished', 'done']
DATE_FORMAT = '%d/%m/%Y'
@dataclass
class Todo:
    name_todo: str
    start_date: datetime 
    dead_line: datetime = None
    is_finished: bool = False
    finish_date: datetime = None

    def __repr__(self) -> str:
        todo_str: str = ""
        todo_str += f'{self.name_todo} -'
        todo_str += f' S: {format_date(self.start_date)}'
        todo_str += f' F: {format_date(self.finish_date)}'
        todo_str += f' DL: {format_date(self.dead_line)}'
        return todo_str


def main():
    todo_list: list[Todo]
    try:
        todo_list = read_todos()
    except (EOFError, FileNotFoundError):
        todo_list = []

    args = sys.argv
    clear_args(args)

    len_args = len(args)
    if len_args > 1:
        command = args[1]
        match command:
            case 'new':
                if len_args == 3:
                     todo = Todo(args[2], # name
                                datetime.now()) # start date
                else:                
                    try:
                        todo = Todo(args[2], # name
                                    datetime.strptime(args[3], DATE_FORMAT), # start date
                                    datetime.strptime(args[4], DATE_FORMAT)) # dead line 
                    except ValueError:
                        print("Formato => todo new 'nome do todo' 'DD/MM/YYYY' 'DD/MM/YYYY' ")
                        return 
                        
                todo_list.append(todo)
                write_todo(todo_list)
                print("TODO criado!")

            case 'list':
                for i, todo in enumerate(todo_list):
                    if len_args < 3:
                        print_unfinished(todo, i)
                    
                    elif args[2] == 'all':
                        print_all(todo, i)

                    elif args[2] == 'finished':
                        print_finished(todo, i)

            case 'done':
                done_todo = todo_list[int(args[2])-1]
                done_todo.is_finished = not done_todo.is_finished
                                
                if done_todo.is_finished:
                    if len_args > 3:
                        done_todo.finish_date = datetime.strptime(args[3], DATE_FORMAT)
                    else:
                        done_todo.finish_date = datetime.now()
                    
                    print_finished(done_todo, int(args[2])-1)
                else:
                    done_todo.finish_date = None
                    print_unfinished(done_todo, int(args[2])-1)
                
                write_todo(todo_list)

            case 'clear':
                if len_args > 2:
                    if args[2] == 'all':
                        todo_list = []
                    else:
                        print("Invalid clear command =>", args[2])

                else:
                    for todo in todo_list:
                        if todo.is_finished:
                            todo_list.remove(todo)
                
                write_todo(todo_list)

            case other:
                print('Invalid TODO command =>', command)

def clear_args(args):
    if args[2] == '':
        args.pop(2)

def print_finished(todo, i):
    if todo.is_finished:
        print(f'[X] {i+1} => {todo}')

def print_all(todo, i):
    if todo.is_finished:
        print(f'[X] {i+1} => {todo}')
    else:
        print(f'[ ] {i+1} => {todo}')

def print_unfinished(todo, i):
    if not todo.is_finished:
        print(f'[ ] {i+1} => {todo}')

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