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
            txt_file = './output/%s.txt' % ''.join([x for x in fn if x.isalnum])
            with open(txt_file, 'w') as w:
                s = ''
                for i,j in k.iteritems():
                    s += "%s,%s\n" % (i,j)
                w.write(s + '\n')
                w.close()
            return k
            #for i in k.iteritems():
            #    print i
        elif gbx_type == 'challenge':
            k['gbx_type'] = gbx_type
            k['filename'] = fn
            with open('.\output\%s.jpg' % k['track_name'], 'wb') as im_f:
                im_f.write(k['thumbnail'])
                # Too spacey.
                im_f.close()
            del k['thumbnail']
            txt_file = './output/%s.txt' % ''.join([x for x in fn if x.isalnum])
            with open(txt_file, 'w') as w:
                s = ''
                for i,j in k.iteritems():
                    s += "%s,%s\n" % (i,j)
                w.write(s + '\n')
                w.close()
            return k
            #for i in k.iteritems():
            #    print i
    else:
        sys.exit('Something went wrong. You should not be seeing this.')

def handle_path(*args):
    lst = []
    lst_of_files = os.listdir(args[0])
    lst_of_files = [os.path.join(args[0], x) for x in lst_of_files]
    for i in lst_of_files:
        gbx_file = i
        path, fn = os.path.split(gbx_file)[0], os.path.split(gbx_file)[1]
        f = open(gbx_file, 'rb')
        k = handle_file(f, fn)
        if k['gbx_type'] == 'replay':
            lst.append(k)
    lst.sort(key=itemgetter('replay_time'))
    csv_file = './output/%s.csv' % os.path.split(path)[1]
    values = [(x['nickname'], x['replay_time']) for x in lst]
    csv_file = open(csv_file, 'wb')
    csv_writer = csv.writer(csv_file, dialect='excel',delimiter=',')
    csv_writer.writerows(values)
    csv_file.close()
    return

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', action='store', dest='f', type=str,
            nargs="+", default=None, help='Set file.')
    parser.add_argument('-p', '--path', action='store', dest='p', type=str,
            nargs="+", default=None, help='Set path.')
    args = parser.parse_args()
    try:
        os.mkdir('output')
    except WindowsError:
        pass
    f = args.f
    p = args.p
    if f and not p:
        for i in f:
            gbx_file = i
            gbx_file = os.path.abspath(gbx_file)
            path, filename = os.path.split(gbx_file)[0], os.path.split(gbx_file)[1]
            f = open(os.path.join(path, gbx_file), 'rb')
            k = handle_file(f, filename)
            for j in k.iteritems():
                print j
    elif p and not f:
        for i in p:
            handle_path(i)
    else:
        sys.exit('You need to set a file.')

if __name__ == '__main__':
    main()

