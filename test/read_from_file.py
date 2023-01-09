import os
import pprint

from ddl_compare import parse_from_file

result = parse_from_file('test_sql.sql')
pprint.pprint(result)