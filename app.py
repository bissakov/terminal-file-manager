from prettytable import PrettyTable
import os
import curses
from curses import wrapper


class Table:
    def __init__(self, title, rows) -> None:
        table = PrettyTable()
        table.title = title
        table.field_names = ['#', 'Name', 'Extension', 'Type', 'Date created', 'Date modified', 'Size']
        table.align['#'] = 'r'
        table.add_rows([self.__get_row(i, item) for i, item in enumerate(rows)])
        self.table = table
        self.all_lines = str(table).split('\n')

    def __get_row(self, i: int, item: str) -> list:
        return [i + 1, item, '', 'Folder', '28.09.2022 21:40:30', '29.09.2022 11:05:16', '1.25Gb']

    def align(self) -> None:
        self.table.align['Name'] = 'l'
        self.all_lines = str(self.table).split('\n')

    def get_header(self) -> list:
        return self.all_lines[0:5]

    def get_footer(self) -> list:
        return self.all_lines[-1:]

    def get_lines(self) -> list:
        return self.all_lines[5::][:-1]


class App:
    def __init__(self, root) -> None:
        self.items = os.listdir(root)
        self.terminal_height: int = os.get_terminal_size().lines
        self.terminal_width: int = os.get_terminal_size().columns
        self.visible_items = self.items[0:0+self.terminal_height - 4]

        table_obj = Table(root, self.items)
        self.header = table_obj.get_header()
        self.header_size = len(self.header)
        self.footer = table_obj.get_footer()
        table_obj.align()
        self.lines = table_obj.get_lines()
        self.work_height = self.terminal_height - self.header_size - 1
        self.table_width = len(self.lines[0])
        self.table_start = (self.terminal_width - self.table_width) // 2

        self.escape_chars = [27, 113, 1081]

        self.x = self.header_size

    def __init_print(self, stdscr) -> None:
        for i, line in enumerate(self.header):
            stdscr.addstr(i, self.table_start, line)
        rows = self.lines[self.x - self.header_size:self.x + self.work_height - self.header_size]
        for i, line in enumerate(rows, start=self.header_size):
            if i == self.header_size:
                stdscr.addstr(i, self.table_start, line, curses.A_STANDOUT)
                continue
            stdscr.addstr(i, self.table_start, line)
        st = self.header_size + (len(self.visible_items) if len(self.items) < self.terminal_height else self.work_height)
        for i, line in enumerate(self.footer, start=st):
            stdscr.addstr(i, self.table_start, line)

        stdscr.refresh()

    def __print_line(self, stdscr, pos_y, line, color=curses.A_NORMAL) -> None:
        stdscr.addstr(pos_y, self.table_start, line, color)

    def __main(self, stdscr) -> None:
        curses.curs_set(0)

        self.__init_print(stdscr)

        while True:
            key = stdscr.getch()
            if key in self.escape_chars:
                break

            if key == curses.KEY_DOWN:
                if self.x < self.terminal_height - 2:
                    self.x += 1
                    x = self.x - self.header_size
                    self.__print_line(stdscr, self.x - 1, self.lines[x - 1])
                    self.__print_line(stdscr, self.x, self.lines[x], curses.A_STANDOUT)
                else:
                    x = self.x - self.header_size
                    self.__print_line(stdscr, self.x, self.lines[x])
                    self.x = self.header_size
                    x = self.x - self.header_size
                    self.__print_line(stdscr, self.x, self.lines[x], curses.A_STANDOUT)
            elif key == curses.KEY_UP:
                if self.x <= self.header_size:
                    x = self.x - self.header_size
                    self.__print_line(stdscr, self.x, self.lines[x])
                    self.x = self.terminal_height - 2 if len(self.items) >= self.terminal_height else len(self.items) + 4
                    x = self.x - self.header_size
                    self.__print_line(stdscr, self.x, self.lines[x], curses.A_STANDOUT)
                else:
                    self.x -= 1
                    x = self.x - self.header_size
                    self.__print_line(stdscr, self.x, self.lines[x], curses.A_STANDOUT)
                    self.__print_line(stdscr, self.x + 1, self.lines[x + 1], curses.A_NORMAL)
            stdscr.addstr(1, 5, f'{self.x-4:02}', curses.A_BOLD)

    def run(self) -> None:
        wrapper(self.__main)


if __name__ == '__main__':
    root = 'D:\\Work'
    app = App(root=root)
    app.run()
