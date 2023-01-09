import pyfiglet
from colorama import Fore,Back, init,Style
from time import sleep
from tqdm import tqdm
import sys
import os
import json
from rich.console import Console
from rich.table import Table
from collections import defaultdict

init()

print()
print()

def print_cli_table(df,context_name=None):
    if df:
        print(Fore.CYAN + 'visualizing ' + context_name + ' parse result ' + Style.RESET_ALL)
        for i in df:
            table = Table(title='column details for '+i['table_name'])
            columns = ["column_name", "column_type", "size", "foreign_key", "refers_to",
                       "on_delete", "on_update", "unique", "nullable", "default", "check"]
            data = list()
            if i['columns']:
                for j in i['columns']:
                    refers_to, on_delete, on_update, is_foreign_key = None, None, None, None

                    if j.get('references'):
                        refers_to = str(j.get('references').get('table'))
                    if j.get('on_delete'):
                        on_delete = str(j.get('references').get('on_delete'))
                    if j.get('on_update'):
                        on_update = str(j.get('references').get('on_update'))
                    if j.get('references'):
                        is_foreign_key = 'yes'

                    data.append([str(j.get('name')), str(j.get('type')), str(j.get('size')),
                                 is_foreign_key, refers_to, on_delete, on_update,
                                 str(j.get('unique')), str(j.get('nullable')), str(j.get('default')),
                                 str(j.get('check'))])
            else:
                print(Fore.YELLOW + 'warning!! no column could be found in first sql' + Style.RESET_ALL)

            for col in columns:
                table.add_column(col)
            for row in data:
                table.add_row(*row, style='bright_green')

            console = Console()
            print(Fore.BLUE + '*****************************************************************************************'+Style.RESET_ALL)
            console.print(table)
            print()

        for i in df :
            table = Table(title='column details for ' + i['table_name'])
            columns = ['table property name','property value']
            data = [
                ['index', str(i.get('index'))],
                ['diststyle', str(i.get('diststyle'))],
                ['distkey', str(i.get('distkey'))],
                ['primary key', str(i.get('primary_key'))],
                ['sort key', str(i.get('sortkey'))],
                ['schema', str(i.get('schema'))],
                ['table space', str(i.get('tablespace'))]
            ]

            for col in columns:
                table.add_column(col)
            for row in data:
                table.add_row(*row, style='bright_green')

            console = Console()
            console.print(table)
            print(Fore.BLUE +'*****************************************************************************************'+Style.RESET_ALL)
            print()

    else:
        print(Fore.RED + 'Error occurred while parsing ' + context_name + ' aborting ' + Style.RESET_ALL)

f = pyfiglet.Figlet(font='big')
print(Fore.CYAN + f.renderText('Compare DDL') + Style.RESET_ALL)
sleep(0.5)
print(Fore.BLUE + '> author : koushik dutta ')
sleep(0.5)
print(Fore.BLUE + '> date : 28-Dec-2022 ')
sleep(0.5)
print(Fore.BLUE + '> purpose : compare two DDL ')
sleep(0.5)
print(Fore.BLUE + '> version : 1.0.0 ')
sleep(0.5)
print(Fore.BLUE + '> OS : ubuntu 18.04 ')
sleep(0.5)
print(Fore.BLUE + '> python version : 3.8 ')
sleep(0.5)
print(Fore.BLUE + '> help : please give me a star in github ')
sleep(0.6)
print(Fore.BLUE + '> docs : read the docs making is in progress ')
sleep(0.6)
print(Fore.BLUE + '> unit test : check ddl_compare/tests ')
sleep(0.6)
print(Fore.BLUE + '> powered by : Flex and YACC in python ')
sleep(0.6)
print(Fore.BLUE + '> Supported DDL : Redshift , Oracle , Mysql , sparkSQL ( tested ) ' + Style.RESET_ALL)
print()
print(Fore.BLUE)

