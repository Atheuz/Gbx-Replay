# -*- coding: utf-8 -*-

import os
from operator import itemgetter
import csv
import util # Handles the files.
from datetime import timedelta
import sys
import argparse

def ms2ts(*args):
    return str(timedelta(milliseconds=args[0]))

def handle_file(*args):
    f, fn = args[0], args[1]
    k = util.process_file(f)
    if k:
        k, gbx_type = k[0], k[1]
        if gbx_type == 'replay':
            k['gbx_type'] = gbx_type
            k['filename'] = fn
            k['replay_timestamp'] = ms2ts(k['replay_time'])
            for i in k.iteritems():
                print i
        elif gbx_type == 'challenge':
            k['gbx_type'] = gbx_type
            k['filename'] = fn
            with open('.\output\%s.jpg' % k['track_name'], 'wb') as im_f:
                im_f.write(k['thumbnail'])
                # Too spacey.
                del k['thumbnail']
            for i in k.iteritems():
                print i
    else:
        print 'Something went wrong. You should not be seeing this.'

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--file', action='store', dest='f', type=str,
            nargs="+", default=None, help='Set file.')
    args = parser.parse_args()
    try:
        os.mkdir('output')
    except WindowsError:
        pass
    f = args.f
    if f:
        for i in f:
            gbx_file = i
            gbx_file = os.path.abspath(gbx_file)
            path, filename = os.path.split(gbx_file)[0], os.path.split(gbx_file)[1]
            #os.chdir(path)
            f = open(os.path.join(path, gbx_file), 'rb')
            #print check_type(f)
            handle_file(f, filename)
    else:
        sys.exit('You need to set a file.')

if __name__ == '__main__':
    main()

