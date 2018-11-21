"""
Adds new papers to whoosh index. If a paper exists in db.p and has a .txt file
in data/txts/ but the path to that file is not stored in the whoosh index that
file will be added to the index.

Note: This locks the database while it is being run and if you're indexing
many files it can take hours.
"""

import os
import pickle
from datetime import datetime as odt
from time import mktime, time
from whoosh.index import create_in, open_dir
from whoosh.fields import Schema, ID, TEXT, DATETIME
from whoosh.qparser import QueryParser
from utils import Config

def get_datetime(record):
    # From https://stackoverflow.com/a/1697907/1775741
    published_struct_time = record['published_parsed']
    dt = odt.fromtimestamp(mktime(published_struct_time))
    return dt

def get_writer(ix):
    writer = ix.writer(procs=4, limitmb=256)
    stem_ana = writer.schema["content"].analyzer
    # Set the cachesize to -1 to indicate unbounded caching
    stem_ana.cachesize = -1
    # Reset the analyzer to pick up the changed attribute
    stem_ana.clean()
    return writer

def main():

    print("Opening index ...")
    ix = open_dir(Config.ix_dir)
    print("Done.")

    # The set of all paths in the index
    indexed_paths = set()
    with ix.searcher() as searcher:
        # Loop over the stored fields in the index
        print("Creating list of indexed paths ...")
        for fields in searcher.all_stored_fields():
            indexed_path = fields['path']
            indexed_paths.add(indexed_path)

    # Load paper database
    db = pickle.load(open('db.p', 'rb'))

    writer = get_writer(ix)

    total_count = 0
    save_inc = 1000
    count = 0
    for pid, data in db.items():
        if count == save_inc:
            print("Saving to disc ...")
            start = time()
            writer.commit()
            duration = time() - start
            print("Took {} seconds".format(duration))
            writer = get_writer(ix)
            total_count += save_inc
            count = 0
            print("Total papers saved {}".format(total_count))
        data = db[pid]
        idvv = '{}v{}'.format(data['_rawid'], data['_version'])
        text_filename = idvv + '.pdf.txt'
        text_path = os.path.join(Config.txt_dir, text_filename)
        if os.path.isfile(text_path) and text_path not in indexed_paths:
            count += 1
            with open(text_path, 'r') as fh:
                content = fh.read()
            dt = get_datetime(data)
            writer.add_document(path=text_path,
                                published=dt,
                                content=content)

    print("Final Save")
    start = time()
    writer.commit()
    print("Final save took {} seconds".format(time() - start))
    print("Total saved documents: {}".format(total_count))

if __name__ == '__main__':
    main()