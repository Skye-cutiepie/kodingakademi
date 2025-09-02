import tkinter as tk
from tkinter import messagebox
import os


class FileManager:
    """
    Handles all file-related operations (CRUD) like creating, reading,
    updating, and deleting files. This keeps file logic separate from the GUI.
    """

    def file_exists(self, filename):
        return os.path.isfile(filename)

    def create_file(self, filename, content):
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        except Exception as e:
            messagebox.showerror("File Error", f"Failed to create file: {e}")
            return False

    def read_file(self, filename):
        if not self.file_exists(filename):
            messagebox.showerror("File Error", f"File '{filename}' not found.")
            return None
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            messagebox.showerror("File Error", f"Failed to read file: {e}")
            return None

    def append_to_file(self, filename, content):
        try:
            with open(filename, 'a', encoding='utf-8') as f:
                if f.tell() > 0 and content:
                    f.write('\n')
                f.write(content)
            return True
        except Exception as e:
            messagebox.showerror("File Error", f"Failed to append to file: {e}")
            return False

    def update_file(self, filename, search_text, new_text):
        content = self.read_file(filename)
        if content is None:
            return False

        if search_text not in content:
            messagebox.showwarning("Update Warning", f"Text '{search_text}' not found in the file.")
            return False

        try:
            updated_content = content.replace(search_text, new_text)
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(updated_content)
            return True
        except Exception as e:
            messagebox.showerror("File Error", f"Failed to update file: {e}")
            return False

    def delete_file(self, filename):
        if not self.file_exists(filename):
            messagebox.showerror("File Error", f"File '{filename}' not found.")
            return False
        try:
            os.remove(filename)
            return True
        except Exception as e:
            messagebox.showerror("File Error", f"Failed to delete file: {e}")
            return False


