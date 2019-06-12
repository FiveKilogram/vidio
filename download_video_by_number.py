#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from geek_time import download_video_by_array
from geek_time import fetch_my_column

if __name__ == "__main__":
    fetch_my_column()
    cid = int(input("input video column id\n> "))
    size = 100
    numbers = input("input Episode numbers like 1,3,4\n> ")
    numberArray = numbers.split(',')
    download_video_by_array(cid, numberArray, 100)
