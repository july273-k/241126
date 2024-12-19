import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

#---------------------------------------
# 한국어 컬럼명 및 추가 속성
column_name_map = {
    'Atomic_Number': '원자번호',
    'Atomic_Mass': '원자량',
    'Atomic_Radius': '원자 반지름',
    'Ionization_Energy': '이온화 에너지',
    'Electronegativity': '전기음성도(파울링 값)',
    'Period': '주기',
    'Group': '족'
}

# 그래프 옵션 (영문 -> 한글)
graph_options = {
    'Atomic_Number': '원자번호',
    'Atomic_Mass': '원자량',
    'Atomic_Radius': '원자 반지름',
    'Ionization_Energy': '이온화 에너지',
    'Electronegativity': '전기음성도(파울링 값)'
}

# 추가로 포함할 속성들(가상 데이터)
# 유효 핵전하(Effective Nuclear Charge), 전자배치(Electronic Configuration), 원자가 전자수(Number of Electrons)
# 여기서는 간단히 가상 데이터를 생성하거나 Atomic_Number 이용
additional_properties = {
    'Effective_Nuclear_Charge': '유효 핵전하',
    'Number_of_Electrons': '원자가 전자수',
    'Electron_Configuration': '전자배치'
}

# 전체 속성 리스트 (추가 속성 포함)
all_properties = {**graph_options, **additional_properties}

@st.cache_data
def load_element_data():
    data = {
        'Element': ['H', 'He', 'Li', 'Be', 'B', 'C', 'N', 'O', 'F', 'Ne',
                    'Na', 'Mg', 'Al', 'Si', 'P', 'S', 'Cl', 'Ar', 'K', 'Ca'],
        'Symbol': ['H', 'He', 'Li', 'Be', 'B', 'C', 'N', 'O', 'F', 'Ne',
                   'Na', 'Mg', 'Al', 'Si', 'P', 'S', 'Cl', 'Ar', 'K', 'Ca'],
        'Atomic_Number': range(1, 21),
        'Atomic_Mass': [1.008, 4.0026, 6.94, 9.0122, 10.81, 12.011, 14.007, 15.999, 18.998, 20.180,
                        22.990, 24.305, 26.982, 28.085, 30.974, 32.06, 35.45, 39.948, 39.0983, 40.078],
        'Atomic_Radius': [53, 31, 167, 112, 87, 67, 56, 48, 42, 38,
                          190, 145, 118, 111, 98, 88, 79, 71, 243, 194],
        'Ionization_Energy': [1312, 2372, 520, 899, 800, 1086, 1402, 1314, 1681, 2081,
                              496, 738, 578, 787, 1012, 1000, 1251, 1521, 419, 590],
        'Electronegativity': [2.20, None, 0.98, 1.57, 2.04, 2.55, 3.04, 3.44, 3.98, None,
                              0.93, 1.31, 1.61, 1.90, 2.19, 2.58, 3.16, None, 0.82, 1.00],
        'Period': [1, 1, 2, 2, 2, 2, 2, 2, 2, 2,
                   3, 3, 3, 3, 3, 3, 3, 3, 4, 4],
        'Group': [1, 18, 1, 2, 13, 14, 15, 16, 17, 18,
                  1, 2, 13, 14, 15, 16, 17, 18, 1, 2]
    }
    df = pd.DataFrame(data)
    # 유효 핵전하 (가상): 원자번호 * 0.85 정도로 가정
    df['Effective_Nuclear_Charge'] = df['Atomic_Number'] * 0.85
    # 전자배치(간단히 대표 형태로)
    electron_config = [
        "1s1", "1s2", "1s2 2s1", "1s2 2s2", "1s2 2s2 2p1", 
        "1s2 2s2 2p2", "1s2 2s2 2p3", "1s2 2s2 2p4", "1s2 2s2 2p5", "1s2 2s2 2p6",
        "1s2 2s2 2p6 3s1", "1s2 2s2 2p6 3s2", "1s2 2s2 2p6 3s2 3p1", "1s2 2s2 2p6 3s2 3p2", 
        "1s2 2s2 2p6 3s2 3p3", "1s2 2s2 2p6 3s2 3p4", "1s2 2s2 2p6 3s2 3p5", "1s2 2s2 2p6 3s2 3p6",
        "1s2 2s2 2p6 3s2 3p6 4s1", "1s2 2s2 2p6 3s2 3p6 4s2"
    ]
    df['Electron_Configuration'] = electron_config
    # 원자가 전자수: 중성 원자 가정 -> 원자가 전자수 = 원자번호
    df['Number_of_Electrons'] = df['Atomic_Number']

    return df

