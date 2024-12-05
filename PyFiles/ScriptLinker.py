import os
from Levenshtein import ratio

def find_and_rename_files_gui(directory, similarity_threshold=0.8):
    files = os.listdir(directory)
    mp4_files = [f for f in files if f.endswith('.mp4')]
    funscript_files = [f for f in files if f.endswith('.funscript')]

    if not mp4_files or not funscript_files:
        return "Brakuje plików .mp4 lub .funscript w katalogu."

    sorted_folder = os.path.join(directory, "Sorted")
    os.makedirs(sorted_folder, exist_ok=True)

    results = []
    manual_matches = []  # Lista plików wymagających ręcznego dopasowania

    for mp4_file in mp4_files:
        mp4_name = os.path.splitext(mp4_file)[0]
        best_match = None
        best_score = 0

        for funscript_file in funscript_files:
            funscript_name = os.path.splitext(funscript_file)[0]
            similarity = ratio(mp4_name, funscript_name)

            if similarity > best_score:
                best_match = funscript_file
                best_score = similarity

        if best_score == 1.00:
            old_mp4_path = os.path.join(directory, mp4_file)
            old_funscript_path = os.path.join(directory, best_match)

            new_mp4_path = os.path.join(sorted_folder, mp4_file)
            new_funscript_path = os.path.join(sorted_folder, best_match)

            os.rename(old_mp4_path, new_mp4_path)
            os.rename(old_funscript_path, new_funscript_path)
            results.append(f"Przeniesiono: {mp4_file} i {best_match}.")
        elif best_score >= similarity_threshold:
            new_mp4_name = os.path.splitext(best_match)[0] + '.mp4'
            old_path = os.path.join(directory, mp4_file)
            new_path = os.path.join(directory, new_mp4_name)
            os.rename(old_path, new_path)
            results.append(f"Zmieniono nazwę: {mp4_file} na {new_mp4_name} (podobieństwo: {best_score:.2f}).")
        else:
            # Dodaj do listy plików wymagających ręcznego dopasowania
            manual_matches.append((mp4_file, best_match, best_score))

    return results, manual_matches
