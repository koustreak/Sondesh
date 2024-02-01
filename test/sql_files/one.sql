create table sales(
            salesid integer not null,
            listid integer not null,
            sellerid integer not null,
            buyerid integer not null encode auto,
            eventid integer not null encode mostly16,
            dateid smallint,
            qtysold smallint not null encode mostly8,
            pricepaid decimal(8,2) encode delta32k,
            commission decimal(8,2) encode delta32k,
            saletime timestamp,
            test_col varchar(160),
            test_col2 varchar(130),
            primary key(salesid),
            foreign key(listid) references listing(listid),
            foreign key(sellerid) references users(userid),
            foreign key(buyerid) references users(userid),
            foreign key(dateid) references date(dateid)
            )
          diststyle auto1
          compound sortkey(salesid,sellerid);