import pycountry
import xlrd
from geopy import geocoders
from geopy.extra.rate_limiter import RateLimiter
from geopy.geocoders import Nominatim

class GeoServices:

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
        countries = []
        if not headers:
            init = 0
        for i in range(init, documento.nrows):
            if documento.row(i)[nro_country_col].value not in countries:
                countries.append(documento.row(i)[nro_country_col].value)
        return countries

    def get_coords_from(self, name):
        """
        return a dictionary with name, lattitud and longitude.
        params, name of city or country
        """
        geolocator = Nominatim(user_agent="spanish")
        geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)
        location = geocode(name)
        return {'name': name, 'lat': location.latitude, 'long': location.longitude}
