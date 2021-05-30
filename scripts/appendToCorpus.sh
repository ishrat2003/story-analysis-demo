parentDirectory="$(pwd)"
echo $parentDirectory
sourceDirectory="$parentDirectory/feed"
archieveDirectory="$parentDirectory/feed-archived"
destinationDirectory="$parentDirectory/corpus"

totalItems=0

helpFunction()
{
   echo "Usage: $0 -t 1"
   echo "Ex: ./scripts/appendToGC.sh -t 10"
   exit 1 # Exit script after printing help
}

while [ "$#" -gt 0 ]; do
  case "$1" in
    -t ) totalItems="$2"; shift 2 ;;
    ? ) helpFunction ;; # Print helpFunction in case parameter is non-existent
  esac
done

echo "totalItems $totalItems"

processContents()
{
    echo "Getting Content:"
    # echo "$parentDirectory/generator/scripts/gc.py --total_items $totalItems --source_directory $sourceDirectory --destination_directory $destinationDirectory"
    python3 "$parentDirectory/generator/scripts/corpus.py" --total_items $totalItems --source_directory $sourceDirectory --destination_directory $destinationDirectory
}

processContents