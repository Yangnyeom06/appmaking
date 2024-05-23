import copy
import requests
import json
import pandas as pd
import openpyxl
import re

num = 0
currentShortestDistance = 100000
booltype = True
choice = ["멀티", "솔로", "1", "2"]

#region staionNode
stationNode = {"동두천": {"소요산": "1.6", "보산": "1.4"}, "소요산": {"동두천": "1.6"}, "보산": {"동두천": "1.4", "동두천중앙": "1.0"}, "동두천중앙": {"보산": "1.0", "지행": "5.6"}, "지행": {"동두천중앙": "5.6", "덕정": "2.9"}, "덕정": {"지행": "2.9", "덕계": "5.3"}, "덕계": {"덕정": "5.3", "양주": "1.6"}, "양주": {"덕계": "1.6", "녹양": "1.3"}, "녹양": {"양주": "1.3", "가능": "1.2"}, "가능": {"녹양": "1.2", "의정부": "1.6"}, "의정부": {"가능": "1.6", "회룡": "1.4"}, "회룡": {"의정부": "1.4", "망월사": "2.3"}, "망월사": {"회룡": "2.3", "도봉산": "1.2"}, "도봉산": {"망월사": "1.2", "도봉": "1.3", "장암": "1.4", "수락산": "1.6"}, "도봉": {"도봉산": "1.3", "방학": "1.7"}, "방학": {"도봉": "1.7", "창동": "1.0"}, "창동": {"방학": "1.0", "녹천": "1.4", "노원": "1.4", "쌍문": "1.3"}, "녹천": {"창동": "1.4", "월계": "1.1"}, "월계": {"녹천": "1.1", "광운대": "1.1"}, "광운대": {"월계": "1.1", "석계": "1.4"}, "석계": {"광운대": "1.4", "신이문": "0.8", "돌곶이": "1.0", "태릉입구": "0.8"}, "신이문": {"석계": "0.8", "외대앞": "0.8"}, "외대앞": {"신이문": "0.8", "회기": "0.8"}, "회기": {"외대앞": "0.8", "청량리": "1.4", "중랑": "1.8"}, "청량리": {"회기": "1.4", "제기동": "1.0", "왕십리": "2.4"}, "제기동": {"청량리": "1.0", "신설동": "0.9"}, "신설동": {"제기동": "0.9", "동묘앞": "0.7", "용두": "1.2", "보문": "1.0"}, "동묘앞": {"신설동": "0.7", "동대문": "0.6", "신당": "0.6", "창신": "0.9"}, "동대문": {"동묘앞": "0.6", "종로5가": "0.8", "혜화": "1.5", "동대문역사문화공원": "0.7"}, "종로5가": {"동대문": "0.8", "종로3가": "0.9"}, "종로3가": {"종로5가": "0.9", "종각": "0.8", "안국": "1.0", "을지로3가": "0.6", "광화문": "1.2", "을지로4가": "1.0"}, "종각": {"종로3가": "0.8", "시청": "1.0"}, "시청": {"종각": "1.0", "서울": "1.1", "충정로": "1.1", "을지로입구": "0.7"}, "서울": {"시청": "1.1", "남영": "1.7", "회현": "0.9", "숙대입구": "1.0", "공덕": "3.3"}, "서울(경의중앙선)": {"신촌(경의중앙선)": "3.1"}, "남영": {"서울": "1.7", "용산": "1.5"}, "용산": {"남영": "1.5", "노량진": "1.8", "효창공원앞": "1.5", "이촌": "1.9"}, "노량진": {"용산": "1.8", "대방": "1.5", "샛강": "1.2", "노들": "1.1"}, "대방": {"노량진": "1.5", "신길": "0.8"}, "신길": {"대방": "0.8", "영등포": "1.0", "영등포시장": "1.1", "여의도": "1.0"}, "영등포": {"신길": "1.0", "신도림": "1.5"}, "신도림": {"영등포": "1.5", "구로": "1.1", "대림": "1.8", "문래": "1.2", "도림천": "1.0"}, "구로": {"신도림": "1.1", "구일": "1.4", "가산디지털단지": "1.1"}, "구일": {"구로": "1.4", "개봉": "1.0"}, "개봉": {"구일": "1.0", "오류동": "1.3"}, "오류동": {"개봉": "1.3", "온수": "1.9"}, "온수": {"오류동": "1.9", "역곡": "1.3", "천왕": "1.5", "까치울": "2.2"}, "역곡": {"온수": "1.3", "소사": "1.5"}, "소사": {"역곡": "1.5", "부천": "1.1", "부천종합운동장": "2.7", "소새울": "1.7"}, "부천": {"소사": "1.1", "중동": "1.7"}, "중동": {"부천": "1.7", "송내": "1.0"}, "송내": {"중동": "1.0", "부개": "1.2"}, "부개": {"송내": "1.2", "부평": "1.5"}, "부평": {"부개": "1.5", "백운": "1.7"}, "백운": {"부평": "1.7", "동암": "1.5"}, "동암": {"백운": "1.5", "간석": "1.2"}, "간석": {"동암": "1.2", "주안": "1.2"}, "주안": {"간석": "1.2", "도화": "1.0"}, "도화": {"주안": "1.0", "제물포": "1.0"}, "제물포": {"도화": "1.0", "도원": "1.4"}, "도원": {"제물포": "1.4", "동인천": "1.2"}, "동인천": {"도원": "1.2", "인천": "1.9"}, "인천": {"동인천": "1.9", "신포": "1.0"}, "가산디지털단지": {"구로": "1.1", "독산": "2.0", "남구로": "0.8", "철산": "1.4"}, "독산": {"가산디지털단지": "2.0", "금천구청": "1.2"}, "금천구청": {"독산": "1.2", "석수": "1.9"}, "석수": {"금천구청": "1.9", "관악": "1.9"}, "관악": {"석수": "1.9", "안양": "2.4"}, "안양": {"관악": "2.4", "명학": "2.2"}, "명학": {"안양": "2.2", "금정": "1.4"}, "금정": {"명학": "1.4", "군포": "2.2", "범계": "2.6", "산본": "2.3"}, "군포": {"금정": "2.2", "당정": "1.6"}, "당정": {"군포": "1.6", "의왕": "2.6"}, "의왕": {"당정": "2.6", "성균관대": "2.9"}, "성균관대": {"의왕": "2.9", "화서": "2.6"}, "화서": {"성균관대": "2.6", "수원": "2.1"}, "수원": {"화서": "2.1", "세류": "2.9", "매교": "1.5", "고색": "2.7"}, "세류": {"수원": "2.9", "병점": "4.3"}, "병점": {"세류": "4.3", "세마": "2.4"}, "세마": {"병점": "2.4", "오산대": "2.7"}, "오산대": {"세마": "2.7", "오산": "2.7"}, "오산": {"오산대": "2.7", "진위": "4.0"}, "진위": {"오산": "4.0", "송탄": "3.8"}, "송탄": {"진위": "3.8", "서정리": "2.2"}, "서정리": {"송탄": "2.2", "지제": "4.8"}, "지제": {"서정리": "4.8", "평택": "3.7"}, "평택": {"지제": "3.7", "성환": "9.4"}, "성환": {"평택": "9.4", "직산": "5.4"}, "직산": {"성환": "5.4", "두정": "5.4"}, "두정": {"직산": "5.4", "천안": "3.0"}, "천안": {"두정": "3.0", "봉명": "1.3"}, "봉명": {"천안": "1.3"}, "아산": {"쌍용(나사렛대)": "1.6", "탕정": "1.6"}, "쌍용(나사렛대)": {"아산": "1.6"}, "탕정": {"아산": "1.6", "배방": "1.8"}, "배방": {"탕정": "1.8", "온양온천": "3.1"}, "온양온천": {"배방": "3.1", "신창": "5.1"}, "신창": {"온양온천": "5.1"}, "충정로": {"시청": "1.1", "아현": "0.8", "애오개": "0.9", "서대문": "0.7"}, "을지로입구": {"시청": "0.7", "을지로3가": "0.8"}, "을지로3가": {"을지로입구": "0.8", "을지로4가": "0.6", "종로3가": "0.6", "충무로": "0.7"}, "을지로4가": {"을지로3가": "0.6", "동대문역사문화공원": "0.9", "종로3가": "1.0"}, "동대문역사문화공원": {"을지로4가": "0.9", "신당": "0.9", "동대문": "0.7", "충무로": "1.3", "청구": "0.9"}, "신당": {"동대문역사문화공원": "0.9", "상왕십리": "0.9", "청구": "0.7", "동묘앞": "0.6"}, "상왕십리": {"신당": "0.9", "왕십리": "0.8"}, "왕십리": {"상왕십리": "0.8", "한양대": "1.0", "행당": "0.9", "마장": "0.7", "응봉": "1.4", "청량리": "2.4", "서울숲": "2.2"}, "한양대": {"왕십리": "1.0", "뚝섬": "1.1"}, "뚝섬": {"한양대": "1.1", "성수": "0.8"}, "성수": {"뚝섬": "0.8", "건대입구": "1.2", "용답": "1.0"}, "건대입구": {"성수": "1.2", "구의": "1.6", "어린이대공원(세종대)": "0.8", "뚝섬유원지": "1.0"}, "구의": {"건대입구": "1.6", "강변": "0.9"}, "강변": {"구의": "0.9", "잠실나루": "1.8"}, "잠실나루": {"강변": "1.8", "잠실": "1.0"}, "잠실": {"잠실나루": "1.0", "잠실새내": "1.2", "몽촌토성(평화의문)": "0.8", "석촌": "1.3"}, "잠실새내": {"잠실": "1.2", "종합운동장": "1.2"}, "종합운동장": {"잠실새내": "1.2", "삼성": "1.0", "봉은사": "1.4", "삼전": "1.4"}, "삼성": {"종합운동장": "1.0", "선릉": "1.3"}, "선릉": {"삼성": "1.3", "역삼": "1.2", "선정릉": "0.7", "한티": "1.1"}, "역삼": {"선릉": "1.2", "강남": "0.8"}, "강남": {"역삼": "0.8", "교대": "1.2", "신논현": "0.9", "양재": "1.5"}, "교대": {"강남": "1.2", "서초": "0.7", "고속터미널": "1.6", "남부터미널": "0.9"}, "서초": {"교대": "0.7", "방배": "1.7"}, "방배": {"서초": "1.7", "사당": "1.6"}, "사당": {"방배": "1.6", "낙성대": "1.7", "총신대입구(이수)": "1.1", "남태령": "1.6"}, "낙성대": {"사당": "1.7", "서울대입구": "1.0"}, "서울대입구": {"낙성대": "1.0", "봉천": "1.0"}, "봉천": {"서울대입구": "1.0", "신림": "1.1"}, "신림": {"봉천": "1.1", "신대방": "1.8"}, "신대방": {"신림": "1.8", "구로디지털단지": "1.1"}, "구로디지털단지": {"신대방": "1.1", "대림": "1.1"}, "대림": {"구로디지털단지": "1.1", "신도림": "1.8", "신풍": "1.4", "남구로": "1.1"}, "문래": {"신도림": "1.2", "영등포구청": "0.9"}, "영등포구청": {"문래": "0.9", "당산": "1.1", "양평": "0.8", "영등포시장": "0.9"}, "당산": {"영등포구청": "1.1", "합정": "2.0", "선유도": "1.0", "국회의사당": "1.5"}, "합정": {"당산": "2.0", "홍대입구": "1.1", "망원": "0.8", "상수": "0.8"}, "홍대입구": {"합정": "1.1", "신촌": "1.3", "서강대": "1.9", "가좌": "1.7", "공덕": "2.8", "디지털미디어시티": "3.4"}, "신촌": {"홍대입구": "1.3", "이대": "0.8"}, "이대": {"신촌": "0.8", "아현": "0.9"}, "아현": {"이대": "0.9", "충정로": "0.8"}, "용답": {"성수": "1.0", "신답": "0.9"}, "신답": {"용답": "0.9", "용두": "1.2"}, "용두": {"신답": "1.2", "신설동": "1.2"}, "도림천": {"신도림": "1.0", "양천구청": "1.7"}, "양천구청": {"도림천": "1.7", "신정네거리": "1.9"}, "신정네거리": {"양천구청": "1.9", "까치산": "1.4"}, "까치산": {"신정네거리": "1.4", "화곡": "1.2", "신정(은행정)": "1.3"}, "주엽": {"대화": "1.6", "정발산": "0.9"}, "대화": {"주엽": "1.6"}, "정발산": {"주엽": "0.9", "마두": "1.4"}, "마두": {"정발산": "1.4", "백석": "2.5"}, "백석": {"마두": "2.5", "대곡": "2.1"}, "대곡": {"백석": "2.1", "화정": "2.6", "능곡": "1.8", "곡산": "1.8"}, "화정": {"대곡": "2.6", "원당": "2.9"}, "원당": {"화정": "2.9", "원흥": "2.1"}, "원흥": {"원당": "2.1", "삼송": "1.7"}, "삼송": {"원흥": "1.7", "지축": "0.0"}, "지축": {"삼송": "0.0", "구파발": "1.5"}, "구파발": {"지축": "1.5", "연신내": "2.0"}, "연신내": {"구파발": "2.0", "불광": "1.3", "독바위": "0.9", "구산": "1.4"}, "불광": {"연신내": "1.3", "녹번": "1.1", "역촌": "1.1", "독바위": "0.8"}, "녹번": {"불광": "1.1", "홍제": "1.6"}, "홍제": {"녹번": "1.6", "무악재": "0.9"}, "무악재": {"홍제": "0.9", "독립문": "1.1"}, "독립문": {"무악재": "1.1", "경복궁": "1.6"}, "경복궁": {"독립문": "1.6", "안국": "1.1"}, "안국": {"경복궁": "1.1", "종로3가": "1.0"}, "충무로": {"을지로3가": "0.7", "동대입구": "0.9", "동대문역사문화공원": "1.3", "명동": "0.7"}, "동대입구": {"충무로": "0.9", "약수": "0.7"}, "약수": {"동대입구": "0.7", "금호": "0.8", "버티고개": "0.7", "청구": "0.8"}, "금호": {"약수": "0.8", "옥수": "0.8"}, "옥수": {"금호": "0.8", "압구정": "2.1", "한남": "1.6", "응봉": "1.8"}, "압구정": {"옥수": "2.1", "신사": "1.5"}, "신사": {"압구정": "1.5", "잠원": "0.9", "논현": "0.7"}, "잠원": {"신사": "0.9", "고속터미널": "1.2"}, "고속터미널": {"잠원": "1.2", "교대": "1.6", "반포": "0.9", "내방": "2.2", "신반포": "0.8", "사평": "1.1"}, "남부터미널": {"교대": "0.9", "양재": "1.8"}, "양재": {"남부터미널": "1.8", "매봉": "1.2", "강남": "1.5", "양재시민의숲": "1.6"}, "매봉": {"양재": "1.2", "도곡": "0.9"}, "도곡": {"매봉": "0.9", "대치": "0.8", "한티": "0.7", "구룡": "0.6"}, "대치": {"도곡": "0.8", "학여울": "0.8"}, "학여울": {"대치": "0.8", "대청": "0.9"}, "대청": {"학여울": "0.9", "일원": "1.1"}, "일원": {"대청": "1.1", "수서": "1.8"}, "수서": {"일원": "1.8", "가락시장": "1.4", "대모산입구": "3.2", "복정": "3.2"}, "가락시장": {"수서": "1.4", "경찰병원": "0.8", "송파": "0.8", "문정": "0.9"}, "경찰병원": {"가락시장": "0.8", "오금": "0.8"}, "오금": {"경찰병원": "0.8", "방이": "0.9", "개롱": "0.9"}, "상계": {"당고개": "1.2", "노원": "1.0"}, "당고개": {"상계": "1.2"}, "노원": {"상계": "1.0", "창동": "1.4", "마들": "1.2", "중계": "1.1"}, "쌍문": {"창동": "1.3", "수유": "1.5"}, "수유": {"쌍문": "1.5", "미아": "1.4"}, "미아": {"수유": "1.4", "미아사거리": "1.5"}, "미아사거리": {"미아": "1.5", "길음": "1.3"}, "길음": {"미아사거리": "1.3", "성신여대입구": "2.4"}, "성신여대입구": {"길음": "2.4", "한성대입구": "1.0", "정릉": "1.2", "보문": "0.9"}, "한성대입구": {"성신여대입구": "1.0", "혜화": "0.9"}, "혜화": {"한성대입구": "0.9", "동대문": "1.5"}, "명동": {"충무로": "0.7", "회현": "0.7"}, "회현": {"명동": "0.7", "서울": "0.9"}, "숙대입구": {"서울": "1.0", "삼각지": "1.2"}, "삼각지": {"숙대입구": "1.2", "신용산": "0.7", "효창공원앞": "1.2", "녹사평": "1.1"}, "신용산": {"삼각지": "0.7", "이촌": "1.3"}, "이촌": {"신용산": "1.3", "동작": "2.7", "용산": "1.9", "서빙고": "1.7"}, "동작": {"이촌": "2.7", "총신대입구(이수)": "1.8", "흑석": "1.4", "구반포": "1.0"}, "총신대입구(이수)": {"동작": "1.8", "사당": "1.1", "내방": "1.0", "남성": "1.0"}, "남태령": {"사당": "1.6", "선바위": "0.9"}, "선바위": {"남태령": "0.9", "경마공원": "0.9"}, "경마공원": {"선바위": "0.9", "대공원": "1.0"}, "대공원": {"경마공원": "1.0", "과천": "1.0"}, "과천": {"대공원": "1.0", "정부과천청사": "3.0"}, "정부과천청사": {"과천": "3.0", "인덕원": "3.0"}, "인덕원": {"정부과천청사": "3.0", "평촌": "1.6"}, "평촌": {"인덕원": "1.6", "범계": "2.6"}, "범계": {"평촌": "2.6", "금정": "2.6"}, "산본": {"금정": "2.3", "수리산": "1.1"}, "수리산": {"산본": "1.1", "대야미": "2.6"}, "대야미": {"수리산": "2.6", "반월": "2.0"}, "반월": {"대야미": "2.0", "상록수": "3.7"}, "상록수": {"반월": "3.7", "한대앞": "1.6"}, "한대앞": {"상록수": "1.6", "중앙": "1.6", "사리": "2.2"}, "중앙": {"한대앞": "1.6", "고잔": "1.4"}, "고잔": {"중앙": "1.4", "초지": "1.5"}, "초지": {"고잔": "1.5", "안산": "1.8", "선부": "1.7", "시우": "1.4"}, "안산": {"초지": "1.8", "신길온천": "2.2"}, "신길온천": {"안산": "2.2", "정왕": "2.9"}, "정왕": {"신길온천": "2.9", "오이도": "1.4"}, "오이도": {"정왕": "1.4", "달월": "2.1"}, "개화산": {"방화": "0.9", "김포공항": "1.2"}, "방화": {"개화산": "0.9"}, "김포공항": {"개화산": "1.2", "송정": "1.2", "개화": "3.6", "공항시장": "0.8", "마곡나루": "2.3", "계양": "6.6", "능곡": "7.4", "원종": "4.3"}, "송정": {"김포공항": "1.2", "마곡": "1.1"}, "마곡": {"송정": "1.1", "발산": "1.2"}, "발산": {"마곡": "1.2", "우장산": "1.1"}, "우장산": {"발산": "1.1", "화곡": "1.0"}, "화곡": {"우장산": "1.0", "까치산": "1.2"}, "신정(은행정)": {"까치산": "1.3", "목동": "0.8"}, "목동": {"신정(은행정)": "0.8", "오목교(목동운동장앞)": "0.9"}, "오목교(목동운동장앞)": {"목동": "0.9", "양평": "1.0"}, "양평": {"오목교(목동운동장앞)": "1.0", "영등포구청": "0.8", "오빈": "2.2", "원덕": "5.8"}, "영등포시장": {"영등포구청": "0.9", "신길": "1.1"}, "여의도": {"신길": "1.0", "여의나루": "1.0", "국회의사당": "0.9", "샛강": "0.8"}, "여의나루": {"여의도": "1.0", "마포": "1.8"}, "마포": {"여의나루": "1.8", "공덕": "0.8"}, "공덕": {"마포": "0.8", "애오개": "1.1", "대흥(서강대앞)": "0.9", "효창공원앞": "0.9", "서강대": "1.0", "서울": "3.3", "홍대입구": "2.8"}, "애오개": {"공덕": "1.1", "충정로": "0.9"}, "서대문": {"충정로": "0.7", "광화문": "1.1"}, "광화문": {"서대문": "1.1", "종로3가": "1.2"}, "청구": {"동대문역사문화공원": "0.9", "신금호": "0.9", "약수": "0.8", "신당": "0.7"}, "신금호": {"청구": "0.9", "행당": "0.9"}, "행당": {"신금호": "0.9", "왕십리": "0.9"}, "마장": {"왕십리": "0.7", "답십리": "1.0"}, "답십리": {"마장": "1.0", "장한평": "1.2"}, "장한평": {"답십리": "1.2", "군자(능동)": "1.5"}, "군자(능동)": {"장한평": "1.5", "아차산(어린이대공원후문)": "1.0", "중곡": "1.1", "어린이대공원(세종대)": "1.1"}, "아차산(어린이대공원후문)": {"군자(능동)": "1.0", "광나루(장신대)": "1.5"}, "광나루(장신대)": {"아차산(어린이대공원후문)": "1.5", "천호(풍납토성)": "2.0"}, "천호(풍납토성)": {"광나루(장신대)": "2.0", "강동": "0.8", "암사": "1.3", "강동구청": "0.9"}, "강동": {"천호(풍납토성)": "0.8", "길동": "0.9", "둔촌동": "1.2"}, "길동": {"강동": "0.9", "굽은다리(강동구민회관앞)": "0.8"}, "굽은다리(강동구민회관앞)": {"길동": "0.8", "명일": "0.8"}, "명일": {"굽은다리(강동구민회관앞)": "0.8", "고덕": "1.2"}, "고덕": {"명일": "1.2", "상일동": "1.1"}, "상일동": {"고덕": "1.1"}, "둔촌동": {"강동": "1.2", "올림픽공원(한국체대)": "1.4"}, "올림픽공원(한국체대)": {"둔촌동": "1.4", "방이": "0.8", "둔촌오륜": "1.0"}, "방이": {"올림픽공원(한국체대)": "0.8", "오금": "0.9"}, "개롱": {"오금": "0.9", "거여": "0.9"}, "거여": {"개롱": "0.9", "마천": "0.9"}, "마천": {"거여": "0.9"}, "역촌": {"응암순환(상선)": "1.5", "불광": "1.1"}, "응암순환(상선)": {"역촌": "1.5", "구산": "0.9", "새절(신사)": "0.9"}, "독바위": {"불광": "0.8", "연신내": "0.9"}, "구산": {"연신내": "1.4", "응암순환(상선)": "0.9"}, "새절(신사)": {"응암순환(상선)": "0.9", "증산(명지대앞)": "0.9"}, "증산(명지대앞)": {"새절(신사)": "0.9", "디지털미디어시티": "1.1"}, "디지털미디어시티": {"증산(명지대앞)": "1.1", "월드컵경기장(성산)": "0.8", "가좌": "1.7", "수색": "1.7", "홍대입구": "3.4", "마곡나루": "8.6"}, "월드컵경기장(성산)": {"디지털미디어시티": "0.8", "마포구청": "0.8"}, "마포구청": {"월드컵경기장(성산)": "0.8", "망원": "1.0"}, "망원": {"마포구청": "1.0", "합정": "0.8"}, "상수": {"합정": "0.8", "광흥창": "0.9"}, "광흥창": {"상수": "0.9", "대흥(서강대앞)": "1.0"}, "대흥(서강대앞)": {"광흥창": "1.0", "공덕": "0.9"}, "효창공원앞": {"공덕": "0.9", "삼각지": "1.2", "용산": "1.5"}, "녹사평": {"삼각지": "1.1", "이태원": "0.8"}, "이태원": {"녹사평": "0.8", "한강진": "1.0"}, "한강진": {"이태원": "1.0", "버티고개": "1.0"}, "버티고개": {"한강진": "1.0", "약수": "0.7"}, "창신": {"동묘앞": "0.9", "보문": "0.8"}, "보문": {"창신": "0.8", "안암(고대병원앞)": "0.9", "성신여대입구": "0.9", "신설동": "1.0"}, "안암(고대병원앞)": {"보문": "0.9", "고려대": "0.8"}, "고려대": {"안암(고대병원앞)": "0.8", "월곡(동덕여대)": "1.4"}, "월곡(동덕여대)": {"고려대": "1.4", "상월곡(한국과학기술연구원)": "0.8"}, "상월곡(한국과학기술연구원)": {"월곡(동덕여대)": "0.8", "돌곶이": "0.8"}, "돌곶이": {"상월곡(한국과학기술연구원)": "0.8", "석계": "1.0"}, "태릉입구": {"석계": "0.8", "화랑대(서울여대입구)": "0.9", "공릉(서울산업대입구)": "0.8", "먹골": "0.9"}, "화랑대(서울여대입구)": {"태릉입구": "0.9", "봉화산": "0.7"}, "봉화산": {"화랑대(서울여대입구)": "0.7", "신내": "1.3"}, "신내": {"봉화산": "1.3", "망우": "2.6", "갈매": "2.6"}, "장암": {"도봉산": "1.4"}, "수락산": {"도봉산": "1.6", "마들": "1.4"}, "마들": {"수락산": "1.4", "노원": "1.2"}, "중계": {"노원": "1.1", "하계": "1.0"}, "하계": {"중계": "1.0", "공릉(서울산업대입구)": "1.3"}, "공릉(서울산업대입구)": {"하계": "1.3", "태릉입구": "0.8"}, "먹골": {"태릉입구": "0.9", "중화": "0.9"}, "중화": {"먹골": "0.9", "상봉": "1.0"}, "상봉": {"중화": "1.0", "면목": "0.8", "중랑": "0.8", "망우": "0.6"}, "면목": {"상봉": "0.8", "사가정": "0.9"}, "사가정": {"면목": "0.9", "용마산": "0.8"}, "용마산": {"사가정": "0.8", "중곡": "0.9"}, "중곡": {"용마산": "0.9", "군자(능동)": "1.1"}, "어린이대공원(세종대)": {"군자(능동)": "1.1", "건대입구": "0.8"}, "뚝섬유원지": {"건대입구": "1.0", "청담": "2.0"}, "청담": {"뚝섬유원지": "2.0", "강남구청": "1.1"}, "강남구청": {"청담": "1.1", "학동": "0.9", "압구정로데오": "1.2", "선정릉": "0.7"}, "학동": {"강남구청": "0.9", "논현": "1.0"}, "논현": {"학동": "1.0", "반포": "0.9", "신사": "0.7", "신논현": "0.8"}, "반포": {"논현": "0.9", "고속터미널": "0.9"}, "내방": {"고속터미널": "2.2", "총신대입구(이수)": "1.0"}, "남성": {"총신대입구(이수)": "1.0", "숭실대입구(살피재)": "2.0"}, "숭실대입구(살피재)": {"남성": "2.0", "상도(중앙대앞)": "0.9"}, "상도(중앙대앞)": {"숭실대입구(살피재)": "0.9", "장승배기": "0.9"}, "장승배기": {"상도(중앙대앞)": "0.9", "신대방삼거리": "1.2"}, "신대방삼거리": {"장승배기": "1.2", "보라매": "0.8"}, "보라매": {"신대방삼거리": "0.8", "신풍": "0.9"}, "신풍": {"보라매": "0.9", "대림": "1.4"}, "남구로": {"대림": "1.1", "가산디지털단지": "0.8"}, "철산": {"가산디지털단지": "1.4", "광명사거리": "1.3"}, "광명사거리": {"철산": "1.3", "천왕": "1.7"}, "천왕": {"광명사거리": "1.7", "온수": "1.5"}, "까치울": {"온수": "2.2", "부천종합운동장": "1.2"}, "부천종합운동장": {"까치울": "1.2", "춘의": "0.8", "원종": "2.1", "소사": "2.7"}, "춘의": {"부천종합운동장": "0.8", "신중동": "1.0"}, "신중동": {"춘의": "1.0", "부천시청": "1.1"}, "부천시청": {"신중동": "1.1", "상동": "0.9"}, "상동": {"부천시청": "0.9", "삼산체육관": "1.1"}, "삼산체육관": {"상동": "1.1", "굴포천": "0.9"}, "굴포천": {"삼산체육관": "0.9", "부평구청": "0.9"}, "부평구청": {"굴포천": "0.9", "산곡": "1.6"}, "산곡": {"부평구청": "1.6", "석남": "2.6"}, "석남": {"산곡": "2.6"}, "암사": {"천호(풍납토성)": "1.3"}, "강동구청": {"천호(풍납토성)": "0.9", "몽촌토성(평화의문)": "1.6"}, "몽촌토성(평화의문)": {"강동구청": "1.6", "잠실": "0.8"}, "석촌": {"잠실": "1.3", "송파": "0.9", "석촌고분": "1.0", "송파나루": "0.8"}, "송파": {"석촌": "0.9", "가락시장": "0.8"}, "문정": {"가락시장": "0.9", "장지": "0.9"}, "장지": {"문정": "0.9", "복정": "0.9"}, "복정": {"장지": "0.9", "남위례": "1.4", "수서": "3.2", "가천대": "2.4"}, "남위례": {"복정": "1.4", "산성": "1.3"}, "산성": {"남위례": "1.3"}, "남한산성입구": {"단대오거리": "0.8"}, "단대오거리": {"남한산성입구": "0.8", "신흥": "0.8"}, "신흥": {"단대오거리": "0.8", "수진": "0.8"}, "수진": {"신흥": "0.8", "모란": "1.0"}, "모란": {"수진": "1.0", "태평": "0.9", "야탑": "2.3"}, "개화": {"김포공항": "3.6"}, "공항시장": {"김포공항": "0.8", "신방화": "0.8"}, "신방화": {"공항시장": "0.8", "마곡나루": "0.9"}, "마곡나루": {"신방화": "0.9", "양천향교": "1.4", "김포공항": "2.3", "디지털미디어시티": "8.6"}, "양천향교": {"마곡나루": "1.4", "가양": "1.3"}, "가양": {"양천향교": "1.3", "증미": "0.7"}, "증미": {"가양": "0.7", "등촌": "1.0"}, "등촌": {"증미": "1.0", "염창": "0.9"}, "염창": {"등촌": "0.9", "신목동": "0.9"}, "신목동": {"염창": "0.9", "선유도": "1.2"}, "선유도": {"신목동": "1.2", "당산": "1.0"}, "국회의사당": {"당산": "1.5", "여의도": "0.9"}, "샛강": {"여의도": "0.8", "노량진": "1.2"}, "노들": {"노량진": "1.1", "흑석": "1.1"}, "흑석": {"노들": "1.1", "동작": "1.4"}, "구반포": {"동작": "1.0", "신반포": "0.7"}, "신반포": {"구반포": "0.7", "고속터미널": "0.8"}, "사평": {"고속터미널": "1.1", "신논현": "0.9"}, "신논현": {"사평": "0.9", "언주": "0.8", "논현": "0.8", "강남": "0.9"}, "언주": {"신논현": "0.8", "선정릉": "0.9"}, "선정릉": {"언주": "0.9", "삼성중앙": "0.8", "강남구청": "0.7", "선릉": "0.7"}, "삼성중앙": {"선정릉": "0.8", "봉은사": "0.8"}, "봉은사": {"삼성중앙": "0.8", "종합운동장": "1.4"}, "삼전": {"종합운동장": "1.4", "석촌고분": "0.8"}, "석촌고분": {"삼전": "0.8", "석촌": "1.0"}, "송파나루": {"석촌": "0.8", "한성백제": "0.8"}, "한성백제": {"송파나루": "0.8"}, "둔촌오륜": {"올림픽공원(한국체대)": "1.0", "중앙보훈병원": "1.7"}, "중앙보훈병원": {"둔촌오륜": "1.7"}, "서빙고": {"이촌": "1.7", "한남": "1.9"}, "한남": {"서빙고": "1.9", "옥수": "1.6"}, "응봉": {"옥수": "1.8", "왕십리": "1.4"}, "중랑": {"회기": "1.8", "상봉": "0.8"}, "망우": {"상봉": "0.6", "양원": "1.7", "신내": "2.6"}, "양원": {"망우": "1.7", "구리": "3.2"}, "구리": {"양원": "3.2", "도농": "1.7"}, "도농": {"구리": "1.7", "양정": "3.7"}, "양정": {"도농": "3.7", "덕소": "2.3"}, "덕소": {"양정": "2.3", "도심": "1.5"}, "도심": {"덕소": "1.5", "팔당": "4.2"}, "팔당": {"도심": "4.2", "운길산": "6.4"}, "운길산": {"팔당": "6.4", "양수": "1.9"}, "양수": {"운길산": "1.9", "신원": "4.7"}, "신원": {"양수": "4.7", "국수": "2.9"}, "국수": {"신원": "2.9", "아신": "4.1"}, "아신": {"국수": "4.1", "오빈": "2.8"}, "오빈": {"아신": "2.8", "양평": "2.2"}, "원덕": {"양평": "5.8", "용문": "5.8"}, "용문": {"원덕": "5.8", "지평": "3.6"}, "지평": {"용문": "3.6"}, "서강대": {"공덕": "1.0", "홍대입구": "1.9"}, "가좌": {"홍대입구": "1.7", "디지털미디어시티": "1.7", "신촌(경의중앙선)": "2.7"}, "수색": {"디지털미디어시티": "1.7", "화전": "0.6"}, "화전": {"수색": "0.6", "강매": "3.4"}, "강매": {"화전": "3.4", "행신": "2.4"}, "행신": {"강매": "2.4", "능곡": "1.0"}, "능곡": {"행신": "1.0", "대곡": "1.8", "김포공항": "7.4"}, "곡산": {"대곡": "1.8", "백마": "1.6"}, "백마": {"곡산": "1.6", "풍산": "1.7"}, "풍산": {"백마": "1.7", "일산": "1.9"}, "일산": {"풍산": "1.9", "탄현": "1.9"}, "탄현": {"일산": "1.9", "야당": "1.7"}, "야당": {"탄현": "1.7", "운정": "2.0"}, "운정": {"야당": "2.0", "금릉": "3.1"}, "금릉": {"운정": "3.1", "금촌": "3.1"}, "금촌": {"금릉": "3.1", "월롱": "2.1"}, "월롱": {"금촌": "2.1", "파주": "4.1"}, "파주": {"월롱": "4.1", "문산": "4.4"}, "문산": {"파주": "4.4"}, "신촌(경의중앙선)": {"가좌": "2.7", "서울(경의중앙선)": "3.1"}, "계양": {"김포공항": "6.6", "검암": "5.5"}, "검암": {"계양": "5.5", "청라국제도시": "4.8"}, "영종": {"운서": "3.6", "청라국제도시": "10.2"}, "운서": {"영종": "3.6", "공항화물청사": "4.3"}, "공항화물청사": {"운서": "4.3", "인천공항1터미널": "2.6"}, "인천공항1터미널": {"공항화물청사": "2.6", "인천공항2터미널": "5.8"}, "인천공항2터미널": {"인천공항1터미널": "5.8"}, "청라국제도시": {"검암": "4.8", "영종": "10.2"}, "갈매": {"신내": "2.6", "별내": "1.5"}, "별내": {"갈매": "1.5", "퇴계원": "1.6"}, "퇴계원": {"별내": "1.6", "사릉": "3.3"}, "사릉": {"퇴계원": "3.3", "금곡": "3.6"}, "금곡": {"사릉": "3.6", "평내호평": "4.0"}, "평내호평": {"금곡": "4.0", "천마산": "4.0"}, "천마산": {"평내호평": "4.0", "마석": "2.2"}, "마석": {"천마산": "2.2", "대성리": "7.4"}, "대성리": {"마석": "7.4", "청평": "7.5"}, "청평": {"대성리": "7.5", "상천": "4.8"}, "상천": {"청평": "4.8", "가평": "7.1"}, "가평": {"상천": "7.1", "굴봉산": "4.7"}, "굴봉산": {"가평": "4.7", "백양리": "2.9"}, "백양리": {"굴봉산": "2.9", "강촌": "5.3"}, "강촌": {"백양리": "5.3", "김유정": "7.4"}, "김유정": {"강촌": "7.4", "남춘천": "5.9"}, "남춘천": {"김유정": "5.9", "춘천": "2.7"}, "춘천": {"남춘천": "2.7"}, "서울숲": {"왕십리": "2.2", "압구정로데오": "1.9"}, "압구정로데오": {"서울숲": "1.9", "강남구청": "1.2"}, "한티": {"선릉": "1.1", "도곡": "0.7"}, "구룡": {"도곡": "0.6", "개포동": "0.7"}, "개포동": {"구룡": "0.7", "대모산입구": "0.6"}, "대모산입구": {"개포동": "0.6", "수서": "3.2"}, "가천대": {"복정": "2.4", "태평": "1.0"}, "태평": {"가천대": "1.0", "모란": "0.9"}, "야탑": {"모란": "2.3", "이매": "1.7"}, "이매": {"야탑": "1.7", "서현": "1.4", "판교": "1.5", "삼동": "6.885"}, "서현": {"이매": "1.4", "수내": "1.1"}, "수내": {"서현": "1.1", "정자": "1.6"}, "정자": {"수내": "1.6", "미금": "1.8", "판교": "3.1"}, "미금": {"정자": "1.8", "오리": "1.1", "동천": "1.7"}, "오리": {"미금": "1.1", "죽전": "1.8"}, "죽전": {"오리": "1.8", "보정": "1.3"}, "보정": {"죽전": "1.3", "구성": "1.6"}, "구성": {"보정": "1.6", "신갈": "1.6"}, "신갈": {"구성": "1.6", "기흥": "1.4"}, "기흥": {"신갈": "1.4", "상갈": "1.9"}, "상갈": {"기흥": "1.9", "청명": "2.8"}, "청명": {"상갈": "2.8", "영통": "1.1"}, "영통": {"청명": "1.1", "망포": "1.5"}, "망포": {"영통": "1.5", "매탄권선": "1.8"}, "매탄권선": {"망포": "1.8", "수원시청": "1.4"}, "수원시청": {"매탄권선": "1.4", "매교": "1.4"}, "매교": {"수원시청": "1.4", "수원": "1.5"}, "고색": {"수원": "2.7", "오목천": "1.6"}, "오목천": {"고색": "1.6", "어천": "5.1"}, "어천": {"오목천": "5.1", "야목": "2.6"}, "야목": {"어천": "2.6", "사리": "4.7"}, "사리": {"야목": "4.7", "한대앞": "2.2"}, "달월": {"오이도": "2.1", "월곶": "1.5"}, "월곶": {"달월": "1.5", "소래포구": "1.3"}, "소래포구": {"월곶": "1.3", "인천논현": "1.1"}, "인천논현": {"소래포구": "1.1", "호구포": "1.3"}, "호구포": {"인천논현": "1.3", "남동인더스파크": "1.3"}, "남동인더스파크": {"호구포": "1.3", "원인재": "1.0"}, "원인재": {"남동인더스파크": "1.0", "연수": "0.9"}, "연수": {"원인재": "0.9", "송도": "2.7"}, "송도": {"연수": "2.7", "인하대": "2.4"}, "인하대": {"송도": "2.4", "숭의": "1.8"}, "숭의": {"인하대": "1.8", "신포": "1.5"}, "신포": {"숭의": "1.5", "인천": "1.0"}, "양재시민의숲": {"양재": "1.6", "청계산입구": "2.9"}, "청계산입구": {"양재시민의숲": "2.9", "판교": "8.2"}, "판교": {"청계산입구": "8.2", "정자": "3.1", "이매": "1.5"}, "동천": {"미금": "1.7", "수지구청": "2.1"}, "수지구청": {"동천": "2.1", "성복": "1.7"}, "성복": {"수지구청": "1.7", "상현": "2.1"}, "상현": {"성복": "2.1", "광교중앙": "2.3"}, "광교중앙": {"상현": "2.3", "광교": "2.0"}, "광교": {"광교중앙": "2.0"}, "삼동": {"이매": "6.885", "경기광주": "4.9"}, "경기광주": {"삼동": "4.9", "초월": "5.0"}, "초월": {"경기광주": "5.0", "곤지암": "4.9"}, "곤지암": {"초월": "4.9", "신둔도예촌": "6.8"}, "신둔도예촌": {"곤지암": "6.8", "이천": "7.8"}, "이천": {"신둔도예촌": "7.8", "부발": "4.5"}, "부발": {"이천": "4.5", "세종왕릉": "8.3"}, "세종왕릉": {"부발": "8.3", "여주": "5.4"}, "여주": {"세종왕릉": "5.4"}, "솔밭공원": {"북한산우이": "0.8", "4.19 민주묘지": "0.7"}, "북한산우이": {"솔밭공원": "0.8"}, "4.19 민주묘지": {"솔밭공원": "0.7", "가오리": "0.9"}, "가오리": {"4.19 민주묘지": "0.9", "화계": "0.8"}, "화계": {"가오리": "0.8", "삼양": "0.8"}, "삼양": {"화계": "0.8", "삼양사거리": "0.7"}, "삼양사거리": {"삼양": "0.7", "솔샘": "0.8"}, "솔샘": {"삼양사거리": "0.8", "북한산보국문": "1.2"}, "북한산보국문": {"솔샘": "1.2", "정릉": "1.2"}, "정릉": {"북한산보국문": "1.2", "성신여대입구": "1.2"}, "원종": {"김포공항": "4.3", "부천종합운동장": "2.1"}, "소새울": {"소사": "1.7", "시흥대야": "2.1"}, "시흥대야": {"소새울": "2.1", "신천": "1.3"}, "신천": {"시흥대야": "1.3", "신현": "3.4"}, "신현": {"신천": "3.4", "시흥시청": "3.6"}, "시흥시청": {"신현": "3.6", "시흥능곡": "1.3"}, "시흥능곡": {"시흥시청": "1.3", "달미": "2.4"}, "달미": {"시흥능곡": "2.4", "선부": "1.6"}, "선부": {"달미": "1.6", "초지": "1.7"}, "시우": {"초지": "1.4", "원시": "1.5"}, "원시": {"시우": "1.5"}}
#endregion

