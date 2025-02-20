import numpy as np
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
import os


class VisualAttackApp(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, padding="10")
        self.parent = parent
        self.parent.title("Визуальная атака битов изображения")
        self.original_image = None
        self.processed_image = None
        self.create_widgets()
        self.grid_widgets()

    def create_widgets(self):
        # Кнопки и элементы управления
        self.btn_open = ttk.Button(self, text="Открыть изображение", command=self.open_image)
        self.btn_save = ttk.Button(self, text="Сохранить результат", command=self.save_result)

        self.bit_label = ttk.Label(self, text="Выберите бит:")
        self.selected_bit = tk.IntVar(value=0)
        self.bit_selector = ttk.Combobox(self, textvariable=self.selected_bit, values=list(range(8)), state="readonly",
                                         width=5)
        self.bit_selector.bind("<<ComboboxSelected>>", self.update_bit)

        # Метки для отображения изображений
        self.original_label = ttk.Label(self, text="Оригинальное изображение")
        self.processed_label = ttk.Label(self, text="Извлечённый бит")
        self.img_display = ttk.Label(self)
        self.result_display = ttk.Label(self)

    def grid_widgets(self):
        # Верхняя панель с кнопками и выбором бита
        self.btn_open.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.btn_save.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        self.bit_label.grid(row=0, column=2, padx=5, pady=5, sticky="e")
        self.bit_selector.grid(row=0, column=3, padx=5, pady=5, sticky="w")

        # Заголовки для изображений
        self.original_label.grid(row=1, column=0, columnspan=2, padx=5, pady=(10, 0))
        self.processed_label.grid(row=1, column=2, columnspan=2, padx=5, pady=(10, 0))

        # Отображение изображений
        self.img_display.grid(row=2, column=0, columnspan=2, padx=5, pady=5)
        self.result_display.grid(row=2, column=2, columnspan=2, padx=5, pady=5)

        self.pack()

    def extract_bit(self, image_path, bit_position):
        image = Image.open(image_path)
        pixels = np.array(image)
        bit_layer = (pixels >> (7 - bit_position)) & 1
        visual_attack_image = (bit_layer * 255).astype(np.uint8)
        result = Image.fromarray(visual_attack_image)
        return result

    def open_image(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("BMP Files", "*.bmp"), ("PNG Files", "*.png"), ("JPEG Files", "*.jpg")]
        )
        if not file_path:
            return

        self.original_image = Image.open(file_path)
        self.processed_image = self.extract_bit(file_path, self.selected_bit.get())
        self.display_images()

    def display_images(self):
        if self.original_image is None or self.processed_image is None:
            return

        # Создаем копии для отображения
        original_disp = self.original_image.copy()
        processed_disp = self.processed_image.copy()
        original_disp.thumbnail((400, 400))
        processed_disp.thumbnail((400, 400))

        self.original_photo = ImageTk.PhotoImage(original_disp)
        self.processed_photo = ImageTk.PhotoImage(processed_disp)

        self.img_display.config(image=self.original_photo)
        self.result_display.config(image=self.processed_photo)

    def save_result(self):
        if self.processed_image is None:
            messagebox.showwarning("Сохранение", "Нет обработанного изображения для сохранения.")
            return

        save_directory = filedialog.askdirectory()
        if not save_directory:
            return

        save_path = os.path.join(save_directory, "extracted_bit.png")
        self.processed_image.save(save_path)
        messagebox.showinfo("Сохранение", f"Изображение сохранено в:\n{save_path}")

    def update_bit(self, event=None):
        if self.original_image is None:
            return
        # Для обновления используем оригинальное изображение с известным путем
        try:
            # Если оригинальное изображение было открыто из файла, используем его путь
            original_path = self.original_image.filename
        except AttributeError:
            # Если оригинальное изображение создано из другого источника, временно сохраняем его
            temp_path = "temp_original_image.png"
            self.original_image.save(temp_path)
            original_path = temp_path
        self.processed_image = self.extract_bit(original_path, self.selected_bit.get())
        self.display_images()


if __name__ == "__main__":
    root = tk.Tk()
    app = VisualAttackApp(root)
    root.mainloop()
