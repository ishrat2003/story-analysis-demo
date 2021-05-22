parentDirectory="$(pwd)"
echo $parentDirectory
sourceDirectory="$parentDirectory/feed"
archieveDirectory="$parentDirectory/feed-archived"
backupZipName=$(date +'%Y_%m_%d')

archive=0
feed=0


helpFunction()
{
   echo "Usage: $0 -a 1 -f 1"
   echo "Ex: ./scripts/fetchFeeds.sh -a 1 -f 1 -s 1"
   echo "Ex: ./scripts/fetchFeeds.sh -t 10 -s 1"
   exit 1 # Exit script after printing help
}

while [ "$#" -gt 0 ]; do
  case "$1" in
    -a ) archive="$2"; shift 2 ;;
    -f ) feed="$2"; shift 2 ;;
    ? ) helpFunction ;; # Print helpFunction in case parameter is non-existent
  esac
done

echo "archive $archive"
echo "feed $feed"

archieveFunction()
{
    cd "$sourceDirectory"
    totalRssFiles=`ls -1 | wc -l`
    if [[ $totalRssFiles -gt 0 ]]
    then
        echo "Total rss files: $totalRssFiles"
        rm "$archieveDirectory/RSS_$backupZipName.zip"
        zip -r "$archieveDirectory/RSS_$backupZipName.zip" .
        echo "Archieved content: $archieveDirectory/RSS_$backupZipName.zip"
        rm *.json
        remainingTotals=`ls -1 | wc -l`
        echo "Total rss files moved. Current files count: $remainingTotals"
    fi

    echo "Archieved files:"
    cd "$archieveDirectory"
    ls -latr
}

processFeed()
{
    echo "Getting feeds:"
    python3 "$parentDirectory/generator/scripts/feeds.py"
}

if [[ $feed -eq 1 ]]
    then
        processFeed
fi

if [[ $archive -eq 1 ]]
    then
        archieveFunction
fi
