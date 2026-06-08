import os # 컴퓨터에 폴더나 파일을 만드는 도구
import re # 특수문자나 이메일을 지우고 (워드클라우드에 쓰일 명사 찾기) 글자 찾는 도구
import sys # 윈도우or맥 내 컴퓨터 운영체제를 확인하는 도구
import time #빠른 크롤링을 위한 시간을 재는 타이머 도구
from collections import Counter # 크롤링한 결과 각 단어가 몇 번 나오는지 세어주는 도구
import matplotlib.pyplot as plt # 그려진 워드클라우드를 이미지로 띄우는 도구
from matplotlib import font_manager # 화면 팝업 제목의 한글이 깨지지 않도록 폰트를 등록하는 도구
from wordcloud import WordCloud # 워드클라우드(글자 크기를 빈도별로 다르게 구름모양으로 시각화) 도구
import requests # 네이버 인터넷에서 HTML 소스코드를 받아오는 도구
from bs4 import BeautifulSoup # 받아온 소스코드에서 뉴스 제목만 골라내는 도구
from konlpy.tag import Okt # 한국어 문장에서 명사만 골라내는 형태소 분석 도구


# 1. 환경 설정 및 한글 폰트 지정
def get_font_path():
    # OS별 한글 폰트 후보 경로 목록 (실제로 존재하는 첫 번째 경로를 사용)
    if sys.platform.startswith('win'):
        candidates = ['C:/Windows/Fonts/malgun.ttf']  # 윈도우: 맑은 고딕
    elif sys.platform.startswith('darwin'):
        candidates = [  # 맥: 애플고딕
            '/System/Library/Fonts/Supplemental/AppleGothic.ttf',
            '/Library/Fonts/AppleGothic.ttf',
        ]
    else:
        candidates = [  # 리눅스(깃허브 코드스페이스 등): 나눔/노토 한글 폰트
            '/usr/share/fonts/truetype/nanum/NanumGothic.ttf',
            '/usr/share/fonts/truetype/nanum/NanumBarunGothic.ttf',
            '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',
            '/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc',
        ]
    for path in candidates:  # 후보 중 실제 설치된 폰트를 찾으면 그 경로를 반환
        if os.path.exists(path):
            return path
    return None  # 한글 폰트를 못 찾으면 None (기본 폰트라 한글이 깨질 수 있음)


FONT_PATH = get_font_path() # 찾아낸 폰트 경로를 FONT_PATH 라는 변수에 저장


