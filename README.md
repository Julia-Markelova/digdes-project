# digdes-project
This project will recognize main named entities of the doc/docx texts with the help of ```natasha``` and ```pullenti```. 
# usage

usage: ```main.py [-h] [-e {pullenti,pullenti-wrapper,natasha} | -oo] dir```

Extract organizations and money from texts and compare it with xml

positional arguments:
```
  dir                   directory with directories which contain doc/docx
                        files with xml-files
```
optional arguments:
```
  -h, --help            show this help message and exit
  -e {pullenti,pullenti-wrapper,natasha}, --extractor {pullenti,pullenti-wrapper,natasha}
                        name of extractor, default "natasha"
  -oo, --only_organizations
                        extract only organizations
```
