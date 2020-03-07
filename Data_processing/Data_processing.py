# -*- encoding:utf-8 -*-
"""
@作者：刘锐
@文件名：QTPY.py
@时间：2019/11/11  12:37
@文档说明:
"""
import os
import random
from globalvar import globalvar as gb
from PyQt5.QtWidgets import (QMessageBox)

'''
"Database_file"  数据库创建时的文件夹路径
"Public_substring" 自动判断的特征字符
'''


def Line_analysis():
    """
    读取数据库中第一个文件，判断其数据处理类型，并且返回文件中的文件列表, 对应数据长度
    """
    path = gb.get_value("Database_file")
    fileList = os.listdir(path)  # 将目录中的数据全部加入列表
    try:
        fileList = sorted(fileList, key=lambda x: os.path.getmtime(os.path.join(path, x)))  # 安照文件修改时间排序
        file_path = path + "/" + fileList[0]
        with open(file_path, "r") as fo:
            Data_list = fo.readlines()
        Random_list = random.sample(Data_list, 10)  # 随机抽取的数据

    except UnicodeDecodeError:
        QMessageBox.warning(None, "严重错误", "(%s)文件读取失败因为该文件的编码格式不对，请将格式改为UTF-8或ANSI"
                            % fileList[0], QMessageBox.Yes)
        Result = 0, 0, 0, 0, 0, 0 , 0, 0
        return Result
    except:
        QMessageBox.warning(None, "严重错误", "请选择正确的数据库", QMessageBox.Yes)
        Result = 0, 0, 0, 0, 0, 0, 0, 0
        return Result
    Data = Data_list[0]  # 取第一个文件第一行的数据去判断
    Line_list = Data.split(",")
    Data_length = len(Line_list)

    if Data_length == 3:  # 如果分割后数量大于2则是2列数据
        Data_processing_judgment = 3

        separator = ","
        seq = Line_list[0:-1]  # 字符串序列
        Line = separator.join(seq) + "\n"  # 由于最后的一个数据自带/n,去掉后需要手动加

        Line_length = len(Line)  # 去除时间后的数据整体长度
        First_length = len(Line_list[0] + "\n")  # 第一列数据长度
        Second_length = len(Line_list[1] + "\n")  # 第二列数据长度

        Public_substring = 0

        First_Public_substring, length = getNumofCommonSubstr(Random_list[0].split(",")[0], Random_list[1].split(",")[0])  # 求出第一列数据的特征
        for i in range(10):
            First_Eventually_substring, length = getNumofCommonSubstr(First_Public_substring, Random_list[i].split(",")[0])
            if First_Eventually_substring == First_Public_substring:
                pass
            else:
                First_Public_substring = First_Eventually_substring  # 如果字符串和
                continue

        Second_Public_substring, length = getNumofCommonSubstr(Random_list[0].split(",")[1], Random_list[1].split(",")[1])  # 求出第二列数据的特征
        for i in range(10):
            Second_Eventually_substring, length = getNumofCommonSubstr(Second_Public_substring, Random_list[i].split(",")[1])
            if Second_Eventually_substring == Second_Public_substring:
                pass
            else:
                Second_Public_substring = Second_Eventually_substring  # 如果字符串和
                continue

    elif Data_length == 2:
        Data_processing_judgment = 2

        Line_length = len(Data)  # 去除时间后的数据整体长度
        First_length = len(Line_list[0] + "\n")  # 第一列数据长度
        Second_length = len(Line_list[1])  # 第二列数据长度

        Public_substring = 0

        First_Public_substring, length = getNumofCommonSubstr(Random_list[0].split(",")[0], Random_list[1].split(",")[0])  # 求出第一列数据的特征
        for i in range(10):
            First_Eventually_substring, length = getNumofCommonSubstr(First_Public_substring, Random_list[i].split(",")[0])
            if First_Eventually_substring == First_Public_substring:
                pass
            else:
                First_Public_substring = First_Eventually_substring  # 如果字符串和
                continue

        Second_Public_substring, length = getNumofCommonSubstr(Random_list[0].split(",")[1], Random_list[1].split(",")[1])  # 求出第二列数据的特征
        for i in range(10):
            Second_Eventually_substring, length = getNumofCommonSubstr(Second_Public_substring, Random_list[i].split(",")[1])
            if Second_Eventually_substring == Second_Public_substring:
                pass
            else:
                Second_Public_substring = Second_Eventually_substring  # 如果字符串和
                continue

    elif Data_length == 1:
        Line_length = len(Data)  # 去除时间后的数据整体长度
        First_length = 0  # 第一列数据长度
        Second_length = 0  # 第二列数据长度
        Data_processing_judgment = 1

        Public_substring, length = getNumofCommonSubstr(Random_list[0], Random_list[1])  # 先求出第一个和第二的第一行数据的最长公共字符串
        for i in range(10):
            Eventually_substring, length = getNumofCommonSubstr(Public_substring, Random_list[i])
            if Eventually_substring == Public_substring:
                pass
            else:
                Public_substring = Eventually_substring  # 如果字符串和
                continue
        First_Public_substring = 0
        Second_Public_substring = 0

    else:
        Data_processing_judgment = 0
        Line_length = 0
        First_length = 0  # 第一列数据长度
        Second_length = 0  # 第二列数据长度

        Public_substring = 0
        First_Public_substring = 0
        Second_Public_substring = 0

    Result = fileList, Data_processing_judgment, Line_length, First_length, Second_length, Public_substring\
        , First_Public_substring, Second_Public_substring

    return Result
    # 返回文件夹中文件列表，数据处理判断位，整行长度，一列长度，二列长度，预判特征字符

