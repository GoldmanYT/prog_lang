from tkinter import *
from tkinter.scrolledtext import ScrolledText
from tkinter.ttk import *
from cpp_functions import *


class UiLayoutConstructor:
    def __init__(self, ratios, orientation='v', padding=0.01):
        if orientation not in ('v', 'h'):
            raise ValueError(f'Incorrect value of parameter `type`: {orientation}. Supports only "v" and "h"')

        if isinstance(ratios, int):
            ratios = [1] * ratios

        # Normalize the ratios
        ratios = [ratio / sum(ratios) for ratio in ratios]

        self.layouts = [dict() for _ in range(len(ratios))]

        padding_count_x = len(ratios) + 1 if orientation == 'h' else 2
        padding_count_y = len(ratios) + 1 if orientation == 'w' else 2
        sum_padding_x = padding
        sum_padding_y = padding
        for index, ratio in enumerate(ratios):
            ratio_x = ratio if orientation == 'h' else 1.0
            ratio_y = ratio if orientation == 'v' else 1.0
            relwidth = self.layouts[index]['relwidth'] = (1.0 - padding * padding_count_x) * ratio_x
            self.layouts[index]['relx'] = sum_padding_x
            relheight = self.layouts[index]['relheight'] = (1.0 - padding * padding_count_y) * ratio_y
            self.layouts[index]['rely'] = sum_padding_y
            if orientation == 'h':
                sum_padding_x += relwidth + padding
            elif orientation == 'v':
                sum_padding_y += relheight + padding

    def __getitem__(self, index) -> dict:
        return self.layouts[index]


