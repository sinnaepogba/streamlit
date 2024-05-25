# prj 파일을 txt로 접근해서 바꿔주고 이걸 다시 prj 형태로 저장을 해서 그 파일을 엑셀 파일로 도출
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import subprocess
import random
import seaborn as sns
import math
import csv

Data_dir = "C:/Users/LAB_1/Desktop/new2/"

Prj_ = '1'
Prj_edit = '1_edit'


#%% 변수 지정

# 외기온도
outdoor_temp = 0

# 세대
number_of_unit = 4
for i in range(number_of_unit):
    unit_ELA = [1.2, 1.4, 1.5, 1.3]         # cm2/m2으로 고정
    unit_area = [90, 80, 100, 110]          # m2으로 고정
    envelope_area = [80, 90, 100, 110]      # m2으로 고정
    unit_temp = [20.3, 21.3, 22.3, 23.3]    # 섭씨로 고정
    unit_temp = list(map(str, [item + 273.15 for item in unit_temp]))
ELA_unit_door = 80                          # cm2으로 고정

# 복도
corridor_area = 30
corridor_temp = 14 + 273.15
ELA_corridor_window = 30

# 샤프트(엘레베이터, 계단실)
number_of_shaft = 4
for i in range(number_of_shaft):
    shaft_area = [30, 40, 50, 60]
    shaft_perimeter = [22, 26, 30, 34]
    shaft_temp = [14, 14.1, 14.2, 14.3]
    shaft_temp = list(map(str, [item + 273.15 for item in shaft_temp]))
ELA_shaft_door = 400

# 로비
ELA_main_door = 100
vestibule_area = 18
vestibule_temp = 7.5 + 273.15
lobby_temp = 10 + 273.15

# 층
floor_height = 2.87     # m로 고정
number_of_level = 40



area = [90, 80, 100, 110, 30, 30, 40, 50, 60]
temp = [20.3, 21.3, 22.3, 23.3, 14, 14, 14.1, 14.2, 14.3]
temp = list(map(str, [item + 273.15 for item in temp]))
ELA = [1.2, 1.4, 1.5, 1.3, ELA_corridor_window, ELA_unit_door, ELA_shaft_door, 1, 1, 1, 1, ELA_main_door]


#%% prj에서 CSV 파일로 데이터 옮기기

with open(Data_dir + Prj_ + '.prj', 'r') as prj:
    prj = prj.read()
    
# 텍스트를 줄 단위로 분할
lines = prj.split('\n')

with open(Data_dir + Prj_ + '.csv', 'w', newline='') as file:
    writer = csv.writer(file, delimiter=',')
    for line in lines:
        # 띄어쓰기로 분할하여 각 열을 CSV 파일에 쓰기
        writer.writerow(line.split())
        
# CSV 열고 데이터프레임으로 전환
with open(Prj_ + '.csv', 'r') as file:
    reader = csv.reader(file)
    csv_list = []
    for row in reader:
        csv_list.append(row)
    
data = pd.DataFrame(csv_list)


#%% 필요 함수

