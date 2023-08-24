
import requests
import json
import pandas as pd
import openpyxl

#subwayNm = str(input("지하철호선명 : "))

#statnNm = str(input("지하철역명 : "))
statnNmlast = "이태원"#str(input("도착지하철역명 : "))

# 서울시 지하철 실시간 열차 위치정보
#url_1 = 'http://swopenAPI.seoul.go.kr/api/subway/76554469476c79753837787569696a/json/realtimePosition/0/100/{}'.format(subwayNm)
# url_1 = 'http://swopenAPI.seoul.go.kr/api/subway/76554469476c79753837787569696a/xml/realtimePosition/0/100/1호선'

# 서울시 지하철 실시간 도착정보 # 사용
url_2 = 'http://swopenAPI.seoul.go.kr/api/subway/4e50657a6d6c797537394443537774/json/realtimeStationArrival/0/100/서울'#.format(statnNm)
# url_2 = 'http://swopenAPI.seoul.go.kr/api/subway/4e50657a6d6c797537394443537774/xml/realtimeStationArrival/0/100/회현'

# 서울시 지하철 실시간 도착정보(일괄)
url_3 = 'http://swopenAPI.seoul.go.kr/api/subway/4e79664e686c797531303844514a4e75/xml/realtimeStationArrival/ALL'

# 엑셀 파일 명
file_name = 'stationList.xlsx'

# 엑셀 파일 읽기
data_list = pd.read_excel(file_name, sheet_name='stationTime', usecols=[0, 1, 2, 3])

df_list = pd.DataFrame(data_list)

#print(df_list)


# 데이터프레임을 딕셔너리로 변환
station_dict = df_list.set_index('STATN_ID')['STATN_NM'].to_dict()

#response_1 = requests.get(url_1)
response_2 = requests.get(url_2)


# 필요 없는 부분 (코드 짤 때 테스트 용)
f1 = open("data.json", 'w', encoding="UTF-8")
f1.write(response_2.text)
f1.close()

# 필요 없는 부분
with open('data.json', 'r', encoding="UTF-8") as file0:
    data0 = file0.read()
    json_data0 = json.loads(data0)

# 필요 없는 부분
f2 = open("data.json", 'w', encoding="UTF-8")
f2.write(json.dumps(json_data0, indent=4, ensure_ascii=False))
f2.close()

# 필요 없는 부분
with open('data.json', 'r', encoding="UTF-8") as file:
    data = file.read()
    json_data = json.loads(data)


outer_dict = {}  # 바깥쪽 딕셔너리 초기화

# 바깥쪽 딕셔너리의 키와 값 생성을 위한 반복문
for i in range(3):
    inner_dict = {}  # 내부 딕셔너리 초기화
    
    # 내부 딕셔너리의 키와 값 생성을 위한 반복문
    for j in range(2):
        key = 'inner_key_{}_{}'.format(i, j)
        value = 'value_{}_{}'.format(i, j)
        inner_dict[key] = value
    
    outer_key = 'outer_key_{}'.format(i)
    outer_dict[outer_key] = inner_dict

print(outer_dict)


stationNode = {}
inner_station = {} # 내부 삽입 딕셔너리 초기화

statn_Tnm = "서울"
statn_Nm = "회현"

inner_station_key = "{}".format(statn_Tnm)
# 역간 거리
station_key_dis = "0.9"

inner_station[inner_station_key] = station_key_dis

outer_station_key = "{}".format(statn_Nm)

stationNode[outer_station_key] = inner_station

# 역으로도 할당 해야함
inner_station = {} # 내부 삽입 딕셔너리 초기화

inner_station_key = "{}".format(statn_Nm)

inner_station[inner_station_key] = station_key_dis

outer_station_key = "{}".format(statn_Tnm)

stationNode[outer_station_key] = inner_station

print(stationNode)


########

statn_Tnm = "서울"
statn_Nm = "숙대입구"

inner_station = {} # 내부 삽입 딕셔너리 초기화

inner_station_key = "{}".format(statn_Tnm)
# 역간 거리
station_key_dis = "0.9"

inner_station[inner_station_key] = station_key_dis

outer_station_key = "{}".format(statn_Nm)

stationNode[outer_station_key] = inner_station

# 역으로도 할당 해야함
inner_station = {} # 내부 삽입 딕셔너리 초기화

inner_station_key = "{}".format(statn_Nm)

inner_station[inner_station_key] = station_key_dis


outer_station_key = "{}".format(statn_Tnm)
print(outer_station_key)

stationNode[outer_station_key] = inner_station

print(stationNode)

stationNode = {}

def add_distance(station_a, station_b, distance):
    inner_station = stationNode.get(station_a, {})
    inner_station[station_b] = distance
    stationNode[station_a] = inner_station
    
    inner_station = stationNode.get(station_b, {})
    inner_station[station_a] = distance
    stationNode[station_b] = inner_station

# 첫 번째 예시
add_distance("서울", "회현", "0.9")
print(stationNode)

# 두 번째 예시
add_distance("서울", "숙대입구", "0.9")
print(stationNode)
