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
    dead_line: datetime
    is_finished: bool = False
    finish_date: datetime = None

    def __repr__(self) -> str:
        todo_str: str = ""
        todo_str += f'{self.name_todo} -'
        todo_str += f' S: {self.start_date.strftime(DATE_FORMAT)}'
        todo_str += f' F: {self.finish_date.strftime(DATE_FORMAT) if self.finish_date else "~".center(10)}'
        todo_str += f' DL: {self.dead_line.strftime(DATE_FORMAT)}'
        return todo_str
    
def main():
    todo_list: list[Todo]
    try:
        todo_list = read_todos()
    except (EOFError, FileNotFoundError):
        todo_list = []

    args = sys.argv
    if len(args) > 1:
        command = args[1]
        match command:
            case 'new':
                todo = Todo(args[2], datetime.strptime(args[3], DATE_FORMAT), datetime.strptime(args[4], DATE_FORMAT))   
                todo_list.append(todo)
                write_todo(todo_list)
                print("TODO criado!")
          
            case 'list':
                for i, todo in enumerate(todo_list):
                    if len(args) < 3:
                        print_unfinished(todo, i)
                    
                    elif args[2] == 'all':
                        print_all(todo, i)

                    elif args[2] == 'finished':
                        print_finished(todo, i)

            case 'done':
                todo_list[int(args[2])-1].is_finished = True
                write_todo(todo_list)

            case 'clear':
                if args[2] == 'all':
                    todo_list = []

                else:
                    for todo in todo_list:
                        if todo.is_finished:
                            todo_list.remove(todo)
                
                write_todo(todo_list)

            case other:
                print('Invalid TODO command =>', command)

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
    
            
if __name__ == '__main__':
    main()