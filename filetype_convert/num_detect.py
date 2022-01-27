#! /usr/local/bin/python3
# -*- coding: utf-8 -*-
"""
识别字符串是否为数值，如果为数值，返回浮点数，否则返回原始字符串
基本思路为先判断是否能通过float转化
再分别讨论含有"_"、","和"%"的情况
主要用于txt转excel时的数字转换，防止excel中出现绿点
"""
import re


# 如果字符串中有%，有以下情况：
# 1. 有多个%号
# 2. 只有1个%号，但不在末尾
# 3. 只有1个%号，且在末尾
def percent_operate(word, word_type="single"):
    """

    :param word: 需要转化的字符串
    :param word_type: 字符串的类型，"single"表示只有%，"double"表示同时有%和逗号
    :return: 如果为数字，返回转化后的float格式，否则返回原始字符串
    """
    if len(re.findall("%", word)) > 1:
        # print(f"{word}:str")
        return word
    elif not word.endswith("%"):
        # print(f"{word}:str")
        return word
    else:
        try:
            if word_type == "double":
                word_after = word.replace(",", "").replace("%", "")
            else:
                word_after = word.replace("%", "")
            float(word_after)
            if isinstance(pass_operate(word_after), float):
                # print(f"{word}:num")
                point_position = word_after.find(".")
                if point_position > -1:
                    digits = len(word_after) - point_position + 1
                else:
                    digits = 2
                return round(float(word_after) / 100, digits)
            else:
                # print(f"{word}:str")
                return word
        except ValueError:
            # print(f"{word}:str")
            return word


# 如果能通过float()进行转化，仍可能存在以下情况：
# 1. 数字中含有下划线
def pass_operate(word):
    """

    :param word: 需要转化的字符串
    :return: 如果为数字，返回转化后的float格式，否则返回原始字符串
    """
    if "_" in word:
        # print(f"{word}:str")
        return word
    else:
        # print(f"{word}:num")
        return float(word)


# 如果无法通过float()进行转化，仍可能存在以下情况：
# 1. 数字中含有逗号
# 2. 数字中含有%号
# 3. 数字中同时含有逗号和%
def not_pass_operate(word):
    """

    :param word: 需要转化的字符串
    :return: 如果为数字，返回转化后的float格式，否则返回原始字符串
    """
    # find()函数如果找不到对应信息会返回-1
    # 如果同时含有逗号和%
    if word.find(",") != -1 and word.find("%") != -1:
        # print("既有逗号，还有%")
        return percent_operate(word, "double")
    # 如果有逗号
    elif word.find(",") != -1:
        # print("只有逗号")
        try:
            word_after = word.replace(",", "")
            float(word_after)
            return pass_operate(word_after)
        except ValueError:
            # print(f"{word}:str")
            return word
    # 如果有%
    elif word.find("%") != -1:
        # print("只有%")
        return percent_operate(word)
    else:
        # print(f"{word}:str")
        return word


# 判断是否能通过float转化
def type_trans(word):
    """

    :param word: 需要转化的字符串
    :return: 如果为数字，返回转化后的float格式，否则返回原始字符串
    """
    # 用float函数先看一下是否能转化为浮点数
    try:
        float(word)
        # print("通过float转化")
        return pass_operate(word)
    except ValueError:
        # print("未通过float转化")
        return not_pass_operate(word)


if __name__ == "__main__":
    print(f"-12.3转化后为：{type_trans('-12.3')}")
    print(f"-12,300转化后为：{type_trans('-12,300')}")
    print(f"-12.3%转化后为：{type_trans('-12.3%')}")
    print(f"-123%aa转化后为：{type_trans('-123%aa')}")
    print(f"-12_3%转化后为：{type_trans('-12_3%')}")
