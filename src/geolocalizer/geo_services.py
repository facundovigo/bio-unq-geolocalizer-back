from geopy import geocoders
from geopy.extra.rate_limiter import RateLimiter
from geopy.geocoders import Nominatim
from Bio import Entrez


class GeoServices:
    def __init__(self, entrez_email, logger):
        Entrez.email = entrez_email
        self.__logger = logger
        self.__module = "GeoServices"

    def geolocalize_seqs(self, seqs):
        self.__logger.log(self.__module, "Geolocalizing sequences...")

        accessions = list(map(lambda s: s["genbank_accession"], seqs))
        handle = Entrez.efetch("nucleotide", id=accessions, retmode="xml")
        response = Entrez.read(handle)

        countries = {}

        for entry in response:
            accession = entry["GBSeq_primary-accession"]

            features = entry["GBSeq_feature-table"]
            features = list(filter(lambda f: f["GBFeature_key"] == "source", features))

            for feature in features:
                qualifiers = feature["GBFeature_quals"]
                qualifiers = list(
                    filter(lambda q: q["GBQualifier_name"] == "country", qualifiers)
                )

                country_values = list(map(lambda q: q["GBQualifier_value"], qualifiers))
                if country_values:
                    countries[accession] = " ".join(country_values)

        result = []
        for seq in seqs:
            if "genbank_accession" in seq and seq["genbank_accession"] in countries:
                result.append(
                    {
                        **seq,
                        **(self.__get_coords_from(countries[seq["genbank_accession"]])),
                    }
                )
            else:
                self.__logger.warn(
                    self.__module,
                    f'Failed to geolocalize {seq["description"]}. Country information not present',
                )

        self.__logger.log(self.__module, "Geolocalization finished.")

        return result

    def __get_coords_from(self, name):
        """
        return a dictionary with name, lattitud and longitude.
        params, name of city or country
        """
        geolocator = Nominatim(user_agent="spanish")
        geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)
        location = geocode(name)
        return {
            "name": name,
            "latitude": location.latitude,
            "longitude": location.longitude,
        }
