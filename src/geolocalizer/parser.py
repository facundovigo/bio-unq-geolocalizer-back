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
  def parse(self, sequence_path, write_output=False):
    full_path = str(Path(sequence_path).absolute())
    if not full_path.endswith('.fasta'): raise InvalidFileError('The file is not a fasta')

    raw_fasta_dic = self.__read_fasta(full_path)
    parsed_geo_seqs = { 'DNA': [], 'RNA': [], 'AMINO': [] }

    for header, raw_seq in raw_fasta_dic.items():
      detected_type = gen_type(raw_seq)
      parsed_geo_seqs[detected_type].append(
        self.__build_geo_seq(header, raw_seq)
      )

    biggest_group = max(list(parsed_geo_seqs.values()), key=len)
    biggest_group_size = len(biggest_group)
    
    if (biggest_group_size < 5):
      raise TooFewSequencesError('You need to include more that 5 sequences of the same type.')
    if (biggest_group_size < 60):
      True # warning

    output_path = ''
    if write_output:
      output_path = self.__write_validated_fasta(sequence_path, biggest_group)
    
    return { 'seqs': biggest_group, 'output_path': output_path }

  def __build_geo_seq(self, header, raw_seq):
    geoloc_extract_regexp = r'(?=\\GEOLOCALIZATION=\((.*?)\)\((.*?)\))'
    geoloc_remove_regexp = r'(\\GEOLOCALIZATION=\(.*?\)\(.*?\))'
    genbank_regexp = r'(?:^)(\w+.\d)'

    parsed_description = re.sub(geoloc_remove_regexp, '', header)
    parsed_description = re.sub(genbank_regexp, '', parsed_description).strip()

    geo_seq = { 
      'description': parsed_description, 
      'seq': raw_seq 
    }
    
    lat_and_long = re.search(geoloc_extract_regexp, header)
    if lat_and_long:
      geo_seq['latitude'] = lat_and_long.group(1)
      geo_seq['longitude'] = lat_and_long.group(2)

    genbank = re.search(genbank_regexp, header)
    if genbank:
      geo_seq['genbank_id'] = genbank.group(0)

    return geo_seq

  def __read_fasta(self, path):
    fasta_dic = {}

    with open(path, 'r') as file:
      current_label = ''

      for line in file:
        if line.startswith('>'):
          current_label = line[1:].strip()
          fasta_dic[current_label] = ''
        else:
          fasta_dic[current_label] += line.strip()
    
    return fasta_dic

  def __path_leaf(self, path):
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)

  def __write_validated_fasta(self, input_name, seqs):
    full_path = str(Path('tmp').absolute())
    Path(full_path).mkdir(parents=True, exist_ok=True)
    output_name = f'tmp/{datetime.timestamp(datetime.now())}_{self.__path_leaf(input_name)}'
    output_name = str(Path(output_name).absolute())
    
    with open(output_name, 'w') as validated_file:
      for seq in seqs:
        validated_file.write(f">{seq['description']}\n")
        validated_file.write(f">{seq['seq']}\n")

    return output_name
