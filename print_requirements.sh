pip freeze > requirements.txt
echo "dependencies = ["; sed -e 's/^/  "/' -e 's/$/",/' requirements.txt; echo "]"