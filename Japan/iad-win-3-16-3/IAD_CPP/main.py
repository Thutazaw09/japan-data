import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import subprocess
import os


class IADWorkbenchPro:
    def __init__(self, root):
        self.root = root
        self.root.title("Optical Engineering Lab | IAD Workbench 2026")
        self.root.geometry("1200x850")
        self.root.configure(bg="#F5F5F7")

        # --- State Variables ---
        self.input_path = tk.StringVar(value="No input loaded")
        self.output_path = tk.StringVar(value="No result generated")

        # --- 1. Top Ribbon ---
        self.ribbon = tk.Frame(
            root, bg="#FFFFFF", height=100, bd=1, relief="flat")
        self.ribbon.pack(side=tk.TOP, fill=tk.X)
        self.ribbon.pack_propagate(False)

        self.create_ribbon_section("PROJECT", 20, [
            ("📂\nOpen", self.browse_input),
            ("💾\nSave", self.save_current_tab),
            ("📁\nSave As", self.save_as_current_tab)
        ])

        self.create_ribbon_section("SOLVER", 260, [
            ("▶\nSOLVE", self.execute_iad, ("#28CD41", "#FFFFFF"))
        ])

        # --- 2. Sidebar (ANSYS Outline Style) ---
        self.sidebar = tk.Frame(root, bg="#E5E5EA", width=260)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)
        self.sidebar.pack_propagate(False)

        # INPUT FILE CARD
        tk.Label(self.sidebar, text="Input Geometry", font=("SF Pro Display",
                 11, "bold"), bg="#E5E5EA").pack(pady=(15, 5), anchor="w", padx=15)
        self.in_card = tk.Frame(self.sidebar, bg="#D1D1D6", padx=10, pady=10)
        self.in_card.pack(fill=tk.X, padx=15, pady=5)
        tk.Label(self.in_card, textvariable=self.input_path, font=(
            "SF Pro Text", 8), bg="#D1D1D6", wraplength=200, justify="left").pack(anchor="w")

        # OUTPUT FILE CARD (New Feature)
        tk.Label(self.sidebar, text="Active Result", font=("SF Pro Display",
                 11, "bold"), bg="#E5E5EA").pack(pady=(15, 5), anchor="w", padx=15)
        self.out_card = tk.Frame(self.sidebar, bg="#D1D1D6", padx=10, pady=10)
        self.out_card.pack(fill=tk.X, padx=15, pady=5)
        tk.Label(self.out_card, textvariable=self.output_path, font=(
            "SF Pro Text", 8), bg="#D1D1D6", wraplength=200, justify="left").pack(anchor="w")

        # Parameters Section
        tk.Label(self.sidebar, text="Parameters", font=("SF Pro Display",
                 11, "bold"), bg="#E5E5EA").pack(pady=(20, 5), anchor="w", padx=15)
        param_frame = tk.Frame(self.sidebar, bg="#E5E5EA")
        param_frame.pack(fill=tk.X, padx=15)

        tk.Label(param_frame, text="MC Photons (-p)", bg="#E5E5EA",
                 font=("SF Pro Text", 9)).pack(anchor="w")
        self.mc_val = tk.Entry(param_frame, font=(
            "SF Pro Text", 10), relief="flat")
        self.mc_val.insert(0, "100000")
        self.mc_val.pack(fill=tk.X, pady=(0, 15))

        tk.Label(param_frame, text="Incident Angle (-i)",
                 bg="#E5E5EA", font=("SF Pro Text", 9)).pack(anchor="w")
        self.angle_val = tk.Entry(param_frame, font=(
            "SF Pro Text", 10), relief="flat")
        self.angle_val.insert(0, "8")
        self.angle_val.pack(fill=tk.X, pady=(0, 15))

        # --- 3. Main Workspace ---
        self.main_view = tk.Frame(root, bg="#F5F5F7")
        self.main_view.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.status_pill = tk.Label(self.main_view, text="READY", bg="#007AFF", fg="white",
                                    font=("SF Pro Text", 8, "bold"), padx=12, pady=4)
        self.status_pill.pack(anchor="w", padx=25, pady=(15, 0))

        self.notebook = ttk.Notebook(self.main_view)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Tabs
        self.tab_input = tk.Frame(self.notebook, bg="white")
        self.input_editor = tk.Text(self.tab_input, wrap=tk.NONE, undo=True, font=(
            "SF Mono", 10), padx=15, pady=15, relief="flat")
        self.input_editor.pack(fill=tk.BOTH, expand=True)
        self.notebook.add(self.tab_input, text="  Input (.rxt)  ")

        self.tab_output = tk.Frame(self.notebook, bg="white")
        self.output_editor = tk.Text(self.tab_output, wrap=tk.NONE, undo=True, font=(
            "SF Mono", 10), padx=15, pady=15, relief="flat", bg="#FBFBFD")
        self.output_editor.pack(fill=tk.BOTH, expand=True)
        self.notebook.add(self.tab_output, text="  Results (.txt)  ")

    def create_ribbon_section(self, title, x, buttons):
        tk.Label(self.ribbon, text=title, font=("SF Pro Text", 7,
                 "bold"), bg="white", fg="#8E8E93").place(x=x, y=5)
        for i, (text, cmd, *color_config) in enumerate(buttons):
            if color_config and isinstance(color_config, tuple):
                bg_color, fg_color = color_config
            else:
                bg_color, fg_color = "#F2F2F7", "#000000"

            btn = tk.Button(self.ribbon, text=text, command=cmd, relief="flat",
                            bg=bg_color, fg=fg_color, font=("SF Pro Text", 8))
            btn.place(x=x + (i * 75), y=22, width=70, height=65)

    def browse_input(self):
        file = filedialog.askopenfilename(
            filetypes=[("IAD Input", "*.rxt"), ("All Files", "*.*")])
        if file:
            self.input_path.set(file)
            with open(file, 'r') as f:
                self.input_editor.delete('1.0', tk.END)
                self.input_editor.insert(tk.END, f.read())
            self.notebook.select(0)
            self.status_pill.config(text="LOADED", bg="#007AFF")

    def _write_file(self, path, editor):
        try:
            content = editor.get('1.0', tk.END).strip()
            with open(path, 'w') as f:
                f.write(content)
            self.status_pill.config(text="FILE SAVED", bg="#5856D6")
        except Exception as e:
            messagebox.showerror("Error", f"Could not save file: {e}")

    def save_current_tab(self):
        current_tab = self.notebook.index(self.notebook.select())
        if current_tab == 0:
            if "No input loaded" in self.input_path.get():
                return self.save_as_current_tab()
            self._write_file(self.input_path.get(), self.input_editor)
        else:
            if "No result generated" in self.output_path.get():
                return self.save_as_current_tab()
            self._write_file(self.output_path.get(), self.output_editor)

    def save_as_current_tab(self):
        current_tab = self.notebook.index(self.notebook.select())
        default_ext = ".rxt" if current_tab == 0 else ".txt"
        file = filedialog.asksaveasfilename(defaultextension=default_ext, filetypes=[
                                            ("Files", f"*{default_ext}")])
        if file:
            editor = self.input_editor if current_tab == 0 else self.output_editor
            self._write_file(file, editor)
            if current_tab == 0:
                self.input_path.set(file)
            else:
                self.output_path.set(file)

    def execute_iad(self):
        if "No input loaded" in self.input_path.get():
            messagebox.showwarning(
                "Logic Error", "Please load an .rxt file first.")
            return

        self.save_current_tab()
        self.status_pill.config(text="SOLVING...", bg="#FF9500")
        self.root.update_idletasks()

        out_file = self.input_path.get().replace(".rxt", ".txt")

        command = [
            "iad.exe", "-o", out_file, "-X", "-i", self.angle_val.get(),
            "-p", self.mc_val.get(), self.input_path.get()
        ]

        try:
            subprocess.run(command, capture_output=True, text=True, check=True)
            with open(out_file, 'r') as f:
                content = f.read()

            self.output_editor.config(state='normal')
            self.output_editor.delete('1.0', tk.END)
            self.output_editor.insert(tk.END, content)
            self.output_path.set(out_file)  # UPDATES THE NEW SIDEBAR CARD

            self.notebook.select(1)
            self.status_pill.config(text="CONVERGED", bg="#28CD41")
        except Exception as e:
            self.status_pill.config(text="ERROR", bg="#FF3B30")
            messagebox.showerror("Solver Error", str(e))


if __name__ == "__main__":
    root = tk.Tk()
    app = IADWorkbenchPro(root)
    root.mainloop()
