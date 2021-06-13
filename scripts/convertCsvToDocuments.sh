parentDirectory="$(pwd)"
echo $parentDirectory
sourceDirectory="$parentDirectory/corpus/tpl/source"
destinationDirectory="$parentDirectory/corpus/tpl"
total_items=0
total_files=0

helpFunction()
{
   echo "Usage: $0 -t 1 -f 1"
   echo "Ex: ./scripts/convertCsvToDocuments.sh -t 1 -f 1"
   exit 1 # Exit script after printing help
}

while [ "$#" -gt 0 ]; do
  case "$1" in
    -t ) total_items="$2"; shift 2 ;;
    -f ) total_files="$2"; shift 2 ;;
    ? ) helpFunction ;; # Print helpFunction in case parameter is non-existent
  esac
done

echo "total_items $total_items"
echo "total_files $total_files"

convertCsvToDocuments()
{
    echo "Getting Content:"
    python3 "$parentDirectory/generator/scripts/convertCsvToDocuments.py" --total_items $total_items --total_files $total_files --source_directory $sourceDirectory --destination_directory $destinationDirectory
}

convertCsvToDocuments