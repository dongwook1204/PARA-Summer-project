from fastapi import FastAPI
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer, util
from konlpy.tag import Okt
from .math_list import get_terms
from . import ai
import jpype.imports
import jpype
import os

app = FastAPI(title="ReloadK AI Backend")


@app.on_event("startup")
def load_models():
    ai.ai_loader.load_sentence_model()
    ai.ai_loader.load_math_terms()




class AILoader:
    def __init__(self):
        self.sentence_model = None
        self.tokenizer = None
        self.math_terms = None

    def load_models(self):
        if self.sentence_model is None:
            MODEL_NAME = "snunlp/KR-SBERT-V40K-klueNLI-augSTS"
            print(f"모델 '{MODEL_NAME}' 로드 시도...")
            self.sentence_model = SentenceTransformer(MODEL_NAME)
            print("SentenceTransformer 모델 로드 완료.")

        if self.tokenizer is None:
            print("Okt 토크나이저 초기화 시도...")
            self.tokenizer = Okt()
            print("Okt 토크나이저 초기화 완료.")

        if self.math_terms is None:
            print("수학 용어 데이터 로드 시도...")
            try:
                self.math_terms = get_terms("math_terms.txt")
                print(f"AILoader.load_models: math_terms 로드 완료. 길이: {len(self.math_terms)}")
            except Exception as e:
                print(f"AILoader.load_models: math_terms 로드 중 예외 발생: {e}")
                raise

        print("모든 모델 및 데이터 로드 성공.")

    def get_tokenizer(self):
        if self.tokenizer is None:
            raise RuntimeError("Okt tokenizer has not been initialized.")
        return self.tokenizer

    def get_sentence_model(self):
        if self.sentence_model is None:
            raise RuntimeError("SentenceTransformer model has not been loaded.")
        return self.sentence_model

    def get_math_terms(self):
        if self.math_terms is None:
            raise RuntimeError("math_terms data has not been loaded.")
        return self.math_terms

ai_loader = AILoader()

def ensure_models_loaded():
    if ai_loader.sentence_model is None:
        print("AI 모델이 아직 로드되지 않았습니다. 자동 로드 시도 중...")
        ai_loader.load_models()
@app.on_event("startup")
async def startup_event():
    print(f"FastAPI Startup Event: PID {os.getpid()} - JVM 초기화 및 모델 로드 시작")


    ai_loader.load_models()
    print("모든 모델 및 데이터 로드 완료.")
    print(f"Startup Event: ai_loader.sentence_model is None: {ai_loader.sentence_model is None}")
    print(f"Startup Event: ai_loader.tokenizer is None: {ai_loader.tokenizer is None}")
    print(f"Startup Event: ai_loader.math_terms is None: {ai_loader.math_terms is None}")
    if ai_loader.math_terms is not None:
        print(f"Startup Event: math_terms 데이터 길이: {len(ai_loader.math_terms)}")


@app.on_event("shutdown")
def shutdown_event():
    print(f"FastAPI Shutdown Event: PID {os.getpid()} - JVM 종료 시작")
    if jpype.isJVMStarted():
        jpype.shutdownJVM()
        print("JVM이 성공적으로 종료되었습니다!")
    else:
        print("JVM이 시작되지 않아 종료할 필요가 없습니다.")

class SubjectRequest(BaseModel):
    topic: str
    text: str

class SubjectResponse(BaseModel):
    related_terms: list
    quiz: str
    answers: list

def extract_nouns(text: str):
    return ai_loader.get_tokenizer().nouns(text)

def find_related_math_terms(topic: str, text: str, math_terms_data: list):
    sentence_model_instance = ai_loader.get_sentence_model()

    cleaned_topic = topic.replace(" ", "")
    extracted_nouns = extract_nouns(text)

    candidate_terms = [noun for noun in extracted_nouns if noun in math_terms_data]
    stopwords = {"정리", "수학"}
    filtered_terms = []
    for term in candidate_terms:
        if term not in stopwords and term not in filtered_terms:
            filtered_terms.append(term)

    if not filtered_terms:
        return []

    topic_sentence = cleaned_topic + "와 관련된 수학 개념"
    term_sentences = [term + "라는 수학 용어" for term in filtered_terms]

    topic_vector = sentence_model_instance.encode(topic_sentence, convert_to_tensor=True)
    term_vectors = sentence_model_instance.encode(term_sentences, convert_to_tensor=True)

    similarities = util.pytorch_cos_sim(topic_vector, term_vectors)[0]
    sorted_indices = similarities.argsort(descending=True)
    top_indices = sorted_indices[:4]

    return [(filtered_terms[i], float(similarities[i])) for i in top_indices]

def make_quiz(text: str, related_terms: list):
    quiz_text = text
    term_positions = []

    for term, _ in related_terms:
        pos = text.find(term)
        if pos != -1:
            quiz_text = quiz_text.replace(term, "____", 1)
            term_positions.append((pos, term))

    term_positions.sort(key=lambda x: x[0])
    ordered_terms = [term for _, term in term_positions]

    return quiz_text, ordered_terms

def generate_cards(subject: str):
    ensure_models_loaded()
    math_terms_data = get_terms()
    related_terms = find_related_math_terms(subject, subject, math_terms_data)
    cards = []
    for term in related_terms:
        question, answer = make_quiz(term, subject)
        cards.append({
            "prompt": question,
            "answer": answer
        })
    return cards