########################################################################################################################

def Single_processing(path, file_now, Line_length, Public_substring, Single_data: dict, Line_length_error: list,
                      Repeated_code_error: dict, Public_substring_error: list):
    """
    没有逗号的数据，即 Data_processing_judgment = 1 的情况，只需要整行的去重,特征判断，数据长度判断即可
    """


    try:
        with open(path, "r") as fo:
            Data = fo.readlines()
            Number_lines_count_now = 0  # 行数计算
        for line_now in Data:
            Number_lines_count_now += 1
            if Line_length != len(line_now):
                Line_length_error.append((line_now, file_now, Number_lines_count_now))  # 存储，数据，文件，行数
                continue

            if Public_substring not in line_now:
                Public_substring_error.append((line_now, file_now, Number_lines_count_now))  # 存储，数据，文件，行数
                continue

            if line_now in Single_data:  # 如果数据在数据库中
                Repeated_code_list = []
                if line_now in  Repeated_code_error:  # 如果数据在重码数据中
                    Repeated_code_list = Repeated_code_error[line_now]
                    Repeated_code_list.append((line_now, file_now, Number_lines_count_now))
                    Repeated_code_error[line_now] = Repeated_code_list
                else:

                    line, file, Number_lines_count, count = Single_data[line_now]  # 取出第一个数据的信息
                    Repeated_code_list.append((line, file, Number_lines_count))
                    Repeated_code_list.append((line_now, file_now, Number_lines_count_now))
                    Repeated_code_error[line_now] = Repeated_code_list
                    # 重码数据的数据结构为：字典{"http://s.jnc.cn/?c=LA8QCYK5H15":[(line, file, Number_lines_count),...]}
            else:
                Single_data[line_now] = (line_now, file_now, Number_lines_count_now, 1)  # 将数据放入去重的字典,存入第一个，忽略后面的数据
    except UnicodeDecodeError:
        return False
    return True

########################################################################################################################

def Double_Entirety_processing(path, file_now, Line_length, Single_data: dict, Line_length_error: list,
                               Repeated_code_error: dict):
    """
    没有逗号的数据，即 Data_processing_judgment = 1 的情况，只需要整行的去重,特征判断，数据长度判断即可
    """

    try:
        with open(path, "r") as fo:
            Data = fo.readlines()
            Number_lines_count_now = 0  # 行数计算
        for line_now in Data:
            Number_lines_count_now += 1
