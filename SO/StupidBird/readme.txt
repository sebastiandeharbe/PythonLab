Comandos: 
pip install -r requeriments.txt
pyinstaller --noconsole --onefile autobot.py

pyinstaller --noconsole --onefile --icon="icon.ico" --add-data "icon.ico;." .\stupidBird.py