import unittest
import os

from geopyspark import initial_spark_conf
from geopyspark.geotrellis import Extent, TileLayout
from geopyspark.geotrellis.constants import SPATIAL
from geopyspark.geotrellis.geotiff import get
from geopyspark.tests.python_test_utils import check_directory, geotiff_test_path
from pyspark import SparkContext



check_directory()


class BaseTestClass(unittest.TestCase):
    if 'TRAVIS' in os.environ:
        master_str = "local[2]"
    else:
        master_str = "local[*]"

    conf = initial_spark_conf(master=master_str, appName="test")
    pysc = SparkContext(conf=conf)

    dir_path = geotiff_test_path("all-ones.tif")

    rdd = get(pysc, SPATIAL, dir_path)
    value = rdd.to_numpy_rdd().collect()[0]

    projected_extent = value[0]
    extent = projected_extent.extent

    expected_tile = value[1].cells
    (_, rows, cols) = expected_tile.shape

    layout = TileLayout(1, 1, cols, rows)
