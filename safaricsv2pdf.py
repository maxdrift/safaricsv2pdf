#!/usr/bin/env python
# -*- coding: utf-8 -*-
import csv
import os
import platform
import sys
from os import listdir
from pathlib import Path

import pdfkit
from jinja2 import Template

MAC_ALIAS = 'macos'
WIN_ALIAS = 'win'

OS_MAPPING = {
    'Darwin': MAC_ALIAS,
    'Windows': WIN_ALIAS
}

ARCH_MAPPING = {
    MAC_ALIAS: {
        '64bit': '64'
    },
    WIN_ALIAS: {
        '64bit': '64',
        '32bit': '32'
    }
}

OS = OS_MAPPING.get(platform.system(), None)
ARCH = ARCH_MAPPING.get(OS, {}).get(platform.architecture()[0], None)
if OS is None or ARCH is None:
    print('ERROR: Unsupported system/architecture.')
    sys.exit(1)

IS_BUNDLED = getattr(sys, 'frozen', False)
BUNDLE_PATH = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
WKHTMLTOPDF_PATH = os.path.join(BUNDLE_PATH, 'lib', OS, ARCH, 'wkhtmltopdf')
if OS == WIN_ALIAS:
    WKHTMLTOPDF_PATH = '.'.join([WKHTMLTOPDF_PATH, 'exe'])

# Template available at: http://codepen.io/maxdrift/pen/jVmqyg
page_template = Template("""
<html>
  <head>
    <style>
    body {
      font-family: "Times New Roman", Times, serif;
    }

    .pb {
      page-break-before: always;
    }

    table {
      width: 100%;
      border-collapse: collapse;
    }

    .center {
      text-align: center;
    }

    tr th {
      border: 2px solid black;
    }

    tbody tr td {
      border: 1px solid black;
      padding: 1px;
      page-break-after: always;
    }

    tbody td {
      white-space: nowrap;
    }

    tbody td:last-child {
      width: 100%;
    }

    tr:nth-child(even) td {
      background-color: #f7f7f7;
    }

    tr:nth-child(odd) td {
      background-color: white;
    }

    thead {
      display: table-header-group;
    }

    tr, td, th, tbody, thead {
      page-break-inside: avoid !important;
    }

    .header-container {
      height: 2.3cm;
    }

    #comp-number {
      border-style: solid;
      border-width: 2px 2px 2px 2px;
      width: 1.5cm;
      height: 1.5cm;
      position: absolute;
      top: 20px;
      right: 10px;
    }

    #comp-number span {
      font-size: 11px;
      text-align: center;
      width: 100%;
      position: absolute;
    }

    .title-text {
      font-size: 25px;
      font-weight: bold;
      display: block;
      padding-bottom: 15px;
    }

    #signature {
      margin-top: 20px;
      margin-bottom: 20px;
      position: absolute;
      right: 50px;
    }
    </style>
  </head>
  <body>
    <div class="header-container">
      <span class="center title-text">{{ comp_name }}</span>
      <span><strong>Gara: </strong>___________________________________</span>
      <span>&nbsp;&nbsp;<strong>Data: </strong>__ / __ / _____</span>
      <span>&nbsp;&nbsp;<strong>Ora: </strong>__ : __</span>

      <div id="comp-number">
        <span>Num. Gara</span>
      </div>
    </div>
    <div>
      <table>
        <thead>
          <tr>
            <th class="center">#</th>
            <th class="center">File</th>
            <th class="center">G.</th>
            <th class="center">N.</th>
            <th>Nome specie</th>
            <th class="center">C.</th>
            <th>Note</th>
          </tr>
        </thead>
        <tbody>{% for row in rows %}
          <tr>
            <td class="center">{{ loop.index }}</td>
            <td class="center">{{ row[0] }}</td>
            <td class="center">{{ row[1] }}</td>
            <td class="center">{{ row[2] }}</td>
            <td>{{ row[3] }}</td>
            <td class="center">{{ row[4] }}</td>
            <td></td>
          </tr>
          {%- endfor %}
        </tbody>
      </table>
      <span id="signature"><strong>Firma:</strong> _______________________________________</span>
    </div>
  </body>
<html>
""")


def read_from_csv(url):
    with open(url, 'r') as csvfile:
        csvdata = csv.reader(csvfile, delimiter=';')
        return [data for data in csvdata if len(data) > 0]


def to_html(filename, csv_data):
    name, ext = os.path.splitext(filename)
    names = [str(n.capitalize()) for n in name.split('_')]
    full_name = ' '.join(names)
    rows = [row for row in csv_data if len(row) == 5 and len(row[0]) > 0]
    html_output = page_template.render(
        comp_name=full_name,
        rows=rows
    )
    return html_output


def to_pdf(html_output, root_path, filename):
    options = {
        'quiet': '',
        'page-size': 'A4',
        'encoding': 'UTF-8'
    }
    pdf_filename = '%s.pdf' % os.path.splitext(filename)[0]
    full_output_path = os.path.join(root_path, pdf_filename)
    if Path(full_output_path).is_file():
        print('PDF file already present, skipping...')
        return
    config = pdfkit.configuration(wkhtmltopdf=WKHTMLTOPDF_PATH.encode('utf-8'))
    pdfkit.from_string(html_output, os.path.abspath(full_output_path), options=options, configuration=config)


if __name__ == '__main__':
    exec_path = None
    if len(sys.argv) <= 1:
        if IS_BUNDLED:
            exec_path = os.path.dirname(sys.executable)
        else:
            print('ERROR: Please provide a CSV file or a directory.')
            sys.exit(1)
    full_path = exec_path or sys.argv[1]
    if os.path.isdir(full_path):
        csv_files = [os.path.join(full_path, f) for f in listdir(full_path) if
                     os.path.isfile(os.path.join(full_path, f)) and f.lower().endswith('.csv')]
    else:
        csv_files = [full_path]
    for f_path in csv_files:
        r_path, fname = os.path.split(f_path)
        csv_d = read_from_csv(f_path)
        html = to_html(fname, csv_d)
        to_pdf(html, r_path, fname)