def basic(data, floor_height, iteration_level, icon):
    
    data[0][62] = iteration_level
    
    # ICON 넣기
    if iteration_level == 1:
        icon = 52
        index = 66
        replacement = [[14, 1, 1, 0], [15, 90, 1, 0], [17, 1, 90, 0], [16, 90, 90, 0],
                       [14, 15, 15, 0], [15, 75, 15, 0], [17, 15, 75, 0], [16, 75, 75, 0], 
                       [15, 40, 1, 0], [14, 50, 1, 0], [21, 40, 15, 0], [21, 50, 15, 0],
                       
                       [19, 45, 75, 0], [21, 45, 90, 0], [18, 75, 46, 0], [20, 90, 46, 0], [18, 1, 46, 0], [20, 15, 46, 0],
                       
                       [5, 22, 9, 9*(iteration_level-1)+1], [5, 72, 9, 9*(iteration_level-1)+2], [5, 22, 81, 9*(iteration_level-1)+3], [5, 72, 81, 9*(iteration_level-1)+4], [5, 45, 26, 9*(iteration_level-1)+5],
                       [23, 23, 1, 13*(iteration_level-1)+1], [23, 77, 1, 13*(iteration_level-1)+2], [23, 23, 90, 13*(iteration_level-1)+3], [23, 77, 90, 13*(iteration_level-1)+4], [23, 45, 15, 13*(iteration_level-1)+5],
                       
                       [18, 15, 30, 0], [15, 40, 30, 0], [20, 40, 45, 0], [18, 15, 45, 0], [18, 15, 60, 0], [16, 40, 60, 0], [14, 50, 30, 0], [20, 75, 30, 0], [18, 50, 45, 0], [20, 75, 45, 0], [17, 50, 60, 0], [20, 75, 60, 0],
                       
                       [23, 30, 15, 13*(iteration_level-1)+6], [23, 60, 15, 13*(iteration_level-1)+7], [23, 30, 75, 13*(iteration_level-1)+8], [23, 60, 75, 13*(iteration_level-1)+9],
                       
                       [5, 28, 38, 9*(iteration_level-1)+6], [5, 62, 38, 9*(iteration_level-1)+7], [5, 28, 52, 9*(iteration_level-1)+8], [5, 62, 52, 9*(iteration_level-1)+9],
                       [23, 30, 30, 13*(iteration_level-1)+10], [23, 60, 30, 13*(iteration_level-1)+11], [23, 30, 60, 13*(iteration_level-1)+12], [23, 60, 60, 13*(iteration_level-1)+13]]

    else:
        icon = 56
        index = 118 + (icon+2)*(iteration_level-2)
        replacement = [[iteration_level, (iteration_level-1)*floor_height, floor_height, 0, 0, 0, f'<{iteration_level}>'], ['!icn', 'col', 'row', '#'],
                        [14, 1, 1, 0], [15, 90, 1, 0], [17, 1, 90, 0], [16, 90, 90, 0],
                        [14, 15, 15, 0], [15, 75, 15, 0], [17, 15, 75, 0], [16, 75, 75, 0], 
                        [15, 40, 1, 0], [14, 50, 1, 0], [21, 40, 15, 0], [21, 50, 15, 0],
                        
                        [19, 45, 75, 0], [21, 45, 90, 0], [18, 75, 46, 0], [20, 90, 46, 0], [18, 1, 46, 0], [20, 15, 46, 0],
                        
                        [5, 22, 9, 9*(iteration_level-1)+1], [5, 72, 9, 9*(iteration_level-1)+2], [5, 22, 81, 9*(iteration_level-1)+3], [5, 72, 81, 9*(iteration_level-1)+4], [5, 45, 26, 9*(iteration_level-1)+5],
                        [23, 23, 1, 17*(iteration_level-2)+14], [23, 77, 1, 17*(iteration_level-2)+15], [23, 23, 90, 17*(iteration_level-2)+16], [23, 77, 90, 17*(iteration_level-2)+17], [23, 45, 15, 17*(iteration_level-2)+18],
                        
                        [18, 15, 30, 0], [15, 40, 30, 0], [20, 40, 45, 0], [18, 15, 45, 0], [18, 15, 60, 0], [16, 40, 60, 0], [14, 50, 30, 0], [20, 75, 30, 0], [18, 50, 45, 0], [20, 75, 45, 0], [17, 50, 60, 0], [20, 75, 60, 0],
                        
                        [23, 30, 15, 17*(iteration_level-2)+19], [23, 60, 15, 17*(iteration_level-2)+20], [23, 30, 75, 17*(iteration_level-2)+21], [23, 60, 75, 17*(iteration_level-2)+22],
                        
                        [5, 28, 38, 9*(iteration_level-1)+6], [5, 62, 38, 9*(iteration_level-1)+7], [5, 28, 52, 9*(iteration_level-1)+8], [5, 62, 52, 9*(iteration_level-1)+9],
                        [23, 30, 30, 17*(iteration_level-2)+23], [23, 60, 30, 17*(iteration_level-2)+24], [23, 30, 60, 17*(iteration_level-2)+25], [23, 60, 60, 17*(iteration_level-2)+26],
                        
                        [25, 29, 38, 17*(iteration_level-2)+27], [25, 63, 38, 17*(iteration_level-2)+28], [25, 29, 52, 17*(iteration_level-2)+29], [25, 63, 52, 17*(iteration_level-2)+30]]
    
    data = pd.concat([data.iloc[:index], pd.DataFrame(replacement), data.iloc[index:]]).reset_index(drop=True)
    
    if iteration_level == 1:
        index=64
    
    # n 변경
    data[3][index] = icon
    
    return data, icon