with tqdm(total=100) as pbar:
    pbar.set_description('initiating process')
    pbar.update(3)
    sleep(0.5)
    try:
        from ddl_compare.dialects import redshift
        pbar.update(10)
        pbar.set_description('Loading Redshift Dialect')
    except:
        print(Fore.RED + 'No Redshift Dialect detected , aborting . To fix it contact koushik')
        sys.exit()

    try:
        sleep(0.5)
        from ddl_compare.dialects import oracle
        pbar.update(10)
        pbar.set_description('Loading Oracle Dialect')
    except:
        print(Fore.RED + 'No Oracle Dialect detected , aborting . To fix it contact koushik')
        sys.exit()

    try:
        sleep(0.5)
        from ddl_compare.dialects import spark_sql
        pbar.update(12)
        pbar.set_description('Loading spark sql Dialect')
    except:
        print(Fore.RED + 'No spark sql Dialect detected , aborting . To fix it contact koushik')
        sys.exit()

    try:
        sleep(0.5)
        from ddl_compare.dialects import sql
        pbar.update(25)
        pbar.set_description('Loading ansi sql Dialect')
    except:
        print(Fore.RED + 'No Ansi sql Dialect detected , aborting . To fix it contact koushik')
        sys.exit()

    try:
        sleep(0.5)
        from ddl_compare.dialects import mysql
        pbar.update(10)
        pbar.set_description('Loading mysql Dialect')
    except:
        print(Fore.RED + 'No mysql Dialect detected , aborting . To fix it contact koushik')
        sys.exit()

    try:
        sleep(0.5)
        from ddl_compare.dialects import hql
        pbar.update(10)
        pbar.set_description('Loading HiveQL Dialect')
    except:
        print(Fore.RED + 'No hiveQL Dialect detected , aborting . To fix it contact koushik')
        sys.exit()

    try:
        sleep(0.5)
        from ddl_compare.ddl_parser import parse_from_file
        pbar.update(12)
        pbar.set_description('Loading SQL file parser')
    except:
        print(Fore.RED + 'No .sql file parser detected , aborting . To fix it contact koushik')
        sys.exit()

    try:
        sleep(0.5)
        from ddl_compare.ddl_parser import  parse_the_ddl
        pbar.update(8)
        pbar.set_description('Loading raw sql parser')
    except:
        print(Fore.RED + 'No raw sql parser detected , aborting . It is required to parse from user input .'
                         ' To fix it contact koushik')
        sys.exit()

    pbar.set_description('Everything is loaded')

print()
print(Fore.GREEN + "All dialects and parser have been loaded successfully"+ Style.RESET_ALL)
print()
print()

if os.path.exists('profile.json') and os.path.getsize('profile.json'):
    print(Fore.BLUE + 'Profile already exist , proceeding with that , if you want to reset remove profile.json')
    print()
else:
    while True:

        print(Fore.BLUE + 'There is no profile of you , let me set one , don\'t worry i m not a spy and this is one time only \n' + Style.RESET_ALL)
        name = input(Fore.BLUE + '> what should i call you : '+Style.RESET_ALL)
        print(Fore.BLUE + '  >> hey '+name+' welcome to DDL Comparator '+'\n')
        favourite_db = input(Fore.BLUE + '> which DB you like most : '+Style.RESET_ALL)
        purpose = input(Fore.BLUE + '> are you going to use it for commercial purpose : '+Style.RESET_ALL)
        what_you_do = input(Fore.BLUE + '> what is your job role : '+Style.RESET_ALL)
        default_outdir = input(Fore.BLUE + '> default output dir for report (leave blank for current directory) : ' + Style.RESET_ALL)
        cloud_platform = input(Fore.BLUE + '> which cloud platform you are going to use : ' + Style.RESET_ALL)
        print()
        profile = {name:name,favourite_db:favourite_db,
                   purpose:purpose,what_you_do:what_you_do,
                   default_outdir:default_outdir,cloud_platform:cloud_platform}
        with open('profile.json', 'w') as fp:
            json.dump(profile,fp)
        print(Fore.CYAN + 'profile has setup successfully \n'+ Style.RESET_ALL)
        break

