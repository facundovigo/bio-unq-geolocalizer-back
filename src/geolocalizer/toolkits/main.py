from Bio_seq import Bio_seq
from utilities import *
from Bio_structs import *
from GeoTreeConvert import *


geo = GeoTreeConvert()

dic = geo.validate_input_data('seqs_validaciones.fasta')
seq_type = geo.get_highest_seq()

print(seq_type)

fasta_dic = convert_fasta_in_dic('seqs_validaciones.fasta')
array_seq = []
error_seq = []
for key in fasta_dic.keys():
    try:
        array_seq.append(Bio_seq(fasta_dic[key], key, gen_type(fasta_dic[key])))
    except:
        error_seq.append(key)

    count = {
        'ADN': 0,
        'ARN': 0,
        'AMINO': 0
    }
for seq in array_seq:
    if seq.seq_type == 'DNA':
        count['ADN'] += 1
    if seq.seq_type == 'RNA':
        count['ARN'] += 1
    if seq.seq_type == 'AMINO':
        count['AMINO'] += 1

max_type_encontrados = max(count, key=count.get)

##array_para_alinear = array_seq.filter(seq.type == max_type_encontrados)


print('err', error_seq)
for seq in array_seq:
    print(seq.show_info())

#print(error_seq, "err")


#dic_to_array_bio_seq(fasta_dic)


# DONE validar si son acidos nucleicos o no
# tomar el primero y  y validar en base a eso
# DONE que no queden seq sin headers
# DONE ni headers sin seq
# cantidad de seq tiene ser considerable

