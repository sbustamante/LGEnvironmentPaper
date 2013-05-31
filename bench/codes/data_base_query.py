# -*- coding: utf-8 -*-
#!/usr/bin/env python
from subprocess import call


def query_DB_satellites(outputpath="../data/", user="anonimo", passwd="secreto"):
    """
    Queries the multidark database to extract all the haloes in the box within a ID range.

    The output is stored as an ascii (CSV) file.
    """
    #define the output file
    outputfile=outputpath+"milky_way_satellites.csv"
    # Build the SQL query
    
    query   = "with milky_way_halos as (select * from Bolshoi..BDMW where snapnum=416  and Mvir > 5.0E11 and Mvir < 6.0E11  ) select sub.* from milky_way_halos mwh, Bolshoi..BDMW sub where sub.snapnum = 416 and  sub.hostFlag = mwh.bdmId"

    # Build the wget command to query the database
    website = "http://wget.multidark.org/MyDB?action=doQuery&SQL="
    username = user
    password = passwd
    
    wget_options=" --content-disposition --cookies=on --keep-session-cookies --save-cookies=cookie.txt --load-cookies=cookie.txt --auth-no-challenge" 
    wget_options=wget_options+" -O "+outputfile +" "
    wget_command="wget --http-user="+username+" --http-passwd="+password+" "+wget_options    
    command=wget_command + "\""+ website + query+"\""
    print ""
    print query
    print ""
    print command
    print ""
    # execute wget in shell
    retcode = call(command,shell=True)

query_DB_satellites(user="x", passwd="x")
