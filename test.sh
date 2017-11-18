unameOut="$(uname -s)"
case "${unameOut}" in
    Linux*)     machine=Linux;;
    Darwin*)    machine=Mac;;
    CYGWIN*)    machine=Cygwin;;
    MINGW*)     machine=MinGw;;
    *)          machine="UNKNOWN:${unameOut}"
esac
if [[ ${machine} == "MinGw" ]]; then
	#echo "MinGw"
	clear
	py $(pwd)/testServer.py &
	sleep 2
	py $(pwd)/testClient.py
elif [[ ${machine} == "Linux" ]]; then
	#echo "Linux"
	clear
	python3 $(pwd)/testServer.py &
	sleep 2
	python3 $(pwd)/testClient.py

fi