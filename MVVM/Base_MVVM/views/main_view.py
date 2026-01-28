import tkinter as tk
from typing import Callable

from viewmodels.calculator_vm import CalculatorViewModel
from viewmodels.observable import Observable


def bind_two_way_string(var: tk.StringVar, obs: Observable[str]) -> Callable[[], None]:
    lock = False
    
    def on_var_changed(*args) -> None:
        if lock:
            return
        obs.set(var.get())
    trace_id = var.trace_add("write", on_var_changed)

    def on_obs_changed(value) -> None:
        nonlocal lock
        if var.get() == value:
            return
        lock = True
        var.set(value)
        lock = False

    unsub = obs.subscribe(on_obs_changed)

    def unbind():
        var.trace_remove("write",trace_id)
        unsub()

    return unbind




class MainView:
    def __init__(self, root: tk.Tk, vm: CalculatorViewModel):
        self.root = root
        self.vm = vm
        root.title("Clean MVVM Calculator (+)")

        tk.Label(root, text="A:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        tk.Label(root, text="B:").grid(row=1, column=0, padx=5, pady=5, sticky="w")

        self.var_a = tk.StringVar()
        self.var_b = tk.StringVar()

        self.entry_a = tk.Entry(root, textvariable=self.var_a, width=20)
        self.entry_b = tk.Entry(root, textvariable=self.var_b, width=20)
        self.entry_a.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        self.entry_b.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        self.btn_add = tk.Button(root, text="Сложить", command=self.vm.add)
        self.btn_add.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

        self.listbox = tk.Listbox(root, height=8, width=40)
        self.listbox.grid(row=3, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")

        self.var_msg = tk.StringVar(value="")
        tk.Label(root, textvariable=self.var_msg, fg="red").grid(
            row=4, column=0, columnspan=2, padx=5, pady=(0, 5), sticky="w"
        )

        root.columnconfigure(1, weight=1)
        root.rowconfigure(3, weight=1)

        # --- binding: поля ввода (two-way) ---
        self._unbind_a = bind_two_way_string(self.var_a, self.vm.a_text)
        self._unbind_b = bind_two_way_string(self.var_b, self.vm.b_text)

        # --- binding: сообщение (one-way) ---
        self._unsub_msg = self.vm.message.subscribe(lambda txt: self.var_msg.set(txt))
        self.var_msg.set(self.vm.message.get())

        # --- binding: история (one-way) ---
        self._unsub_hist = self.vm.history.subscribe(self._render_history)
        self._render_history(self.vm.history.get())

        root.protocol("WM_DELETE_WINDOW", self.on_close)

    def _render_history(self, lines: list[str]) -> None:
        self.listbox.delete(0, tk.END)
        for line in lines:
            self.listbox.insert(tk.END, line)

    def on_close(self) -> None:
        # аккуратно убираем подписки
        self._unbind_a()
        self._unbind_b()
        self._unsub_msg()
        self._unsub_hist()
        self.root.destroy()