##################数据整体进行长度检验、重码检验###############################
            if Line_length != len(line_now):
                Line_length_error.append((line_now, file_now, Number_lines_count_now))  # 存储，数据，文件，行数
                continue
            if line_now in Single_data:  # 如果数据在数据库中
                Repeated_code_list = []
                if line_now in  Repeated_code_error:  # 如果数据在重码数据中
                    Repeated_code_list = Repeated_code_error[line_now]
                    Repeated_code_list.append((line_now, file_now, Number_lines_count_now))
                    Repeated_code_error[line_now] = Repeated_code_list
                else:

                    line, file, Number_lines_count, count = Single_data[line_now]  # 取出第一个数据的信息
                    Repeated_code_list.append((line, file, Number_lines_count))
                    Repeated_code_list.append((line_now, file_now, Number_lines_count_now))
                    Repeated_code_error[line_now] = Repeated_code_list
                    # 重码数据的数据结构为：字典{"http://s.jnc.cn/?c=LA8QCYK5H15":[(line, file, Number_lines_count),...]}
            else:
                Single_data[line_now] = (line_now, file_now, Number_lines_count_now, 1)  # 将数据放入去重的字典,存入第一个，忽略后面的数据

    except UnicodeDecodeError:
        return False
    return True

def Double_First_processing(Single_data: dict, First_length, First_length_error: list, First_Public_substring,
                            First_data: dict, First_Public_substring_error: list, First_Repeated_code_error: dict):
    First_data_list = Single_data.items()  # 返回键值对，该值为去掉整体重码，长度不符后的数据
    for data in First_data_list:
        line_key, Data_pool = data  # 对应字符串，和数据合集
        line, file_name, Number_lines, count = Data_pool  # 取出数据合集中的值
        line_list = line.split(",")
        First_line = line_list[0] + "\n"  # 需要夹换行符
        if First_length != len(First_line):  # 如果长度不符合预期
            First_length_error.append(Data_pool[0:-1])
            continue
        elif First_Public_substring not in First_line:  # 如果特征不在其中
            First_Public_substring_error.append(Data_pool[0:-1])
            continue
        if First_line in First_data:  # 如果数据在数据库中
            Repeated_code_list = []
            if First_line in First_Repeated_code_error:  # 如果数据在重码数据中
                Repeated_code_list = First_Repeated_code_error[First_line]
                Repeated_code_list.append((line, file_name, Number_lines))
                First_Repeated_code_error[First_line] = Repeated_code_list
            else:
                line_age, file_age, Number_lines_count_age, count_age = First_data[First_line]  # 取出第一个数据的信息
                Repeated_code_list.append((line_age, file_age, Number_lines_count_age))
                Repeated_code_list.append((line, file_name, Number_lines))
                First_Repeated_code_error[First_line] = Repeated_code_list
                # 重码数据的数据结构为：字典{"http://s.jnc.cn/?c=LA8QCYK5H15":[(line, file, Number_lines_count),...]}
                # 重码数据的数据结构为：字典{"http://s.jnc.cn/?c=LA8QCYK5H15":[(line, file, Number_lines_count),...]}
        else:
            First_data[First_line] = (line, file_name, Number_lines, 1)  # 将数据放入去重的字典,存入第一个，忽略后面的数据

    return True

def Double_Second_processing(First_data: dict, Second_length, Second_length_error: list, Second_Public_substring,
                             Second_data: dict, Second_Public_substring_error: list, Second_Repeated_code_error: dict):
    Second_data_list = First_data.items()  # 返回键值对，该值为去掉整体重码，长度不符后的数据
    for data in Second_data_list:
        line_key, Data_pool = data  # 对应字符串，和数据合集
        line, file_name, Number_lines, count = Data_pool  # 取出数据合集中的值
        line_list = line.split(",")
        Second_line = line_list[1]
        if Second_length != len(Second_line):  # 如果长度不符合预期
            Second_length_error.append(Data_pool[0:-1])
            continue
        elif Second_Public_substring not in Second_line:  # 如果特征不在其中
            Second_Public_substring_error.append(Data_pool[0:-1])
            continue
        if Second_line in Second_data:  # 如果数据在数据库中
            Repeated_code_list = []
            if Second_line in Second_Repeated_code_error:  # 如果数据在重码数据中
                Repeated_code_list = Second_Repeated_code_error[Second_line]
                Repeated_code_list.append((line, file_name, Number_lines))
                Second_Repeated_code_error[Second_line] = Repeated_code_list
            else:
                line_age, file_age, Number_lines_count_age, count_age = Second_data[Second_line]  # 取出第一个数据的信息
                Repeated_code_list.append((line_age, file_age, Number_lines_count_age))
                Repeated_code_list.append((line, file_name, Number_lines))
                Second_Repeated_code_error[Second_line] = Repeated_code_list
                # 重码数据的数据结构为：字典{"http://s.jnc.cn/?c=LA8QCYK5H15":[(line, file, Number_lines_count),...]}
        else:
            Second_data[Second_line] = (line, file_name, Number_lines, 1)  # 将数据放入去重的字典,存入第一个，忽略后面的数据

    return True

