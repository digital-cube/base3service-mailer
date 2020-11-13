# base3service-mailer

requirements:
  - python3
  - postgresql
  - redis


in postgresql create database user demo, and using this user create databases demo_mailer and test_demo_mailer


perform following steps to run integration tests

```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

./test.sh```