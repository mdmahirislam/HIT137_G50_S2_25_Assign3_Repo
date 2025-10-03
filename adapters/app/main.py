import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

from adapters.vit_classifier import VitImageClassifier         
from adapters.distilgpt2_text import DistilGPT2TextGen       

class App(tk.Tk):
    """
    HIT137 GUI with two Transformers models:
      • Image → Classification (ViT)       
      • Text  → Generation (DistilGPT2)   
    Shows menus/buttons/outputs and OOP concepts.
    """
    def __init__(self):
        super().__init__()
        self.title("HIT137 AI Hub")
        self.geometry("920x720")

        # --- Models ---
        self.ic_model = VitImageClassifier()          
        self.tg_model = DistilGPT2TextGen()           

        # --- State ---
        self.selected_image_path = tk.StringVar(value="")
        self._preview_img = None  # keep reference

        # ============== MENUBAR ==============
        menubar = tk.Menu(self)
        helpmenu = tk.Menu(menubar, tearoff=0)
        helpmenu.add_command(label="Where we used OOP", command=self.show_oop_notes)
        helpmenu.add_command(label="Image Model Info", command=self.show_ic_info)
        helpmenu.add_command(label="Text Model Info", command=self.show_tg_info)
        menubar.add_cascade(label="Help", menu=helpmenu)
        self.config(menu=menubar)

        # ============== TOP FRAME (TEXT GEN) ==============
        tg_frame = tk.LabelFrame(self, text=self.tg_model.display_name)
        tg_frame.pack(fill="x", padx=10, pady=10)

        # Prompt input
        tk.Label(tg_frame, text="Prompt:").grid(row=0, column=0, sticky="ne", padx=8, pady=6)
        self.prompt_box = tk.Text(tg_frame, height=5, width=80)
        self.prompt_box.grid(row=0, column=1, columnspan=3, sticky="we", padx=8, pady=6)

        # Controls
        tk.Label(tg_frame, text="Max New Tokens").grid(row=1, column=0, sticky="e", padx=8)
        self.max_tokens_var = tk.IntVar(value=64)
        tk.Spinbox(tg_frame, from_=1, to=256, textvariable=self.max_tokens_var, width=6).grid(row=1, column=1, sticky="w")

        tk.Label(tg_frame, text="Temperature").grid(row=1, column=2, sticky="e", padx=8)
        self.temp_var = tk.DoubleVar(value=0.7)
        tk.Spinbox(tg_frame, from_=0.1, to=2.0, increment=0.1, textvariable=self.temp_var, width=6).grid(row=1, column=3, sticky="w")

        tk.Label(tg_frame, text="Top-p").grid(row=1, column=4, sticky="e", padx=8)
        self.topp_var = tk.DoubleVar(value=0.9)
        tk.Spinbox(tg_frame, from_=0.1, to=1.0, increment=0.05, textvariable=self.topp_var, width=6).grid(row=1, column=5, sticky="w")

        tg_btns = tk.Frame(tg_frame)
        tg_btns.grid(row=2, column=0, columnspan=6, sticky="w", padx=8, pady=6)
        tk.Button(tg_btns, text="Run Text Generation", command=self.run_tg).pack(side="left", padx=4)
        tk.Button(tg_btns, text="Text Model Info", command=self.show_tg_info).pack(side="left", padx=4)

        # ============== MID FRAME (IMAGE CLASSIFICATION) ==============
        ic_frame = tk.LabelFrame(self, text=self.ic_model.display_name)
        ic_frame.pack(fill="x", padx=10, pady=(0,10))

        tk.Button(ic_frame, text="Choose Image", command=self.choose_image).grid(row=0, column=0, padx=8, pady=8, sticky="w")
        tk.Label(ic_frame, textvariable=self.selected_image_path, wraplength=520, anchor="w", justify="left").grid(row=0, column=1, padx=8, pady=8, sticky="w")

        tk.Label(ic_frame, text="Top-K").grid(row=1, column=0, sticky="e", padx=8)
        self.topk_var = tk.IntVar(value=3)
        tk.Spinbox(ic_frame, from_=1, to=10, textvariable=self.topk_var, width=6).grid(row=1, column=1, sticky="w", padx=8)

        ic_btns = tk.Frame(ic_frame)
        ic_btns.grid(row=2, column=0, columnspan=2, sticky="w", padx=8, pady=4)
        tk.Button(ic_btns, text="Run Classification", command=self.run_ic).pack(side="left", padx=4)
        tk.Button(ic_btns, text="Image Model Info", command=self.show_ic_info).pack(side="left", padx=4)

        # Image preview
        self.preview_label = tk.Label(ic_frame, width=200, height=200, bg="#f5f5f5", relief="groove")
        self.preview_label.grid(row=3, column=0, columnspan=2, padx=8, pady=(4, 10), sticky="w")

        # ============== OUTPUT BOX (shared) ==============
        self.output = tk.Text(self, height=16)
        self.output.pack(fill="both", expand=True, padx=10, pady=10)

        # Footer hint
        hint = tk.Label(self, text="Tip: add apple.jpg and mug.jpg in repo root for quick tests.")
        hint.pack(side="bottom", pady=(0, 8))

    # -------- Handlers: TEXT GEN --------
    def run_tg(self):
        try:
            prompt = self.prompt_box.get("1.0","end").strip()
            text = self.tg_model.run(
                prompt,
                max_new_tokens=self.max_tokens_var.get(),
                temperature=float(self.temp_var.get()),
                top_p=float(self.topp_var.get()),
                do_sample=True
            )
            self.output.delete("1.0", "end")
            self.output.insert("1.0", text)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def show_tg_info(self):
        try:
            info = self.tg_model.brief_info()
        except Exception:
            info = self.tg_model.brief_info()
        self.output.delete("1.0", "end")
        self.output.insert("1.0", info)

    # -------- Handlers: IMAGE CLF --------
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

    def show_ic_info(self):
        try:
            info = self.ic_model.brief_info()
        except Exception:
            info = self.ic_model.brief_info()
        self.output.delete("1.0", "end")
        self.output.insert("1.0", info)

    # -------- Help / OOP Notes ----------
    def show_oop_notes(self):
        notes = (
            "OOP usage:\n"
            "• Inheritance: DistilGPT2TextGen/ VitImageClassifier inherit ModelAdapter.\n"
            "• Multiple Inheritance: both also mix in LoggingMixin.\n"
            "• Encapsulation: _loaded/_model/_pipe hidden inside adapters.\n"
            "• Method Overriding: each adapter implements load() and run().\n"
            "• Multiple Decorators: input validation + bounds + error wrapping on run().\n"
            "• Polymorphism: GUI calls adapter.run(...) without knowing internals."
        )
        self.output.delete("1.0", "end")
        self.output.insert("1.0", notes)

if __name__ == "__main__":
    App().mainloop()