def coefficient(ELA):       # laminar flow, turbulent flow coefficient 산출
    ELA /= 1000
    ct = math.sqrt(2)*0.6*ELA/(10**0.15)
    ftrans = 0.0000181625*30*math.sqrt(ELA)
    ck = 0.0000181625*ftrans/(1.2041*math.pow(ftrans/(ct*math.sqrt(1.2041)), 1/0.65))
    
    return ck, ct


def flow_element(data, number_of_unit, iteration_flow_element, icon):
    
    index = 81 + (number_of_level-1)*(icon+2)+icon-4
    
    iteration_flow_element += 1
    data[0][index] = iteration_flow_element
    
    # 요소 넣기
    ck, ct = coefficient(ELA[iteration_flow_element-1])
    
    index += 3*(iteration_flow_element-1) + 1
    if iteration_flow_element <= number_of_unit:
        replacement = [[iteration_flow_element, 23, 'plr_leak3', f'leakage{iteration_flow_element}'],
                       [],
                       [ck, ct, 0.65, 0.6, 10, 0, 0, ELA[iteration_flow_element-1]/10000, 2, 2, 2, 0]]
    
    elif iteration_flow_element >= 8 and iteration_flow_element <= 11:
        replacement = [[iteration_flow_element, 23, 'plr_shaft', f'shaft{iteration_flow_element-7}'],
                       [],
                       [0.320452, 31.6044, 0.5, floor_height, shaft_area[iteration_flow_element-8], shaft_perimeter[iteration_flow_element-8], 0.1, 0, 0, 0, 0]]
    
    else:
        replacement = [[iteration_flow_element, 23, 'plr_leak1', f'leakage{iteration_flow_element}'],
                       [],
                       [ck, ct, 0.65, 0.6, 10, 0, 0, ELA[iteration_flow_element-1]/10000, 2, 2, 2, 0]]
        
    data = pd.concat([data.iloc[:index], pd.DataFrame(replacement), data.iloc[index:]]).reset_index(drop=True)
    
    return data, iteration_flow_element


def zone(data, icon, iteration_flow_element, iteration_level, iteration_zone):
    
    index = 91 + (number_of_level-1)*(icon+2)+icon-4 + 3*iteration_flow_element
    iteration_zone += 1
    
    data[0][index] = iteration_zone
    
    # 요소 넣기
    if iteration_zone == 1:
        index += iteration_zone
        replacement = [['!','Z#','f','s#', 'k#', 'l#', 'relHt', 'Vol', 'T0', 'P0', 'name', 'clr', 'u[4]', 'axs', 'cdvf', '<cdvf', 'name>', 'cfd', '<cfd', 'name>', '<1D', 'data:>'],
                       [iteration_zone, 3, 0, 0, 0, iteration_level, 0.000, floor_height*area[iteration_zone%9-1], temp[iteration_zone%9-1], 0, f'room{iteration_zone}', -1, 0, 2, 0, 0, 0, 0, 0]]
    else:
        index += iteration_zone + 1
        replacement = [[iteration_zone, 3, 0, 0, 0, iteration_level, 0.000, floor_height*area[iteration_zone%9-1], temp[iteration_zone%9-1], 0, f'room{iteration_zone}', -1, 0, 2, 0, 0, 0, 0, 0]]
    
    data = pd.concat([data.iloc[:index], pd.DataFrame(replacement), data.iloc[index:]]).reset_index(drop=True)
    
    return data, iteration_zone


