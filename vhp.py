#!/usr/bin/env python3
"""Visual Hardware Projector — JCkernel source zip to hardware blocks."""
import os, sys, zipfile, json
import tkinter as tk
from tkinter import filedialog, messagebox

HERE = os.path.dirname(os.path.abspath(__file__))

DEFAULT_MAP = {
    "blocks": [
        {"id": "loader", "title": "UEFI loader", "hw": "BOOTX64", "files": ["main.asm", "BOOTX64"], "letters": "JKGgM0EcCG6"},
        {"id": "gop", "title": "GOP / GPU FB", "hw": "linear framebuffer", "files": ["gop_stamp", "screen.c", "main.asm"], "letters": "GgtE"},
        {"id": "serial", "title": "COM1", "hw": "port 0x3F8", "files": ["entry64.asm"], "letters": "0kbcAB2"},
        {"id": "cpu", "title": "CPU long mode", "hw": "CS 0x18 EFER", "files": ["entry64.asm", "gdt.c", "idt.c", "interrupt64"], "letters": "kbcdi"},
        {"id": "mmu", "title": "MMU / paging", "hw": "CR3 at 8MiB", "files": ["paging.c", "mem_map.h"], "letters": "CPqrst"},
        {"id": "pic", "title": "PIC / timer", "hw": "8259 PIT", "files": ["pic.c", "timer.c"], "letters": ""},
        {"id": "nvme", "title": "NVMe", "hw": "M.2", "files": ["nvme.c", "disk.c"], "letters": ""},
        {"id": "usb", "title": "USB", "hw": "XHCI/UHCI", "files": ["usb.c", "usb_uhci", "usb_msc"], "letters": ""},
        {"id": "csf1", "title": "CSF1", "hw": "volume", "files": ["csf1.c", "crash_dump"], "letters": ""},
    ]
}

def load_map():
    p = os.path.join(HERE, "map.json")
    if os.path.isfile(p):
        with open(p, encoding="utf-8") as f:
            return json.load(f)
    return DEFAULT_MAP

def zip_names(path):
    names = []
    with zipfile.ZipFile(path) as z:
        for n in z.namelist():
            if n.endswith("/"):
                continue
            names.append(n.replace("\\", "/").split("/")[-1])
    return names

class VHP(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Visual Hardware Projector")
        self.geometry("920x640")
        self.configure(bg="#1a1c20")
        self.map = load_map()
        self.zip_files = []
        tk.Label(self, text="Visual Hardware Projector", fg="#2a9d8f", bg="#1a1c20",
                 font=("sans-serif", 16, "bold")).pack(anchor="w", padx=16, pady=(12, 4))
        tk.Label(self, text="Drop a JCkernel .zip  ·  paste serial trail  ·  last letter lights a block",
                 fg="#aaa", bg="#1a1c20").pack(anchor="w", padx=16)
        self.trail = tk.Entry(self, bg="#111", fg="#eee", insertbackground="#eee")
        self.trail.pack(fill="x", padx=16, pady=8)
        self.trail.insert(0, "0EcCG6kbcdAB2CPqrsD")
        self.trail.bind("<KeyRelease>", lambda e: self.draw())
        btns = tk.Frame(self, bg="#1a1c20")
        btns.pack(anchor="w", padx=16)
        tk.Button(btns, text="Open source zip", command=self.open_zip).pack(side="left")
        self.status = tk.Label(self, text="", fg="#c4a574", bg="#1a1c20")
        self.status.pack(anchor="w", padx=16, pady=6)
        self.canvas = tk.Canvas(self, bg="#15161a", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True, padx=16, pady=8)
        self.drop_target_register("DND_Files") if False else None
        self.draw()
        self.bind("<Control-o>", lambda e: self.open_zip())

    def open_zip(self):
        p = filedialog.askopenfilename(filetypes=[("Zip", "*.zip"), ("All", "*")])
        if not p:
            return
        try:
            self.zip_files = zip_names(p)
            self.status.config(text="zip: %s  (%d files)" % (os.path.basename(p), len(self.zip_files)))
        except Exception as e:
            messagebox.showerror("VHP", str(e))
        self.draw()

    def last_letter(self):
        s = "".join(c for c in self.trail.get() if c.isalnum())
        return s[-1] if s else ""

    def draw(self):
        self.canvas.delete("all")
        L = self.last_letter()
        blocks = self.map.get("blocks", [])
        w, h, pad = 200, 120, 12
        hit = None
        for i, b in enumerate(blocks):
            x = pad + (i % 4) * (w + pad)
            y = pad + (i // 4) * (h + pad)
            letters = b.get("letters") or ""
            is_hit = bool(L) and L in letters
            if is_hit:
                hit = b
            fill = "#3a1c1c" if is_hit else "#222"
            outline = "#e74c3c" if is_hit else "#444"
            self.canvas.create_rectangle(x, y, x + w, y + h, fill=fill, outline=outline, width=2)
            self.canvas.create_text(x + 10, y + 12, anchor="nw", fill="#eee", text=b.get("title", ""))
            self.canvas.create_text(x + 10, y + 34, anchor="nw", fill="#aaddff", text=b.get("hw", ""))
            shown = []
            for fn in b.get("files") or []:
                if not self.zip_files or any(fn.lower() in z.lower() for z in self.zip_files):
                    shown.append(fn)
            self.canvas.create_text(x + 10, y + 58, anchor="nw", fill="#888",
                                    text="\n".join(shown[:3]), width=w - 16)
        if L:
            msg = "last letter '%s' → %s" % (L, hit["title"] if hit else "unmapped")
        else:
            msg = "paste serial"
        if self.zip_files:
            msg += "  |  source files detected"
        self.status.config(text=msg)

def main():
    app = VHP()
    if len(sys.argv) > 1 and sys.argv[1].endswith(".zip"):
        app.zip_files = zip_names(sys.argv[1])
        app.draw()
    app.mainloop()

if __name__ == "__main__":
    main()
