import tkinter as tk

from viewmodels.calculator_vm import CalculatorViewModel


class MainView:
    def __init__(self, root: tk.Tk, vm: CalculatorViewModel):
        self.root = root
        self.vm = vm
        root.title("Tkinter-MVVM Calculator (+)")

        tk.Label(root, text="A:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        tk.Label(root, text="B:").grid(row=1, column=0, padx=5, pady=5, sticky="w")

        tk.Entry(root, width=20).grid(textvariable=self.vm.a_text,
            row=0, column=1, padx=5, pady=5, sticky="ew"
        )
        tk.Entry(root, width=20).grid(textvariable=self.vm.message,
            row=1, column=1, padx=5, pady=5, sticky="ew"
        )

        tk.Button(root, text="Сложить", command=self.vm.add).grid(
            row=2, column=0, columnspan=2, padx=5, pady=5, sticky="ew"
        )

        tk.Listbox(root, height=8, width=40).grid(listvariable=self.vm.history,
            row=3, column=0, columnspan=2, padx=5, pady=5, sticky="nsew"
        )

        tk.Label(root, fg="red").grid(
            row=4, column=0, columnspan=2, padx=5, pady=(0, 5), sticky="w"
        )
        
