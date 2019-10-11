#!/bin/bash
#
#
# Made by Luke Henness
# Security Analyst
# H & A Security Solutions
#
#
#
# Place all index names that you need reindexed
# into reindex_list in the same directory as this script.
# Make sure your elasticsearch node IP is correct if not localhost
#
#
#
# Creds for Elasticsearch
user="admin"
pass="hunter1"

# Format for ip is: "http://10.0.10.10:9200" NO SLASH AFTER PORT
ip="https://10.0.10.10:9200"

# Maximum concurrent reindex jobs
max=3

# New extention for reindexed docs
ext="-new"

# Name of index list
toReindex=(`cat "reindex_list"`)

#--------------------------------------------------------
#--------------------check_and_delete--------------------
#--------------------------------------------------------
check_and_delete ()
{
#put code to replace the check and delete in the code below
}



i=0
for index in "${toReindex[@]}"
do
	if [ $max -eq $i ] || [ $max -lt $i ]
	then
		docs=`curl -k -u $user:$pass -HContent-Type:application/json -X GET "${ip}/${index}/_stats" | jq '._all.primaries.docs.count'`
		echo $docs
        echo "Comparing "${toReindex[($i-$max)]}" to "${toReindex[($i-$max)]}"-new"
        echo "not matched yet..."
        echo "MATCHED, deleting "${toReindex[($i-$max)]}
	fi
	echo "Reindexing: "$index
	curl -k -u $user:$pass -HContent-Type:application/json -XPOST "${ip}/_reindex" -d '{
	"source": {
      "index": "'$index'"
    },
    "dest": {
      "index": "'$index'$ext"
    }
	}'
	((i++))
done

length="${#toReindex[@]}"
toDo=$(($length - $max))

until [ $toDo -eq $length ]
do
	echo "Comparing "${toReindex[($toDo)]}" to "${toReindex[($toDo)]}"-new"
    echo "not matched yet..."
    echo "MATCHED, deleting "${toReindex[($toDo)]}
    ((toDo++))
done

echo "Reindexing complete!"
