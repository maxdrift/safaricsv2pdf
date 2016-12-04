# SafariCSV2PDF
Convert Safari Fotosub competitor's CSV to printer-ready PDF

### Prerequisites
- Python 3.5
- GNU make
- PyWin32 (Windows only)

### Build instructions
`$ make` command will:
- create a virtualenv
- install the dependencies
- build an executable file for the current OS inside the **dist** folder

### Usage
1. Download a precompiled executable from [HERE](https://github.com/maxdrift/safaricsv2pdf/releases/latest) or [build it](#build-instructions) from sources
2. gather all CSV files from SF competitors in one folder
3. copy the **SafariCSV2PDF** executable file to the same folder
4. run the executable

it will generate one PDF file for each CSV present in the folder.
