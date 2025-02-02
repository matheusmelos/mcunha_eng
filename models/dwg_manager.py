# Classe inicial DWG, salva apenas o nome e arquivo.
class DWG:
    def __init__(self, dwg_file, dwg_name):
        
        self.dwg_file = dwg_file
        self.dwg_name = dwg_name
        self.material = ' '