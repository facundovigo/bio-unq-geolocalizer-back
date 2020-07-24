from pathlib import Path
from src.geolocalizer.bio_structs import gen_type
import re
from datetime import datetime
import ntpath


class InvalidFileError(Exception):
    def __init__(self, message):
        super().__init__(message)


class TooFewSequencesError(Exception):
    def __init__(self, message):
        super().__init__(message)


class Parser:
    def __init__(self, logger):
        self.__logger = logger
        self.__module = "Parser"

    def parse(self, sequence_path, write_output=False):
        full_path = str(Path(sequence_path).absolute())
        if not (full_path.endswith(".fasta") or full_path.endswith(".fst")):
            err_msg = "The file is not a fasta"
            logger.err(self.__module, err_msg)
            raise InvalidFileError(err_msg)

        raw_fasta_dic = self.__read_fasta(full_path)
        parsed_geo_seqs = {"DNA": [], "RNA": [], "AMINO": []}

        for header, raw_seq in raw_fasta_dic.items():
            detected_type = gen_type(raw_seq)
            try: 
                parsed_geo_seqs[detected_type].append(self.__build_geo_seq(header, raw_seq))
            except:
                self.__logger.warn(
                    self.__module,
                    f'Failed to geolocalize {header}. The seq informaction cannot determine type',
                )
                exit(2)


        biggest_group = max(list(parsed_geo_seqs.values()), key=len)
        biggest_group_size = len(biggest_group)

        if biggest_group_size < 5:
            err_msg = "You need to include more that 5 sequences of the same type."
            self.__logger.err(self.__module, err_msg)
            exit(2)
        if biggest_group_size < 60:
            self.__logger.warn(
                self.__module,
                "Consider providing at least 60 different sequences for optimal results.",
            )

        output_path = ""
        if write_output:
            output_path = self.__write_validated_fasta(sequence_path, biggest_group)

        return {"seqs": biggest_group, "output_path": output_path}

    def __build_geo_seq(self, header, raw_seq):
        if raw_seq != "":
            geo_seq = {"description": header, "seq": raw_seq}
            geo_seq["iqtree_label"] = re.search(r"([^\s]+)", header).group(0)

            genbank_regexp = r"(?=gi\|(.*?)\|\w{2,3}\|(.*?).\d?\|)"

            genbank = re.search(genbank_regexp, header)
            if genbank:
                geo_seq["genbank_gen_info"] = genbank.group(1)
                geo_seq["genbank_accession"] = genbank.group(2)
            else:
                simple_genbank_regexp = r"(?:^)(\w+).\d"
                simple_genbank = re.search(simple_genbank_regexp, header)
                if simple_genbank:
                    geo_seq["genbank_accession"] = simple_genbank.group(1)

            return geo_seq
        else:
            self.__logger.warn(
                    self.__module,
                    f'Failed to geolocalize {header}. Header have not seq information.',
                )
            exit(2)

    def __read_fasta(self, path):
        fasta_dic = {}

        with open(path, "r") as file:
            current_label = ""
            fasta_dic[current_label] = ""
            for line in file:
                if line.startswith(">"):
                    current_label = line[1:].strip()
                    fasta_dic[current_label] = ""
                else:
                    fasta_dic[current_label] += line.strip()
        if fasta_dic[""]!="":
            self.__logger.warn(
                self.__module,
                    f'Failed to geolocalize {fasta_dic[""]} header seq information not present',
                )
        del fasta_dic[""]  

        return fasta_dic

    def __path_leaf(self, path):
        head, tail = ntpath.split(path)
        return tail or ntpath.basename(head)

    def __write_validated_fasta(self, input_name, seqs):
        full_path = str(Path("tmp").absolute())
        Path(full_path).mkdir(parents=True, exist_ok=True)
        output_name = (
            f"tmp/{datetime.timestamp(datetime.now())}_{self.__path_leaf(input_name)}"
        )
        output_name = str(Path(output_name).absolute())

        with open(output_name, "w") as validated_file:
            for seq in seqs:
                validated_file.write(f">{seq['description']}\n")
                validated_file.write(f"{seq['seq']}\n")

        return output_name
