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
    current_url = 'http://swopenAPI.seoul.go.kr/api/subway/70757761536c7975333648456d7754/json/realtimeStationArrival/0/100/{}'.format(df_list["STATN_NM"][station_list])
    # 내용 파싱
    get_url = requests.get(current_url)
    # 읽을 수 있게 json화
    current_json_data = json.loads(get_url.text)

    if ("errorMessage" in current_json_data):
        for i in range(0, int(current_json_data["errorMessage"]["total"])):
            # df_list의 현재 id와 json_data의 현재 id가 같고 현재 역 id와 다음 역 id가 같지 않고 used_stationId에 현재 역 id가 없다면
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

            # df_list의 현재 id와 json_data의 현재 id가 같고                                                                 현재 역 id와 다음 역 id가 같다면
            elif (int(df_list["STATN_ID"][station_list]) == int(current_json_data["realtimeArrivalList"][i]["statnId"]) and int(df_list["STATN_ID"][station_list]) == int(current_json_data["realtimeArrivalList"][i]["statnTid"]) and int(df_list["STATN_ID"][station_list]) not in used_stationId):
                print("진입")
                # 쓸데없는 반복 탐색 방지
                used_stationId.append(int(df_list["STATN_ID"][station_list]))
                # 이전 역 id를 이전 역 이름으로 변환
                statn_Fnm = station_dict[int(current_json_data["realtimeArrivalList"][i]["statnFid"])]
                # 역간 거리
                station_dis = "{}".format(df_list["DISTANCE"][station_list])
                
                # 노드 추가
                add_node(statn_Fnm, df_list["STATN_NM"][station_list], station_dis)
                add_node(df_list["STATN_NM"][station_list], statn_Fnm, station_dis)
            
            if (int(df_list["STATN_ID"][station_list]) == int(current_json_data["realtimeArrivalList"][i]["statnId"]) and str(current_json_data["realtimeArrivalList"][i]["updnLine"]) == "외선" and int(df_list["STATN_ID"][station_list]) != int(current_json_data["realtimeArrivalList"][i]["statnTid"]) and int(df_list["STATN_ID"][station_list]) not in used_stationId):
                # 쓸데없는 반복 탐색 방지
                used_stationId.append(int(df_list["STATN_ID"][station_list]))
                # 다음 역 id를 다음 역 이름으로 변환
                statn_Tnm = station_dict[int(current_json_data["realtimeArrivalList"][i]["statnTid"])]
                # 역간 거리
                station_dis = "{}".format(df_list["DISTANCE"][station_list])
                
                # 노드 추가
                add_node(statn_Tnm, df_list["STATN_NM"][station_list], station_dis)
                add_node(df_list["STATN_NM"][station_list], statn_Tnm, station_dis)

            # df_list의 현재 id와 json_data의 현재 id가 같고                                                                 현재 역 id와 다음 역 id가 같다면
            elif (int(df_list["STATN_ID"][station_list]) == int(current_json_data["realtimeArrivalList"][i]["statnId"]) and int(df_list["STATN_ID"][station_list]) == int(current_json_data["realtimeArrivalList"][i]["statnTid"]) and int(df_list["STATN_ID"][station_list]) not in used_stationId):
                print("진입")
                # 쓸데없는 반복 탐색 방지
                used_stationId.append(int(df_list["STATN_ID"][station_list]))
                # 이전 역 id를 이전 역 이름으로 변환
                statn_Fnm = station_dict[int(current_json_data["realtimeArrivalList"][i]["statnFid"])]
                # 역간 거리
                station_dis = "{}".format(df_list["DISTANCE"][station_list])
                
                # 노드 추가
                add_node(statn_Fnm, df_list["STATN_NM"][station_list], station_dis)
                add_node(df_list["STATN_NM"][station_list], statn_Fnm, station_dis)
            
            if (int(df_list["STATN_ID"][station_list]) == int(current_json_data["realtimeArrivalList"][i]["statnId"]) and str(current_json_data["realtimeArrivalList"][i]["updnLine"]) == "하행" and int(df_list["STATN_ID"][station_list]) != int(current_json_data["realtimeArrivalList"][i]["statnTid"]) and int(df_list["STATN_ID"][station_list]) not in used_stationId):
                # 쓸데없는 반복 탐색 방지
                used_stationId.append(int(df_list["STATN_ID"][station_list]))
                # 다음 역 id를 다음 역 이름으로 변환
                statn_Tnm = station_dict[int(current_json_data["realtimeArrivalList"][i]["statnTid"])]
                # 역간 거리
                station_dis = "{}".format(df_list["DISTANCE"][station_list])
                
                # 노드 추가
                add_node(statn_Tnm, df_list["STATN_NM"][station_list], station_dis)
                add_node(df_list["STATN_NM"][station_list], statn_Tnm, station_dis)

            # df_list의 현재 id와 json_data의 현재 id가 같고                                                                 현재 역 id와 다음 역 id가 같다면
            elif (int(df_list["STATN_ID"][station_list]) == int(current_json_data["realtimeArrivalList"][i]["statnId"]) and int(df_list["STATN_ID"][station_list]) == int(current_json_data["realtimeArrivalList"][i]["statnTid"]) and int(df_list["STATN_ID"][station_list]) not in used_stationId):
                print("진입")
                # 쓸데없는 반복 탐색 방지
                used_stationId.append(int(df_list["STATN_ID"][station_list]))
                # 이전 역 id를 이전 역 이름으로 변환
                statn_Fnm = station_dict[int(current_json_data["realtimeArrivalList"][i]["statnFid"])]
                # 역간 거리
                station_dis = "{}".format(df_list["DISTANCE"][station_list])
                
                # 노드 추가
                add_node(statn_Fnm, df_list["STATN_NM"][station_list], station_dis)
                add_node(df_list["STATN_NM"][station_list], statn_Fnm, station_dis)
            
            else:
                #print("뭔가 잘못됨")
                pass
    else:
        print("{} : {}".format(current_json_data["message"], df_list["STATN_NM"][station_list]))


print(stationNode)
with open('stationNode.json', 'w', encoding="UTF-8") as f : 
	json.dump(stationNode, f, indent=4, ensure_ascii=False)


print(stationNode)