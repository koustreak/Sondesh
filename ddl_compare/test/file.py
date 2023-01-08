import os
import pprint

from ddl_compare import parse_from_file

result = parse_from_file('abc')
pprint.pprint(result)