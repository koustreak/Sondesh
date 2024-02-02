import pprint
from sondesh.ddl_parser import parse_from_file

result = parse_from_file('sql_files/one.sql')
pprint.pprint(result)