class Main:
    """
    Manages the GUI setup, layout, and event handling for the application.
    """

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("GUI CRUD")
        self.root.geometry("750x450")
        self.root.minsize(600, 400)  # Set a minimum size
        self.file_manager = FileManager()
        self.create_widgets()

    def create_widgets(self):
        # --- Top Frame for Filename Input ---
        top_frame = tk.Frame(self.root, padx=10, pady=5)
        top_frame.pack(side="top", fill="x")
        tk.Label(top_frame, text="Nama file:").pack(side="left", padx=(0, 5))
        self.entry_filename = tk.Entry(top_frame)
        self.entry_filename.pack(side="left", expand=True, fill="x")

        # --- Main Frame for Text Areas ---
        main_frame = tk.Frame(self.root, padx=10)
        main_frame.pack(side="top", fill="both", expand=True)
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=1)
        main_frame.grid_rowconfigure(0, weight=1)

        # --- Left Side: Input Text Area ---
        teks_frame = tk.LabelFrame(main_frame, text="Teks", padx=5, pady=5)
        teks_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 5))
        teks_frame.grid_rowconfigure(0, weight=1)
        teks_frame.grid_columnconfigure(0, weight=1)
        self.teks_input = tk.Text(teks_frame, wrap="word")
        self.teks_input.grid(row=0, column=0, sticky="nsew")

        teks_button_frame = tk.Frame(teks_frame)
        teks_button_frame.grid(row=0, column=1, sticky="ns", padx=(5, 0))
        tk.Button(teks_button_frame, text="Create", width=8, command=self.on_create_click).pack(pady=2)
        tk.Button(teks_button_frame, text="Append", width=8, command=self.on_append_click).pack(pady=2)

        # --- Right Side: Display Text Area ---
        tampil_frame = tk.LabelFrame(main_frame, text="Tampil", padx=5, pady=5)
        tampil_frame.grid(row=0, column=1, sticky="nsew", padx=(5, 0))
        tampil_frame.grid_rowconfigure(0, weight=1)
        tampil_frame.grid_columnconfigure(0, weight=1)
        self.tampil_input = tk.Text(tampil_frame, wrap="word", state='disabled')
        self.tampil_input.grid(row=0, column=0, sticky="nsew")

        read_button_frame = tk.Frame(tampil_frame)
        read_button_frame.grid(row=0, column=1, sticky="ns", padx=(5, 0))
        tk.Button(read_button_frame, text="Read", width=8, command=self.on_read_click).pack(pady=2)

        # --- Bottom Frame for Update/Delete Controls ---
        bottom_frame = tk.Frame(self.root, padx=10, pady=10)
        bottom_frame.pack(side="bottom", fill="x")
        bottom_frame.grid_columnconfigure(0, weight=1)
        bottom_frame.grid_columnconfigure(1, weight=1)

        # --- FIX: Using .grid() consistently for the entire update_frame ---
        update_frame = tk.LabelFrame(bottom_frame, text="Update Text", padx=5, pady=5)
        update_frame.grid(row=0, column=0, sticky="ew", padx=(0, 5))
        update_frame.grid_columnconfigure(1, weight=1)
        tk.Label(update_frame, text="Search text:").grid(row=0, column=0, sticky="w", pady=2)
        self.search_entry = tk.Entry(update_frame)
        self.search_entry.grid(row=0, column=1, sticky="ew", padx=5)

        # New frame to hold replace entry and button together
        replace_frame = tk.Frame(update_frame)
        replace_frame.grid(row=1, column=1, sticky="ew", padx=5)
        replace_frame.grid_columnconfigure(0, weight=1)
        tk.Label(update_frame, text="Update text:").grid(row=1, column=0, sticky="w", pady=2)
        self.update_entry = tk.Entry(replace_frame)
        self.update_entry.grid(row=0, column=0, sticky="ew")
        tk.Button(replace_frame, text="Update", command=self.on_update_click).grid(row=0, column=1, padx=(5, 0))

        # Delete section
        delete_frame = tk.LabelFrame(bottom_frame, text="Delete File", padx=5, pady=5)
        delete_frame.grid(row=0, column=1, sticky="ew", padx=(5, 0))
        delete_frame.grid_columnconfigure(0, weight=1)
        tk.Label(delete_frame, text="File:").grid(row=0, column=0, sticky="w")
        self.delete_entry = tk.Entry(delete_frame)
        self.delete_entry.grid(row=0, column=0, sticky="ew", padx=(5, 5))
        tk.Button(delete_frame, text="Delete", command=self.on_delete_click).grid(row=0, column=1)

    def _get_filename(self, entry_widget):
        filename = entry_widget.get().strip()
        if not filename:
            messagebox.showerror("Error", "Filename cannot be empty.")
            return None
        if not filename.endswith('.txt'):
            filename += '.txt'
        return filename

    def on_create_click(self):
        filename = self._get_filename(self.entry_filename)
        if not filename: return
        content = self.teks_input.get("1.0", "end-1c")
        if self.file_manager.create_file(filename, content):
            messagebox.showinfo("Success", f"File '{filename}' created successfully!")
            self.update_display(filename)

    def on_read_click(self):
        filename = self._get_filename(self.entry_filename)
        if not filename: return
        self.update_display(filename)

    def on_append_click(self):
        """Handles the Append button click event."""
        filename = self._get_filename(self.entry_filename)
        if not filename: return

        # FIX: Changed "1.emacs" to the correct index "1.0"
        content = self.teks_input.get("1.0", "end-1c").strip()

        if not content:
            messagebox.showerror("Error", "Input text to append cannot be empty.")
            return

        if self.file_manager.append_to_file(filename, content):
            messagebox.showinfo("Success", f"Content appended to '{filename}' successfully!")
            self.update_display(filename)

    def on_update_click(self):
        filename = self._get_filename(self.entry_filename)
        if not filename: return
        search_text = self.search_entry.get()
        update_text = self.update_entry.get()
        if not search_text:
            messagebox.showerror("Error", "The 'Search text' field cannot be empty.")
            return
        if self.file_manager.update_file(filename, search_text, update_text):
            messagebox.showinfo("Success", f"File '{filename}' was updated.")
            self.update_display(filename)

    def on_delete_click(self):
        filename = self._get_filename(self.delete_entry)
        if not filename: return
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete '{filename}'?"):
            if self.file_manager.delete_file(filename):
                messagebox.showinfo("Success", f"File '{filename}' was deleted.")
                if filename == self._get_filename(self.entry_filename):
                    self.entry_filename.delete(0, "end")
                    self.update_display(None)

    def update_display(self, filename):
        """
        Refreshes the 'Tampil' text area, adding line numbers to match the image.
        """
        self.tampil_input.config(state='normal')
        self.tampil_input.delete("1.0", "end")

        if filename:
            content = self.file_manager.read_file(filename)
            if content:
                lines = content.strip().split('\n')
                # FIX: Add line numbers to the display
                numbered_lines = [f"{i + 1}. {line}" for i, line in enumerate(lines) if line]
                self.tampil_input.insert("1.0", "\n".join(numbered_lines))

        self.tampil_input.config(state='disabled')

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = Main()
    app.run()
