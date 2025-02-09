from tabulate import tabulate
import pandas as pd
import json


class StepCoef:
    """
    Итерация в расширенном алгоритме Евклида
    """
    def __init__(self, prev_step: int = 0, q: int = 0, r: int = 0, x: int = 0, y: int = 0, a: int = 0, b: int = 0, x2: int = 1, x1: int = 0, y2: int = 0, y1: int = 1):
        self.step = prev_step + 1
        self.q = q
        self.r = r
        self.x = x
        self.y = y
        self.a = a
        self.b = b
        self.x2 = x2
        self.x1 = x1
        self.y2 = y2
        self.y1 = y1

    def __str__(self):
        return f"{self.step}. | {self.q} | {self.r} | {self.x} | {self.y} | {self.a} | {self.b} | {self.x2} | {self.x1} | {self.y2} | {self.y1} |"
    def __repr__(self):
        return f"{self.__class__.__name__}(q={self.q!r}, r={self.r!r}, x={self.x!r}, y={self.y!r}, a={self.a!r}, b={self.b!r}, x2={self.x2!r}, x1={self.x1!r}, y2={self.y2!r}, y1={self.y1!r})"

class ExtendedAlgo:
    """
    Расширенный алгоритм Евклида
    нахождение наибольшего общего делителя целых чисел и их коэффициентов
    """
    def __init__(self, a: int = 0, b: int = 0, output: str = ""):
        if a < 0 or b < 0:
            raise ValueError("Аргумены a и b должны быть больше 0!")
        self.a, self.b = (a, b) if a >= b else (b, a)  # целые числа a >= b > 0
        self.steps: [StepCoef] = []
        self.output = output.upper()

    def __str__(self):
        if self.steps:
            json_data = json.dumps([step.__dict__ for step in self.steps])
            df = pd.DataFrame(json.loads(json_data))
            df.sort_values("step", ascending=True, inplace=True)
            result = "Расширенный алгоритм Евклида (расчет целочисленной линейной комбинации ax + by = d)"
            if self.d:
                columns = ["","q","r","x","y","a","b","x2","x1","y2","y1"]
                drop_columns = []
                if self.output == "X":
                    drop_columns = ["y","y2","y1"]
                elif self.output == "Y":
                    drop_columns = ["x","x2","x1"]
                if drop_columns:
                    df = df.drop(columns=drop_columns)
                    for col in drop_columns:
                        columns.remove(col)
                result += f"\n{tabulate(df, headers=columns, tablefmt='rounded_grid', showindex=False)}"
                x, y, d = self.x, self.y, self.d
                result += f"\nРезультат расчета:   xa + yb = {x}·{self.a} {'+' if y > 0 else '-'} {y.__abs__()}·{self.b} = НОД({self.a},{self.b}) = {d}"
                result += f"\nИскомые значения:   x = {x}, y = {y}, d = {d}"
                if d == 1:
                    result += f"\nПроверяемые числа [a = {self.a}] и [b = {self.b}] ВЗАИМНО ПРОСТЫЕ!"
                    result += f"\nОбратный элемент по модулю:   {self.b}ˉ¹(mod {self.a}) = {y}" + (f" = {(self.a + y)}" if y < 0 else "")
            return result
        return ""
    def __repr__(self):
        return f"{self.__class__.__name__}(a={self.a!r}, b={self.b!r})"

    def __iter__(self):
        self.steps = []
        return self
    def __next__(self):
        current_step = self._last_step()
        if not current_step:
            current_step = StepCoef(a=self.a, b=self.b)
            self.steps.append(current_step)
            return current_step
        if current_step.b == 0:
            raise StopIteration
        q = current_step.a // current_step.b  # q = [a/b]
        r = current_step.a % current_step.b  # r = a mod b
        x = current_step.x2 - (q * current_step.x1)
        y = current_step.y2 - (q * current_step.y1)
        a = current_step.b
        b = r
        x2 = current_step.x1
        x1 = x
        y2 = current_step.y1
        y1 = y
        next_step = StepCoef(current_step.step, q, r, x, y, a, b, x2, x1, y2, y1)
        self.steps.append(next_step)
        return next_step

    @property
    def d(self) -> int | None:
        """
        Наибольший общий делитель a и b
        d = НОД(a,b)
        """
        last_step = self._last_step()
        if last_step and last_step.b == 0:
            return (self.a * last_step.x2) + (self.b * last_step.y2)
        return None

    @property
    def x(self) -> int | None:
        """
        Коэффициент при a
        (результат расчета X)
        """
        last_step = self._last_step()
        if last_step and last_step.b == 0:
            return last_step.x2
        return None

    @property
    def y(self) -> int | None:
        """
        Коэффициент при b
        (результат расчета Y)
        """
        last_step = self._last_step()
        if last_step and last_step.b == 0:
            return last_step.y2
        return None

    def _last_step(self) -> StepCoef | None:
        """
        Получить последний шаг итерации
        """
        return self.steps[-1] if self.steps else None

    def calc(self):
        """
        Расчитать коэффициенты и НОД
        """
        self.steps = []
        for _ in self:
            pass
        return self


def algo(a: int, b: int, output: str = ""):
    """
    Расчитать целочисленную линейную комбинацию расширенным алгоритмом Евклида
    """
    ext_algo = ExtendedAlgo(a, b, output).calc()
    print(ext_algo)


if __name__ == "__main__":
    algo(2577, 1137, "Y")
    #print(ExtendedAlgo(176, 13).calc())