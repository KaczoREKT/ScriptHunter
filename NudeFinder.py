import os
import tkinter as tk
from tkinter import messagebox

def check_file():
    # Pobierz wpisaną nazwę pliku
    file_prefix = entry.get()
    if not file_prefix:
        messagebox.showwarning("Brak danych", "Podaj nazwę pliku!")
        return

    # Ścieżki do przeszukania
    paths = [
        "F:/MaxxerPlaylist/To Sort",
        "D:/Homework",
        "E:/Homework"
    ]

    # Przeszukiwanie plików (uwzględniając podfoldery)
    found_files = []
    for path in paths:
        for root_dir, _, files in os.walk(path):  # os.walk iteruje przez katalogi i pliki
            for file in files:
                if file.lower().startswith(file_prefix.lower()):  # Sprawdź prefiks nazwy
                    found_files.append(os.path.join(root_dir, file))  # Zapisz pełną ścieżkę

    # Wyświetlenie wyników
    if found_files:
        result_text.set("\n".join(found_files))
    else:
        result_text.set("Nie znaleziono pliku o podanej nazwie.")

def clear_results():
    entry.delete(0, tk.END)
    result_text.set("")

# Tworzenie głównego okna aplikacji
root = tk.Tk()
root.title("Wyszukiwarka plików")

# Interfejs użytkownika
frame = tk.Frame(root, padx=10, pady=10)
frame.pack()

label = tk.Label(frame, text="Podaj początek nazwy pliku:")
label.pack()

entry = tk.Entry(frame, width=40)
entry.pack()

search_button = tk.Button(frame, text="Szukaj", command=check_file)
search_button.pack(pady=5)

clear_button = tk.Button(frame, text="Wyczyść", command=clear_results)
clear_button.pack()

result_text = tk.StringVar()
result_label = tk.Label(frame, textvariable=result_text, justify=tk.LEFT, wraplength=400, fg="blue")
result_label.pack(pady=10)

# Uruchomienie aplikacji
root.mainloop()
