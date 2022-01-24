#!/bin/bash
#--------------------------------------------------------
#------------------Environment Variables-----------------
#--------------------------------------------------------
# Place all index names that you need reindexed
# into list.txt in the same directory as this script.
# Make sure your elasticsearch node IP is correct.
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

# Recheck timer. The number in seconds to recheck the doc count before deleting the old index
# For docs < 20,000 this can be around 5 seconds. >100,000 should be towards 10-15 seconds
timer=10

# Name of index list
toReindex=(`cat "list.txt"`)


#--------------------------------------------------------
#--------------------check_and_delete--------------------
#--------------------------------------------------------
check_and_delete ()
{
docsOld=$(curl -k -u $user:$pass -HContent-Type:application/json -X GET "${ip}/${toReindex[$1]}/_stats" | jq '._all.primaries.docs.count')
docsNew=$(curl -k -u $user:$pass -HContent-Type:application/json -X GET "${ip}/${toReindex[$1]}-reindexed/_stats" | jq '._all.primaries.docs.count')
until [ $docsOld -eq $docsNew ]
do
	echo "Comparing "${toReindex[$1]}" to "${toReindex[$1]}"-reindexed"
	echo "not matched yet..."
	sleep $timer
	docsNew=$(curl -k -u $user:$pass -HContent-Type:application/json -X GET "${ip}/${toReindex[$1]}-reindexed/_stats" | jq '._all.primaries.docs.count')
done
echo " "
echo " "
echo "Match! DELETING index: "${toReindex[$1]}
# Uncomment to enable deletion
#curl -k -u $user:$pass -X DELETE "${ip}/${toReindex[$1]}"
}

# Check the value of max
if [ $max -lt 1 ]
then
	echo "The value of max needs to be a positive integer"
	exit 1
fi


#--------------------------------------------------------
#----------------------Main Section----------------------
#--------------------------------------------------------
i=0
for index in "${toReindex[@]}"
do
	if [ $max -eq $i ] || [ $max -lt $i ]
	then
		check_and_delete "(($i-$max))"
	fi
	echo " "
	echo " "
	echo "Reindexing: "$index
	echo " "
	curl -k -u $user:$pass -m 30 -HContent-Type:application/json -XPOST "${ip}/_reindex" -d '{
	"source": {
	"index": "'$index'"
	},
	"dest": {
	"index": "'$index'-reindexed"
	}
	}' | jq '.'
	((i++))
done

# Delete the remaining indexes
length="${#toReindex[@]}"
toDo=$(($length - $max))
until [ $toDo -eq $length ]
do
	check_and_delete "$toDo"
	((toDo++))
done

echo " "
echo "--------------------------------------------------------"
echo "----------------Reindexing complete!--------------------"
echo "--------------------------------------------------------"