# 2. 크롤링 기능
def crawl_naver_news(keyword, max_titles=60):
    print(f"'{keyword}' 키워드로 실시간 네이버 뉴스를 수집합니다...")
    titles = [] # 긁어온 뉴스 제목들을 넣을 리스트 생성
    page = 1  # 1페이지부터 시작
   
    # 네이버가 봇으로 생각해 차단할 수도 있음을 방지하기 위해
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
        'Referer': 'https://www.naver.com/'
    }
   
    start_time = time.time() # 비기능 요구사항: 5초 이내 출력을 위해 현재 시작 시간 기록
   
    while len(titles) < max_titles:  # 목표한 제목 개수(60개)를 채울 때까지 무한 반복 실행


        if time.time() - start_time > 4.0: # 비기능 요구사항: 검색 후 시간이 4초가 넘어가면 강제로 멈추고 다음 단계로 이동
            print("시간 제한(5초)으로 인해 현재까지 수집된 데이터로만 진행합니다.")
            break
           
        start_num = (page - 1) * 10 + 1 # 네이버 뉴스 검색 페이지 번호 규칙 계산 (1페이지=1, 2페이지=11, 3페이지=21...)
        # 최신순으로 정렬
        # 검색할 네이버 URL 주소 생성 (requests.utils.quote는 한글 키워드가 깨지지 않게 변환해 줌)
        url = f"https://search.naver.com/search.naver?where=news&query={requests.utils.quote(keyword)}&sm=tab_opt&sort=1&start={start_num}"
       
        try: # 비기능 요구사항: 네트워크 오류 예외 처리. 네이버 주소에 접속 요청 (5초 동안 응답 없으면 끝)
            response = requests.get(url, headers=headers, timeout=3)  # 5초 예산 보호: 단일 요청 대기 상한 3초
            if response.status_code != 200: # 응답 번호가 200(정상)이 아니면 (ex) 403 에러 등)
                print(f"네이버 서버 응답 오류 (코드: {response.status_code})")
                break
        except requests.exceptions.RequestException as e: # 인터넷이 아예 끊긴 경우
            print(f" 네트워크 연결 오류가 발생했습니다: {e}")
            return []
           
        soup = BeautifulSoup(response.text, 'html.parser')  # 네이버에서 받아온 복잡한 HTML 텍스트를 컴퓨터가 분석하기 좋게 BeautifulSoup으로 변환
       
         # 요구사항 반영 : HTML 소스코드 안에서 뉴스 제목을 뜻하는 태그만 가져옴
        links=soup.find_all('a')


        page_titles_found=0 # 뉴스 제목 실제로 몇 개 가져왔는지 셀 변수 설정
        for link in links: # 가져온 뉴스 제목 점검
            title_text=link.get_text().strip() # 링크 내부에 있는 순수한 글자만 가져옴


            if len(title_text) >= 15 and len(title_text) <=60: # 15자 이상 60자 이하 문장만 두고 삭제
                if '구독' in title_text or '신문' in title_text or '바로가기' in title_text: #이 단어 들이 들어간 광고 등의 문장 삭제
                    continue
                if title_text not in titles: # 이미 리스트에 저장되어있지않거나 비어있지 않아야 실행
                    titles.append(title_text) # 리스트에 새로운 제목 추가
                    page_titles_found +=1 # 페이지에서 가져온 뉴스 올리기


            if len(titles) >= max_titles: # 수집 목표 개수 60개 달성하면
                break #더 이상 검사 안함


        if page_titles_found ==0 and page >2: # 다 돌았는데 하나도 없다면
            break # 종료


        page +=1 # 다음페이지로
        time.sleep(0.3) # 0.3초 멈춤
       
    if not titles: # 다 돌았는데도 제목이 하나도 없다면 예외 안내
        print("수집된 뉴스 제목이 없습니다. 네이버 차단 우회를 위해 다른 키워드로 시도해보거나 잠시 후 다시 실행해주세요.")
    else:
        print(f"총 {len(titles)}개의 뉴스 제목 수집 성공!")
       
    return titles # 수집 완료된 뉴스 제목 리스트를 반환


