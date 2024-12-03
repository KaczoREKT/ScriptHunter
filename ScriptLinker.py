import os
import shutil
from Levenshtein import ratio


def unpack_subfolders(directory):
    """
    Przenosi wszystkie pliki z podfolderów do katalogu głównego.
    Usuwa puste podfoldery.
    """
    for root, dirs, files in os.walk(directory, topdown=False):
        for file in files:
            file_path = os.path.join(root, file)
            new_path = os.path.join(directory, file)
            if not os.path.exists(new_path):  # Zapobiega nadpisaniu plików
                try:
                    shutil.move(file_path, new_path)
                    print(f"Przeniesiono {file_path}")
                except PermissionError:
                    print(f"Zostawiono plik {file_path}. Widocznie jest w użyciu.")
            else:
                print(f"Plik '{file}' już istnieje w katalogu głównym. Pomijanie.")
        for dir in dirs:
            dir_path = os.path.join(root, dir)
            if not os.listdir(dir_path):  # Usuwanie pustych folderów
                os.rmdir(dir_path)
    print("Wszystkie pliki z podfolderów zostały przeniesione do katalogu głównego.")


def find_and_rename_files(directory, similarity_threshold=0.8):
    # Pobierz listę plików w katalogu
    files = os.listdir(directory)

    # Podziel pliki według rozszerzeń
    mp4_files = [f for f in files if f.endswith('.mp4')]
    funscript_files = [f for f in files if f.endswith('.funscript')]

    if not mp4_files or not funscript_files:
        print("Brakuje plików .mp4 lub .funscript w katalogu.")
        return

    # Tworzymy folder 'Sorted', jeśli nie istnieje
    sorted_folder = os.path.join(directory, "Sorted")
    os.makedirs(sorted_folder, exist_ok=True)

    for mp4_file in mp4_files:
        mp4_name = os.path.splitext(mp4_file)[0]

        # Porównujemy nazwę pliku .mp4 z każdym plikiem .funscript
        best_match = None
        best_score = 0

        for funscript_file in funscript_files:
            funscript_name = os.path.splitext(funscript_file)[0]
            similarity = ratio(mp4_name, funscript_name)  # Oblicz podobieństwo

            if similarity > best_score:
                best_match = funscript_file
                best_score = similarity

        # Jeśli podobieństwo wynosi 1.00, przenieś oba pliki do 'Sorted'
        if best_score == 1.00:
            old_mp4_path = os.path.join(directory, mp4_file)
            old_funscript_path = os.path.join(directory, best_match)

            new_mp4_path = os.path.join(sorted_folder, mp4_file)
            new_funscript_path = os.path.join(sorted_folder, best_match)

            os.rename(old_mp4_path, new_mp4_path)
            os.rename(old_funscript_path, new_funscript_path)
            print(f"Przeniesiono z {old_funscript_path} do {new_funscript_path}.")

            print(f"Pliki '{mp4_file}' i '{best_match}' zostały przeniesione do folderu 'Sorted'.")
        elif best_score >= similarity_threshold:
            # Automatyczna zmiana nazwy, jeśli podobieństwo przekracza próg
            new_mp4_name = os.path.splitext(best_match)[0] + '.mp4'
            old_path = os.path.join(directory, mp4_file)
            new_path = os.path.join(directory, new_mp4_name)
            os.rename(old_path, new_path)
            print(f"Plik '{mp4_file}' został przemianowany na '{new_mp4_name}' (podobieństwo: {best_score:.2f}).")
        else:
            # Niskie podobieństwo – zapytaj użytkownika
            print(f"Plik '{mp4_file}' nie został dopasowany (najlepsze podobieństwo: {best_score:.2f}).")
            decision = input(
                f"Czy chcesz ręcznie dopasować plik '{mp4_file}' do '{best_match}'? (tak/nie): ").strip().lower()
            if decision == 'tak':
                new_mp4_name = os.path.splitext(best_match)[0] + '.mp4'
                old_path = os.path.join(directory, mp4_file)
                new_path = os.path.join(directory, new_mp4_name)
                os.rename(old_path, new_path)
                print(f"Plik '{mp4_file}' został ręcznie przemianowany na '{new_mp4_name}'.")


# Użycie funkcji
katalog = input("Podaj ścieżkę do katalogu z plikami: ")
#unpack_subfolders(katalog)  # Wypakuj pliki z podfolderów
find_and_rename_files(katalog)