######## 다익스트라 알고리즘은 https://phaphaya.tistory.com/34 의 코드 사용 (설명은 이 사이트에서)

#region reverse_station_dict
# 엑셀 파일 명
file_name = 'stationList.xlsx'

# 엑셀 파일 읽기
data_list = pd.read_excel(file_name, sheet_name='stationTime', usecols=[0, 1, 2, 3])

# 읽은 엑셀 파일을 데이터 프레임화
df_list = pd.DataFrame(data_list)

# 데이터프레임을 딕셔너리로 변환
station_dict = df_list.set_index('STATN_ID')['STATN_NM'].to_dict()

reverse_station_dict = {}

for station_id, station_name in station_dict.items():
    if station_name not in reverse_station_dict:
        reverse_station_dict[station_name] = [station_id]  # 새로운 역 이름에 대해 리스트로 초기화
    else:
        reverse_station_dict[station_name].append(station_id)  # 이미 존재하는 역 이름에 대해 리스트에 추가
        
arriveMessage = ""
#endregion
        
# valid_values 안에 있는 값으로 prompt 값이 들어오는지 확인하는 함수
def get_valid_value(prompt, valid_values):
    if prompt in valid_values:
        return prompt
    else:
        print("유효하지 않은 입력입니다. 다시 입력해주세요")
        return None

