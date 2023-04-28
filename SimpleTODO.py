from dataclasses import dataclass
import datetime

@dataclass
class Todo:
    name_todo: str
    todo_wath: str
    start_date: datetime
    finish_date: datetime
    is_finished: bool = False


def main():
    print('hello world!')

if __name__ == '__main__':
    main()