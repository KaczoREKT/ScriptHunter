import os
import tkinter as tk
from tkinter import filedialog, messagebox
import NudeFinder
import ScriptLinker

def search_files_gui():
    file_prefix = entry_search.get()
    if not file_prefix:
        messagebox.showwarning("Brak danych", "Podaj nazwę pliku!")
        return

    results = NudeFinder.search_file(file_prefix)
    if results:
        result_text.set("\n".join(results))
    else:
        result_text.set("Nie znaleziono pliku o podanej nazwie.")

def handle_manual_match(mp4_file, best_match, directory):
    new_name = best_match.replace('.funscript', '.mp4')
    old_path = os.path.join(directory, mp4_file)
    new_path = os.path.join(directory, new_name)
    os.rename(old_path, new_path)
    messagebox.showinfo("Ręczne dopasowanie", f"Plik '{mp4_file}' został dopasowany do '{new_name}'.")

def run_scriptlinker():
    directory = "/media/kaczorekt/NIE USUWAJ/Homework"
    if not directory:
        return

    similarity_threshold = 0.8
    results, manual_matches = ScriptLinker.find_and_rename_files_gui(directory, similarity_threshold)

    if results:
        messagebox.showinfo("Wyniki", "\n".join(results))
    if manual_matches:
        for mp4_file, best_match, score in manual_matches:
            ask_user_manual_match(mp4_file, best_match, directory, score)

def ask_user_manual_match(mp4_file, best_match, directory, score):
    top = tk.Toplevel(root)
    top.title("Ręczne dopasowanie")

    tk.Label(top, text=f"Plik: {mp4_file}").pack(pady=5)
    tk.Label(top, text=f"Najlepsze dopasowanie: {best_match} (podobieństwo: {score:.2f})").pack(pady=5)

    frame_buttons = tk.Frame(top)
    frame_buttons.pack(pady=10)

    def accept_match():
        handle_manual_match(mp4_file, best_match, directory)
        top.destroy()

    def reject_match():
        messagebox.showinfo("Odrzucono", f"Plik '{mp4_file}' nie został dopasowany.")
        top.destroy()

    tk.Button(frame_buttons, text="Tak", command=accept_match).pack(side=tk.LEFT, padx=10)
    tk.Button(frame_buttons, text="Nie", command=reject_match).pack(side=tk.RIGHT, padx=10)

# GUI
root = tk.Tk()
root.title("Manager Plików")

frame_search = tk.Frame(root, padx=10, pady=10)
frame_search.pack()

tk.Label(frame_search, text="Wyszukiwarka plików:").pack()
entry_search = tk.Entry(frame_search, width=40)
entry_search.bind("<Return>", lambda event: search_files_gui())
entry_search.pack()

search_button = tk.Button(frame_search, text="Szukaj", command=search_files_gui)
search_button.pack(pady=5)

result_text = tk.StringVar()
result_label = tk.Label(frame_search, textvariable=result_text, justify=tk.LEFT, wraplength=400, fg="blue")
result_label.pack(pady=10)

frame_scriptlinker = tk.Frame(root, padx=10, pady=10)
frame_scriptlinker.pack()

link_button = tk.Button(frame_scriptlinker, text="Uruchom Scriptlinker", command=run_scriptlinker)
link_button.pack()

root.mainloop()
