#!/bin/env python
# -*- coding: utf-8 -*-

import json
import argparse
import datetime
import logging
from pprint import pprint
from dateutil.parser import parse

def main():

    logger = logging.getLogger()
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
            '%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)

    parser = argparse.ArgumentParser(
        description='Convert taskwarrior exports to toto.txt format',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('-i', '--input', required=True, help='input json file')
    parser.add_argument('-o', '--output', required=True, help='output destination')
    parser.add_argument('-a', '--archive', help='archive destination, otherwise completed tasks are stored in the same file')
    parser.add_argument('-s', '--skipCompleted', help='Ignore already comlpeted tasks', action="store_true")
    parser.add_argument('-ns', '--noSort', help='Do not sort the results', action="store_true")

    args = parser.parse_args()
    priorities = {'L': '(C)', 'M': '(B)', 'H': '(A)'}

    logger.debug('Starting conversion')

    try:
        json_data=open(args.input).read()
    except Exception as e:
        logger.error('Could not open input file')
        return

    try:
        data = json.loads(json_data)
    except Exception as e:
        logger.error('Invalid json file')
        return

    logger.debug('Found {num} entries'.format(num=len(data)))

    result = [];
    archive = [];

    for entry in data:
        created = parse(entry['entry'])
        stringParts = []

        if entry['status'] == 'completed':
            if args.skipCompleted:
                continue

            stringParts.append('x')

        if 'priority' in entry:
            stringParts.append(priorities.get(entry['priority']))

        if entry['status'] == 'completed':
            stringParts.append(parse(entry['modified']).strftime("%Y-%m-%d"))

        stringParts.append(parse(entry['entry']).strftime("%Y-%m-%d"))

        stringParts.append('{description}')

        if 'project' in entry:
            stringParts.append('+' + entry['project'])

        description = entry['description']
        if 'tags' in entry:
            for tag in entry['tags']:
                if tag in description:
                    description = description.replace(tag, '@' + tag, 1)
                else:
                    stringParts.append('@' + tag)

        if 'due' in entry:
            stringParts.append('due:' + parse(entry['due']).strftime("%Y-%m-%d"))

        string = u' '.join(stringParts).format(description=description)

        if entry['status'] == 'completed' and args.archive:
            archive.append(string)
        else:
            result.append(string)

    if not args.noSort:
        result = sorted(result)
        archive = sorted(archive)

    with open(args.output, 'w') as file:
     file.write(str.join("\n", result))

     if len(archive) > 0:
         with open(args.archive, 'w') as file:
          file.write("\n".join(archive))

    logger.debug('Done')

if __name__ == '__main__':
    main()

    ### todo
    # due
    # x completed
    # tags
    # project
    # replace if exists
    # created at
    # ignore completed
    # completed to archive
