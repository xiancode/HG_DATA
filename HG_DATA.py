#!/sur/bin/env  python2
#-*-coding=utf-8-*-



import os
import string
import operator


def get_year_and_month(startyear=2011,startmonth=1,endyear=2015,endmonth=4):
    '''
    
    '''
    year_month_list = []
    for i in range(startyear,endyear):
        for j in range(startmonth,13):
            year_month_list.append(str(i)+"年-"+str(j)+"月")
    for j in range(1,endmonth+1):
            year_month_list.append(str(endyear)+"年-"+str(j)+"月")
    return year_month_list
        
    
    

def get_file_from_dir(dirname):
    '''
    返回目录下的文件名
    相对路径
    '''
    file_list = []
    for root,dirs,filenames in os.walk(dirname):
        for filename in filenames:
            file_list.append(os.path.join(root,filename))
    return file_list

def replace_growth(s):
    '''
    
    '''
    return string.replace(s, "同比增长", '')


def replace_im_ex(s):
    if s.find("进口") != -1:
        return string.replace(s, "进口","进出口")
    elif s.find("出口") != -1:
        return  string.replace(s, "出口","进出口")

def sorteddict(d):
    '''
    
    '''
    return [(k,d[k]) for k in sorted(d.keys())]


def save_table_data(indicator_dir):
    '''
    
    '''
    file_list = get_file_from_dir(indicator_dir)
    
    fin = open("2010_2015_allmonth_table.txt")
    data = fin.readlines()[1:]
    
    for filename in file_list:
        print "process:",filename
        #filename = "HG_INDICATOR/HG1.txt"
        out_file_name = "HG_CLS_DATA/"+ os.path.basename(filename)[:-4]+"_data.txt"
        #out_file_name = "HG_CLS_DATA/"+ "test"+"_data.txt"
        fout = open(out_file_name,"w")
        with open(filename) as f:
            lines = f.readlines()[1:]
            line_no = 0
            for line in lines:
                line_no += 1
                if line_no%50 == 0:
                    print line_no
                line = line.strip()
                slist = line.split("=")
                if len(slist) == 2:
                    indicator = slist[1]
                    for item in data:
                        #line_no += 1
                        #if line_no % 100000==0:
                            #print line_no
                        item_list = item.split("\t")
                        #print indicator,"----"
                        #print item_list[0],"----"
                        if indicator == item_list[0]:    
                            item = item.strip()
                            fout.write(item+"\t"+"stats"+"\n")
        fout.close()
    fin.close()
    
def explor_growth_indicator(indicator_dir):
    '''
    '''
    no_growth_indicators_tables = []
    file_list = get_file_from_dir(indicator_dir)
    for filename in file_list:
        #filename ="HG_INDICATOR/HG1.txt"
        print "processing:",filename
        with open(filename) as f:
            lines = f.readlines()[1:]
            base_indicators = set()
            growth_indicator = set()
            for line in lines:
                line = line.strip()
                item_list = line.split("=")
                if len(item_list) == 2:
                    indicator = item_list[1]
                    if indicator.find("同比增长") == -1:
                        base_indicators.add(indicator)
                    else:
                        growth_indicator.add(indicator)
        #替换‘同比增长’字符串
        growth_indicator = map(replace_growth, growth_indicator)
        growth_indicator = set(growth_indicator)
        if len(base_indicators) == len(growth_indicator):
            print "同比指标和基本指标个数相等",len(growth_indicator)
            if base_indicators.issubset(growth_indicator) and growth_indicator.issubset(base_indicators):
                print "同比指标和基本指标完全相同"
            else:
                print "同比指标和基本指标不完全相同"
        else:
            print "同比指标个数不等于基本指标个数"
            print "同比指标个数:",len(growth_indicator)
            print "基本指标个数:",len(base_indicators)
            no_growth_indicators_tables.append(filename)
    print '\n'.join(no_growth_indicators_tables)
    
    