df = load_element_data()

#---------------------------------------
# 세션 관리용 변수
if 'user_type' not in st.session_state:
    st.session_state.user_type = None
if 'student_name' not in st.session_state:
    st.session_state.student_name = None
if 'responses' not in st.session_state:
    st.session_state.responses = []
if 'student_grade' not in st.session_state:
    st.session_state.student_grade = None
if 'student_class' not in st.session_state:
    st.session_state.student_class = None

#---------------------------------------
# 로그인 페이지
def login_page():
    st.title("로그인 페이지")
    user_type = st.radio("사용자 타입 선택", ["학생", "교사"])
    if user_type == "학생":
        grade = st.selectbox("학년:", [1,2,3], key="student_grade")
        clas = st.selectbox("반:", list(range(1,11)), key="student_class")
        name = st.text_input("이름:", key="student_name_input")
        if st.button("로그인", key="student_login"):
            if grade and clas and name:
                st.session_state.user_type = "학생"
                st.session_state.student_name = f"{grade}-{clas}-{name}"
                st.session_state.student_grade = grade
                st.session_state.student_class = clas
    elif user_type == "교사":
        pwd = st.text_input("교사용 비밀번호:", type="password", key="teacher_password")
        if st.button("로그인", key="teacher_login"):
            if pwd == "teacher123":  # 교사용 비밀번호
                st.session_state.user_type = "교사"
            else:
                st.warning("비밀번호가 틀렸습니다.")

#---------------------------------------
# 교사용 대시보드
def teacher_dashboard():
    st.title("교사 대시보드")
    st.write("학생 응답 현황을 반별로 확인할 수 있습니다.")
    selected_class = st.selectbox("반 선택", list(range(1,11)), key="teacher_class_filter")
    if len(st.session_state.responses) > 0:
        df_res = pd.DataFrame(st.session_state.responses)
        # 반 필터링 (Student 컬럼: "학년-반-이름" 형태)
        if 'Student' in df_res.columns:
            df_res['Grade'] = df_res['Student'].apply(lambda x: x.split('-')[0] if '-' in x else None)
            df_res['Class'] = df_res['Student'].apply(lambda x: x.split('-')[1] if '-' in x else None)
            filtered = df_res[df_res['Class'] == str(selected_class)]
            if len(filtered) > 0:
                st.dataframe(filtered)
            else:
                st.write("선택한 반에 대한 제출 응답이 없습니다.")
        else:
            st.write("아직 제출된 응답이 없습니다.")
    else:
        st.write("아직 제출된 응답이 없습니다.")

    if st.button("로그아웃", key="teacher_logout"):
        st.session_state.user_type = None
        st.session_state.student_name = None
        st.session_state.student_grade = None
        st.session_state.student_class = None

#---------------------------------------
# [문제 인식 단계] 페이지
def problem_recognition_page():
    st.header("[문제 인식 단계] 데이터 시각화의 중요성 이해하기")
    st.write("**역사적 사례 살펴보기:**")
    st.write("1. 콜레라 확산 지도(John Snow) - 영상:")
    st.video("https://youtu.be/qf30Occ3_KI?si=U7m4yISdqC_dczrp")
    st.write("2. 멘델레예프의 주기율표 - 영상:")
    st.video("https://youtu.be/fPnwBITSmgU?si=hiqFPCVOLjU4NWwn")

    st.write("Q1. 왜 데이터 시각화가 중요한가?")
    q1 = st.text_area("답변:", key="q1_response")
    st.write("Q2. 시각화를 통해 어떤 패턴을 보다 쉽게 이해할 수 있는가?")
    q2 = st.text_area("답변:", key="q2_response")
    if st.button("답변 제출", key="q_response_submit"):
        st.session_state.responses.append({
            "Student": st.session_state.student_name,
            "Grade": st.session_state.student_grade,
            "Class": st.session_state.student_class,
            "Q1": q1,
            "Q2": q2
        })
        st.success("답변이 제출되었습니다!")

