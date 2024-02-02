import json
import logging
import os
from copy import deepcopy
from typing import Dict, List, Tuple

from sondesh.output import dialects as d

output_modes = [
    "mssql",
    "mysql",
    "oracle",
    "hql",
    "sql",
    "snowflake",
    "redshift",
    "bigquery",
]


logger = logging.getLogger('sondesh')


def get_table_from_tables_data(tables_dict: Dict, table_id: Tuple[str, str]) -> Dict:
    """get table by name and schema or rise exception"""
    target_table = tables_dict.get(table_id)
    if target_table is None:

        raise ValueError(
            f"Found ALTER statement to not existed TABLE {table_id[0]} with SCHEMA {table_id[1]}"
        )
    return target_table


def add_index_to_table(tables_dict: Dict, statement: Dict, output_mode: str) -> Dict:
    """populate 'index' key in output data"""
    table_id = (statement["table_name"], statement["schema"])
    target_table = get_table_from_tables_data(tables_dict, table_id)

    del statement["schema"]
    del statement["table_name"]

    if output_mode != "mssql":
        del statement["clustered"]

    target_table["index"].append(statement)

    return tables_dict


def create_alter_column(index: int, column: Dict, ref_statement: Dict) -> Dict:
    """create alter column metadata"""
    column_reference = ref_statement["columns"][index]
    alter_column = {
        "name": column["name"],
        "constraint_name": column.get("constraint_name"),
    }
    alter_column["references"] = deepcopy(ref_statement)
    alter_column["references"]["column"] = column_reference
    del alter_column["references"]["columns"]
    return alter_column


def prepare_alter_columns(target_table: Dict, statement: Dict) -> Dict:
    """prepare alters column metadata"""
    alter_columns = []
    for num, column in enumerate(statement["columns"]):
        alter_columns.append(create_alter_column(num, column, statement["references"]))
    if not target_table["alter"].get("columns"):
        target_table["alter"]["columns"] = alter_columns
    else:
        target_table["alter"]["columns"].extend(alter_columns)
    return target_table


def add_alter_to_table(tables_dict: Dict, statement: Dict) -> Dict:
    """add 'alter' statement to the table"""
    table_id = (statement["alter_table_name"], statement["schema"])

    target_table = get_table_from_tables_data(tables_dict, table_id)

    if "columns" in statement:
        prepare_alter_columns(target_table, statement)
    elif "check" in statement:
        if not target_table["alter"].get("checks"):
            target_table["alter"]["checks"] = []
        statement["check"]["statement"] = " ".join(statement["check"]["statement"])
        target_table["alter"]["checks"].append(statement["check"])
    elif "unique" in statement:
        target_table = set_alter_to_table_data("unique", statement, target_table)
        target_table = set_unique_columns_from_alter(statement, target_table)
    elif "default" in statement:
        target_table = set_alter_to_table_data("default", statement, target_table)
        target_table = set_default_columns_from_alter(statement, target_table)
    elif "primary_key" in statement:
        target_table = set_alter_to_table_data("primary_key", statement, target_table)
    return tables_dict


def set_default_columns_from_alter(statement: Dict, target_table: Dict) -> Dict:
    for column in target_table["columns"]:
        if statement["default"]["columns"]:
            for column_name in statement["default"]["columns"]:
                if column["name"] == column_name:
                    column["default"] = statement["default"]["value"]
    return target_table


def set_unique_columns_from_alter(statement: Dict, target_table: Dict) -> Dict:
    for column in target_table["columns"]:
        for column_name in statement["unique"]["columns"]:
            if column["name"] == column_name:
                column["unique"] = True
    return target_table


def set_alter_to_table_data(key: str, statement: Dict, target_table: Dict) -> Dict:
    if not target_table["alter"].get(key + "s"):
        target_table["alter"][key + "s"] = []
    if "using" in statement:
        statement[key]["using"] = statement["using"]
    target_table["alter"][key + "s"].append(statement[key])
    return target_table


def init_table_data() -> Dict:
    return {
        "columns": [],
        "primary_key": None,
        "alter": {},
        "checks": [],
        "index": [],
        "partitioned_by": [],
        "tablespace": None,
    }


def process_alter_and_index_result(
    tables_dict: Dict, table: Dict, output_mode: str
) -> Dict:
    if table.get("index_name"):
        tables_dict = add_index_to_table(tables_dict, table, output_mode)

    elif table.get("alter_table_name"):
        tables_dict = add_alter_to_table(tables_dict, table)

    return tables_dict


def process_entities(tables_dict: Dict, table: Dict, output_mode: str) -> Dict:
    """process tables, types, sequence and etc. data"""
    is_it_table = True

    if table.get("table_name"):
        table_data = init_table_data()
        table_data = d.populate_dialects_table_data(output_mode, table_data)
        table_data.update(table)
        table_data = set_unique_columns(table_data)
    else:
        table_data = table
        is_it_table = False

    if is_it_table:
        table_data = process_is_it_table_item(table_data, tables_dict)

    table_data = normalize_ref_columns_in_final_output(table_data)

    d.dialects_clean_up(output_mode, table_data)
    return table_data