def flow_path(data, number_of_unit, icon, iteration_flow_element, iteration_zone, iteration_level, iteration_flow_path):
    
    index = 95 + (number_of_level-1)*(icon+2)+icon-4 + 3*iteration_flow_element + iteration_zone+1
    iteration_flow_path += 1
    
    data[0][index] = iteration_flow_path
    
    # 요소 넣기
    direction = [4,4,1,1]
    
    if iteration_level == 1:
        if iteration_flow_path % 13 == 0:
            path_number = 13
        else:
            path_number = iteration_flow_path % 13
    else:
        if (iteration_flow_path-13) % 17 == 0:
            path_number = 17
        else:
            path_number = (iteration_flow_path-13) % 17
    
    
    if iteration_flow_path == 1:
        index += iteration_flow_path
        replacement = [['!','P#','f','n#', 'm#', 'e#', 'f#', 'w#', 'a#', 's#', 'c#', 'l#', 'X', 'Y', 'relHt', 'mult', 'wPset', 'wPmod', 'wazm', 'Fahs', 'Xmax', 'Xmin', 'icn', 'dir', 'u[4]', 'cdvf', '<cdvf', 'name>', 'cfd', '<cfd', 'data[4]>'],
                       [iteration_flow_path, 0, -1, 1, 1, 0,0,0,0,0,iteration_level, 0.000, 0.000, floor_height/2, envelope_area[path_number-1], 0, 0, -1, 0, 0, 0, 23, direction[path_number-1], -1, 0, 0, 0, 0, 0, 0]]
    
    elif path_number <= number_of_unit:
        index += iteration_flow_path + 1
        replacement = [[iteration_flow_path, 0, -1, 9*(iteration_level-1)+path_number, path_number, 0,0,0,0,0,iteration_level, 0.000, 0.000, floor_height/2, envelope_area[path_number-1], 0, 0, -1, 0, 0, 0, 23, direction[path_number-1], -1, 0, 0, 0, 0, 0, 0]]
    
    elif path_number <= number_of_unit + 1:
        index += iteration_flow_path + 1
        replacement = [[iteration_flow_path, 0, -1, 9*(iteration_level-1)+5, 5, 0,0,0,0,0,iteration_level, 0.000, 0.000, floor_height/2, 1, 0, 0, -1, 0, 0, 0, 23, direction[path_number-(number_of_unit+1)], -1, 0, 0, 0, 0, 0, 0]]
    
    elif path_number <= 2*number_of_unit + 1:
        index += iteration_flow_path + 1
        replacement = [[iteration_flow_path, 0, 9*(iteration_level-1)+path_number-5, 9*(iteration_level-1)+5, 6, 0,0,0,0,0,iteration_level, 0.000, 0.000, floor_height/2, 1, 0, 0, -1, 0, 0, 0, 23, direction[path_number-(number_of_unit+2)], -1, 0, 0, 0, 0, 0, 0]]
    
    elif path_number <= 2*number_of_unit + number_of_shaft + 1:
        index += iteration_flow_path + 1
        replacement = [[iteration_flow_path, 0, 9*(iteration_level-1)+5, 9*(iteration_level-1)+path_number-(number_of_unit), 7, 0,0,0,0,0,iteration_level, 0.000, 0.000, floor_height/2, 1, 0, 0, -1, 0, 0, 0, 23, direction[path_number-(2*number_of_unit+2)], -1, 0, 0, 0, 0, 0, 0]]
    
    else:
        index += iteration_flow_path + 1
        replacement = [[iteration_flow_path, 0, 9*(iteration_level-1)+(path_number-4)-(number_of_unit), 9*(iteration_level-2)+(path_number-4)-(number_of_unit), path_number-6, 0,0,0,0,0,iteration_level, 0.000, 0.000, floor_height/2, 1, 0, 0, -1, 0, 0, 0, 25, 3, -1, 0, 0, 0, 0, 0, 0]]
    
    data = pd.concat([data.iloc[:index], pd.DataFrame(replacement), data.iloc[index:]]).reset_index(drop=True)
    
    return data, iteration_flow_path


#%% 수정

icon = 0
iteration_zone = 0
iteration_flow_element = 0
iteration_flow_path = 0
iteration_level = 0

# 기본 설정
data[0][3] = 150
data[1][3] = 120
data[2][64] = floor_height

# OUTDOOR TEMPERATURE 설정
data[0][7] = outdoor_temp + 273.15
# ICON 넣기
for iteration_level in range(1, number_of_level+1):
    data, icon = basic(data, floor_height, iteration_level, icon)
# FLOW ELEMENT 넣기
for i in range(number_of_unit+3+number_of_shaft+1):
    data, iteration_flow_element = flow_element(data, number_of_unit, iteration_flow_element, icon)
# ZONE 넣기
for iteration_level in range(1, number_of_level+1):
    for i in range(number_of_unit+1+number_of_shaft):
        data, iteration_zone = zone(data, icon, iteration_flow_element, iteration_level, iteration_zone)
# FLOW PATH 넣기
for iteration_level in range(1, number_of_level+1):
    if iteration_level == 1:
        for i in range(2*number_of_unit+1+number_of_shaft):
            data, iteration_flow_path = flow_path(data, number_of_unit, icon, iteration_flow_element, iteration_zone, iteration_level, iteration_flow_path)
    else:
        for i in range(2*number_of_unit+1+2*number_of_shaft):
            data, iteration_flow_path = flow_path(data, number_of_unit, icon, iteration_flow_element, iteration_zone, iteration_level, iteration_flow_path)
