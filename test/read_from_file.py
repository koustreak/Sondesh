import os
import pprint

from ddl_parse import parse_from_file

result = parse_from_file('test_sql.sql')
pprint.pprint(result)