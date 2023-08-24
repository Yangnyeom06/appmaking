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
data = pd.read_excel(file_name, sheet_name='Data', usecols=[1, 2])

df = pd.DataFrame(data)

# 데이터프레임을 딕셔너리로 변환
station_dict = df.set_index('STATN_ID')['STATN_NM'].to_dict()


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

# 진짜 쓸 부분
# json_data = json.loads(response_2.text)

# 상행 하행 확인하고 상행과 하행인 경우 나눠서 확인
# statnTid(다음지하철역ID) 확인
# 확인한 ID를 엑셀파일에서 찾아 지하철역명으로 변경
# 과정 반복후 리스트에 첨가
# 현재 역ID와 다음 역ID가 같으면 같은경로라고 설정
# 한번 지나갔던 곳이면 break를 통해 탈출
station_list_nm = []
station_list = []

num = 0
url_num = 0
json_data_num = 0

def station_cal(station_start, station_end, sub_station_list):
    global num, url_num, json_data_num # 전역 변수 가져오기
    # 데이터 추출
    sub_url = 'http://swopenAPI.seoul.go.kr/api/subway/4e50657a6d6c797537394443537774/json/realtimeStationArrival/0/100/{}'.format(station_start)
    getUrl = requests.get(sub_url)
    sub_json_data = json.loads(getUrl.text)
    #print(sub_json_data)
    #print('before : ', sub_station_list)
    for j in range(0, int(sub_json_data["errorMessage"]["total"])):
        num += 1
        globals()["station_list_"+str(num)] = sub_station_list
        print('sub_station_list_{}'.format(num), globals()["station_list_{}".format(num)])
        #print(station_start)
        
        # 다음 역 id를 다음 역 이름으로 변환
        sub_statn_Tnm = station_dict[int(sub_json_data["realtimeArrivalList"][j]["statnTid"])]
        # 역 중복 방지
        if sub_statn_Tnm not in sub_station_list and json_data["realtimeArrivalList"][j]["statnTid"] != json_data["realtimeArrivalList"][j]["statnId"] and json_data["realtimeArrivalList"][j]["statnFid"] != json_data["realtimeArrivalList"][j]["statnId"]:
            globals()["station_list_"+str(num)].append(sub_statn_Tnm)
            print(globals()["station_list_"+str(num)])
            sub_station_list = globals()['station_list_{}'.format(num)]
            if (sub_statn_Tnm != station_end):
                #print('after : ', sub_station_list)
                station_cal(sub_statn_Tnm, statnNmlast, sub_station_list)
            else:
                break


for i in range(0, int(json_data["errorMessage"]["total"])):
    
    # 다음 역 id를 다음 역 이름으로 변환
    statn_Tnm = station_dict[int(json_data["realtimeArrivalList"][i]["statnTid"])]
    # 역 중복 방지
    if statn_Tnm not in station_list_nm and json_data["realtimeArrivalList"][i]["statnTid"] != json_data["realtimeArrivalList"][i]["statnId"]:
        num += 1
        globals()["station_list_"+str(num)] = []
        # 역 중복 방지
        station_list_nm.append(statn_Tnm)
        #print('station_list_nm : ', station_list_nm)
        # 처음 시작 역 리스트에 더하기
        globals()['station_list_{}'.format(num)].append(json_data["realtimeArrivalList"][i]["statnNm"])
        # 다음 역 리스트에 더하기
        globals()['station_list_{}'.format(num)].append(statn_Tnm)
        sub_station_list0 = globals()['station_list_{}'.format(num)]
        #print('sub_station_list', sub_station_list)
        if (statn_Tnm != statnNmlast):
            #print('first', sub_station_list0)
            station_cal(statn_Tnm, statnNmlast, sub_station_list0)
        else:
            break

'''
print(json_data["realtimeArrivalList"][0])
for i in range(0, int(json_data["errorMessage"]["total"])):
    if json_data["realtimeArrivalList"][i]["updnLine"] == "상행":
        station_list_1.append(json_data["realtimeArrivalList"][i]["statnNm"])
        subUrl = 'http://swopenAPI.seoul.go.kr/api/subway/4e50657a6d6c797537394443537774/json/realtimeStationArrival/0/100/{}'.format(json_data["realtimeArrivalList"][i]["statnTid"])
'''
'''
for i in range(0, num):
    if (globals()['station_list_{}'.format(i)]) != []:
        # 2차원 리스트를 1차원 리스트로 풀기
        #globals()['station_list_{}'.format(i)] = sum(globals()['station_list_{}'.format(i)], [])
        print("station_list_{}".format(i) ,globals()['station_list_{}'.format(i)])
'''
#globals()["subUrl_"+str(url_num)] = 'http://swopenAPI.seoul.go.kr/api/subway/4e50657a6d6c797537394443537774/json/realtimeStationArrival/0/100/회현'
#getUrl = requests.get(globals()["subUrl_"+str(url_num)])
#globals()["json_data_"+str(json_data_num)] = json.loads(getUrl.text)
#print(globals()['json_data_{}'.format(json_data_num)]["realtimeArrivalList"][0]["statnTid"])
