

echo "clean"
rm -R -v octopylog/*.*


echo "create directory"
mkdir octopylog
mkdir octopylog/images
mkdir octopylog/network
mkdir octopylog/wxcustom
echo "copy file"
cp -v  ../src/*.py octopylog/
cp -v  ../src/network/*.py octopylog/network
cp -v  ../src/images/*.png octopylog/images
cp -v  ../src/wxcustom/*.py octopylog/wxcustom


echo "Version (x.x.x) :"
read version

name_file="octopylog-$version.tar.gz" 
echo "Create package : $name_file"

tar -pczf $name_file octopylog

echo "end"


