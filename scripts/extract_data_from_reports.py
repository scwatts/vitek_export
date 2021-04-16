#!/usr/bin/env python3
import argparse
import csv
import pathlib
import sys
import xml.etree.ElementTree as ET


def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--table_fp', required=True, type=pathlib.Path,
            help='Input isolate_lab_report.tsv')
    args = parser.parse_args()
    if not args.table_fp.exists():
        parser.error(f'Input file {args.table_fp} does not exist')
    return args


def main():
    # Get arguments
    args = get_arguments()

    # Iterate reports and extract data
    with args.table_fp.open('r') as fh:
        # Read header
        header_in = fh.readline().rstrip().split('\t')
        header_out = None
        # Parse with csv to correctly tokenise with quote character, using tab as delim
        for line_tokens in csv.reader(fh, delimiter='\t', quotechar='"'):
            record = {name: value for name, value in zip(header_in, line_tokens)}
            lab_id, mics = process_report_xml(record['data'])
            # Create a header, check it is consistent, print if needed
            if len(mics) == 0:
                continue
            header = ['vitek_id', 'lab_id', *mics[0].keys()]
            if header_out == None:
                header_out = header
                print(*header_out, sep='\t')
            if header != header_out:
                print('error: got mismatched headers', file=sys.stderr)
            for mic in mics:
                print(record['id'], lab_id, *mic.values(), sep='\t')


def process_report_xml(xml):
    root = ET.fromstring(xml)
    lab_id = root.find('.//IsolateInfo').get('labIDNum')
    data = [el.attrib for el in root.findall('.//AstDrugResultInfo')]
    return lab_id, data


if __name__ == '__main__':
    main()
