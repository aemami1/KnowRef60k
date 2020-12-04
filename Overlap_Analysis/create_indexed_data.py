# -*- coding: utf-8 -*-
 
import os
from whoosh.index import create_in
from whoosh.fields import Schema, TEXT, ID, STORED
import sys
import os.path

from whoosh.qparser import QueryParser
from whoosh import scoring,index
from tqdm import tqdm

 
def get_schema():
  return Schema(path=ID(stored=True), time=STORED, content=TEXT(stored=True))

def add_docs(writer, path):

  fileobj = open(path, "r",encoding='utf-8')
  fullText = fileobj.readlines()
  fileobj.close()
  for text in fullText:
    modtime = os.path.getmtime(path)
    writer.add_document(path=path,content=text, time=modtime)

def index_my_docs(dirname,filepaths, clean=False):
  if clean:
    clean_index(dirname,filepaths)
  else:
    incremental_index(dirname,filepaths)

def clean_index(dirname,filepaths):
  counter=0
  # Always create the index from scratch
  ix = index.create_in(dirname, schema=get_schema())
  writer = ix.writer()

  # Assume we have a function that gathers the filenames of the
  # documents to be indexed
  for path,i in zip(filepaths,tqdm(range(len(filepaths)))):
    print(path)
    add_docs(writer, path)
    if counter>3:
      break
    counter=counter+1
  writer.commit(merge=False)


def incremental_index(dirname,filepaths):
    ix = index.open_dir(dirname)
    counter=1
    # The set of all paths in the index
    indexed_paths = set()
    # The set of all paths we need to re-index
    to_index = set()

    with ix.searcher() as searcher:
      writer = ix.writer()
      # Loop over the stored fields in the index
      for fields in searcher.all_stored_fields():
        indexed_path = fields['path']
        indexed_paths.add(indexed_path)

        if not os.path.exists(indexed_path):
          # This file was deleted since it was indexed
          writer.delete_by_term('path', indexed_path)

        else:
          # Check if this file was changed since it
          # was indexed
          indexed_time = fields['time']
          mtime = os.path.getmtime(indexed_path)
          if mtime > indexed_time:
            # The file has changed, delete it and add it to the list of
            # files to reindex
            writer.delete_by_term('path', indexed_path)
            to_index.add(indexed_path)

      # Loop over the files in the filesystem
      # Assume we have a function that gathers the filenames of the
      # documents to be indexed
      for path,i in zip(filepaths,tqdm(range(len(filepaths)))):
        if path in to_index or path not in indexed_paths:
          # This is either a file that's changed, or a new file
          # that wasn't indexed before. So index it!
          print(path)
          add_docs(writer, path)
          if counter % 10 ==0:
            print("committing:")
            writer.commit(merge=False)
            writer = ix.writer()
          counter+=1


      writer.commit(merge=False)

 

 if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Extract Predicates from datasets.')
    parser.add_argument("--corpus", type=str, choices=["bookcorpus", "wikipedia", "stories", "openwebtext",
                        "cc-news"], required=True)
    params = parser.parse_args()

    root="Raw_Corpora/"+params.corpus
    filepaths = [os.path.join(root,i) for i in os.listdir(root)]
    dirname="Indexed_Corpora/"+params.corpus
    index_my_docs(dirname,filepaths, clean=False)
