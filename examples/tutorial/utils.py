import os

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
    
def collect_files(path, acceptedFormats = [], recursive = True):
    """Collect all files of accepted format in a given directory."""
    
    acceptedFormatsLower = {ext.lower() for ext in acceptedFormats}
    finalList = []
    
    if recursive:
        for root, _, files in os.walk(path):
            for file in files:
                if not acceptedFormats or os.path.splitext(file)[1][1:].lower() in acceptedFormatsLower:
                    finalList.append(os.path.join(root, file))
    else:
        for file in os.listdir(path):
            full_path = os.path.join(path, file)
            if os.path.isfile(full_path):
                if not acceptedFormats or os.path.splitext(file)[1][1:].lower() in acceptedFormatsLower:
                    finalList.append(full_path)
    
    return finalList