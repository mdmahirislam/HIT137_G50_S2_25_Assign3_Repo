import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
from adapters.vit_classifier import VitImageClassifier

class App(tk.Tk):
    """
    Minimal GUI for Nathan's image classification.
    Shows menus/buttons/outputs and ties into the adapter polymorphically.
    """
    def __init__(self):
        super().__init__()
        self.title("HIT137 AI Hub")
        self.geometry("780x560")

        # --- Model (Nathan) ---
        self.ic_model = VitImageClassifier()  # default: google/vit-base-patch16-224
        self.selected_image_path = tk.StringVar(value="")

        # --- Menu bar (About / Help) ---
        menubar = tk.Menu(self)
        helpmenu = tk.Menu(menubar, tearoff=0)
        helpmenu.add_command(label="Where we used OOP", command=self.show_oop_notes)
        helpmenu.add_command(label="Model Info", command=self.show_model_info)
        menubar.add_cascade(label="Help", menu=helpmenu)
        self.config(menu=menubar)

        # --- Panel: Image Classification ---
        frame = tk.LabelFrame(self, text=self.ic_model.display_name)
        frame.pack(fill="x", padx=10, pady=10)

        tk.Button(frame, text="Choose Image", command=self.choose_image).grid(row=0, column=0, padx=8, pady=8, sticky="w")
        tk.Label(frame, textvariable=self.selected_image_path, wraplength=520, anchor="w", justify="left").grid(row=0, column=1, padx=8, pady=8, sticky="w")

        tk.Label(frame, text="Top-K:").grid(row=1, column=0, sticky="e", padx=8)
        self.topk_var = tk.IntVar(value=3)
        tk.Spinbox(frame, from_=1, to=10, textvariable=self.topk_var, width=6).grid(row=1, column=1, sticky="w", padx=8)

        btns = tk.Frame(frame)
        btns.grid(row=2, column=0, columnspan=2, sticky="w", padx=8, pady=4)
        tk.Button(btns, text="Run Classification", command=self.run_ic).pack(side="left", padx=4)
        tk.Button(btns, text="Model Info", command=self.show_model_info).pack(side="left", padx=4)
        tk.Button(btns, text="Clear", command=lambda: self.output.delete("1.0", "end")).pack(side="left", padx=4)
        tk.Button(btns, text="Copy Results", command=self.copy_results).pack(side="left", padx=4)

        # --- Image preview ---
        self.preview_label = tk.Label(frame, width=200, height=200, bg="#f5f5f5", relief="groove")
        self.preview_label.grid(row=3, column=0, columnspan=2, padx=8, pady=(4, 10), sticky="w")
        self._preview_img = None  # keep a reference so image isn’t garbage-collected

        # --- Output box ---
        self.output = tk.Text(self, height=20)
        self.output.pack(fill="both", expand=True, padx=10, pady=10)

        # Footer hint
        hint = tk.Label(self, text="Tip: add apple.jpg and mug.jpg to the repo root, then 'Choose Image' and Run.")
        hint.pack(side="bottom", pady=(0, 8))

    # ----- Handlers -----
    def choose_image(self):
        path = filedialog.askopenfilename(
            title="Select image",
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp *.gif *.webp"), ("All files", "*.*")]
        )
        if path:
            self.selected_image_path.set(path)
            try:
                img = Image.open(path).convert("RGB")
                img.thumbnail((200, 200))
                self._preview_img = ImageTk.PhotoImage(img)
                self.preview_label.configure(image=self._preview_img)
            except Exception as e:
                self._preview_img = None
                self.preview_label.configure(image="", text="(preview failed)")
                messagebox.showerror("Preview error", str(e))

    def run_ic(self):
        try:
            results = self.ic_model.run(self.selected_image_path.get(), top_k=self.topk_var.get())
            self.output.delete("1.0", "end")
            self.output.insert("1.0", "Top predictions:\n")
            for i, r in enumerate(results, 1):
                self.output.insert("end", f"{i}. {r['label']}  (score: {r['score']:.4f})\n")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def show_model_info(self):
        try:
            info = self.ic_model.brief_info()
        except Exception:
            info = self.ic_model.brief_info()  # ensure model loads, then try again
        self.output.delete("1.0", "end")
        self.output.insert("1.0", info)

    def show_oop_notes(self):
        notes = (
            "OOP usage in Image Classification:\n"
            "• Inheritance: VitImageClassifier(ModelAdapter) shares a common interface.\n"
            "• Multiple Inheritance: VitImageClassifier also mixes in LoggingMixin.\n"
            "• Encapsulation: _loaded/_model/_pipe are internal and hidden from GUI.\n"
            "• Method Overriding: load() and run() implement adapter-specific behavior.\n"
            "• Multiple Decorators: @ensure_image_path, @topk_bounds, @catch_errors.\n"
            "• Polymorphism: GUI calls model.run(...) without knowing model internals."
        )
        self.output.delete("1.0", "end")
        self.output.insert("1.0", notes)

    def copy_results(self):
        txt = self.output.get("1.0","end")
        self.clipboard_clear(); self.clipboard_append(txt)
        messagebox.showinfo("Copied", "Results copied to clipboard")

if __name__ == "__main__":
    App().mainloop()
