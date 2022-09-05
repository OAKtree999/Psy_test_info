import streamlit as st
import pandas as pd
import numpy as np
import base64
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode

# 페이지 설정
st.set_page_config(
    page_title='정신건강검진 도구 정보',
    layout='wide',
)

# 제목, 부제목, 설명문구
st.header("정신건강검진 도구 정보")
st.warning('''정신건강검진 도구의 기준 및 다운로드를 제공하고자 제작하였습니다.
           아래 테이블의 체크박스를 선택하시면 PDF 미리보기 및 다운로드를 할 수 있습니다. ''')

# 엑셀 파일 데이터 프레임으로 변환
@st.cache
def excel_load(file):
    data = pd.read_excel(file)
    return data

# 풍선 효과
def ballon():
    st.balloons()
    
# PDF 다운로드 버튼
def down_pdf(file_path, file_name):
    with open(f'{file_path}.pdf',"rb") as file:
        st.download_button(
            label="{0} 받기".format(file_name),
            data=file,
            file_name=f'{file_name}.pdf',
            mime="application/octet-stream",
            on_click=ballon, # 클릭시 풍선 효과
        )

# PDF 미리보기 및 다운로드 버튼
def show_pdf(file_name):
    file_path = './PDF_file/{0}'.format(file_name)
    with open(f'{file_path}.pdf',"rb") as file:
        base64_pdf = base64.b64encode(file.read()).decode('utf-8')
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="600" height="890" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)
    down_pdf(file_path, file_name)

# 선택한 심리검사 리스트, 미리보기, 다운로드 버튼
def selected_list():
    test_list = st.multiselect('선택한 심리검사',
                    options=df['약어'],
                    default=df['약어']
                    )
    for i in test_list:
        try:
            show_pdf(i) 
        except:
            st.error('{0} 심리검사의 PDF파일은 없습니다.'.format(i))
            
# 엑셀 파일 불러오기
data = excel_load('psyTable.xlsx')

# Grid 옵션
gb = GridOptionsBuilder.from_dataframe(data)
gb.configure_pagination(enabled=True, paginationAutoPageSize=False, paginationPageSize=30) # 페이지 리스트
gb.configure_side_bar() # 사이드 바 추가
gb.configure_selection('multiple', use_checkbox=True, groupSelectsChildren="Group checkbox select children", header_checkbox=True) # 체크박스 옵션
gridOptions = gb.build() 

# Grid 선택 옵션
grid_response = AgGrid(
    pd.DataFrame(data),
    gridOptions=gridOptions,
    data_return_mode='AS_INPUT',
    update_mode='MODEL_CHANGED',
    columns_auto_size_mode="FIT_CONTENTS",
    enable_enterprise_modules=True,
    # height=350,
)

# 테이블에서 선택된 데이터 Dataframe으로 변환
data = grid_response['data']
selected = grid_response['selected_rows']
df = pd.DataFrame(selected)

# 선택한 데이터 출력
try:
    selected_list()
    st.info('타오른다 제작 😃')
except:
    st.info("테이블에서 '순서' 좌측에 체크박스를 선택해주세요.")

