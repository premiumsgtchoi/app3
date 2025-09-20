# 0. 필요한 라이브러리를 가져옵니다.
import streamlit as st
import random
# import requests # [API] API 요청을 위해 requests 라이브러리를 추가합니다.

#-----------------------------------------------------------------
# 0. [API] 날씨 API 요청 함수
#-----------------------------------------------------------------

# 도시 이름과 API 키를 받아 해당 도시의 날씨 정보를 가져오는 함수입니다.
# def get_weather(city, api_key):
#     base_url = "https://api.openweathermap.org/data/2.5/weather"
#     params = {
#         'q': city,
#         'appid': api_key,
#         'units': 'metric', # 섭씨 온도로 받기
#         'lang': 'kr'      # 한국어로 설명 받기
#     }
#     try:
#         response = requests.get(base_url, params=params, timeout=5)
#         data = response.json()
        
#         # API 응답이 성공적일 때(cod == 200) 필요한 정보만 추출하여 반환합니다.
#         if data['cod'] == 200:
#             weather = {
#                 'description': data['weather'][0]['description'],
#                 'icon': data['weather'][0]['icon'],
#                 'temperature': data['main']['temp']
#             }
#             return weather
#         else:
#             return None # 실패 시 None 반환
#     except Exception:
#         return None # 예외 발생 시 None 반환

#-----------------------------------------------------------------
# 1. 화면 구성 (UI: User Interface) 및 Session State 초기화
#-----------------------------------------------------------------

st.set_page_config(page_title="오늘의 발표자 뽑기", page_icon="🎯")

# [핵심] Session State 초기화: 앱의 '기억 저장소'를 설정합니다.
if 'picked_numbers' not in st.session_state:
    st.session_state.picked_numbers = []

st.title("🎯 오늘의 발표자 뽑기")
st.divider()

total_students = st.number_input("전체 학생 수를 입력하세요.", min_value=1, value=25, step=1)
allow_duplicates = st.checkbox("중복 추첨 허용")
st.divider()

#-----------------------------------------------------------------
# 2. 발표자 뽑기 로직 (Session State 사용 버전)
#-----------------------------------------------------------------

# 버튼과 결과 표시 영역을 컬럼으로 나눕니다.
col1, col2 = st.columns([0.4, 0.6])

with col1:
    start_button = st.button("🔍 발표자 뽑기", use_container_width=True)

with col2:
    if start_button:
        picked_number = None # 뽑힌 번호를 저장할 변수 초기화
        
        # --- 중복 추첨을 허용하지 않는 경우 ---
        if not allow_duplicates:
            all_numbers = list(range(1, total_students + 1))
            available_numbers = [num for num in all_numbers if num not in st.session_state.picked_numbers]

            if available_numbers:
                picked_number = random.choice(available_numbers)
                st.session_state.picked_numbers.append(picked_number)
            else:
                st.warning("모든 학생이 발표를 완료했습니다! 🥳")

        # --- 중복 추첨을 허용하는 경우 ---
        else:
            picked_number = random.randint(1, total_students)
            st.session_state.picked_numbers.append(picked_number)

        # --- 결과 표시 ---
        if picked_number is not None:
            st.header(f"🎉 {picked_number}번! 당첨! 🎉")
            st.balloons()
            
        # # -----------------------------------------------------------------
        # # [API] 날씨 정보 표시 기능 추가
        # # -----------------------------------------------------------------
        # st.divider()
        # st.markdown("##### 발표할 장소의 현재 날씨는?")
        
        # with st.spinner('실시간 날씨 정보를 가져오는 중...'):
        #     # st.secrets를 통해 .streamlit/secrets.toml 파일의 API 키를 안전하게 불러옵니다.
        #     try:
        #         api_key = st.secrets["openweathermap"]["api_key"]
        #         weather_data = get_weather("Seoul", api_key)

        #         if weather_data:
        #             icon_url = f"https://openweathermap.org/img/wn/{weather_data['icon']}@2x.png"
                    
        #             sub_col1, sub_col2 = st.columns([0.7, 0.3])
        #             with sub_col1:
        #                 st.metric("현재 기온", f"{weather_data['temperature']} °C")
        #                 st.write(f"날씨: **{weather_data['description']}**")
        #             with sub_col2:
        #                 st.image(icon_url)
        #         else:
        #             st.error("날씨 정보를 가져오는 데 실패했습니다.")
        #     except KeyError:
        #         st.error("API Key를 secrets.toml 파일에 설정해주세요.")
        # # -----------------------------------------------------------------


#-----------------------------------------------------------------
# 3. 추첨 이력 표시
#-----------------------------------------------------------------

st.divider()
st.subheader("📜 **추첨된 번호**")
st.subheader(str(st.session_state.picked_numbers))
reset_buttion = st.button("⚠️ 추첨 이력 초기화", key="reset_button")
if reset_buttion:
    st.session_state.picked_numbers = []
    st.success("추첨 이력이 초기화되었습니다.")
