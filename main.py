import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import polib
import time
from progress.bar import Bar
from mtranslate import translate
from threading import Thread

def translate_entry(entry, target_language):
    """Translates the text of an entry and updates the translated message."""
    translated_text = translate(entry.msgid, target_language)
    entry.msgstr = translated_text

def translate_po_file(input_path, output_path, target_language, progress_callback):
    """
    Translates a .po file to the specified language and saves the result to a new file.

    :param input_path: Path to the input .po file.
    :param output_path: Path to the output .po file.
    :param target_language: Language code to translate to.
    :param progress_callback: Callback function to update the progress.
    """
    # Load the .po file
    po_file = polib.pofile(input_path)

    # Set up the progress bar
    total_entries = len(po_file)
    progress_bar = Bar('Translating', max=total_entries)

    # Start the timer
    start_time = time.time()

    # Translate each entry
    for i, entry in enumerate(po_file):
        translate_entry(entry, target_language)
        progress_bar.next()
        elapsed_time = time.time() - start_time
        estimated_total_time = (elapsed_time / (i + 1)) * total_entries
        remaining_time = estimated_total_time - elapsed_time
        words_per_minute = (i + 1) / (elapsed_time / 60)
        progress_callback(i + 1, total_entries, remaining_time, words_per_minute)

    # Finish the progress bar and save the file
    progress_bar.finish()
    po_file.save(output_path)
    messagebox.showinfo('Success', 'Translation completed successfully!')

def start_translation():
    input_file = filedialog.askopenfilename(filetypes=[('PO files', '*.po')])
    if not input_file:
        return
    
    # Get the target language from user input
    target_language = simpledialog.askstring("Input", "Enter the target language code (e.g., 'fr' for French):")
    if not target_language:
        return
    
    # Format the target language code for the filename
    formatted_language = f"{target_language.upper()}_{target_language.upper()}"

    # Generate the output file path
    output_file = filedialog.asksaveasfilename(
        defaultextension=".po",
        filetypes=[('PO files', '*.po')],
        initialfile=f"translated_{formatted_language}.po"
    )
    if not output_file:
        return

    def update_progress(current, total, remaining, words_per_minute):
        progress_var.set(f'Translated {current}/{total} entries\nEstimated time left: {remaining:.2f} seconds\nWords per minute: {words_per_minute:.2f}')
        root.update_idletasks()

    progress_var.set('Starting translation...')
    thread = Thread(target=translate_po_file, args=(input_file, output_file, target_language, update_progress))
    thread.start()

# Create the GUI
root = tk.Tk()
root.title('PO File Translator')

frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

translate_button = tk.Button(frame, text='Translate PO File', command=start_translation)
translate_button.pack()

progress_var = tk.StringVar()
progress_label = tk.Label(frame, textvariable=progress_var)
progress_label.pack(pady=10)

root.mainloop()
