parentDirectory="$(pwd)"
feedDirectory="$parentDirectory/feed-temp"
archieveDirectory="$parentDirectory/feed-archived"

processContents()
{
    echo "Getting Content:"
    python3 "$parentDirectory/generator/scripts/gc.py --total_items 0 --source_directory $feedDirectory"
}

mkdir $feedDirectory/
cp $archieveDirectory/*.zip $feedDirectory/
cd $tempDirectory
unzip *.zip
rm *.zip

processContents

rm -R $feedDirectory


