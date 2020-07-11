def colored(seq):
    colors = {
        "A": "\033[92m",
        "C": "\033[94m",
        "G": "\033[93m",
        "T": "\033[91m",
        "U": "\033[91m",
        "reset": "\033[0;0m",
    }
    tmp_str = ""
    for nuc in seq:
        if nuc in colors:
            tmp_str += colors[nuc] + nuc
        else:
            tmp_str += colors["reset"] + nuc
    return tmp_str + "\033[0;0m"


def read_file(path):
    with open(path, "r") as file:
        return [line.strip() for line in file.readlines()]


def write_file(path, seq, mode="w"):
    """w graba una sola linea / a append al contenido existente en el archivo"""
    with open(path, mode) as file:
        file.write(seq + "\n")


def convert_fasta_in_dic(path):
    FASTA_File = read_file(path)
    FASTA_Dic = {}
    FASTA_Label = ""
    for line in FASTA_File:
        if ">" in line:
            FASTA_Label = line
            FASTA_Dic[FASTA_Label] = ""
        else:
            if FASTA_Label != "":
                FASTA_Dic[FASTA_Label] += line
    return FASTA_Dic
