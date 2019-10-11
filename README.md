# Elastic-ReIndex
This project aims to simplify and automate the re-indexing and compression of documents with conflicting fields in Elasticsearch

### Dependencies:
* jq

### What is does
This script takes a list of indexes (provided by you) from a the reindex_list file. Once the environmental variables are set correctly, the script will run through and reindex each index, check that it has properly obtained all previous documents, then delete the old index.

### How To Use
To use this script place in a new-line delimited list of desired indexes into reindex_list. Edit the environmental variables in reindex.sh and then run the script: `user@linux:~$ bash reindex.sh`

### Planned features
* Index compression
* Error detection
* Automatic detection of conflicting fields
