#!/usr/bin/env python3
import argparse
import pathlib


import pyexcel_xlsx


def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--table_dir', required=True, type=pathlib.Path,
            help='Directory containing individual .tsv tables')
    parser.add_argument('--output_fp', required=True, type=pathlib.Path,
            help='Output fiepath')
    args = parser.parse_args()
    if not args.table_dir.exists():
        parser.error('Input directory %s does not exist' % args.table_dir)
    return args


def main():
    # Get command line arguments
    args = get_arguments()

    # Get all tables and read in as nested lists
    combined_data = dict()
    table_fps = args.table_dir.glob('*tsv')
    for table_fp in table_fps:
        with table_fp.open('r') as fh:
           data = [line.rstrip().split('\t') for line in fh]
           combined_data[table_fp.stem] = data

    # Write excel
    pyexcel_xlsx.save_data(str(args.output_fp), combined_data)


if __name__ == '__main__':
    main()
