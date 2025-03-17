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