import os
from whoosh.index import create_in, exists_in
from whoosh.fields import Schema, ID, TEXT, DATETIME
from utils import Config


def main():
    # Create the index directory if it doesn't exist
    if not os.path.exists(Config.ix_dir):
      print('creating ', Config.ix_dir)
      os.makedirs(Config.ix_dir)

    # Initialize schema and index storage files
    if exists_in(Config.ix_dir):
        print("An index already exists!")
        return

    print("Creating index in {}".format(Config.ix_dir))
    schema = Schema(path=ID(unique=True, stored=True), published=DATETIME, content=TEXT)
    ix = create_in(Config.ix_dir, schema)

if __name__ == '__main__':
    main()