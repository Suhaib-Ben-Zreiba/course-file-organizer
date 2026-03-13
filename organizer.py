import os
import re
import shutil
from collections import defaultdict

SOURCE_FOLDER = "sample_files"

FILE_CATEGORIES = {
    "pdf": "PDFs",
    "doc": "Documents",
    "docx": "Documents",
    "txt": "TextFiles",
    "c": "Code",
    "cpp": "Code",
    "py": "Code",
    "java": "Code",
    "jpg": "Images",
    "jpeg": "Images",
    "png": "Images",
}

NOISE_WORDS = {
    "final", "copy", "draft", "new", "latest", "version", "v1", "v2", "v3"
}

def get_category(extension: str) -> str:
    return FILE_CATEGORIES.get(extension.lower(), "Other")

def split_words(name: str):
    # Remove bracketed markers like (1), [2]
    name = re.sub(r"[\(\[\{]\d+[\)\]\}]", "", name)

    # Replace separators with spaces
    name = re.sub(r"[_\-]+", " ", name)

    # Separate letters and digits: lecture1 -> lecture 1
    name = re.sub(r"([a-zA-Z])(\d)", r"\1 \2", name)
    name = re.sub(r"(\d)([a-zA-Z])", r"\1 \2", name)

    words = name.lower().split()
    cleaned = [w for w in words if w not in NOISE_WORDS]
    return cleaned

def normalize_base_name(filename: str) -> str:
    base, ext = os.path.splitext(filename)
    words = split_words(base)

    if not words:
        return "file"

    # Preserve meaningful numbers
    result = "_".join(words)

    # Remove repeated adjacent tokens: notes_notes -> notes
    parts = result.split("_")
    deduped = []
    for part in parts:
        if not deduped or deduped[-1] != part:
            deduped.append(part)

    result = "_".join(deduped)

    return result

def safe_name(destination_folder: str, filename: str) -> str:
    base, ext = os.path.splitext(filename)
    candidate = filename
    copy_count = 1

    while os.path.exists(os.path.join(destination_folder, candidate)):
        if copy_count == 1:
            candidate = f"{base}_copy{ext}"
        else:
            candidate = f"{base}_copy{copy_count}{ext}"
        copy_count += 1

    return candidate

def organize_files(folder: str) -> None:
    if not os.path.isdir(folder):
        print(f"Folder '{folder}' does not exist.")
        return

    files = sorted(os.listdir(folder))

    moved_count = 0
    renamed_count = 0
    skipped_count = 0
    duplicate_count = 0

    for filename in files:
        old_path = os.path.join(folder, filename)

        if not os.path.isfile(old_path):
            skipped_count += 1
            continue

        base, ext = os.path.splitext(filename)
        ext_clean = ext[1:].lower() if ext else ""
        category = get_category(ext_clean)
        destination_folder = os.path.join(folder, category)
        os.makedirs(destination_folder, exist_ok=True)

        normalized_base = normalize_base_name(filename)
        new_name = f"{normalized_base}{ext.lower()}"

        final_name = safe_name(destination_folder, new_name)
        if final_name != new_name:
            duplicate_count += 1

        if final_name != filename:
            renamed_count += 1

        new_path = os.path.join(destination_folder, final_name)
        shutil.move(old_path, new_path)
        moved_count += 1

        print(f"Moved: {filename} -> {category}/{final_name}")

    print("\nSummary")
    print("--------------------")
    print(f"Renamed:            {renamed_count}")
    print(f"Moved:              {moved_count}")
    print(f"Skipped:            {skipped_count}")
    print(f"Duplicates handled: {duplicate_count}")

if __name__ == "__main__":
    organize_files(SOURCE_FOLDER)