def visitPlace(routing, visit): # 다익스트라
    routing[visit]['visited'] = 1
    for toGo, betweenDist in stationNode[visit].items():
        round_betweenDist = round(float(betweenDist), 1)
        toDist = round(routing[visit]['shortestDist'] + round_betweenDist, 1)
        if (routing[toGo]['shortestDist'] >= toDist) or  not routing[toGo]['route']:
            routing[toGo]['shortestDist'] = toDist
            routing[toGo]['route'] = copy.deepcopy(routing[visit]['route'])
            routing[toGo]['route'].append(visit)

def compareDistance(StatnNm1, StatnNm2): # 다익스트라
    if (StatnNm1 != None and StatnNm2 != None):
        global num
        global routeResult
        global shortestDistResult
        num += 1
        globals()["routing{}".format(num)] = {}
        for place in stationNode.keys():
            globals()["routing{}".format(num)][place]={'shortestDist':0, 'route':[], 'visited':0}
        visitPlace(globals()["routing{}".format(num)], StatnNm1)
        if (StatnNm1 != StatnNm2):
            while 1 :

                minDist = round(max(globals()["routing{}".format(num)].values(), key=lambda x:x['shortestDist'])['shortestDist'], 1)
                toVisit = ''
                for name, search in globals()["routing{}".format(num)].items():
                    if 0 < round(float(search['shortestDist']), 1) <= minDist and not search['visited']:
                        minDist = round(float(search['shortestDist']), 1)
                        toVisit = name

                if toVisit == '':
                    break

                visitPlace(globals()["routing{}".format(num)], toVisit)

            globals()["routing{}".format(num)][StatnNm2]['route'].append(StatnNm2)

            routeResult = globals()["routing{}".format(num)][StatnNm2]['route']
            shortestDistResult = globals()["routing{}".format(num)][StatnNm2]['shortestDist']

            if (booltype):
                print("\n", "[", StatnNm1, "->", StatnNm2,"]")
                print("Route : ", globals()["routing{}".format(num)][StatnNm2]['route'])
                print("ShortestDistance : ", globals()["routing{}".format(num)][StatnNm2]['shortestDist'])

        else:
            print("\n", "[", StatnNm1, "->", StatnNm2,"]")
            print("Route : ", StatnNm1)
            print("ShortestDistance : 0.0")
            routeResult = globals()["routing{}".format(num)][StatnNm2]['route']
            shortestDistResult = globals()["routing{}".format(num)][StatnNm2]['shortestDist']