# LOBBY 넣기
data[7][91 + (number_of_level-1)*(icon+2)+icon-4 + 3*iteration_flow_element + 3] = floor_height * vestibule_area
data[8][91 + (number_of_level-1)*(icon+2)+icon-4 + 3*iteration_flow_element + 3] = vestibule_temp
data[10][91 + (number_of_level-1)*(icon+2)+icon-4 + 3*iteration_flow_element + 3] = 'vestibule'

data[8][91 + (number_of_level-1)*(icon+2)+icon-4 + 3*iteration_flow_element + 6] = lobby_temp
data[10][91 + (number_of_level-1)*(icon+2)+icon-4 + 3*iteration_flow_element + 6] = 'lobby'

data[4][95 + (number_of_level-1)*(icon+2)+icon-4 + 3*iteration_flow_element + iteration_zone+1 + 3] = 12
data[4][95 + (number_of_level-1)*(icon+2)+icon-4 + 3*iteration_flow_element + iteration_zone+1 + 8] = 12

        
#%% prj_edit과 CSV로 데이터 옮기기

# 데이터프레임을 문자열로 변환
data_revised = data.to_string(index=False, header=False, na_rep='', float_format='{:g}'.format)

# 열 값들을 띄어쓰기로 구분하고 행을 줄 바꿈으로 구분
prj_revised = '\n'.join([' '.join(row.split()) for row in data_revised.split('\n')]).replace("None", "")

with open(Data_dir + f"{Prj_edit}.prj", 'w') as file:
    file.write(prj_revised)
    
    
# 텍스트를 줄 단위로 분할
lines = prj_revised.split('\n')

with open(Data_dir + f"{Prj_edit}.csv", 'w', newline='') as file:
    writer = csv.writer(file, delimiter=',')
    for line in lines:
        # 띄어쓰기로 분할하여 각 열을 CSV 파일에 쓰기
        writer.writerow(line.split())



#%% 시스템 상 함수

def find_and_replace(data, target_str, replacement):    # 개구부 변경
    # Initialize the index for the first occurrence of the target string
    index = data.find(target_str)
    
    # Iterate through the string to find all occurrences
    while index != -1:
        # Update the index of the next occurrence
        next_index = data.find(target_str, index + 1)
        if next_index == -1:
            # If there are no more occurrences, replace the last one found
            index = index + 18
            # print(index)
            data = data[:index] + replacement + data[index + len(target_str):]
            break
        index = next_index
    
    return data

def extract_and_create_df(string, start_char, end_char):        # 'level' 추가
    start_index = string.find(start_char)
    if start_index == -1:
        print(f"Start character '{start_char}' not found.")
        return None
    
    end_index = string.find(end_char, start_index + len(start_char))
    if end_index == -1:
        print(f"End character '{end_char}' not found after the start character.")
        return None
    
    # Extract the substring between start and end characters
    extracted_text = string[start_index + len(start_char):end_index]
    
    # Split the extracted text into lines if it contains newline characters
    lines = extracted_text.split('\n')
    
    # Create a list of dictionaries where each dictionary represents a row in the dataframe
    data = []
    for line in lines:
        data.append({'Extracted_Text': line})
    
    # Create a DataFrame from the list of dictionaries
    df = pd.DataFrame(data)
    
    return df.iloc[:,0].str.split(expand=True)


def making_room(df_Result):     # 'room' 추가
    
    # Link 열을 문자열에서 정수형으로 변환
    df_Result['Link'] = df_Result['Link'].astype(int)

    conditions = {
        6: 1,
        7: 2,
        8: 3,
        9: 4
    }
    
    filtered_df_list = []

    # 첫 13행 처리
    for remainder, room_value in conditions.items():
        temp_df = df_Result.iloc[:13][df_Result.iloc[:13]['Link'] % 17 == remainder].copy()
        if not temp_df.empty:  # temp_df가 비어 있지 않은 경우에만 처리
            temp_df['room'] = room_value
            filtered_df_list.append(temp_df)
    
    # 14행부터 처리
    for remainder, room_value in conditions.items():
        temp_df = df_Result.iloc[13:][(df_Result.iloc[13:]['Link'] - 13) % 17 == remainder].copy()
        if not temp_df.empty:  # temp_df가 비어 있지 않은 경우에만 처리
            temp_df['room'] = room_value
            filtered_df_list.append(temp_df)
    
    # 필터링된 데이터 프레임 합치기
    if filtered_df_list:
        filtered_df = pd.concat(filtered_df_list)
    else:
        filtered_df = pd.DataFrame()  # 조건에 맞는 행이 없으면 빈 데이터프레임 생성

    return filtered_df

