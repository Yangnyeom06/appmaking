import requests
import json
import pandas as pd
import openpyxl

#subwayNm = str(input("지하철호선명 : "))

#statnNm = str(input("지하철역명 : "))
#statnNmlast = str(input("도착지하철역명 : "))

# 서울시 지하철 실시간 열차 위치정보
#url_1 = 'http://swopenAPI.seoul.go.kr/api/subway/76554469476c79753837787569696a/json/realtimePosition/0/100/{}'.format(subwayNm)
# url_1 = 'http://swopenAPI.seoul.go.kr/api/subway/76554469476c79753837787569696a/xml/realtimePosition/0/100/1호선'

# 서울시 지하철 실시간 도착정보 # 사용
url_2 = 'http://swopenAPI.seoul.go.kr/api/subway/4e50657a6d6c797537394443537774/json/realtimeStationArrival/0/100/서울'#.format(statnNm)
# url_2 = 'http://swopenAPI.seoul.go.kr/api/subway/4e50657a6d6c797537394443537774/xml/realtimeStationArrival/0/100/서울'

# 서울시 지하철 실시간 도착정보(일괄)
url_3 = 'http://swopenAPI.seoul.go.kr/api/subway/4e79664e686c797531303844514a4e75/xml/realtimeStationArrival/ALL'

# 엑셀 파일 명
file_name = 'stationList.xlsx'

# 엑셀 파일 읽기
df = pd.read_excel(file_name, sheet_name='Data', usecols=[1, 2])
#print(df)
#response_1 = requests.get(url_1)
response_2 = requests.get(url_2)

station_list = []

json_data = json.loads(response_2.text)



# 상행 하행 확인하고 상행과 하행인 경우 나눠서 확인
# statnTid(다음지하철역ID) 확인
# 확인한 ID를 엑셀파일에서 찾아 지하철역명으로 변경
# 과정 반복후 리스트에 첨가
# 현재 역ID와 다음 역ID가 같으면 같은경로라고 설정

station_list_1 = []
print(json_data["realtimeArrivalList"][0])
for i in range(0, int(json_data["errorMessage"]["total"])):
    #station_list_1.append(json_data["realtimeArrivalList"][i]["statnNm"])
    pass
station_list_1.append(json_data["realtimeArrivalList"][i]["statnNm"])
print(station_list_1)
