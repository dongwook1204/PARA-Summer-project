from sentence_transformers import SentenceTransformer, util  # 문장 임베딩 모델과 유틸 함수 임포트
from konlpy.tag import Okt  # 한국어 형태소 분석기 Okt 임포트
from math_list import get_terms  # 수학 용어 리스트를 불러오는 함수 임포트

MODEL_NAME = 'snunlp/KR-SBERT-V40K-klueNLI-augSTS'  # 사용할 한국어 SBERT 모델 이름 지정
sentence_model = SentenceTransformer(MODEL_NAME)  # SBERT 모델 로드
tokenizer = Okt()  # Okt 형태소 분석기 객체 생성

def get_user_input():
    topic_input = input("주제를 입력하세요: ")  # 사용자로부터 주제 입력 받기
    text_input = input("관련된 글을 입력하세요: ")  # 사용자로부터 관련 글 입력 받기
    return topic_input, text_input  # 두 입력값 반환

def extract_nouns(text):
    return tokenizer.nouns(text)  # 입력된 텍스트에서 명사만 추출하여 반환

def find_related_math_terms(topic, text, math_terms):
    cleaned_topic = topic.replace(" ", "")  # 주제에서 공백 제거
    extracted_nouns = extract_nouns(text)  # 텍스트에서 명사 추출

    candidate_terms = [noun for noun in extracted_nouns if noun in math_terms]  # 추출한 명사 중 수학 용어 리스트에 있는 것만 후보로 선정
    stopwords = {"정리", "수학"}  # 제외할 불용어 집합 정의
    filtered_terms = []  # 불용어 및 중복 제거 후 용어를 저장할 리스트 초기화
    for term in candidate_terms:
        if term not in stopwords and term not in filtered_terms:  # 불용어가 아니고 중복되지 않는 경우
            filtered_terms.append(term)  # 리스트에 추가

    if not filtered_terms:  # 만약 필터링 후 용어가 하나도 없다면
        return []  # 빈 리스트 반환

    topic_sentence = cleaned_topic + "와 관련된 수학 개념"  # 주제 문장 생성
    term_sentences = [term + "라는 수학 용어" for term in filtered_terms]  # 각 용어에 대한 문장 생성

    topic_vector = sentence_model.encode(topic_sentence, convert_to_tensor=True)  # 주제 문장 임베딩 벡터 생성
    term_vectors = sentence_model.encode(term_sentences, convert_to_tensor=True)  # 용어 문장 임베딩 벡터 생성

    similarities = util.pytorch_cos_sim(topic_vector, term_vectors)[0]  # 주제와 각 용어 간 코사인 유사도 계산
    sorted_indices = similarities.argsort(descending=True)  # 유사도 높은 순서대로 인덱스 정렬
    top_indices = sorted_indices[:4]  # 상위 4개 용어 인덱스 선택

    return [(filtered_terms[i], float(similarities[i])) for i in top_indices]  # 상위 4개 용어와 유사도 튜플 리스트 반환

def make_quiz(text, related_terms):
    quiz_text = text  # 원본 텍스트를 퀴즈 텍스트로 복사
    term_positions = []  # 용어와 위치를 저장할 리스트 초기화

    for term, _ in related_terms:
        pos = text.find(term)  # 텍스트에서 해당 용어의 위치 찾기
        if pos != -1:  # 만약 용어가 텍스트에 있으면
            term_positions.append((pos, term))  # 위치와 용어를 튜플로 저장

    term_positions.sort(key=lambda x: x[0])  # 용어가 등장하는 위치 기준으로 정렬
    ordered_terms = [term for _, term in term_positions]  # 위치순으로 정렬된 용어 리스트 생성

    for term in ordered_terms:
        quiz_text = quiz_text.replace(term, "____", 1)  # 각 용어를 텍스트에서 첫번째만 빈칸으로 교체

    return quiz_text, ordered_terms  # 빈칸 처리된 텍스트와 정답 용어 리스트 반환

math_terms = get_terms("math_terms.txt")  # 텍스트 파일에서 수학 용어 리스트 불러오기
topic, text = get_user_input()  # 사용자로부터 주제와 관련 글 입력 받기
related_terms = find_related_math_terms(topic, text, math_terms)  # 주제와 관련된 용어 찾기

if related_terms:  # 관련 용어가 있으면
    print("\n주제와 관련된 용어들:")
    for index, (term, score) in enumerate(related_terms, start=1):  # 관련 용어 출력
        print(f"{index}. {term} (유사도: {score:.3f})")

    quiz_text, correct_terms = make_quiz(text, related_terms)  # 퀴즈용 텍스트와 정답 리스트 생성
    print("\n퀴즈 형식:")
    print(quiz_text)  # 퀴즈 텍스트 출력

    user_answer = input("\n빈칸에 들어갈 단어들을 순서대로 입력하세요 (띄어쓰기로 구분함): ").split()  # 사용자 답안 입력받고 리스트로 분리

    print("\n정답 확인:")
    for i, (correct, user) in enumerate(zip(correct_terms, user_answer), start=1):  # 정답과 사용자 답안 비교
        if correct == user:  # 맞으면
            print(f"{i}. {user} ✅ 정답")
        else:  # 틀리면
            print(f"{i}. {user} ❌ (정답: {correct})")
else:  # 관련 용어가 없으면
    print("\n주제와 관련된 용어가 없음.")  # 메시지 출력
