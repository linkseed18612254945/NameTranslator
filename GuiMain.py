from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import DataBase


# 基础界面参数
AUTHOR = 'Kun Li'
VERSION = '1.00'
TITLE = 'NameTranslator'+'     Ver ' + VERSION


class NameTranslator:
    def __init__(self, master):
        self.master = master
        self.mainframe = ttk.Frame(self.master)
        self.style = ttk.Style()
        self.style.configure("BW.TLabel", background="white")
        self.input_box = ttk.Notebook(self.mainframe)
        self.basic_frame = ttk.Frame(self.input_box, padding=(5, 5))
        self.advanced_frame = ttk.Frame(self.input_box, padding=(5, 5))
        self.input_box.add(self.basic_frame, text='Basic')
        self.input_box.add(self.advanced_frame, text='Advance')
        self.output_frame = ttk.Frame(self.mainframe)
        self.result_frame = ttk.Frame(self.output_frame, borderwidth=3, relief='ridge', padding=(5, 5), style='BW.TLabel')
        self.detail_frame = ttk.Frame(self.output_frame)
        self.detail_box = ttk.Treeview(self.detail_frame, height=12, show='headings',
                                       columns=('中文名', '英文名', '出现频次'))
        self.result_content = StringVar()
        self.grid_frame()
        self.create_detail()
        self.create_result()
        self.create_basic()
        self.en_name_ids = []
        DataBase.init_connect()

    def grid_frame(self):
        self.mainframe.grid()
        self.input_box.grid(column=0, row=0, columnspan=1, sticky=(N, S, E, W))
        self.output_frame.grid(column=1, row=0, sticky=(N, S, E, W))
        self.result_frame.grid(column=0, row=0, sticky=(N, S, W, E))
        self.detail_frame.grid(column=0, row=1, sticky=(N, S, W, E))

    def create_detail(self):
        self.detail_box.column('中文名', width=130, anchor='center')
        self.detail_box.column('英文名', width=130, anchor='center')
        self.detail_box.column('出现频次', width=130, anchor='center')
        self.detail_box.heading('中文名', text='中文名')
        self.detail_box.heading('英文名', text='英文名')
        self.detail_box.heading('出现频次', text='出现频次')
        self.detail_box.grid(column=0, row=0, sticky=(N, S, E, W))
        detail_box_ybar = ttk.Scrollbar(self.output_frame, orient=VERTICAL, command=self.detail_box.yview)
        self.detail_box.configure(yscrollcommand=detail_box_ybar.set)
        detail_box_ybar.grid(column=1, row=1, sticky=(N, S))

    def create_result(self):
        label1 = ttk.Label(self.result_frame, text='规范英文名 ：', style='BW.TLabel')
        label1.grid(column=0, row=0, padx=50, pady=50, sticky=(N, S, W, E))
        result_label = ttk.Label(self.result_frame, textvariable=self.result_content, style='BW.TLabel')
        result_label.grid(column=1, row=0, pady=30, sticky=(N, S, W, E))

    def create_basic(self):
        label1 = ttk.Label(self.basic_frame, text='基本翻译')
        label1.grid(column=0, row=0, columnspan=2, pady=50)
        label2 = ttk.Label(self.basic_frame, text='输入中文名')
        label2.grid(column=0, row=1, padx=20, sticky=(N, S, W, E))
        ch_name = StringVar()
        name_input = ttk.Entry(self.basic_frame, width=15, textvariable=ch_name)
        name_input.grid(column=1, row=1)
        submit_button = ttk.Button(self.basic_frame, text='查询', command=lambda: self.translate(ch_name))
        submit_button.grid(column=0, row=2, columnspan=2, pady=80)

    def translate(self, ch_name):
        if ch_name.get() == '':
            messagebox.showinfo(message='请输入中文姓名')
            return -1
        if len(ch_name.get()) >= 5 or len(ch_name.get()) <= 1:
            messagebox.showinfo(message='中文姓名长度必须为二到四字')
            return -1
        for i in ch_name.get():
            if ord(i) <= 127:
                messagebox.showinfo(message='请正确输入中文姓名')
                return -1
        data_query = DataBase.DataBaseConnector(ch_name.get())
        en_detail = data_query.search()
        en_name = data_query.best
        data_query.close()
        self.result_content.set(en_name)
        if en_detail[0][0]:
            ch_show = ch_name.get()
        else:
            ch_show = '无记录'
        self.detail_show(ch_show, en_detail)

    def detail_show(self, ch_name, en_detail):
        if self.en_name_ids:
            for i in self.en_name_ids:
                self.detail_box.delete(i)
            self.en_name_ids = []
        for i in en_detail:
            en_num = self.detail_box.insert('', 0, values=(ch_name, i[0], i[1]))
            self.en_name_ids.append(en_num)


def main():
    root = Tk()
    root.title(TITLE)
    root.geometry('640x400-400+200')
    root.resizable(True, True)
    NameTranslator(root)
    root.mainloop()

if __name__ == '__main__':
    main()
