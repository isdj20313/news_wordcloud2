# =====================================================================
#  네이버 뉴스 실시간 의제 워드클라우드 생성기
#  - 사용자가 입력한 키워드로 네이버 뉴스 '제목'을 크롤링하고,
#    한국어 '명사'만 추출해 빈도순으로 워드클라우드를 만들어 저장/표시한다.
#  - 전체 흐름: 한글폰트 설정 → 크롤링 → 전처리/명사추출 → 시각화/저장
# =====================================================================

import os  # os: 폴더 생성(makedirs), 경로 존재 확인(path.exists), 환경변수(JAVA_HOME) 설정에 쓰는 운영체제 모듈
import re  # re: 정규표현식 모듈. 이메일/특수문자 제거, 파일명 금지문자 치환에 사용
import sys  # sys: 운영체제 종류 확인(sys.platform)과 프로그램 강제 종료(sys.exit)에 사용
import time  # time: 시작 시각 기록·경과시간 측정(5초 제한), 요청 사이 대기(sleep)에 사용
from collections import Counter  # Counter: 리스트 안 각 단어가 몇 번 나오는지 자동으로 세어주는 도구
import matplotlib.pyplot as plt  # plt: 완성된 워드클라우드를 화면 팝업 창으로 띄우는 시각화 도구
from matplotlib import font_manager  # font_manager: 팝업 제목의 한글이 깨지지 않도록 폰트를 등록하는 도구
from wordcloud import WordCloud  # WordCloud: 단어 빈도에 따라 글자 크기를 다르게 그려주는 워드클라우드 도구
import requests  # requests: 네이버 서버에 접속해 HTML 소스코드를 받아오는 인터넷 통신 도구
from bs4 import BeautifulSoup  # BeautifulSoup: 받아온 HTML에서 원하는 부분(뉴스 제목)을 골라내는 분석 도구
from konlpy.tag import Okt  # Okt: 한국어 문장에서 조사를 떼고 '명사'만 추출하는 형태소 분석기


# 1. 환경 설정 및 한글 폰트 지정
def get_font_path():  # 현재 운영체제에 맞는 한글 폰트 파일 경로를 찾아서 돌려주는 함수
    # OS별 한글 폰트 후보 경로 목록 (아래에서 실제로 존재하는 첫 번째 경로를 사용)
    if sys.platform.startswith('win'):  # 운영체제가 윈도우('win'으로 시작)이면
        candidates = ['C:/Windows/Fonts/malgun.ttf']  # 윈도우 기본 한글 폰트 '맑은 고딕' 경로
    elif sys.platform.startswith('darwin'):  # 운영체제가 맥('darwin')이면
        candidates = [  # 맥의 한글 폰트(애플고딕) 후보들
            '/System/Library/Fonts/Supplemental/AppleGothic.ttf',  # 맥 기본 애플고딕 위치
            '/Library/Fonts/AppleGothic.ttf',  # 일부 맥 버전의 애플고딕 위치
        ]
    else:  # 그 외(리눅스, 깃허브 코드스페이스 등)이면
        candidates = [  # 리눅스에서 흔히 쓰는 한글 폰트(나눔/노토) 후보들
            '/usr/share/fonts/truetype/nanum/NanumGothic.ttf',  # 나눔고딕
            '/usr/share/fonts/truetype/nanum/NanumBarunGothic.ttf',  # 나눔바른고딕
            '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',  # 노토 산스 CJK 폰트(opentype 경로)
            '/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc',  # 노토 산스 CJK 폰트(truetype 경로)
        ]
    for path in candidates:  # 후보 경로를 하나씩 확인
        if os.path.exists(path):  # 그 경로에 폰트 파일이 실제로 존재하면
            return path  # 그 경로를 결과로 돌려주고 함수 종료
    return None  # 후보 중 설치된 폰트가 하나도 없으면 None 반환(기본 폰트 사용→한글이 깨질 수 있음)


FONT_PATH = get_font_path()  # 프로그램 시작 시 한 번 폰트 경로를 찾아 전역 변수 FONT_PATH에 저장해 둠


