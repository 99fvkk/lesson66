import tkinter as tk

from models.operation import Operation


class CalculatorViewModel:
    def __init__(self, master: tk.Misc):
        self.a_text = tk.StringVar(master=master,value="")
        self.b_text = tk.StringVar(master=master,value="")

        self.message = tk.StringVar(master=master,value="")
        self.history = tk.StringVar(master=master,value=[])

    
    def add(self) -> None:
        a_str = self.a_text.get().strip().replace(",",".")
        b_str = self.a_text.get().strip().replace(",",".")

        try:
            a = float(a_str)
            b = float(b_str)
        except ValueError:
            self.message.set("Error")
            return
        
        op = Operation(a, b)
        lines = self.history.get()
        lines.append(op.format_result())
        self.history.set(lines)

        self.message.set("")
        self.a_text.set("")
        self.b_text.set("")
        