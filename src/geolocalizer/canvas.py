from pathlib import Path
from Bio import Phylo
import folium


class Canvas:
    def __init__(self, parsed_seqs, treefile_path, logger):
        self.parsed_seqs = self.__arrange_seqs(parsed_seqs)
        self.treefile_path = str(Path(treefile_path).absolute())
        self.__logger = logger
        self.__module = "Canvas"

    def create_map(self):
        fmap = folium.Map(tiles="cartodbpositron", zoom_start=1)
        tree = Phylo.read(self.treefile_path, "newick")
        root = tree.root

        self.__logger.log(self.__module, Phylo.draw_ascii(tree))

        if not tree.rooted:
            new_root = root.get_terminals()[0]
            new_clades = list(filter(lambda c: c.name != new_root.name, root.clades))
            new_root.clades = new_clades
            root = new_root

        self.__visit_tree_and_add(root.name, root, fmap)

        return fmap

    def create_map_and_save_to(self, to):
        map = self.create_map()
        map.save(to)
        self.__logger.log(self.__module, f"Map saved to {to}")
        return to

    def __visit_tree_and_add(self, terminal_parent, clade, fmap):
        if clade.name and clade.name in self.parsed_seqs:
            seq = self.parsed_seqs[clade.name]

            if "latitude" in seq and "longitude" in seq:
                folium.Marker(
                    [seq["latitude"], seq["longitude"]],
                    popup=seq["description"],
                    tooltip=seq["genbank_accession"],
                ).add_to(fmap)
            else:
                self.__logger.log(self.__module, f'Coordinates missing for {seq["description"]}.')

        if clade.is_terminal():
            if terminal_parent in self.parsed_seqs and clade.name in self.parsed_seqs:
                start_seq = self.parsed_seqs[terminal_parent]
                end_seq = self.parsed_seqs[clade.name]

                valid_start = "latitude" in start_seq and "longitude" in start_seq
                valid_end = "latitude" in end_seq and "longitude" in end_seq

                if valid_start and valid_end:
                    self.__add_line(start_seq, end_seq, fmap)
                    self.__add_arrow_head(start_seq, end_seq, fmap)
        else:
            left_tree = clade.clades[0]
            right_tree = clade.clades[1]

            if left_tree.is_terminal() and right_tree.is_terminal():
                self.__visit_tree_and_add(terminal_parent, left_tree, fmap)
                self.__visit_tree_and_add(terminal_parent, right_tree, fmap)
            elif left_tree.is_terminal():
                self.__visit_tree_and_add(terminal_parent, left_tree, fmap)
                self.__visit_tree_and_add(left_tree.name, right_tree, fmap)
            else:
                self.__visit_tree_and_add(terminal_parent, right_tree, fmap)
                self.__visit_tree_and_add(right_tree.name, left_tree, fmap)

    def __add_line(self, start_seq, end_seq, fmap):
        start_coord = (start_seq["latitude"], start_seq["longitude"])
        end_coord = (end_seq["latitude"], end_seq["longitude"])

        folium.PolyLine(
            locations=[start_coord, end_coord], weight=2, color="blue"
        ).add_to(fmap)

    def __add_arrow_head(self, start_seq, end_seq, fmap):
        start_coord = (start_seq["latitude"], start_seq["longitude"])
        end_coord = (end_seq["latitude"], end_seq["longitude"])

        return folium.RegularPolygonMarker(
            location=end_coord,
            fill_color="blue",
            number_of_sides=2,
            radius=6,
            rotation=90,
        ).add_to(fmap)

    def __arrange_seqs(self, seqs):
        return_dict = {}
        for seq in seqs:
            return_dict[seq["iqtree_label"]] = seq

        return return_dict
