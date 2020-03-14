# NIST800-53-R4-XML-PARSER
The purpose of this repository is to play around with the nist 800 xml document using python.
It is meant to be used as a learning activity.

Some guides:
https://data-flair.training/blogs/python-best-practices/
https://www.python.org/dev/peps/pep-0008/

## Some useful things
* This is best experminted with in the pyhon console:
```bash
python3.7
```
```python3.7
import nist_xmlparser
px = nist_xmlparser.NIST800('./800-53-controls.xml')
px.print_control('number', 'AC-1')
```
This will print out the control whose _number_ is _AC-1_.

* It is a good idea to get aquainted with the structure of the xml file.
```bash
head -n40 800-53-controls.xml
```

* Understand that the document uses namespaces, which is incorporated into the logic
of the parser (try to find how).
