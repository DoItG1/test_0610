# Custom Action 구현 (MSSQL + HuggingFace 연동)
from rasa_sdk import Action
from rasa_sdk.executor import CollectingDispatcher
import pyodbc
from transformers import pipeline

class ActionGetSummary(Action):
    def name(self):
        return "action_get_summary"

    def run(self, dispatcher, tracker, domain):
        # MSSQL 예제 쿼리
        query = """
            SELECT '내과 2500건, 소아과 1200건, 정형외과 800건, 기타 500건' AS stats
        """

        try:
            # MSSQL 연결 (본인 환경에 맞게 수정)
            conn = pyodbc.connect(
                "DRIVER={ODBC Driver 17 for SQL Server};"
                "SERVER=192.168.0.100;"
                "DATABASE=EMRDB;"
                "UID=dbuser;"
                "PWD=dbpass"
            )
            cursor = conn.cursor()
            cursor.execute(query)
            result = cursor.fetchone()
            stats_text = result.stats if result else "데이터 없음"

            # Hugging Face summarization pipeline
            summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
            summary = summarizer(stats_text, max_length=50, min_length=10, do_sample=False)

            # 응답
            dispatcher.utter_message(text=f"📊 통계 요약: {summary[0]['summary_text']}")

        except Exception as e:
            dispatcher.utter_message(text=f"오류 발생: {str(e)}")

        return []
