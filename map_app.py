import requests
import json
import pandas as pd
import openpyxl
import copy


startStatnNm = str(input("지하철역명 : "))
lastStatnNm = str(input("도착 지하철역명 : "))

# 엑셀 파일 명
file_name = 'stationList.xlsx'

# 엑셀 파일 읽기
data_list = pd.read_excel(file_name, sheet_name='stationTime', usecols=[0, 1, 2, 3])

# 읽은 엑셀 파일을 데이터 프레임화
df_list = pd.DataFrame(data_list)

# 데이터프레임을 딕셔너리로 변환
station_dict = df_list.set_index('STATN_ID')['STATN_NM'].to_dict()

stationNode = {}
used_stationId = []

stationNode = {}

# 노드 추가 함수
def add_node(station_a, station_b, distance):
    inner_station = stationNode.get(station_a, {})
    inner_station[station_b] = distance
    stationNode[station_a] = inner_station
    
    inner_station = stationNode.get(station_b, {})
    inner_station[station_a] = distance
    stationNode[station_b] = inner_station


for station_list in range(len(station_dict)):
    # api 호출
    current_url = 'http://swopenAPI.seoul.go.kr/api/subway/4e50657a6d6c797537394443537774/json/realtimeStationArrival/0/100/{}'.format(df_list["STATN_NM"][station_list])
    # 내용 파싱
    get_url = requests.get(current_url)
    # 읽을 수 있게 json화
    current_json_data = json.loads(get_url.text)

    if ("errorMessage" in current_json_data):
        for i in range(0, int(current_json_data["errorMessage"]["total"])):
            # df_list의 현재 id와 json_data의 현재 id가 같고 upnLine이 상행이고 현재 역 id와 다음 역 id가 같지 않고 used_stationId에 현재 역 id가 없다면
            if (int(df_list["STATN_ID"][station_list]) == int(current_json_data["realtimeArrivalList"][i]["statnId"]) and str(current_json_data["realtimeArrivalList"][i]["updnLine"]) == "상행" and int(df_list["STATN_ID"][station_list]) != int(current_json_data["realtimeArrivalList"][i]["statnTid"]) and int(df_list["STATN_ID"][station_list]) not in used_stationId):
                # 쓸데없는 반복 탐색 방지
                used_stationId.append(int(df_list["STATN_ID"][station_list]))
                # 다음 역 id를 다음 역 이름으로 변환
                statn_Tnm = station_dict[int(current_json_data["realtimeArrivalList"][i]["statnTid"])]
                # 역간 거리
                station_dis = "{}".format(df_list["DISTANCE"][station_list])
                
                # 노드 추가
                add_node(statn_Tnm, df_list["STATN_NM"][station_list], station_dis)
                add_node(df_list["STATN_NM"][station_list], statn_Tnm, station_dis)

            else:
                pass
    else:
        print("{} : {}".format(current_json_data["message"], df_list["STATN_NM"][station_list]))


print(stationNode)


######## 여기 이하는 https://phaphaya.tistory.com/34 의 코드 사용 (설명은 이 사이트에서)
print ("-----------[", startStatnNm, "->", lastStatnNm,"]----------")

routing = {}
for place in stationNode.keys():
    routing[place]={'shortestDist':0, 'route':[], 'visited':0}

def visitPlace(visit):
    routing[visit]['visited'] = 1
    for toGo, betweenDist in stationNode[visit].items():
        toDist = routing[visit]['shortestDist'] + betweenDist
        if (routing[toGo]['shortestDist'] >= toDist) or  not routing[toGo]['route']:
            routing[toGo]['shortestDist'] = toDist
            routing[toGo]['route'] = copy.deepcopy(routing[visit]['route'])
            routing[toGo]['route'].append(visit)

visitPlace(startStatnNm)

while 1 :

    minDist = max(routing.values(), key=lambda x:x['shortestDist'])['shortestDist']
    toVisit = ''
    for name, search in routing.items():
        if 0 < search['shortestDist'] <= minDist and not search['visited']:
            minDist = search['shortestDist']
            toVisit = name

    if toVisit == '':
        break

    visitPlace(toVisit)

    print ("["+toVisit+"]")
    print ("Dist :", minDist)

print ("\n", "[", startStatnNm, "->", lastStatnNm,"]")
print ("Route : ", routing[lastStatnNm]['route'])
print ("ShortestDistance : ", routing[lastStatnNm]['shortestDist'])
########