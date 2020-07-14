import xlrd
from geopy import geocoders
from geopy.extra.rate_limiter import RateLimiter
from geopy.geocoders import Nominatim

class GeoServices:

    def get_coords_from(self,name):
        geolocator = Nominatim(user_agent="spanish")
        geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)
        location = geocode(name)
        return {'latitude': location.latitude, 'longitude': location.longitude}



    def get_countries_from_xls(self, input_file, nro_id_col=1, nro_country_col=3, nro_shet=0, headers=True):
        """
        Return a list of countries
        Params:
            input_file: file's path
            nro_id_col: the id_gbank's position column in the table
            nro_country_col: the country's position column in the table
            nro_shet: document's shet number
            headers: if have headers true, else false
        """
        init = 1
        documento = xlrd.open_workbook(input_file).sheet_by_index(nro_shet)
        dictionary = dict()
        if not headers:
            init = 0
        for i in range(init, documento.nrows):
            dictionary[(documento.cell_value(i, nro_id_col)[3:-1])] = (documento.cell_value(i, nro_country_col)) 
        return dictionary
    
    def get_location_for_idseq(self, listseq, dicc):
        result = []
        for seqq in listseq:
            if dicc[seqq['genbank_accession']]:
                result.append({**seqq, **(self.get_coords_from(dicc[seqq['genbank_accession']]))})
        return result      


pepe = [{'genbank_accession': 'HQ864247.1', 'seq': 'ASDASDASDASDASDASDASDASDA'}, {'genbank_accession': 'KC210091', 'seq': 'ASDASDASDASDASDASDASDASDA'}]

geo = GeoServices()
countries =  geo.get_countries_from_xls('files/tabla_accession_numbers_loc.xls')
countries2 = geo.get_location_for_idseq(pepe, countries)
print(countries2)