def multi(startStation1, startStation2, arriveStation):
    global currentShortestDistance
    global booltype
    global routeResult
    global shortestDistResult

    global stopover_arrive_routeResult
    global startStation1_stopover_routeResult
    global startStation2_stopover_routeResult

    global stopover_arrive_shortestDistResult
    global startStation1_stopover_shortestDistResult
    global startStation2_stopover_shortestDistResult

    startStatnNm1 = get_valid_value(startStation1, stationNode)
    startStatnNm2 = get_valid_value(startStation2, stationNode)
    lastStatnNm = get_valid_value(arriveStation, stationNode)

    #############################################
    compareDistance(startStatnNm1, startStatnNm2)

    booltype = False

    for startStatnNm in globals()["routing{}".format(num)][startStatnNm2]['route']:
        compareDistance(startStatnNm, lastStatnNm) # 처음 시작1 ~ 처음 시작2 사이에 있는 역에서 마지막역까지의 거리

    booltype = True

    for i in range(1, num + 1):
        if (globals()["routing{}".format(i)][lastStatnNm]['shortestDist'] <= currentShortestDistance):
            currentShortestRoute = globals()["routing{}".format(i)][lastStatnNm]['route']
            currentShortestDistance = globals()["routing{}".format(i)][lastStatnNm]['shortestDist']

            try:
                stopover = currentShortestRoute[0]
            except:
                pass

    compareDistance(startStatnNm1, stopover) # 처음 시작1 부터 경유역까지
    startStation1_stopover_routeResult = globals()["routing{}".format(num)][stopover]['route']
    startStation1_stopover_shortestDistResult = globals()["routing{}".format(num)][stopover]['shortestDist']
    compareDistance(startStatnNm2, stopover) # 처음 시작2 부터 경유역까지
    startStation2_stopover_routeResult = globals()["routing{}".format(num)][stopover]['route']
    startStation2_stopover_shortestDistResult = globals()["routing{}".format(num)][stopover]['shortestDist']

    stopover_arrive_routeResult = currentShortestRoute
    stopover_arrive_shortestDistResult = currentShortestDistance

    print()
    print("currentShortestRoute : ", currentShortestRoute)
    print("currentShortestDistance : ", currentShortestDistance)
    #############################################