########################################################################################################################

def Three_Entirety_processing(path, file_now, Line_length, Single_data: dict, Line_length_error: list,
                               Repeated_code_error: dict):
    """
    没有逗号的数据，即 Data_processing_judgment = 1 的情况，只需要整行的去重,特征判断，数据长度判断即可
    """

    try:
        with open(path, "r") as fo:
            Data = fo.readlines()
            Number_lines_count_now = 0  # 行数计算
        for line_original in Data:
            Line_list = line_original.split(",")
            separator = ","
            seq = Line_list[0:-1]  # 字符串序列
            line_now = separator.join(seq) + "\n"  # 由于最后的一个数据自带/n,去掉后需要手动加

            Number_lines_count_now += 1
            ##################数据整体进行长度检验、重码检验###############################
            if Line_length != len(line_now):
                Line_length_error.append((line_original, file_now, Number_lines_count_now))  # 存储，数据，文件，行数
                continue
            if line_now in Single_data:  # 如果数据在数据库中
                Repeated_code_list = []
                if line_now in  Repeated_code_error:  # 如果数据在重码数据中
                    Repeated_code_list = Repeated_code_error[line_now]
                    Repeated_code_list.append((line_original, file_now, Number_lines_count_now))
                    Repeated_code_error[line_now] = Repeated_code_list
                else:

                    line, file, Number_lines_count, count = Single_data[line_now]  # 取出第一个数据的信息
                    Repeated_code_list.append((line, file, Number_lines_count))
                    Repeated_code_list.append((line_original, file_now, Number_lines_count_now))
                    Repeated_code_error[line_now] = Repeated_code_list
                    # 重码数据的数据结构为：字典{"http://s.jnc.cn/?c=LA8QCYK5H15":[(line, file, Number_lines_count),...]}
            else:
                Single_data[line_now] = (line_original, file_now, Number_lines_count_now, 1)  # 将数据放入去重的字典,存入第一个，忽略后面的数据

    except UnicodeDecodeError:
        return False
    return True

def Three_First_processing(Single_data: dict, First_length, First_length_error: list, First_Public_substring,
                            First_data: dict, First_Public_substring_error: list, First_Repeated_code_error: dict):
    First_data_list = Single_data.items()  # 返回键值对，该值为去掉整体重码，长度不符后的数据
    for data in First_data_list:
        line_key, Data_pool = data  # 对应字符串，和数据合集
        line, file_name, Number_lines, count = Data_pool  # 取出数据合集中的值
        line_list = line_key.split(",")
        First_line = line_list[0] + "\n"  # 需要夹换行符
        if First_length != len(First_line):  # 如果长度不符合预期
            First_length_error.append(Data_pool[0:-1])
            continue
        elif First_Public_substring not in First_line:  # 如果特征不在其中
            First_Public_substring_error.append(Data_pool[0:-1])
            continue
        if First_line in First_data:  # 如果数据在数据库中
            Repeated_code_list = []
            if First_line in First_Repeated_code_error:  # 如果数据在重码数据中
                Repeated_code_list = First_Repeated_code_error[First_line]
                Repeated_code_list.append((line, file_name, Number_lines))
                First_Repeated_code_error[First_line] = Repeated_code_list
            else:
                line_age, file_age, Number_lines_count_age, count_age = First_data[First_line]  # 取出第一个数据的信息
                Repeated_code_list.append((line_age, file_age, Number_lines_count_age))
                Repeated_code_list.append((line, file_name, Number_lines))
                First_Repeated_code_error[First_line] = Repeated_code_list
                # 重码数据的数据结构为：字典{"http://s.jnc.cn/?c=LA8QCYK5H15":[(line, file, Number_lines_count),...]}
                # 重码数据的数据结构为：字典{"http://s.jnc.cn/?c=LA8QCYK5H15":[(line, file, Number_lines_count),...]}
        else:
            First_data[First_line] = (line, file_name, Number_lines, 1)  # 将数据放入去重的字典,存入第一个，忽略后面的数据
    return True

