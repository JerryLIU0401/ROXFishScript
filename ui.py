import tkinter as tk
from tkinter import messagebox
from script import Script

class Roxui():
    def __init__(self):
        # 建立主視窗
        self.root = tk.Tk()
        self.root.title("文字輸入介面")
        self.root.geometry("300x300")

        # 視窗標籤
        window_label = tk.Label(self.root, text="請輸入視窗名稱：", font=("Arial", 12))
        window_label.pack(pady=10)

        # 輸入框
        self.window_entry = tk.Entry(self.root, width=30, font=("Arial", 12))
        self.window_entry.pack(pady=5)

        # 次數標籤
        counts_label = tk.Label(self.root, text="請輸入釣魚次數： (預設為100)", font=("Arial", 12))
        counts_label.pack(pady=10)

        # 輸入框
        self.counts_entry = tk.Entry(self.root, width=30, font=("Arial", 12))
        self.counts_entry.pack(pady=5)

        # 提交按鈕
        button = tk.Button(self.root, text="提交", command=self.on_submit, font=("Arial", 12))
        button.pack(pady=10)

        self.user_input = ''
        self.user_counts = 100

        self.root.mainloop()
    def on_submit(self):
        """處理按下按鈕時的事件"""
        self.user_input = self.window_entry.get()  # 獲取輸入框的內容
        if self.counts_entry.get():
            self.user_counts = int(self.counts_entry.get())  # 獲取輸入框的內容
        self.root.destroy()

    def getEntry(self):
        return self.user_input, self.user_counts

    # def show_window(self):
    #     """重新顯示視窗"""
    #     self.root.deiconify()

    # def setLoop(self):
    #     self.root.mainloop()
    #
    def destroy(self):
        self.root.destroy()
