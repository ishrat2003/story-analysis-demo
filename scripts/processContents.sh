cp builds/myApp_v_*.apk artifacts/
parentDirectory="$(pwd)"
tempDirectory="$parentDirectory/feed-temp"
archieveDirectory="$parentDirectory/feed-archived"

helpFunction()
{
   echo "Usage: $0 -t totalItems"
   echo -e "\t-t: totalItems ex: 10"
   echo "Ex: ./scripts/processContents.sh -t 10"
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
    python3 "$parentDirectory/generator/scripts/contents.py --total_items $totalItems"
}
mkdir $tempDirectory/
cp $archieveDirectory/*.zip $tempDirectory/
cd $tempDirectory
unzip *.zip
rm *.zip

processContents

rm -R $tempDirectory/