class Window:
    def __init__(self):
        rel_elem_full = UiLayoutConstructor(1)[0]
        rel_elem_half_left = UiLayoutConstructor(2, 'h')[0]
        rel_elem_half_right = UiLayoutConstructor(2, 'h')[1]
        rel_elem_95_5_v = UiLayoutConstructor((95, 5), 'v')
        rel_elem_80_20_v = UiLayoutConstructor((80, 20), 'v')
        # rel_elem_10_90_v = UiLayoutConstructor((10, 90), 'v')

        self.root = Tk()
        self.root.geometry('1200x800')

        left_frame = Frame(self.root)

        top_left_frame = Labelframe(left_frame, text='Исходный код программы')
        # save_load_button_frame = Frame(top_left_frame)
        # load_button = Button(save_load_button_frame, text='Загрузить', command=self.load_button_action)
        # save_button = Button(save_load_button_frame, text='Сохранить', command=self.save_button_action)
        self.program_code_text = Text(top_left_frame, font=('Consolas', 14))

        bottom_left_frame = Labelframe(left_frame, text='Список найденных ошибок')
        self.errors_text = ScrolledText(bottom_left_frame, font=('Cascadia Mono', 14), foreground='#dd0000')

        right_tab_widget = Notebook(self.root)

        scaner_frame = Labelframe(right_tab_widget, text='Сформированные токены')
        self.scanner_output_text = ScrolledText(scaner_frame, font=('Consolas', 14))
        start_scanner_button = Button(scaner_frame, text='Запуск', command=self.start_scanner_button_action)

        sgt_frame = Frame(right_tab_widget)  # СУТ
        sgt_top_frame = Frame(sgt_frame)

        three_address_commands_frame = Labelframe(sgt_top_frame, text='Трёхадресные команды')
        memory_allocation_frame = Labelframe(sgt_top_frame, text='Распределение памяти')

        three_address_commands_text = ScrolledText(three_address_commands_frame)
        memory_allocation_text = ScrolledText(memory_allocation_frame)
        start_sgt_button = Button(sgt_frame, text='Запуск', command=self.start_sgt_button_action)

        scaner_frame.place(**rel_elem_full)
        self.scanner_output_text.place(**rel_elem_95_5_v[0])
        start_scanner_button.place(**rel_elem_95_5_v[1])

        sgt_frame.place(**rel_elem_full)
        sgt_top_frame.place(**rel_elem_95_5_v[0])

        three_address_commands_frame.place(**rel_elem_half_left)
        three_address_commands_text.place(**rel_elem_full)

        memory_allocation_frame.place(**rel_elem_half_right)
        memory_allocation_text.place(**rel_elem_full)

        start_sgt_button.place(**rel_elem_95_5_v[1])

        right_tab_widget.add(scaner_frame, text='Сканер')
        right_tab_widget.add(sgt_frame, text='СУТ')

        left_frame.place(**rel_elem_half_left)
        top_left_frame.place(**rel_elem_80_20_v[0])
        # save_load_button_frame.place(**rel_elem_10_90_v[0])
        # load_button.place(**rel_elem_half_left)
        # save_button.place(**rel_elem_half_right)
        self.program_code_text.place(**rel_elem_full)

        bottom_left_frame.place(**rel_elem_80_20_v[1])
        self.errors_text.place(**rel_elem_full)

        right_tab_widget.place(**rel_elem_half_right)

        self.load_program_code()
        self.update_syntax_highlight()

        self.indexes = []

        self.root.mainloop()

    def get_tk_index(self, index):
        l = 0
        r = len(self.indexes)
        while r - l > 1:
            m = (r + l) // 2
            if self.indexes[m] >= index:
                r = m
            else:
                l = m
        return f'{l + 1}.{index - self.indexes[l] - 1}'

    def load_program_code(self):
        self.program_code_text.delete('1.0', END)
        try:
            with open('program_code.txt', 'r', encoding='utf-8') as file:
                code = file.read()
        except FileNotFoundError:
            code = ''
        self.program_code_text.insert(END, code)

        self.program_code_text.tag_configure('keyword', foreground='#ff7700')
        self.program_code_text.tag_configure('comment', foreground='#dd0000')
        self.program_code_text.tag_configure('const', foreground='#0000ff')
        self.program_code_text.tag_configure('error', background='#ff7777')

        self.program_code_text.bind("<KeyRelease>", self.update_syntax_highlight)

    def update_syntax_highlight(self, *_):
        code_to_tag = {
            Token.lcProg: 'keyword',
            Token.lcUsing: 'keyword',
            Token.lcClass: 'keyword',
            Token.lcStart: 'keyword',
            Token.lcStop: 'keyword',
            Token.lcVar: 'keyword',
            Token.lcWhile: 'keyword',
            Token.lcNum: 'const',
            Token.lcCom: 'comment',
            Token.lcErr: 'error',
        }
        for tag in code_to_tag.values():
            self.program_code_text.tag_delete(tag)

        self.program_code_text.tag_configure('keyword', foreground='#ff7700')
        self.program_code_text.tag_configure('comment', foreground='#dd0000')
        self.program_code_text.tag_configure('const', foreground='#0000ff')
        self.program_code_text.tag_configure('error', background='#ff7777')

        code = self.program_code_text.get('1.0', END)
        tokens = scanner.get_tokens(code)
        self.indexes = [-1] + [i for i in range(len(code)) if code[i] == '\n']
        for token in tokens:
            tag = code_to_tag.get(token.code)
            if tag is not None:
                index1 = self.get_tk_index(token.start)
                index2 = self.get_tk_index(token.end)
                self.program_code_text.tag_add(tag, index1, index2)

    def start_scanner_button_action(self):
        program_code = self.program_code_text.get('1.0', END)
        tokens = scanner.get_tokens(program_code)

        self.scanner_output_text.delete('1.0', END)
        self.scanner_output_text.insert(END, '\n'.join(str(token) for token in tokens))

        has_errors = False
        self.errors_text.delete('1.0', END)
        for token in tokens:
            if token.code == token.lcErr:
                index = self.get_tk_index(token.start)
                self.errors_text.insert(END, f'{index}: {token.get_attr()}\n')
                has_errors = True
        if not has_errors:
            self.errors_text.insert(END, 'Лексический анализ успешно завершен')

    def start_sgt_button_action(self):
        print('Запуск СУТ')


if __name__ == '__main__':
    Window()
