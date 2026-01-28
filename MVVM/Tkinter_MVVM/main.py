import tkinter as tk

from viewmodels.calculator_vm import CalculatorViewModel
from views.main_view import MainView


def main() -> None:
    root = tk.Tk()

    vm = CalculatorViewModel(master=root)
    MainView(root, vm)

    root.mainloop()


if __name__ == "__main__":
    main()
