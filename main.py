from tkinter import *
from tkinter.ttk import *


def main():
    padding = 0.01
    start = 0.0
    end = 1.0
    center = 0.5

    root = Tk()
    root.geometry('1280x720')

    top_left_frame = Labelframe(root, text='Исходный код программы')
    load_button = Button(top_left_frame, text='Загрузить')
    save_button = Button(top_left_frame, text='Сохранить')
    program_code_text = Text(top_left_frame)

    bottom_left_frame = Labelframe(root, text='Список найденных ошибок')
    errors_text = Text(bottom_left_frame)

    right_tab_widget = Notebook(root)

    scaner_frame = Labelframe(right_tab_widget, text='Сформированные токены')
    scanner_output_text = Text(scaner_frame)
    start_scanner_button = Button(scaner_frame, text='Запуск')

    sgt_frame = Frame(right_tab_widget)  # СУТ

    scaner_frame.place(
        relx=start + padding,
        rely=start + padding,
        relwidth=1.0 - padding * 2,
        relheight=1.0 - padding * 2,
    )
    scanner_output_text.place(
        relx=start + padding,
        rely=start + padding * 0.5,
        relwidth=1.0 - padding * 2,
        relheight=0.95 - padding * 1.5,
    )
    start_scanner_button.place(
        relx=start + padding,
        rely=start + 0.95 + padding,
        relwidth=1.0 - padding * 2,
        relheight=0.05 - padding * 1.5,
    )

    sgt_frame.place(
        relx=start + padding,
        rely=start + padding,
        relwidth=1.0 - padding * 2,
        relheight=1.0 - padding * 2,
    )

    right_tab_widget.add(scaner_frame, text='Сканер')
    right_tab_widget.add(sgt_frame, text='СУТ')

    top_left_frame.place(
        relx=start + padding,
        rely=start + padding,
        relwidth=0.5 - padding * 1.5,
        relheight=0.8 - padding * 1.5,
    )
    load_button.place(
        relx=start + padding,
        rely=start + padding,
        relwidth=0.5 - padding * 1.5,
        relheight=0.1 - padding * 1.5,
    )
    save_button.place(
        relx=start + 0.5 + padding * 0.5,
        rely=start + padding,
        relwidth=0.5 - padding * 1.5,
        relheight=0.1 - padding * 1.5,
    )
    program_code_text.place(
        relx=start + padding,
        rely=start + 0.1 + padding * 0.5,
        relwidth=1.0 - padding * 2,
        relheight=0.9 - padding * 1.5,
    )

    bottom_left_frame.place(
        relx=start + padding,
        rely=start + 0.8 + padding * 0.5,
        relwidth=0.5 - padding * 1.5,
        relheight=0.2 - padding * 1.5,
    )
    errors_text.place(
        relx=start + padding,
        rely=start + padding,
        relwidth=1.0 - padding * 2,
        relheight=1.0 - padding * 2,
    )

    right_tab_widget.place(
        relx=center + padding * 0.5,
        rely=start + padding,
        relwidth=0.5 - padding * 1.5,
        relheight=1.0 - padding * 2,
    )

    root.mainloop()


if __name__ == '__main__':
    main()