def Three_Second_processing(First_data: dict, Second_length, Second_length_error: list, Second_Public_substring,
                             Second_data: dict, Second_Public_substring_error: list, Second_Repeated_code_error: dict):
    Second_data_list = First_data.items()  # 返回键值对，该值为去掉整体重码，长度不符后的数据
    for data in Second_data_list:
        line_key, Data_pool = data  # 对应字符串，和数据合集
        line, file_name, Number_lines, count = Data_pool  # 取出数据合集中的值
        line_list = line.split(",")
        Second_line = line_list[1] + "\n"
        if Second_length != len(Second_line):  # 如果长度不符合预期
            Second_length_error.append(Data_pool[0:-1])
            continue
        elif Second_Public_substring not in Second_line:  # 如果特征不在其中
            Second_Public_substring_error.append(Data_pool[0:-1])
            continue
        if Second_line in Second_data:  # 如果数据在数据库中
            Repeated_code_list = []
            if Second_line in Second_Repeated_code_error:  # 如果数据在重码数据中
                Repeated_code_list = Second_Repeated_code_error[Second_line]
                Repeated_code_list.append((line, file_name, Number_lines))
                Second_Repeated_code_error[Second_line] = Repeated_code_list
            else:
                line_age, file_age, Number_lines_count_age, count_age = Second_data[Second_line]  # 取出第一个数据的信息
                Repeated_code_list.append((line_age, file_age, Number_lines_count_age))
                Repeated_code_list.append((line, file_name, Number_lines))
                Second_Repeated_code_error[Second_line] = Repeated_code_list
                # 重码数据的数据结构为：字典{"http://s.jnc.cn/?c=LA8QCYK5H15":[(line, file, Number_lines_count),...]}
        else:
            Second_data[Second_line] = (line, file_name, Number_lines, 1)  # 将数据放入去重的字典,存入第一个，忽略后面的数据

    return True

########################################################################################################################

def Dispose_Single_processing(path, file_now, Line_length, Public_substring, Single_data: dict, Line_length_error: list,
                              Repeated_code_error: dict, Public_substring_error: list):
    """
    没有逗号的数据，即 Data_processing_judgment = 1 的情况，只需要整行的去重,特征判断，数据长度判断即可
    """
    try:
        with open(path, "r") as fo:
            Data = fo.readlines()
            Number_lines_count_now = 0  # 行数计算
        for line_now in Data:
            Number_lines_count_now += 1

            if Line_length != len(line_now):
                Line_length_error.append((line_now, file_now, Number_lines_count_now))  # 存储，数据，文件，行数
                continue

            if Public_substring not in line_now:
                Public_substring_error.append((line_now, file_now, Number_lines_count_now))  # 存储，数据，文件，行数
                continue
            if line_now in Single_data:  # 如果数据在数据库中
                Repeated_code_list = []
                if line_now in  Repeated_code_error:  # 如果数据在重码数据中
                    Repeated_code_list = Repeated_code_error[line_now]
                    Repeated_code_list.append((line_now, file_now, Number_lines_count_now))
                    Repeated_code_error[line_now] = Repeated_code_list
                else:
                    line, file, Number_lines_count, count = Single_data[line_now]  # 取出第一个数据的信息
                    Repeated_code_list.append((line, file, Number_lines_count))
                    Repeated_code_list.append((line_now, file_now, Number_lines_count_now))
                    Repeated_code_error[line_now] = Repeated_code_list
                    # 重码数据的数据结构为：字典{"http://s.jnc.cn/?c=LA8QCYK5H15":[(line, file, Number_lines_count),...]}
            else:
                Single_data[line_now] = (line_now, file_now, Number_lines_count_now, 1)  # 将数据放入去重的字典,存入第一个，忽略后面的数据
    except UnicodeDecodeError:
        return False
    return True

########################################################################################################################