#%% Simulation 변경 요소

with open(Data_dir + f"{Prj_edit}.prj", 'r') as prj:
      prj = prj.read()

# 외기온도 변경(-14.5C)
prj_revised_1 = prj
# prj_revised_1 = prj.replace(prj[269:276], str(267.25).ljust(7,"0"))     # 267.25K = -5.9C
# prj_revised_1 = prj.replace(prj[269:276], str(258.95).ljust(7,"0"))     # 258.95K = -14.2C

# 1층 바깥 로비 908
# 1층 안쪽 로비 907
# B1층 바깥 로비 934
# B1층 안쪽 로비 933
# B2층 1번 바깥 로비 946
# B2층 1번 안쪽 로비 945
# B2층 2번 바깥 로비 937
# B2층 2번 안쪽 로비 936

Entrance = ['907', '908', '933', '934', '936', '937', '945', '946']

# Lobby_Door_B1 = 12
# Lobby_Door_B1-2 = 13
# Lobby_Door_B2 = 14
# Lobby_Door_1 = 15
# Lobby_Door_2 = 16
# Open_door = 17
# Open_lobby = 18

Door = ['16', '15', '13', '12', '13', '14', '13', '14']

# 공동현관문 개/폐 변경
# for i in range(0, 8):
#     target_str = Entrance[i]      # 바꿀 현관문 위치
#     replacement = '18' + ' '
#     prj_revised_1 = find_and_replace(prj_revised_1, target_str, replacement)

    
#%% 파일 저장

with open(Data_dir + f"{Prj_edit}.prj", 'w') as file:
    file.write(prj_revised_1)
 
sp_1 = subprocess.Popen([Data_dir + 'contamx3.exe', Data_dir + f"{Prj_edit}.prj"])
sp_1.wait()
sp_2 = subprocess.Popen([Data_dir + 'simread_ysm.exe', Data_dir + f"{Prj_edit}.sim"])
sp_2.wait()

result = open(Data_dir + f"{Prj_edit}.lfr", 'r', encoding='EUC-KR').read()[43:].split()


#%% Heatmap 그리기

# df_Result 수정
column = 6
df_Result = pd.DataFrame(np.array(result).reshape(int(len(result)/column), column), columns = ['Date', 'Time', 'Link', 'dP (Pa)', 'F0 (kg/s)', 'F1 (kg/s)'])

# 'level' 추가
flow_path = extract_and_create_df(prj_revised_1, "paths:", "-999")
flow_path = flow_path.rename(columns=flow_path.iloc[1])[2:678].reset_index(drop=True)
df_Result['level'] = flow_path['c#'].astype(int)

# 'room' 추가
filtered_df = making_room(df_Result)
filtered_df = filtered_df.drop(6)

pivot_df = filtered_df.pivot(index='level', columns='room', values='dP (Pa)').astype(float)
new_yticklabels = [f"{label}F" for label in pivot_df.index]

plt.rcParams['font.family'] = 'Times New Roman'
plt.figure(figsize=(15, 30))

ax = sns.heatmap(pivot_df, cmap='RdBu', vmin = -40, vmax = 40, xticklabels=False, yticklabels=new_yticklabels,\
            annot=True, annot_kws = {'size' : 30, "color": "black"}, fmt=".0f", linewidths=1.2)
# ax = sns.heatmap(pivot_df, cmap='RdBu_r', annot=True, fmt=".3f", vmin = 0, vmax =1, linewidths=1.2)

plt.gca().invert_yaxis()
# plt.xticks(fontsize=20)
plt.yticks(fontsize=30, rotation=0)

# plt.title('Heatmap of Pressure Difference by Random Entrance and Time', fontsize=30)
plt.xlabel('')
plt.ylabel('')

cbar = ax.collections[0].colorbar
cbar.set_label('Pressure [Pa]', fontsize=60, rotation=270, labelpad=40)
cbar.ax.tick_params(labelsize=40)
cbar.ax.invert_yaxis()
cbar.set_ticks([-40,-20,0,20,40])

