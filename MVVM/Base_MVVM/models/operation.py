from dataclasses import dataclass

@dataclass
class Operation:
    a: float
    b: float

    def result(self):
        return self.a+self.b
    
    def format_result(self):
        return f"{self.a} + {self.b} = {self.result()}"
                    
    