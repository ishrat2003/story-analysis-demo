parentDirectory="$(pwd)"
echo $parentDirectory
sourceDirectory="$parentDirectory/corpus"
destinationDirectory="$parentDirectory/site/data"

totalTopics=0
start='2021-05-24'
end='2021-05-30'


helpFunction()
{
   echo "Usage: $0 -s '2021-05-24' -e '2021-05-30'"
   echo "Ex: ./scripts/generateDisplay.sh -s '2021-05-24' -e '2021-05-30'"
   exit 1 # Exit script after printing help
}

while [ "$#" -gt 0 ]; do
  case "$1" in
    -s ) start="$2"; shift 2 ;;
    -e ) end="$2"; shift 2 ;;
    ? ) helpFunction ;; # Print helpFunction in case parameter is non-existent
  esac
done

echo "totalTopics $totalTopics"
echo "start $start"
echo "end $end"

processDisplay()
{
    echo "Generating GC Dispay:"
    python3 "$parentDirectory/generator/scripts/generateDisplay.py"  \
    --start $start  \
    --end $end \
    --source_directory $sourceDirectory  \
    --destination_directory $destinationDirectory \

}

processDisplay