#---------------------------------------
# [시각화 단계] 페이지
def visualization_page():
    st.header("[시각화 단계] 데이터 속성을 선택하여 그래프 만들기")
    st.write("**원소 데이터 확인하기**")

    df_ko = df.rename(columns=column_name_map)
    df_ko['원소'] = df['Element']  # 원소명 컬럼 추가
    st.dataframe(df_ko)

    st.subheader("그래프 설정 (직접 그래프의 종류, X축, Y축 속성을 선택)")
    x_axis_label = st.selectbox("X축에 표시할 데이터", list(graph_options.values()), key="x_axis")
    y_axis_label = st.selectbox("Y축에 표시할 데이터", list(graph_options.values()), key="y_axis")
    color_axis_label = st.selectbox("색상으로 구분할 데이터", ['None'] + list(graph_options.values()), key="color_axis")
    graph_type = st.selectbox("그래프 유형 선택", ['산점도 (Scatter Plot)', '선 그래프 (Line Plot)', '막대 그래프 (Bar Chart)'], key="graph_type")

    inv_graph_options = {v: k for k, v in graph_options.items()}
    x_axis = inv_graph_options[x_axis_label]
    y_axis = inv_graph_options[y_axis_label]
    color_axis = inv_graph_options[color_axis_label] if color_axis_label != 'None' else None

    # 주기 필터
    period_filter = st.multiselect("표시할 주기 선택 (선택하지 않으면 모든 주기 표시)", sorted(df['Period'].unique()), key="period_filter")
    if period_filter:
        data = df[df['Period'].isin(period_filter)]
    else:
        data = df

    if graph_type == '산점도 (Scatter Plot)':
        fig = px.scatter(
            data, x=x_axis, y=y_axis,
            color=color_axis,
            title=f"{graph_options[x_axis]} vs {graph_options[y_axis]} (산점도)",
            hover_data=['Element', 'Symbol']
        )
    elif graph_type == '선 그래프 (Line Plot)':
        fig = px.line(
            data, x=x_axis, y=y_axis,
            color=color_axis,
            title=f"{graph_options[x_axis]} vs {graph_options[y_axis]} (선 그래프)",
            hover_data=['Element', 'Symbol']
        )
    elif graph_type == '막대 그래프 (Bar Chart)':
        fig = px.bar(
            data, x=x_axis, y=y_axis,
            color=color_axis,
            title=f"{graph_options[x_axis]} vs {graph_options[y_axis]} (막대 그래프)",
            hover_data=['Element', 'Symbol']
        )

    st.plotly_chart(fig)

    # 패턴 서술
    st.write("위 그래프를 보고 패턴을 서술하세요 (자유 응답):")
    graph_analysis = st.text_area("그래프 분석:", key="graph_analysis")
    if st.button("그래프 분석 제출", key="graph_analysis_submit"):
        st.session_state.responses.append({
            "Student": st.session_state.student_name,
            "Grade": st.session_state.student_grade,
            "Class": st.session_state.student_class,
            "Graph Analysis": graph_analysis
        })
        st.success("그래프 분석이 제출되었습니다!")

    st.write("---")
    st.write("**추가 활동 예시:**")
    st.write("- 활동A: 원자량 값을 이용한 주기별 원자 반지름 막대 그래프")
    st.write("- 활동B: 원자 반지름 값을 이용한 주기별 원자 반지름 막대 그래프")
    st.write("- 활동C: 이온화 에너지를 이용한 주기별 그래프 (점/선 그래프)")
    st.write("- 활동D: 전기음성도 히트맵으로 표현")