def result_format(
    result: List[Dict], output_mode: str, group_by_type: bool
) -> List[Dict]:
    """method to format final output after parser"""
    final_result = []
    tables_dict = {}
    for table in result:
        # process each item in parser output
        if "index_name" in table or "alter_table_name" in table:
            tables_dict = process_alter_and_index_result(
                tables_dict, table, output_mode
            )
        else:
            # process tables, types, sequence and etc. data
            table_data = process_entities(tables_dict, table, output_mode)
            final_result.append(table_data)
    if group_by_type:
        final_result = group_by_type_result(final_result)
    return final_result


def process_is_it_table_item(table_data: Dict, tables_dict: Dict) -> Dict:
    if table_data.get("table_name"):
        tables_dict[(table_data["table_name"], table_data["schema"])] = table_data
    else:
        logger.error(
            "\n Something goes wrong. Possible you try to parse unsupported statement \n "
        )
    if not table_data.get("primary_key"):
        table_data = check_pk_in_columns_and_constraints(table_data)
    else:
        table_data = remove_pk_from_columns(table_data)

    if table_data.get("unique"):
        table_data = add_unique_columns(table_data)

    for column in table_data["columns"]:
        if column["name"] in table_data["primary_key"]:
            column["nullable"] = False
    return table_data


def normalize_ref_columns_in_final_output(table_data: Dict) -> Dict:
    # todo: this is hack, need to remove it
    if "references" in table_data:
        del table_data["references"]
    if "ref_columns" in table_data:
        for col_ref in table_data["ref_columns"]:
            name = col_ref["name"]
            for column in table_data["columns"]:
                if name == column["name"]:
                    del col_ref["name"]
                    column["references"] = col_ref
        del table_data["ref_columns"]
    return table_data


def set_column_unique_param(table_data: Dict, key: str) -> Dict:
    for column in table_data["columns"]:
        if key == "constraints":
            unique = table_data[key].get("unique", [])
            if unique:
                check_in = unique["columns"]
            else:
                check_in = []
        else:
            check_in = table_data[key]
        if column["name"] in check_in:
            column["unique"] = True
    return table_data


def set_unique_columns(table_data: Dict) -> Dict:

    unique_keys = ["unique_statement", "constraints"]

    for key in unique_keys:
        if table_data.get(key, None):
            # get column names from unique constraints & statements
            table_data = set_column_unique_param(table_data, key)
    if "unique_statement" in table_data:
        del table_data["unique_statement"]
    return table_data


def group_by_type_result(final_result: List[Dict]) -> Dict[str, List]:
    result_as_dict = {
        "tables": [],
        "types": [],
        "sequences": [],
        "domains": [],
        "schemas": [],
        "ddl_properties": [],
        "comments": [],
    }
    keys_map = {
        "table_name": "tables",
        "sequence_name": "sequences",
        "type_name": "types",
        "domain_name": "domains",
        "schema_name": "schemas",
        "tablespace_name": "tablespaces",
        "database_name": "databases",
        "value": "ddl_properties",
        "comments": "comments",
    }
    for item in final_result:
        for key in keys_map:
            if key in item:
                _type = result_as_dict.get(keys_map.get(key))
                if _type is None:
                    result_as_dict[keys_map.get(key)] = []
                    _type = result_as_dict[keys_map.get(key)]
                if key != "comments":
                    _type.append(item)
                else:
                    _type.extend(item["comments"])
                break
    if result_as_dict["comments"] == []:
        del result_as_dict["comments"]
    return result_as_dict


def add_unique_columns(table_data: Dict) -> Dict:
    for column in table_data["columns"]:
        if column["name"] in table_data["unique"]:
            column["unique"] = True
    del table_data["unique"]
    return table_data


def remove_pk_from_columns(table_data: Dict) -> Dict:
    for column in table_data["columns"]:
        del column["primary_key"]
    return table_data


def check_pk_in_columns_and_constraints(table_data: Dict) -> Dict:
    pk = []
    for column in table_data["columns"]:
        if column["primary_key"]:
            pk.append(column["name"])
        del column["primary_key"]
    if table_data.get("constraints") and table_data["constraints"].get("primary_keys"):
        for key_constraints in table_data["constraints"]["primary_keys"]:
            pk.extend(key_constraints["columns"])
    table_data["primary_key"] = pk
    return table_data


def dump_data_to_file(table_name: str, dump_path: str, data: List[Dict]) -> None:
    """method to dump json schema"""
    if not os.path.isdir(dump_path):
        os.makedirs(dump_path, exist_ok=True)
    with open("{}/{}_schema.json".format(dump_path, table_name), "w+") as schema_file:
        json.dump(data, schema_file, indent=1)