def generate_up_value(indicator_dir):
    '''
    
    '''
    file_list = get_file_from_dir(indicator_dir)
    #file_list = ['HG_CLS_DATA/HG1_data.txt']
    
    for filename in file_list:
        print filename
        #对HG20_data文件,计算分地区进出口综合
        if filename.find('HG20_data') !=-1:
            location_trade(filename)
            
        #以指标 地区 地区代码 月份为Key
        #以年份 数值 为value建立字典
        base_data_dict = {}
        indicator_set = set()
        with open(filename) as f:
            lines = f.readlines()
            for line in lines:
                line = line.strip()
                item_list = line.split('\t')
                #判断行内格式是否正确
                if len(item_list) == 8:
                    indicator = item_list[0].strip('[S]')
                    indicator_set.add(indicator)
                    area,area_code,year,month,num,unit = item_list[1:-1]
                    key = indicator+'@'+area+'@'+area_code+'@'+month
                    value_tmp_list = [year,num,unit]
                    if base_data_dict.has_key(key):
                        base_data_dict[key].append(value_tmp_list)
                    else:
                        base_data_dict.setdefault(key,[])
        #找到需要计算同比增长的指标
        #indicator_list = base_data_dict.keys()
        base_indicators = set()
        growth_indicators = set()
        for indicator in indicator_set:
            if indicator.find("同比增长") == -1:
                base_indicators.add(indicator)
            else:
                growth_indicators.add(indicator)
        #calculate_indicators = set()
        growth_indicators = map(replace_growth, growth_indicators)
        growth_indicators = set(growth_indicators)
        #需要计算同比增长的指标集
        calculate_indicators = set()
        if len(base_indicators) == len(growth_indicators):
            print "同比指标和基本指标个数相等",len(growth_indicators)
            if base_indicators.issubset(growth_indicators) and growth_indicators.issubset(base_indicators):
                print "同比指标和基本指标完全相同"
            else:
                print "同比指标和基本指标不完全相同"
                calculate_indicators = base_indicators - growth_indicators
                print calculate_indicators
        else:
            print "同比指标个数不等于基本指标个数"
            print "同比指标个数:",len(growth_indicators)
            print "基本指标个数:",len(base_indicators)
            calculate_indicators = base_indicators - growth_indicators
                #print '\n'.join(calculate_indicators)
            #按照月份来计算同比增长
        cal_resut = []
        if len(calculate_indicators) > 0:
            for key,value_list in base_data_dict.iteritems():
                tmp_indicator = key.split('@')[0]
                if tmp_indicator in calculate_indicators:
                    num_dict = {}
                    for year_item in value_list:
                        if len(year_item) == 3:
                            year,num,unit = year_item
                            year_no = year.strip('年')
                            num_dict[string.atoi(year_no)] = [string.atof(num),unit]
                        #对词典 按照年份排序 生成序列
                    sorted_list = sorteddict(num_dict)
                    up_nums = []
                    for i in range(len(sorted_list)-1):
                        #判断年份是否相差为1年
                        if sorted_list[i+1][0]-sorted_list[i][0]==1:
                            cur_cal_year = sorted_list[i+1][0]
                            #list
                            cur_num_unit = sorted_list[i+1][1]
                            #list
                            last_num_unit = sorted_list[i][1]
                                #判断单位是否相同
                            if cur_num_unit[1] == last_num_unit[1]:
                                ratio_num = round((cur_num_unit[0]/last_num_unit[0]-1)*100,2)
                                #print (cur_num_unit[0]/last_num_unit[0]-1)*100
                                
                                up_nums.append([cur_cal_year,ratio_num])
                            else:
                                print key,cur_cal_year,"单位不统一"
                        #保存计算得到的数据
                    out_indicator,out_area,out_area_code,out_month = key.split('@')
                    out_indicator += "同比增长[S]"
                    for item in up_nums:
                        out_year = item[0]
                        out_num = item[1]
                        cal_resut.append([out_indicator,out_area,out_area_code,str(out_year),out_month,str(out_num),"%","calculated"])
            #outfilename = "/home/jay/workspace_new/HG_DATA/HG_CAL_DATA/" + os.path.basename(filename)[:-4]+"_calculated.txt"
            outfilename = filename
            #fout = open(outfilename,'w')
            fout = open(outfilename,'a+')        
            for line in cal_resut:
                fout.write('\t'.join(line)+"\n")
            fout.close()    
        #
        print filename,"calculate end!"
        
