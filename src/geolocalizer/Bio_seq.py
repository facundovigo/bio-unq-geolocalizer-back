from Bio_structs import Nucleotide_base, DNA_Codons, RNA_Codons
from collections import Counter
import random


class BioSeq:
    """DNA sequence Class. Default value: ATCG, DNA, No label"""

    def __init__(self, seq="ATCG", label="No label", seq_type="DNA"):
        self.seq = seq.upper()
        self.label = label
        self.seq_type = seq_type
        self.is_valid = self.__validate()
        assert (
            self.is_valid
        ), f"Provider data does not seem to be a correct sequence: {self.seq}"

    def __validate(self):
        if len(self.seq) != 0:
            return set(Nucleotide_base[self.seq_type]).issuperset(self.seq)
        return False

    def show_info(self):
        return f"[Label]: {self.label}\n[Sequence]: {self.seq}\n[Biotype]: {self.seq_type}\n[Length]: {len(self.seq)}"

    def generate_random_sequence(self, length=10, seq_type="DNA"):
        """Generate a random sequence, provided the length and type"""
        seq = "".join([random.choice(Nucleotide_base[seq_type]) for x in range(length)])
        self.__init__(seq, seq_type, "Randomly Generated sequence")

    def count_nuc_frecuency(self):
        """Return a dictionary, count the nucleotides occurrence"""
        return dict(Counter(self.seq))

    def transcription(self):
        """Return a string, this is a trascription of seq"""
        if self.seq_type == "DNA":
            return self.seq.replace("T", "U")
        return "Not a DNA sequence"

    def reverse_complement(self):
        """
        Return a string.
        Swap adenine with thymine and guanine with cytosine
        """
        if self.seq_type == "DNA":
            mapping = str.maketrans("ATCG", "TAGC")
        else:
            mapping = str.maketrans("AUCG", "UAGC")
        return self.seq.translate(mapping)[::-1]

    def gc_content_in(self):
        """Return the percent of occurrence of G & C in the seq"""
        return round(self.seq.count("C") + self.seq.count("G") / len(self.seq) * 100)

    def gc_content_in_subsection(self, k=20):
        """
        Return a list of percent of occurrence of G&C.
        The length of each block is determined by k.
        """
        res = []
        for i in range(0, len(self.seq) - k + 1, k):
            subseq = self.seq[i : i + k]
            res.append(round(subseq.count("C") + subseq.count("G") / len(subseq) * 100))
        return res

    def translate_seq(self, init_pos=0):
        """Translate a DNA seq in an aminoacid seq"""
        if self.seq_type == "DNA":
            return [
                DNA_Codons[self.seq[pos : pos + 3]]
                for pos in range(init_pos, len(self.seq) - 2, 3)
            ]
        else:
            return [
                RNA_Codons[self.seq[pos : pos + 3]]
                for pos in range(init_pos, len(self.seq) - 2, 3)
            ]

    def codon_usage(self, aminoacid):
        """Return the frecuency of each codon encoding a given aminoacid in DNA/RNA seq"""
        ret_list = []
        if self.seq_type == "DNA":
            for i in range(0, len(self.seq) - 2, 3):
                if DNA_Codons[self.seq[i : i + 3]] == aminoacid:
                    ret_list.append(self.seq[i : i + 3])
        elif self.seq_type == "RNA":
            for i in range(0, len(self.seq) - 2, 3):
                if RNA_Codons[self.seq[i : i + 3]] == aminoacid:
                    ret_list.append(self.seq[i : i + 3])
        frecuency_dic = dict(Counter(ret_list))
        totalWigth = sum(frecuency_dic.values())
        for seq in frecuency_dic:
            frecuency_dic[seq] = round(frecuency_dic[seq] / totalWigth, 2)
        return frecuency_dic

    def generate_reading_frames(self):
        """Generate de six reading frames a of a DNA/RNA seq, including reverse complement"""
        frames = []
        frames.append(self.translate_seq(0))
        frames.append(self.translate_seq(1))
        frames.append(self.translate_seq(2))
        temp_seq = Bio_seq(self.reverse_complement(), self.seq_type)
        frames.append(temp_seq.translate_seq(0))
        frames.append(temp_seq.translate_seq(1))
        frames.append(temp_seq.translate_seq(2))
        del temp_seq
        # le dice al garbage collector q lo elimine de mem
        return frames

    def proteins_from_frame(self, amin_seq):
        """
        Compute all possible proteins in an aminoacid seq.
        Return a list of these
        """
        current_prots = []
        proteins = []
        for aa in amin_seq:
            if aa == "_":
                """STOP accumulating amin if '_' was found"""
                if current_prots:
                    for p in current_prots:
                        proteins.append(p)
                    current_prots = []
            else:
                """START accumulating amin if 'M' was found"""
                if aa == "M":
                    current_prots.append("")
                for i in range(len(current_prots)):
                    current_prots[i] += aa
        return proteins

    def all_proteins_from_orfs(self, init_read_pos=0, end_read_pos=0, orderer=False):
        # Compute all possible proteins for all open reading frames.
        if end_read_pos > init_read_pos:
            tmp_seq = Bio_seq(self.seq[init_read_pos:end_read_pos], self.seq_type)
            frames = tmp_seq.generate_reading_frames()
        else:
            frames = self.generate_reading_frames()
        del tmp_seq
        res = []
        for frame in frames:
            proteins = self.proteins_from_frame(frame)
            for protein in proteins:
                res.append(protein)
        if orderer:
            return sorted(res, key=len, reverse=True)
        return res
