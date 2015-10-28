#!/usr/bin/env  python2
#-*- coding=utf-8 -*-
#Author:shizhongxian@126.com
#2015-06


import sys


type = sys.getfilesystemencoding()


def Rec2Table(rec_filename,table_name,max_fields_num=100):
    '''
    
    '''
    fout = open(table_name,"w")
    fin    = open(rec_filename)
    line = fin.readline()
    if line.strip() !="<REC>":
        print "REC文件内容不正确，请检查文件:".decode("utf-8").encode(type),rec_filename
        sys.exit()
    indicators = []
    index_num = 0
    #获取指标名称
    while line:
        line = fin.readline()
        if line.strip() !="<REC>":
            pos  = line.find(">=")
            indicator = line[1:pos]
            indicators.append(indicator)
            index_num += 1
        elif  line.strip() == "<REC>":
            break
        if index_num > max_fields_num:
            print "REC文件的字段超过了最大字段限制,请检查REC文件,或增大max_fields_num参数".decode("utf-8").encode(type)
            break;
    fin.close()
    fout.write("\t".join(indicators)+"\n")
    #
    print "当前REC文件中指标为:".decode("utf-8").encode(type)
    for indicator in indicators:
        print indicator.decode("utf-8").encode(type)
    # 转化为table
    line_no  = 0
    fin    = open(rec_filename)
    line = fin.readline()
    values = []
    records = 0
    while line:
        line = fin.readline()
        line_no += 1
        if line.strip() != "<REC>":
            pos = line.find(">=")
            value = line[pos+2:]
            value = value.strip()
            values.append(value) 
        if line.strip() == "<REC>":
            #判断列表长度是否等于指标数
            if len(values) == index_num:
                #输出值
                fout.write("\t".join(values)+"\n")
                records += 1
            values = []
    fout.close()
    print "转化".decode("utf-8").encode(type),records,"条记录".decode("utf-8").encode(type)
    return table_name
    

    
if __name__ == "__main__":
    fin_name = sys.argv[1]
    fout_name = sys.argv[2]
    #Rec2Table("N2015040068.txt", "N2015040068_rec.txt",max_fields_num=200)
    #Rec2Table("2010_2015_allmonth.txt", "2010_2015_allmonth_table.txt",max_fields_num=200)
    Rec2Table(fin_name, fout_name, max_fields_num=200)
    print "End!"
                   
         
        
