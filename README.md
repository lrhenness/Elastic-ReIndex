# Elastic-ReIndex

This project aims to simplify and automate the re-indexing and compression of documents with conflicting fields in Elasticsearch


## Dependencies:
* [jq](https://stedolan.github.io/jq/) - a lightweight and flexible command-line JSON processor


## Features - Current


- Environment wide reindexing of indices.
  - Import indexes from text file
- Variable concurrent reindex jobs
- Delete completed indices
  - Doc count comparisons between new/old


## Features - Planned


- Runtime variables
	- Give date range of indexes to be reindexed
	- Give job buffer variable
	- Give new extention variable
	- Ability to remove previous extentions
- Statistics
	- Progress percentage
	- Average speed in indexes/second
- Regex capabilities
	- Dynamically edit "-word" extentions after dates for indices
	- Environmental variable error detection
- Index compression
    - Shrink support
    - _all reduction

## Breakdown
This script takes a list of indexes (provided by you) from a the `list.txt` file. Once the environmental variables are set correctly, the script will run through and reindex each index, check that it has properly obtained all previous documents, then delete (commented out by default) the old index.

### How To Use It
To use this script place in a new-line delimited list of desired indexes into `list.txt` (see example file). Edit the environmental variables in reindex.sh and then run the script: `user@linux:~$ bash reindex.sh`
