from prettytable import PrettyTable
import keyboard
import os

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class Controller():
    def __init__(self):
        self.x = 0
        root = 'D:\Work'
        self.items = os.listdir(root)
        self.active_items = []
        self.size = 0
        self.table = PrettyTable()

    def hook_controls(self):
        keyboard.add_hotkey('up', self.go_up)
        keyboard.add_hotkey('down', self.go_down)

        keyboard.wait('esc')

    def go_up(self):
        self.x -= 1
        if self.x < 0:
            self.x = len(self.items) - 1
            # self.x = 0
            # return
        self.print_table()

    def go_down(self):
        self.x += 1
        if self.x > len(self.items) - 1:
            self.x = 0
        self.print_table()

    def print_table(self):
        self.active_items = self.items[self.x : self.x + os.get_terminal_size().lines - 1]
        self.size = len(self.active_items)
        self.cls()
        for i in range(0, self.x + self.size):
            line = bcolors.WARNING + self.items[i] + bcolors.ENDC if i == self.x else self.items[i]
            self.table.add_row([i, line])
        print(self.table)
        print('\033[?25l', end='')

    def cls(self):
        self.table = PrettyTable()
        self.table.align = 'l'
        self.table.field_names = ['Index', 'Name']
        os.system('cls' if os.name=='nt' else 'clear')

if __name__ == '__main__':    
    controller = Controller()
    controller.hook_controls()