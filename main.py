#  Copyright (c) ChernV (@otter18), 2022.

from random import randint, choice

from fpdf import FPDF

# A4 page format
WIGHT = 210
HEIGHT = 297
MARGIN = 15


def generate_task(n):
    gen = set()
    while len(gen) < n:
        q = randint(0, 2)
        if q == 0:
            a = randint(1, 29)
            b = randint(1, 30 - a)
            gen.add(f'{a} + {b} = ____')
        elif q == 1:
            a = randint(2, 20)
            b = randint(1, max(1, a - 1))
            gen.add(f'{a} - {b} = ____')
        elif q == 2:
            a = randint(1, 10)
            b = choice([2, 5, 10])
            if randint(0, 1):
                gen.add(f'{a} * {b} = ____')
            else:
                gen.add(f'{b} * {a} = ____')

    return list(gen)


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
    gen_pdf('task.pdf', generate_task(50), 4)
