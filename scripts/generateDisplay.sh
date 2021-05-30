parentDirectory="$(pwd)"
echo $parentDirectory
sourceDirectory="$parentDirectory/corpus"
destinationDirectory="$parentDirectory/site/data/gc"

totalTopics=0
year='2021'
month='05'


helpFunction()
{
   echo "Usage: $0 -t 15 -y 2021 -m 05"
   echo "Ex: ./scripts/generateGcDisplay.sh -t 10"
   exit 1 # Exit script after printing help
}

while [ "$#" -gt 0 ]; do
  case "$1" in
    -t ) totalTopics="$2"; shift 2 ;;
    -y ) year="$2"; shift 2 ;;
    -m ) month="$2"; shift 2 ;;
    ? ) helpFunction ;; # Print helpFunction in case parameter is non-existent
  esac
done

echo "totalTopics $totalTopics"
echo "year $year"
echo "month $month"

processDisplay()
{
    echo "Generating GC Dispay:"
    # echo "$parentDirectory/generator/scripts/gc.py --total_items $totalItems --source_directory $sourceDirectory --destination_directory $destinationDirectory"
    python3 "$parentDirectory/generator/scripts/display.py" --total_topics $totalTopics --year $year --month $month --source_directory $sourceDirectory --destination_directory $destinationDirectory
}

processDisplay