def Dispose_Double_Entirety_processing(path, file_now, Line_length, Read_data: dict, Single_data: dict, Line_length_error: list,
                               Repeated_code_error: dict):
    """
    没有逗号的数据，即 Data_processing_judgment = 1 的情况，只需要整行的去重,特征判断，数据长度判断即可
    """
    Single_data_list = Read_data.items()
    for i in Single_data_list:
        key, valve = i
        line, filename, Number_lines_count, count = valve  # 将值中的数据取出
        Single_data[line] = (line, filename, Number_lines_count, count)
    try:
        with open(path, "r") as fo:
            Data = fo.readlines()
            Number_lines_count_now = 0  # 行数计算
        for line_now in Data:
            Number_lines_count_now += 1
##################数据整体进行长度检验、重码检验###############################
            if Line_length != len(line_now):
                Line_length_error.append((line_now, file_now, Number_lines_count_now))  # 存储，数据，文件，行数
                continue
            if line_now in Single_data:  # 如果数据在数据库中
                Repeated_code_list = []
                if line_now in  Repeated_code_error:  # 如果数据在重码数据中
                    Repeated_code_list = Repeated_code_error[line_now]
                    Repeated_code_list.append((line_now, file_now, Number_lines_count_now))
                    Repeated_code_error[line_now] = Repeated_code_list
                else:

                    line, file, Number_lines_count, count = Single_data[line_now]  # 取出第一个数据的信息
                    Repeated_code_list.append((line, file, Number_lines_count))
                    Repeated_code_list.append((line_now, file_now, Number_lines_count_now))
                    Repeated_code_error[line_now] = Repeated_code_list
                    # 重码数据的数据结构为：字典{"http://s.jnc.cn/?c=LA8QCYK5H15":[(line, file, Number_lines_count),...]}
            else:
                Single_data[line_now] = (line_now, file_now, Number_lines_count_now, 1)  # 将数据放入去重的字典,存入第一个，忽略后面的数据

    except UnicodeDecodeError:
        return False
    return True

def Dispose_Double_First_processing(Single_data: dict, First_length, First_length_error: list, First_Public_substring,
                            First_data: dict, First_Public_substring_error: list, First_Repeated_code_error: dict):
    First_data_list = Single_data.items()  # 返回键值对，该值为去掉整体重码，长度不符后的数据
    for data in First_data_list:
        line_key, Data_pool = data  # 对应字符串，和数据合集
        line, file_name, Number_lines, count = Data_pool  # 取出数据合集中的值
        line_list = line.split(",")
        First_line = line_list[0] + "\n"  # 需要夹换行符
        if First_length != len(First_line):  # 如果长度不符合预期
            First_length_error.append(Data_pool[0:-1])
            continue
        elif First_Public_substring not in First_line:  # 如果特征不在其中
            First_Public_substring_error.append(Data_pool[0:-1])
            continue
        if First_line in First_data:  # 如果数据在数据库中
            Repeated_code_list = []
            if First_line in First_Repeated_code_error:  # 如果数据在重码数据中
                Repeated_code_list = First_Repeated_code_error[First_line]
                Repeated_code_list.append((line, file_name, Number_lines))
                First_Repeated_code_error[First_line] = Repeated_code_list
            else:
                line_age, file_age, Number_lines_count_age, count_age = First_data[First_line]  # 取出第一个数据的信息
                Repeated_code_list.append((line_age, file_age, Number_lines_count_age))
                Repeated_code_list.append((line, file_name, Number_lines))
                First_Repeated_code_error[First_line] = Repeated_code_list
                # 重码数据的数据结构为：字典{"http://s.jnc.cn/?c=LA8QCYK5H15":[(line, file, Number_lines_count),...]}
                # 重码数据的数据结构为：字典{"http://s.jnc.cn/?c=LA8QCYK5H15":[(line, file, Number_lines_count),...]}
        else:
            First_data[First_line] = (line, file_name, Number_lines, 1)  # 将数据放入去重的字典,存入第一个，忽略后面的数据
    return True

