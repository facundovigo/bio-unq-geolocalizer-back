from utilities import *
from bio_seq import *
from bio_structs import *


class GeoTreeConvert:
    def __init__(self):
        self.seqs = []
        self.error_seq = []

    def validate_input_data(self, path):
        """"
        Clean empty headers and sequences without headers.
        Identify sequence types and return a dictionary with the valid data and the errors found.
        """
        fasta_dic = convert_fasta_in_dic(path)
        for key in fasta_dic.keys():
            try:
                self.seqs.append(Bio_seq(fasta_dic[key], key, gen_type(fasta_dic[key])))
            except:
                self.error_seq.append(key)
        return {"seq": self.seqs, "error_seq": self.error_seq}

    def get_highest_seq(self):
        count = {"ADN": 0, "ARN": 0, "AMINO": 0}
        for seq in self.seqs:
            if seq.seq_type == "DNA":
                count["ADN"] += 1
            if seq.seq_type == "RNA":
                count["ARN"] += 1
            if seq.seq_type == "AMINO":
                count["AMINO"] += 1

        return max(count, key=count.get)