def trade_top(filename = 'HG_CLS_DATA/HG7_data.txt',cal_year='2015年',cal_month='1月'):
    '''
    
    '''
    year_num = string.atoi(cal_year.strip("年"))
    last_year = str(year_num-1)+"年"
    #filename = 'HG_CLS_DATA/HG7_data.txt'
    #国家 [出口 ,进口]
    cur_data_dict = {}
    last_data_dict = {}
    #indicator_set = set()
    with open(filename) as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip()
            item_list = line.split('\t')
            #判断行内格式是否正确
            if len(item_list) == 8:
                area,area_code,year,month,num,unit = item_list[1:-1]
                indicator = item_list[0]
                if year == cal_year and month == cal_month and indicator.find('组织')==-1 and indicator.find('联盟')==-1  and indicator.find('洲')==-1:
                    indicator = item_list[0]
                    pos1 = indicator.find(',')
                    pos2 = indicator.find(')[')
                    trade_area = indicator[pos1+1:pos2]
                    if cur_data_dict.has_key(trade_area):
                        if indicator.find('出口') != -1:
                            cur_data_dict[trade_area][0] = string.atof(num)
                        elif indicator.find('进口') != -1:
                            cur_data_dict[trade_area][1] = string.atof(num)
                    else:
                        cur_data_dict.setdefault(trade_area,['-','-'])
                        if indicator.find('出口') != -1:
                            cur_data_dict[trade_area][0] = string.atof(num)
                        elif indicator.find('进口') != -1:
                            cur_data_dict[trade_area][1] = string.atof(num)
                elif year==last_year and month == cal_month:
                    indicator = item_list[0]
                    pos1 = indicator.find(',')
                    pos2 = indicator.find(')[')
                    trade_area = indicator[pos1+1:pos2]
                    if last_data_dict.has_key(trade_area):
                        if indicator.find('出口') != -1:
                            last_data_dict[trade_area][0] = string.atof(num)
                        elif indicator.find('进口') != -1:
                            last_data_dict[trade_area][1] = string.atof(num)
                    else:
                        last_data_dict.setdefault(trade_area,['-','-'])
                        if indicator.find('出口') != -1:
                            last_data_dict[trade_area][0] = string.atof(num)
                        elif indicator.find('进口') != -1:
                            last_data_dict[trade_area][1] = string.atof(num)
        #顺差
        cur_tmp_list = []
        for k,v in cur_data_dict.iteritems():
            if len(v) == 2 and v[0]!='-' and v[1]!='-':
                cur_tmp_list.append((k,v[0]-v[1]))
        last_tmp_dict = {}
        for k,v in last_data_dict.iteritems():
            if len(v) == 2 and v[0]!='-' and v[1]!='-':
                last_tmp_dict[k] = v[0]-v[1]
        
        outfile_name = "HG_CAL_DATA/" + cal_year + "_" + cal_month + "_" + "trade_area_data.txt"
        #fout = open("HG_CAL_DATA/trade_area_data.txt","w")
        fout = open(outfile_name,"w")
        #顺差从小到大排序
        cur_tmp_list.sort(key=operator.itemgetter(1))
        #顺差国家  
        fb_area = cur_tmp_list[-10:]
        for item in fb_area:
            fout.write(item[0]+"\t"+str(item[1])+"\t"+str(last_tmp_dict[item[0]])+"\n")
        #逆差国家
        fout.write("\n")
        ub_area =cur_tmp_list[:10] 
        for item in ub_area:
            fout.write(item[0]+"\t"+str(item[1])+"\t"+str(last_tmp_dict[item[0]])+"\n")
        #tmp_list.sort(key=operator.itemgetter(1))
        
def save_to_xls(start_time='2011年1月',end_time='2015年5月'):
    '''
    
    '''
    
    
def location_trade(filename = 'HG_CLS_DATA/HG20_data.txt'):
    '''
    
    '''
    print filename
    print "计算商品出口总额(经营单位所在地)数据"
    year_months = get_year_and_month()
    for tmp_time in year_months:
        item_list = tmp_time.split('-')
        if len(item_list) == 2:
            cal_year = item_list[0]
            cal_month = item_list[1]
            cal_data = []
            with open(filename) as f:
                line = f.readline()
                while line:
                    #过滤掉同比数据
                    if line.find("同比增长") == -1:
                        item_list = line.split("\t")
                        if len(item_list) == 8:
                            indicator,area,area_code,year,month,num,unit = item_list[0:-1]
                            #获取特定年份、月份数据
                            if year == cal_year and month == cal_month:
                                if indicator == "商品出口总额(经营单位所在地)[S]" or indicator == "商品进口总额(经营单位所在地)[S]":
                                    indicator = area + indicator
                                else:
                                    pass    
                                #保存需要计算的指标和数值
                                cal_data.append([indicator,area,area_code,year,month,num,unit])
                    line = f.readline()
            ex_im_num_dict = {}
            for tmp_list in cal_data:
                if len(tmp_list) == 7:
                    indicator,area,area_code,year,month,num,unit = tmp_list
                    ex_im_indicator = replace_im_ex(indicator)
                    ex_im_num_dict.setdefault(ex_im_indicator,['-','-',area,area_code,year,month,num,unit])
                    #当前地区添加出口数据
                    if indicator.find("出口") !=-1:
                        ex_im_num_dict[ex_im_indicator][0] = string.atof(num)
                    #当前地区添加进口数据
                    elif indicator.find("进口") !=-1:
                        ex_im_num_dict[ex_im_indicator][1] = string.atof(num)
                    else:
                        print indicator,"指标不包含进口 出口"
            #输出数据         
            fout = open(filename,"a+")
            #fout = open("test.txt","a+")   
            for k,value_list in ex_im_num_dict.iteritems():
                ex_num,im_num,area,area_code,year,month,num,unit = value_list
                if ex_num !='-' and im_num !='-':
                    ex_im_sum = ex_num + im_num
                    out_list = [area,area_code,year,month,str(ex_im_sum),unit,"caculated"]
                    fout.write(k + "\t" + '\t'.join(out_list)+"\n")
            fout.close()
    print "所在地进出口数据计算结束!"
        
        
        

if __name__ == "__main__":
    #save_table_data("HG_INDICATOR/")
    #explor_growth_indicator("HG_INDICATOR/")
    generate_up_value("HG_CLS_DATA")
    #trade_top()
    #location_trade()
    #get_year_and_month()
    print "End!"
    
    
    
    
    
