#!/usr/bin/env python3

# Copyright 2020 Jachym Cepicky (jachym.cepicky opengeolabs.cz)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
# of the Software, and to permit persons to whom the Software is furnished to do
# so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""
Script for loading latest RUIAN administrative areas - flats - and stores it to
CSV file.


Dependencies:

    `pip3 install -r requirementst.txt`

    * gdal

Author:

    Jachym Cepicky <jachym.cepicky opengeolabs cz>
    http://opengeolabs.cz

License:

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""

import argparse
import logging
import os
import sys
import csv
import requests
import datetime
from calendar import monthrange
import tempfile
from zipfile import ZipFile
from osgeo import ogr
import atexit
import shutil

ZSJ_URL = 'https://vdp.cuzk.cz/vymenny_format/soucasna/{date}_ST_UKSH.xml.zip'
OBCE_CISELNIK = 'https://www.cuzk.cz/CUZK/media/CiselnikyISUI/UI_OBEC/UI_OBEC.zip?ext=.zip'
OBEC_URL = 'https://vdp.cuzk.cz/vymenny_format/soucasna/{date}_OB_{kod}_UKSH.xml.zip'

TO_BE_REMOVED = []

logger = logging.getLogger('RUIAN2DB')
logger.setLevel(logging.INFO)


@atexit.register
def clear():
    global TO_BE_REMOVED

    for mydir in TO_BE_REMOVED:
        print(f"removing {mydir}")
        shutil.rmtree(mydir)


def _get_date():

    now = datetime.datetime.now()
    month = now.month-1
    year = now.year
    if month == 0:
        month = 12
        year = now.year - 1
    days = monthrange(year=year, month=month)
    return "{}{:02d}{}".format(year, month, days[1])


def get_data(url, pref="obce"):

    global TO_BE_REMOVED
    out_dir_name = tempfile.mkdtemp(prefix=pref)
    out_temp_name = tempfile.mktemp(dir=out_dir_name, suffix=".zip")
    TO_BE_REMOVED.append(out_dir_name)

    with open(out_temp_name, "wb") as out_zip:
        r = requests.get(url, stream=True)
        for chunk in r.iter_content(8192):
            out_zip.write(chunk)

    with ZipFile(out_temp_name, "r") as myzip:
        myzip.extractall(path=out_dir_name)

    return out_dir_name


def get_obec_file(kod):
    """Download fresh data from CUZK server - always last day of previous month
    """

    global logger

    last_day = _get_date()
    url = OBEC_URL.format(date=last_day, kod=kod)
    out_dir_name = get_data(url, "obec")
    data_file = f"{last_day}_OB_{kod}_UKSH.xml"
    output_file_name = os.path.join(out_dir_name, data_file)
    return output_file_name


def outputcsv(layer, fileobj):
    "Write output data to target CSV file (can be STDOUT)

    :param layer: osgeo.ogr.Layer
    :param fileobj: python `file` object with `write()` method
    """

    writer = csv.writer(fileobj)
    writer.writerow(["Kod", "TypStavebnihoObjektuKod", "ZpusobVyuzitiKod",
                     "PocetBytu", "PocetPodlazi", "x", "y"
                     ])

    feature = layer.GetNextFeature()
    while feature:
        assert feature
        geom = feature.GetGeometryRef().GetPoint()
        writer.writerow([
            feature.GetField("Kod"),
            feature.GetField("TypStavebnihoObjektuKod"),
            feature.GetField("ZpusobVyuzitiKod"),
            feature.GetField("PocetBytu"),
            feature.GetField("PocetPodlazi"),
            geom[0], geom[1]
        ])
        feature = layer.GetNextFeature()


def main(obec, typy_objektu, output):
    """
    Download fresh data for given municipality (obec) and filter according to 
    object types from the layer StavebniObjekty

    :param obec:  municipality ID
    :param typy_objektu: List of ZpusobVyuzitiKod
    :param output: output file name
    """

    global logger

    obec_file = get_obec_file(obec)
    logger.info(f"Importing obec {obec}")
    source = ogr.Open(obec_file)
    assert source

    layer = source.GetLayerByName("StavebniObjekty")
    assert layer

    kody = ["ZpusobVyuzitiKod = {}".format(obj) for obj in typy_objektu]
    layer.SetAttributeFilter(" OR ".join(kody))

    if output:
        with open(output, "w") as output_file:
            outputcsv(layer, output_file)
    else:
        outputcsv(layer, sys.stdout)

    return


def parse_args():
    parser = argparse.ArgumentParser(
        description='Import address points from RUIAN to PostgreSQL database'
    )
    parser.add_argument('--obec', type=int,
                        default=None, required=True,
                        help='Kod obce')
    parser.add_argument('--typy', type=int,
                        nargs="+",
                        required=False,
                        default=[6, 7],
                        help='kód stavebního objektu (6, 7)')
    parser.add_argument('--csv', type=str,
                        help='Výstupní CSV')

    args = parser.parse_args()

    return args


if __name__ == "__main__":
    args = parse_args()

    kody = [int(k) for k in args.typy]
    main(args.obec, kody, args.csv)
