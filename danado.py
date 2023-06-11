import polib
import time
from progress.bar import Bar
from mtranslate import translate

def translate_entry(entry, dest_language):
    translation = translate(entry.msgid, dest_language)
    entry.msgstr = translation

def translate_po_file(input_file, output_file, dest_language='fr'):
    # Charger le fichier .po
    po = polib.pofile(input_file)

    # Configurer la barre de progression
    bar = Bar('Traduction de Saint-Translatius', max=len(po))

    # Démarrer le compteur de temps
    start_time = time.time()

    # Traduire chaque entrée
    for entry in po:
        translate_entry(entry, dest_language)
        bar.next()

    # Mettre à jour le temps écoulé et terminer la barre de progression
    elapsed_time = time.time() - start_time
    bar.finish()

    # Enregistrer le fichier traduit
    po.save(output_file)

    # Afficher les statistiques
    print(f'Traduction terminée en {elapsed_time:.2f} secondes.')

# Exemple d'utilisation
input_file = 'input.po'
output_file = 'output.po'
translate_po_file(input_file, output_file)