def Dispose_Double_Second_processing(First_data: dict, Second_length, Second_length_error: list, Second_Public_substring,
                             Second_data: dict, Second_Public_substring_error: list, Second_Repeated_code_error: dict):
    Second_data_list = First_data.items()  # 返回键值对，该值为去掉整体重码，长度不符后的数据
    for data in Second_data_list:
        line_key, Data_pool = data  # 对应字符串，和数据合集
        line, file_name, Number_lines, count = Data_pool  # 取出数据合集中的值
        line_list = line.split(",")
        Second_line = line_list[1]
        if Second_length != len(Second_line):  # 如果长度不符合预期
            Second_length_error.append(Data_pool[0:-1])
            continue
        elif Second_Public_substring not in Second_line:  # 如果特征不在其中
            Second_Public_substring_error.append(Data_pool[0:-1])
            continue
        if Second_line in Second_data:  # 如果数据在数据库中
            Repeated_code_list = []
            if Second_line in Second_Repeated_code_error:  # 如果数据在重码数据中
                Repeated_code_list = Second_Repeated_code_error[Second_line]
                Repeated_code_list.append((line, file_name, Number_lines))
                Second_Repeated_code_error[Second_line] = Repeated_code_list
            else:
                line_age, file_age, Number_lines_count_age, count_age = Second_data[Second_line]  # 取出第一个数据的信息
                Repeated_code_list.append((line_age, file_age, Number_lines_count_age))
                Repeated_code_list.append((line, file_name, Number_lines))
                Second_Repeated_code_error[Second_line] = Repeated_code_list
                # 重码数据的数据结构为：字典{"http://s.jnc.cn/?c=LA8QCYK5H15":[(line, file, Number_lines_count),...]}
        else:
            Second_data[Second_line] = (line, file_name, Number_lines, 1)  # 将数据放入去重的字典,存入第一个，忽略后面的数据

    return True
########################################################################################################################

def Dispose_Three_Entirety_processing(path, file_now, Line_length, Read_data: dict, Single_data: dict, Line_length_error: list,
                               Repeated_code_error: dict):
    """
    没有逗号的数据，即 Data_processing_judgment = 1 的情况，只需要整行的去重,特征判断，数据长度判断即可
    """
    Single_data_list = Read_data.items()
    for i in Single_data_list:
        key, valve = i
        line, filename, Number_lines_count, count = valve  # 将值中的数据取出
        Line_list = line.split(",")
        separator = ","
        seq = Line_list[0:-1]  # 字符串序列
        line_now = separator.join(seq) + "\n"  # 由于最后的一个数据自带/n,去掉后需要手动加
        Single_data[line_now] = (line, filename, Number_lines_count, count)
    try:
        with open(path, "r") as fo:
            Data = fo.readlines()
            Number_lines_count_now = 0  # 行数计算
        for line_original in Data:
            Line_list = line_original.split(",")
            separator = ","
            seq = Line_list[0:-1]  # 字符串序列
            line_now = separator.join(seq) + "\n"  # 由于最后的一个数据自带/n,去掉后需要手动加

            Number_lines_count_now += 1
            ##################数据整体进行长度检验、重码检验###############################
            if Line_length != len(line_now):
                Line_length_error.append((line_original, file_now, Number_lines_count_now))  # 存储，数据，文件，行数
                continue
            if line_now in Single_data:  # 如果数据在数据库中
                Repeated_code_list = []
                if line_now in  Repeated_code_error:  # 如果数据在重码数据中
                    Repeated_code_list = Repeated_code_error[line_now]
                    Repeated_code_list.append((line_original, file_now, Number_lines_count_now))
                    Repeated_code_error[line_now] = Repeated_code_list
                else:

                    line_age, file_age, Number_lines_count_age, count_age = Single_data[line_now]  # 取出第一个数据的信息
                    Repeated_code_list.append((line_age, file_age, Number_lines_count_age))
                    Repeated_code_list.append((line_original, file_now, Number_lines_count_now))
                    Repeated_code_error[line_now] = Repeated_code_list
                    # 重码数据的数据结构为：字典{"http://s.jnc.cn/?c=LA8QCYK5H15":[(line, file, Number_lines_count),...]}
            else:
                Single_data[line_now] = (line_original, file_now, Number_lines_count_now, 1)  # 将数据放入去重的字典,存入第一个，忽略后面的数据
    except UnicodeDecodeError:
        return False
    return True

