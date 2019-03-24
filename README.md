# Factorio Data Dumper  

Runs the lua files that come with Factorio and dumps the data in a `.json`. 

```
git clone https://github.com/LeonPoon/factorio_data_dumper.git
cd factorio_data_dumper
virtualenv -p $(which python3) "$PWD"
"$PWD/bin/pip3" install -e . -r "$PWD/requirements.txt"
"$PWD/bin/python3" -m factorio_data_dumper > factorio.json
```
