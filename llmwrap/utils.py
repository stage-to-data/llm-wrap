import os
import json

def read_txt(path : str) -> str:
    if os.path.isfile(path):
        if os.path.splitext(path)[1].lower() == ".txt":
            with open(path, 'r') as f:
                return f.read()
        else:
            print(f"{path} is not a text file.")
            return None
    else:
        print(f"{path} doesn't exist.")
        return None
    
def write_json(path : str, content : dict, indent : int = 4) -> None:
    """
    Donner un chemin de destination et du contenu et enregistrer au format json.
    
    Si le dossier n'existe pas, cette fonction créera le dossier de manière récursive.
    """
    if os.path.splitext(path)[1] == ".json":
        check_dir_exists(path)

        with open(path, 'w', encoding='utf-8') as f:
            json.dump(content, f, ensure_ascii = False, indent = indent)
    else:
        print("Erreur ! Il faut donner un fichier avec une extension \"json\" !")

def check_dir_exists(filepath):
    """Check if folder exists, if not, create it."""
    if os.path.isdir(os.path.dirname(filepath)) == False:
        os.makedirs(os.path.dirname(filepath))

def read_json(path : str) -> dict:
    """Read a json file"""
    if os.path.isfile(path):
        if os.path.splitext(path)[1].lower() == ".json":
            with open(path, 'r') as f:
                return json.load(f)
        else:
            print(f"{path} is not a json file.")
            return None
    else:
        print(f"{path} doesn't exist.")
        return None