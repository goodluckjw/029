import streamlit as st
from processing.law_processor import get_law_list_from_api, get_highlighted_articles

st.set_page_config(page_title="검색어를 포함하는 법률 목록")

st.title("🔍 검색어를 포함하는 법률 목록")
st.caption("📄 본문 중에 검색어를 포함하는 법률의 목록을 반환합니다.")

# 세션 상태 초기화
if "stop_search" not in st.session_state:
    st.session_state.stop_search = False
if "search_word" not in st.session_state:
    st.session_state.search_word = ""
if "clicked_mst" not in st.session_state:
    st.session_state.clicked_mst = None
if "clicked_keyword" not in st.session_state:
    st.session_state.clicked_keyword = ""
if "law_details" not in st.session_state:
    st.session_state.law_details = {}

search_word = st.text_input("찾을 단어", value=st.session_state.search_word)

col1, col2, col3 = st.columns(3)
with col1:
    start = st.button("🚀 시작하기")
with col2:
    stop = st.button("🛑 멈춤")
with col3:
    reset = st.button("🔄 초기화")

if reset:
    st.session_state.search_word = ""
    st.session_state.clicked_mst = None
    st.session_state.clicked_keyword = ""
    st.session_state.stop_search = False
    st.session_state.law_details = {}
    st.rerun()

if stop:
    st.session_state.stop_search = True

if start:
    if not search_word:
        st.warning("검색어를 입력해주세요.")
    else:
        st.session_state.search_word = search_word
        st.session_state.stop_search = False

        with st.spinner("법령 검색 중..."):
            laws = get_law_list_from_api(search_word)
            st.success(f"✅ 총 {len(laws)}개의 법령을 찾았습니다.")

            for law in laws:
                if st.session_state.stop_search:
                    st.warning("⛔ 검색이 중단되었습니다.")
                    break

                with st.expander(f"📘 {law['법령명']} [+]"):
                    st.markdown(f"[🔗 원문 보기]({law['URL']})", unsafe_allow_html=True)

                    key = law['MST']
                    if st.button(f"📂 {law['법령명']} 조문 보기", key=key):
                        st.session_state.clicked_mst = key
                        st.session_state.clicked_keyword = search_word
                        st.session_state.law_details[key] = get_highlighted_articles(key, search_word)

                    if key in st.session_state.law_details:
                        st.markdown(st.session_state.law_details[key], unsafe_allow_html=True)