def Dispose_Three_First_processing(Single_data: dict, First_length, First_length_error: list, First_Public_substring,
                            First_data: dict, First_Public_substring_error: list, First_Repeated_code_error: dict):
    First_data_list = Single_data.items()  # 返回键值对，该值为去掉整体重码，长度不符后的数据
    for data in First_data_list:
        line_key, Data_pool = data  # 对应字符串，和数据合集
        line, file_name, Number_lines, count = Data_pool  # 取出数据合集中的值
        line_list = line_key.split(",")
        First_line = line_list[0] + "\n"  # 需要夹换行符
        if First_length != len(First_line):  # 如果长度不符合预期
            First_length_error.append(Data_pool[0:-1])
            continue
        elif First_Public_substring not in First_line:  # 如果特征不在其中
            First_Public_substring_error.append(Data_pool[0:-1])
            continue
        if First_line in First_data:  # 如果数据在数据库中
            Repeated_code_list = []
            if First_line in First_Repeated_code_error:  # 如果数据在重码数据中
                Repeated_code_list = First_Repeated_code_error[First_line]
                Repeated_code_list.append((line, file_name, Number_lines))
                First_Repeated_code_error[First_line] = Repeated_code_list
            else:
                line_age, file_age, Number_lines_count_age, count_age = First_data[First_line]  # 取出第一个数据的信息
                Repeated_code_list.append((line_age, file_age, Number_lines_count_age))
                Repeated_code_list.append((line, file_name, Number_lines))
                First_Repeated_code_error[First_line] = Repeated_code_list
                # 重码数据的数据结构为：字典{"http://s.jnc.cn/?c=LA8QCYK5H15":[(line, file, Number_lines_count),...]}
                # 重码数据的数据结构为：字典{"http://s.jnc.cn/?c=LA8QCYK5H15":[(line, file, Number_lines_count),...]}
        else:
            First_data[First_line] = (line, file_name, Number_lines, 1)  # 将数据放入去重的字典,存入第一个，忽略后面的数据
    return True

def Dispose_Three_Second_processing(First_data: dict, Second_length, Second_length_error: list, Second_Public_substring,
                             Second_data: dict, Second_Public_substring_error: list, Second_Repeated_code_error: dict):
    Second_data_list = First_data.items()  # 返回键值对，该值为去掉整体重码，长度不符后的数据
    for data in Second_data_list:
        line_key, Data_pool = data  # 对应字符串，和数据合集
        line, file_name, Number_lines, count = Data_pool  # 取出数据合集中的值
        line_list = line.split(",")
        Second_line = line_list[1] + "\n"
        if Second_length != len(Second_line):  # 如果长度不符合预期
            Second_length_error.append(Data_pool[0:-1])
            continue
        elif Second_Public_substring not in Second_line:  # 如果特征不在其中
            Second_Public_substring_error.append(Data_pool[0:-1])
            continue
        if Second_line in Second_data:  # 如果数据在数据库中
            Repeated_code_list = []
            if Second_line in Second_Repeated_code_error:  # 如果数据在重码数据中
                Repeated_code_list = Second_Repeated_code_error[Second_line]
                Repeated_code_list.append((line, file_name, Number_lines))
                Second_Repeated_code_error[Second_line] = Repeated_code_list
            else:
                line_age, file_age, Number_lines_count_age, count_age = Second_data[Second_line]  # 取出第一个数据的信息
                Repeated_code_list.append((line_age, file_age, Number_lines_count_age))
                Repeated_code_list.append((line, file_name, Number_lines))
                Second_Repeated_code_error[Second_line] = Repeated_code_list
                # 重码数据的数据结构为：字典{"http://s.jnc.cn/?c=LA8QCYK5H15":[(line, file, Number_lines_count),...]}
        else:
            Second_data[Second_line] = (line, file_name, Number_lines, 1)  # 将数据放入去重的字典,存入第一个，忽略后面的数据
    return True

########################################################################################################################
def getNumofCommonSubstr(str1, str2):
    """
    读取数据库中第一个文件，判断其特征字符
    """
    lstr1 = len(str1)
    lstr2 = len(str2)
    record = list([0 for i in range(lstr2)] for j in range(lstr1))  # 多一位
    maxNum = 0  # 最长匹配长度
    p = 0  # 匹配的起始位

    for i in range(lstr1):
        for j in range(lstr2):
            if str1[i] == str2[j]:
                # 相同则累加
                record[i][j] = record[i - 1][j - 1] + 1
                if record[i][j] > maxNum:
                    # 获取最大匹配长度
                    maxNum = record[i][j]
                    # 记录最大匹配长度的终止位置
                    p = i + 1
    return str1[p - maxNum:p], maxNum
