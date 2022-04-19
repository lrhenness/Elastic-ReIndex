# Elastic-Reindex
## _Bulk reindexing in Elasticsearch or Opensearch using Python_

Use at your own risk! This is not production ready by any means. 
That being said, This script runs fairly reliably in testing and with close monitoring.

The following information assumes you know a little bit about the task of reindexing indices in Elasticsearch.

### Features:
* Reindexing a limitless amount of source indices to a limitless amount of destination indices/aliases
* Task & total progress displayed during runtime
* *light* error checking and error queue
    * The program currently tests for the following from Elastic's task API: `completed = True` AND `task.status.created == task.status.total`
    * If the above criteria is not met, the source index is not deleted and the task ID is added to an error queue to be displayed at the end of the script for manually resolving.
* Debug mode for checking requests and responses
* Auto-delete index (when finished reindexing) toggle for more cautious reindexing.
* Cross-capatable with Opensearch as of current versions at time of commit (`Elasticsearch 7.16`, `Opensearch 1.1`)

### Limitations:
* Error checking/handling is not terribly robust
* Elastic credentials are stored in the script. If you'd like to be more secure, you'll need to modify the following variable assignments in the beginning of the script to point to secure credential strings using any number of methods:
    * username
    * password
* SSL verification is turned off and `urllib3.exceptions.InsecureRequestWarning` is disabled. This is not safe and you should modify the script to verify certificates when working with credentials over HTTPS.

### How to use:
* First, you'll need to manually create the destination index with any settings you'd like. If you are not sure how to set this up, you probably shouldn't use this script just yet in order to limit potential data destruction. **This script contains a function to auto-delete data when the reindex is "complete" and it is turned on by default. Please be sure you know what you are doing.**
    * In specific cases, I recommend setting `"index.mapping.ignore_malformed": true` in the destination index/alias. Again, at your own risk. Refs:
        * https://github.com/elastic/elasticsearch/issues/22471
        * https://www.elastic.co/guide/en/elasticsearch/reference/current/ignore-malformed.html
    * The destination index should probably be an alias if you are working with a large set of data to reindex
* Modify:
    * `list.txt` This is the input of source & destination indices to reindex. The format is currently a colon separated, line-delimited list of `source:destination` indices. Be weary of whitespace - the script will interpret it as intentional. Correct and expected syntax example:
        ```
        logstash-example1-source-00345:logstash-example-destination-alias
        logstash-example1-source-00346:logstash-example-destination-alias
        logstash-example2-source-2022-08-22:logstash-example-destination-2022-08-22
        logstash-example2-source-2022-08-23:logstash-example-destination-2022-08-23
        ```
    * `reindex.py` The following variable assignment configurations in the beginning:
        * `username` Elasticsearch username with sufficient permissions
        * `password` Elasticsearch password. **See limitations section above about securing credentials**
        * `host` Elasticsearch hostname or IP. For clusters, this should be the client node.
        * `port` Elasticsearch port
* [optional] Multithreading:
   * For now, the only way to multithread reindexes is to run multiple instances of `reindex.py` using different `list.txt` files. Create as many `list.txt` files as you need, all with unique indices similar to the following:
   * Then, create as many `reindex.py` files as `list.txt` files. For each new `reindex.py` file, find and replace `list.txt` in the code to the name of a new `list.txt`, something like `list2.txt`
   * Finally, run all `reindex.py` scripts simultaneously. tmux is a decent tool for this.

### Hopes for the future:
* More robust error checking & handling
   * Add `updated` return to `completed` to compare to `total`.
* Runtime options:
   * quit - graceful (q): Cancels the current reindex, presents error queue and list of indices touched/untouched. Asks to update list.txt to remove completed indices
   * quit - force (f): Simply exits the script gracefully. Leaves current reindex task running on ES's backend. May cause duplicate data
* Prettier stdout
* Application Logging - Already have a stdout debug logging option, but I would like standardized logs for further review/ingestion into ELK/Opensearch
* Containerization - For automating bulk reindexes using an API or web front-end
* Pre-run options to dynamically create the index template, index (alias), and specify `"index.mapping.ignore_malformed": true` if desired.
