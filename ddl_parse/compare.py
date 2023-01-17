import json
import os
from colorama import Fore,Back, init,Style
from rich.console import Console
from rich.table import Table

init()

def compare_df(query_one_df,query_two_df,context_one,context_two):
    validator = None
    string_vs_varchar = None
    timezone_diff = None
    encoding_diff = None
    distyle_diff = None

    if os.path.exists('../validator.json') and os.path.getsize('../validator.json'):
        with open('../validator.json') as fp:
            validator = json.load(fp)
            if validator :
                string_vs_varchar = validator['string_vs_varchar']
                timezone_diff = validator['timezone_diff']
                encoding_diff = validator['encoding_diff']
                distyle_diff = validator['distyle_diff']

    if validator is None:
        print(Fore.YELLOW + ' WARNING !! User validator profile is Blank ')

    if query_one_df and query_two_df :
        print(Fore.CYAN + 'visualizing compare result ' + Style.RESET_ALL)
        table = Table(title='comparing '+context_one+' vs '+context_two+' column level ')
        table_tab = Table(title='comparing ' + context_one + ' vs ' + context_two+' table level ')

        difference_tab = []
        columns_tab = ["property name", "value in " + context_one, "value in " + context_two]

        if query_one_df.get('table_name')!=query_two_df.get('table_name'):
            difference_tab.append(['table name found in sql',query_one_df.get('table_name'),query_two_df.get('table_name')])

        if query_one_df.get('tablespace')!=query_two_df.get('tablespace'):
            difference_tab.append(['tablespace',query_one_df.get('tablespace'),query_two_df.get('tablespace')])

        if query_one_df.get('schema')!=query_two_df.get('schema'):
            difference_tab.append(['schema',query_one_df.get('schema'),query_two_df.get('schema')])

        keys_one = None
        keys_two = None
        type_one = None
        type_two = None


        if query_one_df.get('sortkey'):
            keys_one = ','.join(query_one_df.get('sortkey').get('keys'))
            type_one = query_one_df.get('sortkey').get('type')

        if query_two_df.get('sortkey'):
            keys_two = ','.join(query_two_df.get('sortkey').get('keys'))
            type_two = query_two_df.get('sortkey').get('type')

        if (keys_one != keys_two) and (keys_one or keys_two):
            difference_tab.append(['sort keys',keys_one,keys_two])

        if (type_one != type_two) and (type_one or type_two):
            difference_tab.append(['sort type',type_one,type_two])

        if query_two_df.get('index') != query_one_df.get('index'):
            difference_tab.append(['index',','.join(query_one_df.get('index')),','.join(query_two_df.get('index'))])

        if query_two_df.get('partitioned_by') != query_one_df.get('partitioned_by'):
            difference_tab.append(['partition',','.join(query_one_df.get('partitioned_by')),
                                   ','.join(query_two_df.get('partitioned_by'))])

        if query_two_df.get('diststyle') != query_one_df.get('diststyle'):
            difference_tab.append(['distribution style',query_one_df.get('diststyle'),query_two_df.get('diststyle')])

        if query_two_df.get('checks') != query_one_df.get('checks'):
            difference_tab.append(['checks constraints', ','.join(query_one_df.get('checks')),
                                   ','.join(query_two_df.get('checks'))])

        if difference_tab:
            for col in columns_tab:
                table_tab.add_column(col)
            for row in difference_tab:
                table_tab.add_row(*row, style='bright_green')
            # table level difference

            console = Console()
            print(Fore.BLUE + '*****************************************************************************************' + Style.RESET_ALL)
            console.print(table_tab)
            print()
        else:
            print()
            print(Fore.GREEN + 'No Table Level Difference could be found '+Style.RESET_ALL)

        columns = ["column name", "property" , "value in "+context_one, "value in "+context_two]

        query_one_cols = query_one_df['columns']
        query_two_cols = query_two_df['columns']

        difference = []

        for j in query_one_cols:
            refers_to_one, on_delete_one, on_update_one, is_foreign_key_one = None, None, None, None

            if j.get('references'):
                refers_to_one = str(j.get('references').get('table'))
            if j.get('on_delete'):
                on_delete_one = str(j.get('references').get('on_delete'))
            if j.get('on_update'):
                on_update_one = str(j.get('references').get('on_update'))
            if j.get('references'):
                is_foreign_key_one = 'yes'

            col_name_one = str(j.get('name'))
            col_type_one = str(j.get('type'))
            col_size_one = str(j.get('size'))
            isunique_one = str(j.get('unique'))
            isnull_one = str(j.get('nullable'))
            default_val_one = str(j.get('default'))
            check_val_one = str(j.get('check'))
            encode_one = str(j.get('encode'))

            temp_two = list(filter(lambda x:x['name']==col_name_one,query_two_cols))
            col_name_two = None
            if temp_two:
                temp_two = temp_two[0]
                col_name_two = str(temp_two.get('name'))
                col_type_two = str(temp_two.get('type'))
                col_size_two = str(temp_two.get('size'))
                isunique_two = str(temp_two.get('unique'))
                isnull_two = str(temp_two.get('nullable'))
                default_val_two = str(temp_two.get('default'))
                check_val_two = str(temp_two.get('check'))
                encode_two = str(temp_two.get('encode'))

                if col_type_one != col_type_two:
                    difference.append([col_name_two,'datatype',col_type_one,col_type_two])

                if col_size_two != col_size_one:
                    difference.append([col_name_two,'size',col_size_one,col_size_two])

                if isunique_two != isunique_one:
                    difference.append([col_name_two,'is unique',isunique_one,isunique_two])

                if isnull_one != isnull_two:
                    difference.append([col_name_two,'nullable',isnull_one,isnull_two])

                if default_val_two != default_val_one:
                    difference.append([col_name_two,'default value',default_val_one,default_val_two])

                if check_val_two != check_val_one:
                    difference.append([col_name_two,'check constraint',check_val_one,check_val_two])

                if encode_one != encode_two:
                    difference.append([col_name_two,'encode',encode_one,encode_two])

                refers_to_two, on_delete_two, on_update_two, is_foreign_key_two = None, None, None, None

                if j.get('references'):
                    refers_to_two = str(j.get('references').get('table'))
                if j.get('on_delete'):
                    on_delete_two = str(j.get('references').get('on_delete'))
                if j.get('on_update'):
                    on_update_two = str(j.get('references').get('on_update'))
                if j.get('references'):
                    is_foreign_key_two = 'yes'

                if is_foreign_key_two != is_foreign_key_one:
                    difference.append([col_name_two,'foreign key',is_foreign_key_one,is_foreign_key_two])

                if refers_to_two != refers_to_one:
                    difference.append([col_name_two,'foreign key reference',refers_to_one,refers_to_two])

                if on_delete_two != on_delete_one:
                    difference.append([col_name_two,'on delete clause',on_delete_one,on_delete_two])

                if on_update_two != on_update_one:
                    difference.append([col_name_two,'on update clause',on_update_one,on_update_two])

                query_two_cols = list(filter(lambda g:g['name']!=col_name_one,query_two_cols))

            else:
                difference.append([col_name_one,'is_found','yes','no'])

        if query_two_cols:
            for k in query_two_cols:
                difference.append([k['name'],'is_found','no','yes'])

        if difference:
            for col in columns:
                table.add_column(col)
            for row in difference:
                table.add_row(*row, style='bright_green')
            # table level difference

            console = Console()
            print(
                Fore.BLUE + '*****************************************************************************************' + Style.RESET_ALL)
            console.print(table)
            print()
        else:
            print()
            print(Fore.GREEN + 'No Column Level Difference could be found '+Style.RESET_ALL)
