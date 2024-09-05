# src/main.py
from tkinterdnd2 import TkinterDnD
from ui import CSVLinkGeneratorApp

if __name__ == "__main__":
    root = TkinterDnD.Tk()
    app = CSVLinkGeneratorApp(root)
    root.mainloop()