#  Copyright (c) ChernV (@otter18), 2022.
import enum
from random import randint, choice

from fpdf import FPDF

# A4 page format
WIGHT = 210
HEIGHT = 297
MARGIN = 15


class TaskType(enum.Enum):
    SUM_AND_SPACE = 0
    PLUS_AND_MINUS = 1
    PLUS_MINUS_MULT = 2


def generate_task(n: int, t: TaskType):
    used = set()
    res = []
    while len(res) < n:
        if t == TaskType.SUM_AND_SPACE:
            b = randint(5, 20)
            a = randint(5, max(5, b - 5))

            if (a, b) in used:
                continue
            used.add((a, b))

            q = randint(0, 1)
            if q == 0:
                res.append(f'____ + {a} = {b}')
            elif q == 1:
                res.append(f'{a} + ____ = {b}')
        elif t == TaskType.PLUS_AND_MINUS:
            q = randint(0, 1)
            if q == 0:
                a = randint(1, 30)
                b = randint(1, max(1, 30 - a))

                while (a, '+', b) in used:
                    a = randint(1, 30)
                    b = randint(1, max(1, 30 - a))

                used.add((a, '+', b))
                used.add((b, '+', a))

                res.append(f'{a} + {b} = ____')
            elif q == 1:
                a = randint(2, 30)
                b = randint(1, max(1, a - 1))

                while (a, '-', b) in used:
                    a = randint(2, 50)
                    b = randint(1, max(1, a - 1))

                used.add((a, '-', b))
                res.append(f'{a} - {b} = ____')
        elif t == TaskType.PLUS_MINUS_MULT:
            q = randint(0, 2)
            if q == 0:
                a = randint(1, 30)
                b = randint(1, max(1, 30 - a))

                while (a, '+', b) in used:
                    a = randint(1, 30)
                    b = randint(1, max(1, 30 - a))

                used.add((a, '+', b))
                used.add((b, '+', a))

                res.append(f'{a} + {b} = ____')
            elif q == 1:
                a = randint(2, 30)
                b = randint(1, max(1, a - 1))

                while (a, '-', b) in used:
                    a = randint(2, 50)
                    b = randint(1, max(1, a - 1))

                used.add((a, '-', b))
                res.append(f'{a} - {b} = ____')
            elif q == 2:
                a = randint(1, 5)
                b = choice([2, 10])

                if randint(0, 1):
                    res.append(f'{a} * {b} = ____')
                else:
                    res.append(f'{b} * {a} = ____')

    return res


def split2cols(tasks, n):
    a = (len(tasks) + n - 1) // n
    res = []
    for i in range(n):
        res.append(tasks[i * a: (i + 1) * a])

    return res


def gen_pdf(name, tasks, col_cnt=2):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=15)

    tasks = split2cols(tasks, col_cnt)

    delta_x = (WIGHT - 2 * MARGIN) // col_cnt
    delta_y = (HEIGHT - 2 * MARGIN) // len(tasks[0])
    for i in range(len(tasks)):
        for j in range(len(tasks[i])):
            pdf.text(MARGIN + i * delta_x, MARGIN + j * delta_y, tasks[i][j])

    pdf.output(name)


if __name__ == '__main__':
    gen_pdf(name='src/task.pdf', tasks=generate_task(50, TaskType.PLUS_MINUS_MULT), col_cnt=4)