# 2. 크롤링 기능
def crawl_naver_news(keyword, max_titles=60):  # 키워드로 네이버 뉴스 제목을 max_titles개까지 수집하는 함수
    print(f"'{keyword}' 키워드로 실시간 네이버 뉴스를 수집합니다...")  # 진행 상황 안내 출력
    titles = []  # 수집한 뉴스 제목을 담을 빈 리스트
    page = 1  # 검색 결과 페이지 번호 (1페이지부터 시작)

    # 네이버가 자동 프로그램(봇)으로 의심해 차단하지 않도록, 실제 브라우저처럼 보이는 요청 헤더 설정
    headers = {
        # User-Agent: 크롬 브라우저로 접속한 것처럼 위장하는 정보
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        # Accept: 브라우저가 받을 수 있는 콘텐츠(문서) 형식 목록
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        # Accept-Language: 한국어 페이지를 우선 받도록 요청
        'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
        # Referer: 네이버 메인에서 들어온 것처럼 보이게 하는 직전 페이지 주소
        'Referer': 'https://www.naver.com/'
    }

    start_time = time.time()  # 비기능 요구사항(5초 이내 출력): 수집 시작 시각을 기록해 둠

    while len(titles) < max_titles:  # 목표 개수(max_titles)를 채울 때까지 페이지를 넘기며 반복
        if time.time() - start_time > 4.0:  # 비기능 요구사항: 수집이 4초를 넘으면(전체 5초 보장용)
            print("시간 제한(5초)으로 인해 현재까지 수집된 데이터로만 진행합니다.")  # 안내 메시지 출력 후
            break  # 반복을 멈추고 다음 단계로 이동

        start_num = (page - 1) * 10 + 1  # 네이버 검색의 '시작 글번호' 규칙(1, 11, 21 ...)을 페이지 번호로 계산
        # 검색 URL 생성: where=news(뉴스 검색), sort=1(최신순), start=시작 글번호
        # requests.utils.quote(keyword): 한글 키워드가 주소에서 깨지지 않도록 인코딩
        url = f"https://search.naver.com/search.naver?where=news&query={requests.utils.quote(keyword)}&sm=tab_opt&sort=1&start={start_num}"

        try:  # 비기능 요구사항: 네트워크 오류에 대비한 예외 처리 블록
            response = requests.get(url, headers=headers, timeout=3)  # 해당 URL에 접속 요청 (최대 3초 대기, 5초 예산 보호)
            if response.status_code != 200:  # 응답 코드가 200(정상)이 아니면 (예: 403 차단)
                print(f"네이버 서버 응답 오류 (코드: {response.status_code})")  # 오류 코드 안내
                break  # 수집 중단
        except requests.exceptions.RequestException as e:  # 인터넷 끊김 등 통신 자체가 실패하면
            print(f" 네트워크 연결 오류가 발생했습니다: {e}")  # 오류 내용 안내
            return []  # 빈 리스트를 반환하며 함수 종료

        soup = BeautifulSoup(response.text, 'html.parser')  # 받아온 HTML 문자열을 분석하기 쉬운 객체로 변환

        # 요구사항 반영: HTML 안의 모든 <a>(링크) 태그를 가져옴 (뉴스 제목 대부분이 링크 글자이기 때문)
        links = soup.find_all('a')

        page_titles_found = 0  # 이번 페이지에서 새로 담은 제목 개수를 셀 변수
        for link in links:  # 링크 태그를 하나씩 검사
            title_text = link.get_text().strip()  # 링크 안의 순수한 글자만 꺼내고 앞뒤 공백 제거

            if len(title_text) >= 15 and len(title_text) <= 60:  # 글자 수가 15~60자인 것만 '뉴스 제목'으로 간주
                if '구독' in title_text or '신문' in title_text or '바로가기' in title_text:  # 광고/메뉴성 단어가 들어있으면
                    continue  # 제목이 아니라고 보고 건너뜀
                if title_text not in titles:  # 아직 리스트에 없는(중복이 아닌) 제목이면
                    titles.append(title_text)  # 리스트에 새 제목 추가
                    page_titles_found += 1  # 이번 페이지 수집 개수 1 증가

            if len(titles) >= max_titles:  # 목표 개수를 다 채웠으면
                break  # 더 검사하지 않고 이 페이지 반복 종료

        if page_titles_found == 0 and page > 2:  # 2페이지를 넘었는데도 새로 담은 제목이 하나도 없으면
            break  # 더 가져올 게 없다고 보고 전체 반복 종료

        page += 1  # 다음 페이지로 이동
        time.sleep(0.3)  # 너무 빠른 연속 요청으로 차단되지 않도록 0.3초 쉼

    if not titles:  # 반복이 끝났는데 수집된 제목이 하나도 없으면
        print("수집된 뉴스 제목이 없습니다. 네이버 차단 우회를 위해 다른 키워드로 시도해보거나 잠시 후 다시 실행해주세요.")  # 안내
    else:  # 제목이 하나라도 있으면
        print(f"총 {len(titles)}개의 뉴스 제목 수집 성공!")  # 수집 개수 안내

    return titles  # 수집한 제목 리스트를 반환


