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
    * `list.txt` This is the input of source & destination indices to reindex. The format is currently a colon separated, line-delimited list of `source:destination` indices. Be weary of whitespac - the script will interpret it as intentional. Correct and expected syntax example:
        ```
        logstash-stage-logs-2021.07.01:logstash-stage-logs-reindex
        logstash-stage-logs-2021.07.02:logstash-stage-logs-reindex
        logstash-stage-logs-2021.07.03:logstash-stage-logs-reindex
        logstash-dev-logs-2021.06.14:logstash-dev-logs-reindex
        logstash-dev-logs-2021.06.15:logstash-dev-logs-reindex
        logstash-prod-logs-2021.06.14:logstash-prod-logs-reindex
        logstash-prod-logs-2021.06.15:logstash-prod-logs-reindex
        ```
    * `reindex.py` The following variable assignment configurations in the beginning:
        * `username` Elasticsearch username with sufficient permissions
        * `password` Elasticsearch password. **See limitations section above about securing credentials**
        * `host` Elasticsearch hostname or IP. For clusters, this should be the client node.
        * `port` Elasticsearch port
