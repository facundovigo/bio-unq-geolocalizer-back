from src.geolocalizer.parser import Parser
from src.geolocalizer.geo_services import GeoServices
from src.geolocalizer.alignAndTree import AlignAndTree
from src.geolocalizer.canvas import Canvas

if __name__ == "__main__":
    parsed_fasta = Parser().parse(
        "tests/sequences/geolocalized_seqs.fasta", write_output=True
    )
    geo_services = GeoServices()
    countries = geo_services.get_countries_from_xls(
        "src/geolocalizer/files/tabla_accession_numbers_loc.xls"
    )
    geo_seqs = geo_services.get_location_for_idseq(parsed_fasta["seqs"], countries)

    align_and_tree = AlignAndTree()
    output_path = align_and_tree.align_fasta(parsed_fasta["output_path"])
    tree_path = align_and_tree.tree_from_align(output_path)

    Canvas(geo_seqs, tree_path).create_map_and_save_to("tmp/mapa_prueba.html")