# 3. 데이터 전처리 및 명사 골라내기
def preprocess_and_extract_nouns(titles):  # 제목 리스트를 받아 명사만 추려 빈도를 세는 함수
    print("데이터 전처리 및 명사 추출 시작...")  # 진행 상황 안내
    # 자바 실행 경로(JAVA_HOME): Okt가 자바 기반이라 필요. 윈도우에서만 지정(리눅스/맥의 기존 설정 보호)
    if sys.platform.startswith('win'):  # 운영체제가 윈도우이면
        os.environ['JAVA_HOME'] = r'C:\Program Files\Java\jdk-26.0.1'  # 설치된 JDK 경로를 환경변수로 지정
    okt = Okt()  # 한국어 형태소 분석기 Okt 객체 생성 (이때 내부 자바 엔진이 가동됨)
    all_nouns = []  # 모든 제목에서 추출한 명사를 모을 리스트

    # 자주 나오지만 주제와 무관한, 분석에 의미 없는 단어 모음 — 결과에서 제외할 '불용어'
    stopwords = {'기자', '뉴스', '연합뉴스', '뉴시스', '뉴스1', 'YTN', '속보', '개최', '출시', '선정', '진행', '오전', '오후', '이번', '금지', '배포', '무단'}

    for title in titles:  # 제목을 하나씩 처리
        # 요구사항 반영: 제목에 섞인 기자 이메일 주소(xxx@yyy.zzz)를 찾아 삭제
        title = re.sub(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', '', title)
        # 한글/영어/숫자/공백만 남기고 그 외 특수문자·한자·기호는 모두 삭제
        title = re.sub(r'[^가-힣a-zA-Z0-9\s]', '', title)

        try:  # 형태소 분석 중 오류가 나도 멈추지 않도록 예외 처리
            nouns = okt.nouns(title)  # 문장에서 조사를 떼고 명사만 리스트로 추출
            # 요구사항 반영: 2글자 이상이면서 불용어가 아닌 명사만 남김 (한 글자·불용어 제거)
            filtered_nouns = [noun for noun in nouns if len(noun) >= 2 and noun not in stopwords]
            all_nouns.extend(filtered_nouns)  # 걸러낸 명사들을 전체 리스트에 합침
        except Exception:  # 분석 중 어떤 오류가 발생하면
            continue  # 그 제목은 건너뛰고 다음 제목으로

    return Counter(all_nouns)  # {단어: 등장횟수} 형태로 빈도를 세어 반환


# 4. 워드클라우드 시각화 및 자동 저장
def generate_wordcloud(word_counts, keyword):  # 단어 빈도(word_counts)로 워드클라우드를 만들어 저장·표시하는 함수
    if not word_counts:  # 단어가 하나도 없으면(분석 결과가 비어 있으면)
        print(" 추출된 명사가 없어 워드클라우드를 만들 수 없습니다.")  # 안내 후
        return  # 함수 종료

    print("워드클라우드 이미지 생성 중...")  # 진행 상황 안내

    if FONT_PATH is None:  # 비기능 요구사항(한글 깨짐 방지): 한글 폰트를 못 찾았으면
        print("경고: 한글 폰트를 찾지 못했습니다. 글자가 깨질 수 있습니다. (리눅스: 'sudo apt install fonts-nanum' 후 다시 실행하세요)")  # 경고·해결법 안내

    wc = WordCloud(  # 워드클라우드 생성기를 설정값과 함께 만듦
        font_path=FONT_PATH,  # 한글이 보이도록 위에서 찾은 폰트 지정
        background_color='white',  # 배경색: 흰색
        width=800,  # 이미지 가로 크기(픽셀)
        height=600,  # 이미지 세로 크기(픽셀)
        max_words=80,  # 화면에 표시할 최대 단어 수(상위 80개)
        colormap='viridis'  # 글자 색상 테마(viridis: 보라~노랑 계열)
    )
    # 요구사항 반영: 단어 빈도수에 따라 글자 크기를 다르게 해서 워드클라우드 그림을 생성
    wc.generate_from_frequencies(word_counts)
    # 요구사항 반영: 결과 이미지를 저장할 폴더 경로 지정
    output_dir = './output'
    if not os.path.exists(output_dir):  # 그 폴더가 아직 없으면
        os.makedirs(output_dir)  # 새로 만듦

    safe_keyword = re.sub(r'[\\/*?:"<>|]', '_', keyword)  # 파일명에 못 쓰는 금지문자(\ / : * ? " < > |)를 '_'로 치환
    save_path = f"{output_dir}/wordcloud_{safe_keyword}.png"  # 최종 저장 파일 경로 만들기

    wc.to_file(save_path)  # 워드클라우드 이미지를 png 파일로 저장
    print(f" 워드클라우드가 로컬 폴더에 성공적으로 저장되었습니다: {save_path}")  # 저장 위치 안내

    # 깃허브 코드스페이스 등에서는 팝업이 안 뜰 수 있어, 저장된 파일을 직접 보라고 안내
    print("팁: 왼쪽 파일 목록에 생성된 'output' 폴더 안의 png 파일을 클릭하면 이미지를 직접 볼 수 있습니다!")

    # 요구사항 반영(시각화 출력): 만든 워드클라우드를 화면 팝업 창으로 띄움
    if FONT_PATH:  # 폰트를 찾았다면 팝업 '제목'의 한글도 깨지지 않게 matplotlib 기본 폰트로 등록
        plt.rcParams['font.family'] = font_manager.FontProperties(fname=FONT_PATH).get_name()
    plt.figure(figsize=(8, 6))  # 팝업 창(그림 영역)의 크기 설정
    plt.imshow(wc, interpolation='bilinear')  # 워드클라우드 이미지를 부드럽게(bilinear) 화면에 표시
    plt.axis('off')  # 그래프의 축·눈금 숨기기(그림만 깔끔하게 보이도록)
    plt.title(f"'{keyword}' 뉴스 워드클라우드")  # 팝업 창 상단 제목 설정
    plt.show()  # 팝업 창 띄우기 (데스크톱 GUI 환경에서 표시됨)


#  메인 실행
if __name__ == "__main__":  # 이 파일을 직접 실행했을 때만 아래 코드가 동작(다른 파일에서 import하면 실행 안 됨)
    print("=========================================")  # 시작 화면 윗 구분선
    print(" 네이버 뉴스 실시간 의제 워드클라우드 생성기")  # 프로그램 제목 출력
    print("=========================================")  # 시작 화면 아랫 구분선

    user_keyword = input("분석하고 싶은 뉴스 키워드를 입력하세요: ").strip()  # 사용자에게 키워드를 입력받고 앞뒤 공백 제거

    if not user_keyword:  # 아무것도 입력하지 않았으면(빈 문자열이면)
        print("키워드가 입력되지 않았습니다.")  # 안내 후
        sys.exit()  # 프로그램 종료

    start_total_time = time.time()  # 전체 소요 시간 측정을 위한 시작 시각 기록

    news_titles = crawl_naver_news(user_keyword, max_titles=60)  # ① 키워드로 뉴스 제목 크롤링

    if news_titles:  # 수집된 제목이 있으면
        word_counts = preprocess_and_extract_nouns(news_titles)  # ② 전처리 후 명사 추출·빈도 계산
        generate_wordcloud(word_counts, user_keyword)  # ③ 워드클라우드 생성·저장·표시
        print(f"총 소요 시간: {time.time() - start_total_time:.2f}초")  # 전체 걸린 시간 출력
