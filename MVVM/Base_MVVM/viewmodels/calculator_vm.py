from typing import List

from models.operation import Operation
from viewmodels.observable import Observable


class CalculatorViewModel:
    def __init__(self):
        self.a_text = Observable[str]("")
        self.b_text = Observable[str]("")

        self.message = Observable[str]("")
        self.history = Observable[List[str]]([])


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
        