# 3. 데이터 전처리 및 명사 골라내기
def preprocess_and_extract_nouns(titles):
    print("데이터 전처리 및 명사 추출 시작...")
    # 자바 실행 경로(JAVA_HOME) — 윈도우에서만 강제 지정 (리눅스/맥의 기존 설정을 덮어쓰지 않도록)
    if sys.platform.startswith('win'):
        os.environ['JAVA_HOME'] = r'C:\Program Files\Java\jdk-26.0.1'
    okt = Okt() # 오픈소스인 한국어 형태소 분석기(Okt) 실행
    all_nouns = []  # 걸러진 명사들만 담을 리스트 생성
   
    # 필터링 해야할 무의미한 단어 리스트 생성
    stopwords = {'기자', '뉴스', '연합뉴스', '뉴시스', '뉴스1', 'YTN', '속보', '개최', '출시', '선정', '진행', '오전', '오후', '이번', '금지', '배포', '무단'}
   
    for title in titles:
        # 요구사항 반영 : 뉴스 제목에 포함된 기자 이메일 주소 삭제
        title = re.sub(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', '', title)
        # 특수문자 및 한자, 기호 제거 (한글, 영어, 숫자만 남김)
        title = re.sub(r'[^가-힣a-zA-Z0-9\s]', '', title)
       
        try:
            nouns = okt.nouns(title)
            # 형태소 분석기가 문장에서 조사를 다 떼어내고 명사만 잘라냄
            # 요구사항 반영 : 글자 길이가 2글자 이상이고, 불용어 리스트에 포함되지 않는 단어만 필터링
            filtered_nouns = [noun for noun in nouns if len(noun) >= 2 and noun not in stopwords]
            all_nouns.extend(filtered_nouns) # 최종 리스트에 추가


        except Exception:
            continue  # 에러 나는 문장은 패스하고 다음 문장 진행
       
    return Counter(all_nouns) # 단어별로 몇 번 등장했는지 카운트해서 반환


# 4. 워드클라우드 시각화 및 자동 저장
def generate_wordcloud(word_counts, keyword):
    if not word_counts: # 만약 단어가 하나도 없다면 안내 후 종료
        print(" 추출된 명사가 없어 워드클라우드를 만들 수 없습니다.")
        return
       
    print("워드클라우드 이미지 생성 중...")

    if FONT_PATH is None:  # 비기능 요구사항(한글 깨짐 방지): 한글 폰트를 못 찾았으면 경고
        print("경고: 한글 폰트를 찾지 못했습니다. 글자가 깨질 수 있습니다. (리눅스: 'sudo apt install fonts-nanum' 후 다시 실행하세요)")
   
    wc = WordCloud(
        font_path=FONT_PATH, # 위에서 설정한 한글 폰트
        background_color='white', # 배경색은 흰색
        width=800,
        height=600, # 이미지 가로세로 크기 결정
        max_words=80, # 최대 80개 단어까지만 화면에 표시
        colormap='viridis' # 워드클라우드 글자 색상 테마 선택
    )
    # 요구사항 반영 : 계산된 단어 빈도수를 기반으로 글자 크기를 다르게한 워드클라우드 생성
    wc.generate_from_frequencies(word_counts)
     # 요구사항 반영 : 결과를 저장할 폴더를 컴퓨터에 새로 만듦
    output_dir = './output'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
       
    safe_keyword = re.sub(r'[\\/*?:"<>|]', '_', keyword) # 파일 이름에 들어갈 수 없는 금지 문자(\ / : * ? " < > |) 언더바(_)로
    save_path = f"{output_dir}/wordcloud_{safe_keyword}.png" # 저장할 파일 경로 설정
   
    wc.to_file(save_path)
    print(f" 워드클라우드가 로컬 폴더에 성공적으로 저장되었습니다: {save_path}")
   
    # 깃허브 코드스페이스에서는 팝업 창이 안 뜰 수 있으므로 저장 안내
    print("팁: 왼쪽 파일 목록에 생성된 'output' 폴더 안의 png 파일을 클릭하면 이미지를 직접 볼 수 있습니다!")

    # 요구사항 반영(시각화 출력) : 생성된 워드클라우드를 화면 팝업으로 띄움
    if FONT_PATH:  # matplotlib 제목 글자도 한글이 깨지지 않도록 폰트 지정
        plt.rcParams['font.family'] = font_manager.FontProperties(fname=FONT_PATH).get_name()
    plt.figure(figsize=(8, 6))
    plt.imshow(wc, interpolation='bilinear')  # 워드클라우드 이미지를 화면에 표시
    plt.axis('off')  # 축/눈금 숨김
    plt.title(f"'{keyword}' 뉴스 워드클라우드")
    plt.show()  # 팝업 창 출력 (GUI 환경에서 표시됨)


#  메인 실행
if __name__ == "__main__":
    print("=========================================")
    print(" 네이버 뉴스 실시간 의제 워드클라우드 생성기")
    print("=========================================")
   
    user_keyword = input("분석하고 싶은 뉴스 키워드를 입력하세요: ").strip()
   
    if not user_keyword:
        print("키워드가 입력되지 않았습니다.")
        sys.exit()
       
    start_total_time = time.time()
   
    news_titles = crawl_naver_news(user_keyword, max_titles=60)
   
    if news_titles:
        word_counts = preprocess_and_extract_nouns(news_titles)
        generate_wordcloud(word_counts, user_keyword)
        print(f"총 소요 시간: {time.time() - start_total_time:.2f}초")
