#!/usr/bin/env python3
import argparse
import pathlib
import sys


def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_fp', required=True, type=pathlib.Path,
            help='Raw SQL MIC dump filepath')
    args = parser.parse_args()
    if not args.input_fp.exists():
        parser.error(f'Input file {args.input_fp} does not exist')
    return args


def main():
    # Get command line arguments
    args = get_arguments()

    # Read all data into memory
    records = dict()
    with args.input_fp.open('r') as fh:
        line_token_gen = (line.rstrip().split(',') for line in fh)
        header_tokens = next(line_token_gen)
        for line_tokens in line_token_gen:
            assert len(line_tokens) == len(header_tokens)
            record = {k: v for k, v in zip(header_tokens, line_tokens)}
            if record['id'] not in records:
                records[record['id']] = list()
            records[record['id']].append(record)

    # Print according to output target
    data_map = {
        'labid': 'tube_code',
        'none_data': 'data',
        'vitek_run_none': 'vitek_run',
        'creation_date_timestamp': 'vitek_date',
        'vitek_OD_none': 'vitek_OD',
        'Ampicillin': 'Ampicillin (AMP)',
        'Amoxicillin/Clavulanic Acid': 'Amoxicillin/Clavulanic (AUG)',
        'Amikacin': 'Amikacin (AMK)',
        'Ceftazidime': 'Ceftazidime (CAZ)',
        'Ciprofloxacin': 'Ciprofloxacin (CIP)',
        'Ceftriaxone': 'Ceftriaxone (CRO)',
        'Cefazolin': 'Cefazolin (CFZ)',
        'Cefepime': 'Cefepime (FEP)',
        'Cefoxitin': 'Cefoxitin (CFX)',
        'Nitrofurantoin':'Nitrofurantoin (NIT)',
        'Gentamicin': 'Gentamicin (GEN)',
        'Meropenem': 'Meropenem (MEM)',
        'Norfloxacin': 'Norfloxacin (NOR)',
        'Trimethoprim/Sulfamethoxazole': 'Trimethoprim/Sulfamethoxazole (SXT)',
        'Ticarcillin/Clavulanic Acid': 'Ticarcillin/Clavulanic acid (TIM)',
        'Tobramycin': 'Tobramycin (TOB)',
        'Trimethoprim': 'Trimethoprim (TMP)',
        'Piperacillin/Tazobactam': 'Piperacillin/Tazobactam (PTZ)',
    }
    ab_ignore = {
        'Benzylpenicillin',
        'Cefoxitin Screen',
        'Clindamycin',
        'Daptomycin',
        'Erythromycin',
        'Fusidic Acid',
        'Inducible Clindamycin Resistance',
        'Linezolid',
        'Mupirocin',
        'Oxacillin',
        'Rifampicin',
        'Teicoplanin',
        'Tetracycline',
        'Vancomycin',
    }
    relation_op_map = {
        'LessThan': '<',
        'Equals': '=',
        'GreaterThan': '>',
    }

    print(*data_map.values(), sep='\t')
    for record_set in records.values():
        data_output = {k: 'no_data' for k in data_map.values()}

        tube_codes = set()
        vitek_dates = set()
        for record in record_set:
            tube_codes.add(record['labid'])

            datetime_str = record['creation_date_timestamp']
            date_str, time_str = datetime_str.split(' ')
            vitek_dates.add(date_str)

            ab_name = record['long_name']
            if ab_name not in data_map and ab_name in ab_ignore:
                continue
            elif ab_name not in data_map:
                print(f'error: got unknown antibiotic {ab_name} that isn\'t ignored', file=sys.stderr)
                sys.exit(1)
            mic_str = f"{relation_op_map[record['relationship_operator']]} {record['mic']}"
            data_output[data_map[ab_name]] = mic_str
        assert len(tube_codes) == 1
        assert len(vitek_dates) == 1
        data_output['tube_code'] = list(tube_codes)[0]
        data_output['vitek_date'] = list(vitek_dates)[0]
        print(*data_output.values(), sep='\t')


if __name__ == '__main__':
    main()


