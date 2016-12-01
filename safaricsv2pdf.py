#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
from os import listdir
from pathlib import Path
from datetime import datetime
from jinja2 import Template
import csv
import pdfkit
# from PyPDF2 import PdfFileWriter, PdfFileReader


IS_BUNDLED = getattr(sys, 'frozen', False)

page_template = Template("""
<html>
  <head>
    <style>
    body {
      font-family: "Times New Roman", Times, serif;
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

    tfoot {
      display: table-footer-group;
    }

    tfoot tr td {
      border: none;
      display: table-footer-group;
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

# page_template = """
# <html>
#   <head>
#     <style>
#     body {{
#         font-family: "Lucida Grande", "Helvetica Nueue", Arial, sans-serif;
#     }}
#     table {{
#         width: 100%;
#         border-collapse: collapse;
#     }}
#     .center {{
#         text-align: center;
#     }}
#     .slim {{
#         display: inline-block;
#     }}
#     tr th{{
#         border: 2px solid black;
#     }}
#     tbody tr td {{
#         border: 1px solid black;
#         padding: 1px;
#         page-break-after: always;
#     }}
#     tbody td {{
#       white-space:nowrap;
#     }}
#     tbody td:last-child {{
#         width: 100%;
#     }}
#     tr:nth-child(even) td{{
#         background-color: #f7f7f7;
#     }}
#     tr:nth-child(odd) td{{
#         background-color: white;
#     }}
#     thead {{
#         display: table-header-group;
#     }}
#     tfoot {{
#         display: table-footer-group;
#     }}
#     tfoot tr td {{
#         border: none;
#         display: table-footer-group;
#     }}
#     </style>
#   </head>
#   <body>
#     <h2 class="center">{comp_name}</h2>
#     <div>
#       <table>
#           <thead>
#             <tr>
#               <th class="center">#</th>
#               <th class="center">File</th>
#               <th class="center">G.</th>
#               <th class="center">N.</th>
#               <th >Nome specie</th>
#               <th class="center">C.</th>
#               <th>Note</th>
#             </tr>
#           </thead>
#           <tbody>
#             {rows}
#           </tbody>
#           <tfoot>
#             <tr>
#                 <td></td>
#                 <td></td>
#                 <td></td>
#                 <td></td>
#                 <td></td>
#                 <td></td>
#                 <td>
#                     <small>{date}</small>
#                 </td>
#             </tr>
#           </tfoot>
#       </table>
#     </div>
#   </body>
# <html>
# """

# row_template = """
#           <td class="center">{seq}</td>
#           <td class="center">{file_name}</td>
#           <td class="center">{jury}</td>
#           <td class="center">{fish_num}</td>
#           <td>{fish_name}</td>
#           <td class="center">{coeff}</td>
#           <td></td>
#         </tr>
# """

def read_from_csv(url):
    with open(url, 'r') as csvfile:
        csvdata = csv.reader(csvfile, delimiter=';')
        return [data for data in csvdata if len(data) > 0]

def to_html(root_path, filename, csv_data):
    name, ext = os.path.splitext(filename)
    names = [n.capitalize() for n in name.split('_')]
    full_name = ' '.join(names)
    # rows = ''
    rows = [row for row in csv_data if len(row) == 5 and len(row[0]) > 0]
    # for i, row in enumerate(csv_data):
    #     if len(row[0]) == 0: continue
    #     rows += row_template.format(seq=i + 1,
    #                                 file_name=row[0],
    #                                 jury=row[1],
    #                                 fish_num=row[2],
    #                                 fish_name=row[3],
    #                                 coeff=row[4])
    # today = datetime.now()
    # timestamp = today.strftime('%d %b %Y, %H:%M:%S')
    # html_output = page_template.format(date=timestamp,
    #                                    comp_name=full_name,
    #                                    rows=rows)
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
        print("PDF file already present, skipping...")
        return
    # pdfkit.configuration(wkhtmltopdf='./lib/macos/64/wkhtmltopdf')
    pdfkit.from_string(html_output, os.path.abspath(full_output_path), options=options)

if __name__ == '__main__':
    exec_path = None
    if len(sys.argv) <= 1:
        exec_path = os.path.dirname(sys.executable)
        # print('Please provide a CSV file or directory.')
        # sys.exit(1)
    full_path = exec_path or sys.argv[1]
    print('cwd', full_path)
    if os.path.isdir(full_path):
        csv_files = [os.path.join(full_path, f) for f in listdir(full_path) if os.path.isfile(os.path.join(full_path, f)) and f.lower().endswith('.csv')]
        print('HERE', csv_files)
    else:
        csv_files = [full_path]
    for f_path in csv_files:
        root_path, filename = os.path.split(f_path)
        csv_data = read_from_csv(f_path)
        html = to_html(f_path, filename, csv_data)
        to_pdf(html, root_path, filename)
