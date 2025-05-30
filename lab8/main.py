import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk

class TextStegoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Текстовая стеганография — Метод пробелов")
        self.text_data = ""
        self.setup_ui()

    def setup_ui(self):
        self.root.geometry("650x450")
        self.root.configure(padx=20, pady=20, bg="#f4f4f4")

        # Заголовок
        title = tk.Label(self.root, text="Текстовая стеганография — Метод пробелов", font=("Helvetica", 14, "bold"),
                         bg="#f4f4f4")
        title.pack(pady=(0, 10))

        # Блок управления
        control_frame = ttk.LabelFrame(self.root, text="Управление")
        control_frame.pack(fill="x", pady=10)

        ttk.Button(control_frame, text="Загрузить текст", command=self.load_text).grid(row=0, column=0, padx=10,
                                                                                       pady=10)

        ttk.Label(control_frame, text="Сообщение для встраивания:").grid(row=1, column=0, sticky="w", padx=10)
        self.message_entry = ttk.Entry(control_frame, width=60)
        self.message_entry.grid(row=1, column=1, padx=10, pady=5)

        ttk.Button(control_frame, text="Встроить сообщение", command=self.embed_message).grid(row=2, column=0, padx=10,
                                                                                              pady=10)
        ttk.Button(control_frame, text="Сохранить результат", command=self.save_text).grid(row=2, column=1, padx=10,
                                                                                           pady=10, sticky="w")
        ttk.Button(control_frame, text="Извлечь сообщение", command=self.extract_message).grid(row=2, column=1, padx=10,
                                                                                               pady=10, sticky="e")

        # Блок вывода
        output_frame = ttk.LabelFrame(self.root, text="Результат")
        output_frame.pack(fill="both", expand=True, pady=10)

        self.output_label = tk.Label(output_frame, text="", wraplength=600, justify="left", bg="white", fg="#333",
                                     anchor="nw", padx=10, pady=10)
        self.output_label.pack(fill="both", expand=True)

    def load_text(self):
        filepath = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if filepath:
            with open(filepath, "r", encoding="utf-8") as f:
                self.text_data = f.read()
            messagebox.showinfo("Файл загружен", "Текст успешно загружен.")

    def save_text(self):
        if not self.text_data:
            messagebox.showwarning("Ошибка", "Нет текста для сохранения.")
            return
        filepath = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if filepath:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(self.text_data)
            messagebox.showinfo("Сохранено", "Файл успешно сохранён.")

    def embed_message(self):
        if not self.text_data:
            messagebox.showwarning("Ошибка", "Сначала загрузите текст.")
            return

        message = self.message_entry.get()
        if not message:
            messagebox.showwarning("Ошибка", "Введите сообщение.")
            return

        message += '\0'  # стоп-символ
        binary = ''.join(f"{ord(c):08b}" for c in message)

        # Разделение по словам вручную
        words = []
        word = ''
        for ch in self.text_data:
            if ch.isspace():
                if word:
                    words.append(word)
                    word = ''
            else:
                word += ch
        if word:
            words.append(word)

        if len(words) < len(binary):
            messagebox.showerror("Мало текста", "Мало слов для скрытия сообщения. Добавь ещё!")
            return

        embedded_text = ''
        for i, word in enumerate(words):
            embedded_text += word
            if i < len(binary):
                embedded_text += '  ' if binary[i] == '1' else ' '
            else:
                embedded_text += ' '

        self.text_data = embedded_text
        capacity = len(words)
        used = len(binary)
        percent = used / capacity * 100
        messagebox.showinfo("Готово", f"Сообщение встроено. Использовано {used} из {capacity} слов (%.2f%%)." % percent)

    def extract_message(self):
        if not self.text_data:
            messagebox.showwarning("Ошибка", "Нет текста для анализа.")
            return

        bits = ''
        i = 0
        while i < len(self.text_data):
            if self.text_data[i].isspace():
                space_count = 0
                while i < len(self.text_data) and self.text_data[i] == ' ':
                    space_count += 1
                    i += 1
                if space_count == 1:
                    bits += '0'
                elif space_count == 2:
                    bits += '1'
            else:
                i += 1

        chars = []
        for j in range(0, len(bits), 8):
            byte = bits[j:j+8]
            if len(byte) < 8:
                break
            ch = chr(int(byte, 2))
            if ch == '\0':
                break
            chars.append(ch)

        message = ''.join(chars)
        self.output_label.config(text="Извлечённое сообщение:\n" + message)

if __name__ == "__main__":
    root = tk.Tk()
    style = ttk.Style()
    style.theme_use('clam')
    app = TextStegoApp(root)
    root.mainloop()