parentDirectory="$(pwd)"
echo $parentDirectory

helpFunction()
{
   echo "Usage: $0 -t 1"
   echo "Ex: ./scripts/appendToCorpus.sh -t 10 -s bbc|tpl"
   exit 1 # Exit script after printing help
}

while [ "$#" -gt 0 ]; do
  case "$1" in
    -t ) totalItems="$2"; shift 2 ;;
    -s ) source="$2"; shift 2 ;;
    ? ) helpFunction ;; # Print helpFunction in case parameter is non-existent
  esac
done

commonPath="$parentDirectory/corpus/$source"
destinationDirectory="$commonPath"

if [[ $source == 'bbc' ]]
then
  sourceDirectory="$commonPath/feed"
  archieveDirectory="$commonPath/feed-archived"
elif [[ $source == 'tpl' ]]
then
  sourceDirectory="$commonPath/lists"
elif [[ $source == 'tpl_lc' ]]
then
  sourceDirectory="$commonPath/lists"
fi

totalItems=0
echo "totalItems $totalItems"

processContents()
{
    echo "Getting Content:"
    # echo "$parentDirectory/generator/scripts/gc.py --total_items $totalItems --source_directory $sourceDirectory --destination_directory $destinationDirectory"
    python3 "$parentDirectory/generator/scripts/buildCorpus.py" --source $source --total_items $totalItems --source_directory $sourceDirectory --destination_directory $destinationDirectory
}

processContents