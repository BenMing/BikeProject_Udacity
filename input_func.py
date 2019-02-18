#!/usr/bin/env python
# coding: utf-8

# In[1]:


def get_user_input(message, month_day_list):
    """
    获取用户输入月份/星期
    Args:
        (str) message - 指示用户输入什么信息
        (str) month_day_list - 数据集中可查的月份或星期列表
    Returns:
        (str) user_input - 用户输入
    """

    while True:
        user_input = input(message).lower()
        if user_input in month_day_list:
            break
        if user_input == 'all':
            break
        else:
            print("我没看懂你说的是什么。")

    return user_input
