for i in *.json 
do
echo "Uploading $i"
b=`basename $i .json` 
curl --upload-file $i localhost:5000/11097/$b -s
echo ""
done