def solo(startStation, arriveStation):
    try:
        startStatnNm = get_valid_value(startStation, stationNode)
        lastStatnNm = get_valid_value(arriveStation, stationNode)

        compareDistance(startStatnNm, lastStatnNm)
    except:
        pass
    
    
def station_time(startStation, nextStation):
    
    global arriveMessage
    global statnNm
    global statnTNm
    mintime = None
    
    current_url = 'http://swopenAPI.seoul.go.kr/api/subway/70757761536c7975333648456d7754/json/realtimeStationArrival/0/50/{}'.format(startStation)
    # 내용 파싱
    get_url = requests.get(current_url)
    # 읽을 수 있게 json화
    current_json_data = json.loads(get_url.text)
    
    if ("errorMessage" in current_json_data):
        for i in range(0, int(current_json_data["errorMessage"]["total"])):
            
            statnNm = (int(current_json_data["realtimeArrivalList"][i]["statnId"]))
            statnTNm = (int(current_json_data["realtimeArrivalList"][i]["statnTid"]))
            
            if (statnNm in reverse_station_dict[startStation]) and (statnTNm in reverse_station_dict[nextStation]):
                message = current_json_data["realtimeArrivalList"][i]["arvlMsg2"]
                time = current_json_data["realtimeArrivalList"][i]["barvlDt"]
                
                
                if isinstance(message, str):
                    if (mintime == None or mintime >= time):
                        mintime = time
                        message = re.sub(r'\([^)]*\)', '', message).strip()
                        message = message.replace("도착", "").strip()
                        arriveMessage = message + " 도착"
    


if __name__ == "__main__":
    pass
    #choiceType = get_valid_value("선택하세요 (1 : 멀티, 2 : 솔로) : ", choice)

    #if (choiceType == "멀티" or choiceType == "1"):
    #multi("서울", "방화", "신도림")
    #elif (choiceType == "솔로" or choiceType == "2"):
        #solo()
    #else:
    #    pass