#---------------------------------------
# [해석 단계] 페이지
def interpretation_page():
    st.header("[해석 단계] 전자배치 및 유효 핵전하와의 연계 해석")

    # 원소 데이터 (한글 컬럼) 준비
    df_ko = df.rename(columns=column_name_map)
    df_ko['원소'] = df['Element']
    # 전기음성도(파울링 값) 칼럼 이미 있음
    # 인터랙티브 주기율표에 사용할 속성 선택
    prop_list = list(all_properties.values())
    selected_property = st.selectbox("관찰할 속성 선택", prop_list, key="interpret_selected_property")
    inv_all_props = {v: k for k,v in all_properties.items()}
    selected_eng_property = inv_all_props[selected_property]

    # 전기음성도(파울링 값) -> 이미 df에 Electronegativity로 있으니 df_ko에도 반영
    df_ko['전기음성도(파울링 값)'] = df['Electronegativity']

    # 주기율표 인터랙티브 시각화 (snippet 반영)
    # 여기서는 x를 'Group'으로, y를 'Period'로 해서 주기율표 형태를 구성
    fig = px.scatter(
        df_ko,
        x="족",
        y="주기",
        size=selected_property,
        color="전기음성도(파울링 값)",
        text="원소",
        hover_data=["원소", "원자번호", selected_property],
        size_max=40,
        labels={"족": "족(Group)", "주기": "주기(Period)"},
        title=f"주기율표 - {selected_property}"
    )
    fig.update_yaxes(autorange="reversed")  # 주기율표 형식으로 Y축 반전
    st.plotly_chart(fig, use_container_width=True)

    response = st.text_area(f"{selected_property}의 경향성을 서술해보세요:", key="interpretation_response")
    if st.button("응답 제출", key="analysis"):
        if response.strip():
            new_response = {
                "Student": st.session_state.student_name,
                "Grade": st.session_state.student_grade,
                "Class": st.session_state.student_class,
                "활동": "주기적 경향성 정리",
                "질문": f"{selected_property} 경향성",
                "응답": response.strip()
            }
            st.session_state.responses.append(new_response)
            st.success("응답이 제출되었습니다!")

    st.write("**전자배치 관점:**")
    st.write("- 같은 주기에서 오른쪽으로 갈수록 양성자 수 증가 → 유효 핵전하 증가")
    st.write("- 전자껍질 수 동일 → 가리움 효과 변화 적음 → 오른쪽으로 갈수록 원자 반지름 감소, 이온화 에너지 증가, 전기음성도 증가")

    st.write("**교사 비계 질문 예시:**")
    st.write("- “원자 반지름이 왜 오른쪽으로 갈수록 작아질까요?”")
    st.write("- “이온화 에너지가 커진다는 것은 전자를 떼어내기 어렵다는 의미인데, 왜 그렇게 될까요?”")
    st.write("- “유효 핵전하란 무엇이고, 왜 주기적 경향성과 관련이 있을까요?”")

    st.subheader("해석 활동 (자유 응답)")
    periodic_trend = st.text_area("주기적 경향성에 대한 해석:", key="periodic_trend")
    electronic_effect = st.text_area("전자배치와 유효 핵전하 관련 해석:", key="electronic_effect")

    if st.button("해석 제출", key="interpretation_submit"):
        st.session_state.responses.append({
            "Student": st.session_state.student_name,
            "Grade": st.session_state.student_grade,
            "Class": st.session_state.student_class,
            "Periodic_Trend": periodic_trend,
            "Electronic_Effect": electronic_effect
        })
        st.success("해석 답변이 제출되었습니다!")