# Validation profiler will be setup accordingly
# if os.path.exists('validation.json') and os.path.getsize('profile.json'):
error_ct = 0
choice = 'none'
while True and error_ct<2:
    choice = input(Fore.CYAN + 'Do you want to compare file or provide SQL as user input (please type either file or raw) \n'+Style.RESET_ALL)
    if choice.upper() not in ('FILE','RAW'):
        print(Fore.RED + 'Wrong input given , answer should be either file or raw '+Style.RESET_ALL)
        error_ct+=1
    elif error_ct == 2:
        print(Fore.RED + 'You have crossed maximum limit of choice , aborting '+Style.RESET_ALL)
        sys.exit()
    else:
        print(Fore.CYAN + 'You have entered '+choice+' for this session '+Style.RESET_ALL)
        break

print()

err_dialect = 0
while True and err_dialect < 2:
    dialect = input(Fore.BLUE + '> Which dialect you want to use now , \n'
                                '1.redshift\n2.oracle\n3.hql\n4.snowflake\n5.mysql\n'+Style.RESET_ALL)
    if dialect.upper() not in ['REDSHIFT','ORACLE','SNOWFLAKE','MYSQL','HQL']:
        print(Fore.RED + 'Please enter a valid value '+Style.RESET_ALL)
        err_dialect+=1
    elif err_dialect == 2:
        print(Fore.RED + 'Exceeded maximum limit of providing input'+Style.RESET_ALL)
        sys.exit()
    else:
        break

print()

while True:
    if choice.upper() == 'FILE':
        first_file = input(Fore.BLUE + '> Your first .sql file ? '+Style.RESET_ALL)
        second_file = input(Fore.BLUE + '> Your first .sql file ? ' + Style.RESET_ALL)
        print()

        if os.path.exists(first_file) and os.path.getsize(first_file) :
            if os.path.splitext(first_file)[1].upper() != '.SQL':
                print(Fore.YELLOW + ' WARNING !! your first input '+first_file+' is not a .sql file '+Style.RESET_ALL)
                print()
        else:
            print(Fore.RED + ' file not found '+first_file+Style.RESET_ALL)
            print()
            sys.exit()

        if os.path.exists(second_file) and os.path.getsize(second_file):
            if os.path.splitext(second_file)[1].upper() != '.SQL':
                print(Fore.YELLOW + ' WARNING !! your second input '+second_file+' is not a .sql file '+Style.RESET_ALL)
                print()
        else:
            print(Fore.RED + ' file not found '+second_file+Style.RESET_ALL)
            print()
            sys.exit()

        print(Fore.CYAN + 'parsing '+first_file+Style.RESET_ALL)
        first_file_parse_result = parse_from_file(first_file)
        print(Fore.CYAN + 'done!!'+first_file+Style.RESET_ALL)

        print()

        print(Fore.CYAN + 'parsing '+second_file+Style.RESET_ALL)
        second_file_parse_result = parse_from_file(second_file)
        print(Fore.CYAN + 'done!!'+first_file+Style.RESET_ALL)

        print()

        print_cli_table(first_file_parse_result,'first_file_parse_result')
        print()
        print_cli_table(second_file_parse_result, 'second_file_parse_result')
        print()

    else:
        first_sql_input = input(Fore.BLUE + 'Please enter your first sql '+Style.RESET_ALL)
        second_sql_input = input(Fore.BLUE + 'Please enter your second sql ' + Style.RESET_ALL)

        if first_sql_input is None or second_sql_input is None:
            print(Fore.RED + 'Please provide both of the mandatory input'+Style.RESET_ALL)

        print(Fore.CYAN + 'parsing first_sql_input '+ Style.RESET_ALL)
        first_sql_parse_result = parse_from_file(first_sql_input)
        print(Fore.CYAN + 'done!!' + Style.RESET_ALL)

        print()

        print(Fore.CYAN + 'parsing second_sql_input ' + Style.RESET_ALL)
        second_sql_parse_result = parse_from_file(second_sql_input)
        print(Fore.CYAN + 'done!!' + Style.RESET_ALL)

        print()

        print_cli_table(first_sql_parse_result, 'first_sql_parse_result')
        print()
        print_cli_table(second_sql_parse_result, 'second_sql_parse_result')
        print()

    choice = input(Fore.CYAN + '> Do you want to use the tool again ? N for No , press anything else for Yes '+Style.RESET_ALL)
    if choice.upper() == 'N':
        print(Fore.CYAN + 'Good Bye , have a good day\n'+ Style.RESET_ALL)
        break
    else:
        continue