plt.show()

# plt.savefig(savefilepath+'Interzonal2.png', format='png')


#%% Heatmap 그리기

# df_Result 수정
column = 6
df_Result = pd.DataFrame(np.array(result).reshape(int(len(result)/column), column), columns = ['Date', 'Time', 'Link', 'dP (Pa)', 'F0 (kg/s)', 'F1 (kg/s)'])

# 'level' 추가
flow_path = extract_and_create_df(prj_revised_1, "paths:", "-999")
flow_path = flow_path.rename(columns=flow_path.iloc[1])[2:678].reset_index(drop=True)
df_Result['level'] = flow_path['c#'].astype(int)

# 'room' 추가
filtered_df = making_room(df_Result)
filtered_df = filtered_df.drop(6)

pivot_df = filtered_df.pivot(index='level', columns='room', values='F0 (kg/s)').astype(float)
new_yticklabels = [f"{label}F" for label in pivot_df.index]

plt.rcParams['font.family'] = 'Times New Roman'
plt.figure(figsize=(15, 30))

ax = sns.heatmap(pivot_df, cmap='BrBG_r', vmin = -1, vmax = 1, xticklabels=False, yticklabels=new_yticklabels,\
            annot=True, annot_kws = {'size' : 30, "color": "black"}, fmt=".3f", linewidths=1.2)

plt.gca().invert_yaxis()
# plt.xticks(fontsize=20)
plt.yticks(fontsize=30, rotation=0)

# plt.title('Heatmap of Pressure Difference by Random Entrance and Time', fontsize=30)
plt.xlabel('')
plt.ylabel('')

cbar = ax.collections[0].colorbar
cbar.set_label('Pressure [Pa]', fontsize=60, rotation=270, labelpad=40)
cbar.ax.tick_params(labelsize=40)
cbar.ax.invert_yaxis()
cbar.set_ticks([-1,-0.5,0,0.5,1])

plt.show()

# plt.savefig(savefilepath+'Interzonal2.png', format='png')


#%% 지상층 Scatterplot 그리기

plt.rcParams['figure.figsize']=[15,30]
plt.rcParams['font.family'] = 'Times New Roman'
plt.rc('axes',labelsize = 50)
plt.rc('axes',titlesize = 20)
plt.rc('legend', fontsize= 25)
plt.rc('figure',titlesize = 20)

scatter_df = filtered_df[filtered_df['room']==3][['level', 'dP (Pa)']].astype(float)

# # Measured Data
# x = [25, 18, 7, -26]
# y = [3, 7, 20, 47]

# sns.scatterplot(x=x, y=y, marker='x', s=500, c='black', zorder=2)
sns.scatterplot(data=scatter_df, x='dP (Pa)', y='level', marker='d', s=500, c='black', zorder=2)
plt.plot(scatter_df['dP (Pa)'], scatter_df['level'], c='black')

# 그리드
plt.grid(linewidth=2, zorder=1)

# 축 설정
plt.xticks(range(-30, 31, 10), fontsize=40)
plt.yticks(range(5, 43, 5), fontsize=40)

# 그래프 제목과 라벨 설정
plt.xlabel('Pressure Difference [Pa]')
plt.ylabel('Floor')
# plt.legend()

# 그래프 표시
plt.show()


#%% 지하층 Scatterplot 그리기

# Measured Data
x1 = [31, 16, 19]
x2 = [8, 20, 9]
y = [-2, -1, 0]

plt.rcParams['figure.figsize']=[16,9]
plt.rcParams['font.family'] = 'Times New Roman'
plt.rc('axes',labelsize = 30)
plt.rc('axes',titlesize = 30)
# plt.rc('legend', fontsize= 25)
plt.rc('figure',titlesize = 30)

plt.scatter(x1, y, marker='d', s=500, c='black', zorder=2)
plt.scatter(x2, y, marker='o', s=500, c='black', zorder=2)
plt.plot(x1, y, c='black')
plt.plot(x2, y, c='black')
    
# 그리드
plt.grid(linewidth=2, zorder=1)

# 축 설정
plt.xticks(range(0, 35, 5), fontsize=30)
plt.yticks(range(-2, 1), fontsize=30)

# 그래프 제목과 라벨 설정
plt.xlabel('Pressure Difference [Pa]')
plt.ylabel('Floor')
# plt.legend()

# 그래프 표시
plt.show()
    