#---------------------------------------
# [추가 활동] 페이지
def additional_activities_page():
    st.header("[추가 활동] 속성 선택 및 히트맵 통한 상관관계 탐색")
    st.write("여기서 원하는 속성을 선택하여 X축, Y축을 지정하거나 히트맵으로 상관관계를 확인할 수 있습니다.")

    # 모든 속성(유효 핵전하, 전자배치, 원자가 전자수 포함) 사용 가능
    numeric_cols = ['Atomic_Number', 'Atomic_Mass', 'Atomic_Radius', 'Ionization_Energy', 'Electronegativity', 'Effective_Nuclear_Charge', 'Number_of_Electrons']
    # 전자배치는 문자열이므로 수치형 그래프에서는 제외. 하지만 상관관계에서는 제외.
    # 그래프용 셀렉션 (수치형)
    available_for_xy = {c: all_properties[c] for c in all_properties if c in ['Atomic_Number','Atomic_Mass','Atomic_Radius','Ionization_Energy','Electronegativity','Effective_Nuclear_Charge','Number_of_Electrons']}

    x_axis_label_add = st.selectbox("X축 데이터 선택", list(available_for_xy.values()), key="x_axis_add")
    y_axis_label_add = st.selectbox("Y축 데이터 선택", list(available_for_xy.values()), key="y_axis_add")
    color_axis_label_add = st.selectbox("색상 데이터 선택", ['None'] + list(available_for_xy.values()), key="color_axis_add")
    graph_type_add = st.selectbox("그래프 유형 선택", ['산점도 (Scatter Plot)', '선 그래프 (Line Plot)', '막대 그래프 (Bar Chart)'], key="graph_type_add")

    inv_all_props = {v: k for k,v in all_properties.items()}
    x_axis_add = inv_all_props[x_axis_label_add]
    y_axis_add = inv_all_props[y_axis_label_add]
    color_axis_add = inv_all_props[color_axis_label_add] if color_axis_label_add != 'None' else None

    period_filter_add = st.multiselect("표시할 주기 선택 (선택하지 않으면 모든 주기 표시)", sorted(df['Period'].unique()), key="period_filter_add")
    if period_filter_add:
        data_add = df[df['Period'].isin(period_filter_add)]
    else:
        data_add = df

    if graph_type_add == '산점도 (Scatter Plot)':
        fig_add = px.scatter(
            data_add, x=x_axis_add, y=y_axis_add,
            color=color_axis_add,
            title=f"{all_properties[x_axis_add]} vs {all_properties[y_axis_add]} (산점도)",
            hover_data=['Element', 'Symbol']
        )
    elif graph_type_add == '선 그래프 (Line Plot)':
        fig_add = px.line(
            data_add, x=x_axis_add, y=y_axis_add,
            color=color_axis_add,
            title=f"{all_properties[x_axis_add]} vs {all_properties[y_axis_add]} (선 그래프)",
            hover_data=['Element', 'Symbol']
        )
    elif graph_type_add == '막대 그래프 (Bar Chart)':
        fig_add = px.bar(
            data_add, x=x_axis_add, y=y_axis_add,
            color=color_axis_add,
            title=f"{all_properties[x_axis_add]} vs {all_properties[y_axis_add]} (막대 그래프)",
            hover_data=['Element', 'Symbol']
        )

    st.plotly_chart(fig_add)

    # 히트맵
    st.subheader("히트맵으로 상관관계 확인하기")
    selected_properties = st.multiselect("상관관계 분석할 속성 선택", list(all_properties.values()), 
                                         default=list(graph_options.values()))
    selected_eng = [inv_all_props[p] for p in selected_properties if p in inv_all_props]

    corr_df = df[selected_eng].corr(numeric_only=True)

    fig_corr, ax = plt.subplots()
    sns.heatmap(corr_df, annot=True, cmap='RdBu_r', 
                xticklabels=[all_properties[c] for c in corr_df.columns],
                yticklabels=[all_properties[r] for r in corr_df.columns], ax=ax)
    ax.set_title("선택한 속성들의 상관관계 히트맵")
    st.pyplot(fig_corr)

    st.write("히트맵에서 관찰되는 상관관계를 해석해보세요:")
    heatmap_analysis = st.text_area("히트맵 해석:", key="heatmap_analysis")
    if st.button("히트맵 해석 제출", key="heatmap_analysis_submit"):
        st.session_state.responses.append({
            "Student": st.session_state.student_name,
            "Grade": st.session_state.student_grade,
            "Class": st.session_state.student_class,
            "Heatmap Analysis": heatmap_analysis
        })
        st.success("히트맵 해석이 제출되었습니다!")

    st.write("또한, 전자배치와 유효 핵전하 관점에서 왜 이러한 상관관계가 나타나는지 생각해보세요.")

    if st.button("로그아웃", key="student_logout_additional"):
        st.session_state.user_type = None
        st.session_state.student_name = None
        st.session_state.student_grade = None
        st.session_state.student_class = None

#---------------------------------------
def main():
    if st.session_state.user_type is None:
        # 로그인 페이지
        login_page()
    else:
        if st.session_state.user_type == "교사":
            teacher_dashboard()
        elif st.session_state.user_type == "학생":
            tabs = st.tabs(["문제 인식 단계", "시각화 단계", "해석 단계", "추가 활동"])
            with tabs[0]:
                problem_recognition_page()
            with tabs[1]:
                visualization_page()
            with tabs[2]:
                interpretation_page()
            with tabs[3]:
                additional_activities_page()

#---------------------------------------
if __name__ == "__main__":
    main()
