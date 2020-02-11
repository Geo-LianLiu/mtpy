from unittest import TestCase
import numpy as np
import pytest

from mtpy.utils.gis_tools import HAS_GDAL, ll_to_utm, utm_to_ll, project_point_ll2utm, project_point_utm2ll, transform_ll_to_utm, \
    transform_utm_to_ll, project_points_ll2utm


class TestGisTools(TestCase):
    def setUp(self):
        self.nref = 23  # 23, "WGS-84"
        self.lat = -34.299442
        self.lon = 149.201031

        self.zone = '55H'
        self.easting = 702562.773
        self.northing = 6202448.526
        self.atol = 0.3  # tolerance of error
        self.from_epsg = 4326
        self.to_epsg = 28355

    def test_ll_to_utm(self):
        zone, easting, northing = ll_to_utm(self.nref, self.lat, self.lon)

        print((zone, easting, northing))

        self.assertTrue(zone == self.zone)
        self.assertTrue(np.isclose(easting, self.easting, atol=self.atol))
        self.assertTrue(np.isclose(northing, self.northing, atol=self.atol))

    def test_utm_to_ll(self):
        # test UTM to LL
        new_lat, new_lon = utm_to_ll(self.nref, self.northing, self.easting, self.zone)

        print((new_lat, new_lon))

        self.assertTrue(np.isclose(self.lat, new_lat, atol=self.atol))
        self.assertTrue(np.isclose(self.lon, new_lon, atol=self.atol))

    def test_project_point_ll2utm(self):
        easting, northing, zone = project_point_ll2utm(self.lat, self.lon)

        print((zone, easting, northing))


        if isinstance(zone, np.bytes_) or (zone, np.unicode_):
            zone = zone.decode('UTF-8')

        self.assertTrue(zone == self.zone)
        self.assertTrue(np.isclose(easting, self.easting))
        self.assertTrue(np.isclose(northing, self.northing))

    def test_project_point_utm2ll(self):
        new_lat, new_lon = project_point_utm2ll(self.easting, self.northing, self.zone)

        print((new_lat, new_lon))

        self.assertTrue(np.isclose(self.lat, new_lat))
        self.assertTrue(np.isclose(self.lon, new_lon))

        # testing with epsg
        new_lat, new_lon = project_point_utm2ll(self.easting, self.northing, utm_zone=self.zone, epsg=self.to_epsg)

        print((new_lat, new_lon))

        self.assertTrue(np.isclose(self.lat, new_lat))
        self.assertTrue(np.isclose(self.lon, new_lon))

    def test_project_points_ll2utm(self):
        easting, northing, zone = project_points_ll2utm(np.ones(5) * self.lat,
                                                        np.ones(5) * self.lon)

        print((zone, easting, northing))

        self.assertTrue(zone == self.zone)
        self.assertTrue(np.sum(np.isclose(easting, np.ones(5) * self.easting))==5)
        self.assertTrue(np.sum(np.isclose(northing, np.ones(5) * self.northing))==5)

    if HAS_GDAL:
        def test_transform_ll_to_utm(self):
            utm_cs, utm_point = transform_ll_to_utm(self.lon, self.lat)

            easting = utm_point[0]
            northing = utm_point[1]

            print((easting, northing))

            # self.assertTrue(zone, self.zone)
            self.assertTrue(np.isclose(easting, self.easting))
            self.assertTrue(np.isclose(northing, self.northing))

        def test_transform_utm_to_ll(self):
            new_lon, new_lat, evel = transform_utm_to_ll(self.easting, self.northing, self.zone)

            print((new_lat, new_lon))

            self.assertTrue(np.isclose(self.lat, new_lat))
            self.assertTrue(np.isclose(self.lon, new_lon))
    # end if
