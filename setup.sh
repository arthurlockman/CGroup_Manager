# Run this script to setup the project on your machine.
# You may need to modify this script to fit your exact setup.
virtualenv -p python3 venv
source ./venv/bin/activate
ln -s /usr/lib64/python3.5/site-packages/gi ./venv/lib64/python3.5/site-packages/
cd pycairo
python setup.py install
cd ..
pip install -r requirements.txt
