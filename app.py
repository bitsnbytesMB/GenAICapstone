import tkinter as tk
from tkinter import filedialog, messagebox, Listbox, END, Scrollbar, Menu, Toplevel, Label, Entry, ttk
from PIL import Image, ImageTk
import os
from utils import *

# Main
class PDFReaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Reader Tool 1.0")

        # Initialize dictionaries and lists
        self.summaries = load_summaries()
        self.image_refs = []

        # Create main frame
        main_frame = tk.Frame(root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Create menu bar
        self.menu_bar = Menu(root)
        root.config(menu=self.menu_bar)

        # File menu
        file_menu = Menu(self.menu_bar, tearoff=0)
        file_menu.add_command(label="Open PDF", command=self.upload_pdf)
        file_menu.add_command(label="Save Summary", command=self.save_summary_as_text)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=root.quit)
        self.menu_bar.add_cascade(label="File", menu=file_menu)

        # Options menu
        options_menu = Menu(self.menu_bar, tearoff=0)
        options_menu.add_command(label="Clear Text Area", command=self.clear_text_area)
        options_menu.add_command(label="Delete Summary", command=self.delete_summary)
        self.menu_bar.add_cascade(label="Options", menu=options_menu)

        # About menu
        about_menu = Menu(self.menu_bar, tearoff=0)
        about_menu.add_command(label="About", command=self.show_about)
        self.menu_bar.add_cascade(label="About", menu=about_menu)

        # Help menu
        help_menu = Menu(self.menu_bar, tearoff=0)
        help_menu.add_command(label="Help", command=self.show_help)
        self.menu_bar.add_cascade(label="Help", menu=help_menu)

        # Left navigation bar
        self.listbox = Listbox(main_frame, width=40, height=20, selectmode=tk.SINGLE,
                               font=("Arial", 12), activestyle='none')
        self.listbox.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10), pady=10)
        scrollbar = Scrollbar(main_frame, orient=tk.VERTICAL)
        scrollbar.config(command=self.listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=10)
        self.listbox.config(yscrollcommand=scrollbar.set)
        self.listbox.bind('<<ListboxSelect>>', self.display_summary)

        # Main display area
        self.text_area = tk.Text(main_frame, wrap=tk.WORD, height=20, font=("Arial", 12), padx=10, pady=10)
        self.text_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10), pady=10)

        # Upload button
        self.upload_button = tk.Button(root, text="Upload PDF", command=self.upload_pdf,
                                       font=("Arial", 12), padx=10, pady=5)
        self.upload_button.pack(side=tk.TOP, fill=tk.X, padx=10, pady=(0, 10))

        self.upload_button.bind("<Enter>", self.on_enter)
        self.upload_button.bind("<Leave>", self.on_leave)

        self.load_listbox()

    def on_enter(self, event):
        event.widget['background'] = '#d9d9d9'

    def on_leave(self, event):
        event.widget['background'] = 'SystemButtonFace'

    def load_listbox(self):
        self.listbox.delete(0, END)
        for title in self.summaries.keys():
            self.listbox.insert(END, title)

    def upload_pdf(self):
        file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if file_path:
            try:
                text = extract_text_from_pdf(file_path)
                bullet_points = get_summary_and_metadata_from_text(text)
                summary = "\n".join(bullet_points)
                title = os.path.basename(file_path)
                self.summaries[title] = summary

                # Extract images and add names to summary
                image_filenames = extract_images_from_pdf(file_path)
                if image_filenames:
                    summary += "\n\nExtracted Images:\n" + "\n".join(image_filenames)
                    self.summaries[title] = summary

                save_summaries(self.summaries)
                self.load_listbox()
                self.text_area.delete(1.0, END)
                self.text_area.insert(1.0, summary)
                messagebox.showinfo("Success!", "Import successful!")
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def display_summary(self, event):
        selected_index = self.listbox.curselection()
        if selected_index:
            selected_title = self.listbox.get(selected_index)
            summary = self.summaries[selected_title]
            self.text_area.delete(1.0, END)

            if "\n\nExtracted Images:\n" in summary:
                summary_text, image_filenames_text = summary.split("\n\nExtracted Images:\n", 1)
                image_filenames = image_filenames_text.split("\n")
            else:
                summary_text = summary
                image_filenames = []

            self.text_area.insert(1.0, summary_text)

            self.image_refs = []
            for image_filename in image_filenames:
                try:
                    img = Image.open(image_filename)
                    img.thumbnail((500, 500))
                    img = ImageTk.PhotoImage(img)
                    self.text_area.image_create(END, image=img)
                    self.text_area.insert(END, "\n")
                    self.image_refs.append(img)
                except Exception as e:
                    print(f"Loading error {image_filename}: {e}")

    def clear_text_area(self):
        self.text_area.delete(1.0, END)

    def delete_summary(self):
        selected_index = self.listbox.curselection()
        if selected_index:
            selected_title = self.listbox.get(selected_index)
            del self.summaries[selected_title]
            save_summaries(self.summaries)
            self.load_listbox()
            self.text_area.delete(1.0, END)

    def save_summary_as_text(self):
        selected_index = self.listbox.curselection()
        if selected_index:
            selected_title = self.listbox.get(selected_index)
            summary = self.summaries[selected_title]
            file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
            if file_path:
                try:
                    with open(file_path, 'w') as file:
                        file.write(summary)
                    messagebox.showinfo("Entry saved", "Summary saved!")  # Feedback message
                except Exception as e:
                    messagebox.showinfo("Error", f"An error occurred: {str(e)}")

    def show_about(self):
        about_window = Toplevel(self.root)
        about_window.title("About")
        about_window.geometry("400x150")
        Label(about_window, text="This program was made by Maximilian Berens\n\nfor 2024S 136031-1 GenAI for Humanists", font=("Arial", 12)).pack(pady=10)

    def show_help(self):
        help_window = Toplevel(self.root)
        help_window.title("Help")
        help_window.geometry("800x150")
        Label(help_window, text="Instructions on how to use the program:\n\n1. Click the button to upload a PDF file. Be mindful of the size of the file, considering API-costs.\n2. After a short while, the summary and metadata will be displayed.\n3. You can save the summary as a .txt-file. All entries will be saved in the program upon closing it for the next use.\n4. Use the options in the menu bar for more functionalities.", font=("Arial", 12)).pack(pady=10)

if __name__ == "__main__":
    root = tk.Tk()

    # Center the window on screen
    window_width = 800
    window_height = 600
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x_coordinate = (screen_width / 2) - (window_width / 2)
    y_coordinate = (screen_height / 2) - (window_height / 2)
    root.geometry("%dx%d+%d+%d" % (window_width, window_height, x_coordinate, y_coordinate))

    # Start the program
    app = PDFReaderApp(root)

    root.mainloop()
