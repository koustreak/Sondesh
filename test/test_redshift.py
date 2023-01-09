import pprint

from ddl_compare import parse_the_ddl

def test_redshift():

    ddl = '''
        create table sales(
            salesid integer not null,
            listid integer not null,
            sellerid integer not null,
            buyerid integer not null encode auto,
            eventid integer not null encode mostly16,
            dateid smallint not null,
            qtysold smallint not null encode mostly8,
            pricepaid decimal(8,2) encode delta32k,
            commission decimal(8,2) encode delta32k,
            saletime timestamp,
            primary key(salesid),
            foreign key(listid) references listing(listid),
            foreign key(sellerid) references users(userid),
            foreign key(buyerid) references users(userid),
            foreign key(dateid) references date(dateid)
            )
            distkey(listid)
            compound sortkey(listid,sellerid)
    '''
    result = parse_the_ddl(ddl).run(group_by_type=True, output_mode="redshift")
    pprint.pprint(result)

test_redshift()