import datetime
from math import floor, ceil
from typing import Dict, List
import numpy as np
import google.generativeai as genai
import json
import re

# 🚨 1. [필수] TIME_ZONE 상수 정의 추가 (SajuEngine 밖에서 사용됨)
TIME_ZONE = datetime.timezone(datetime.timedelta(hours=9)) 

# --- [1. 사주 데이터 상수 임포트 (saju_data.py 파일 필수)] ---
try:
    from saju_data import (
        CHEONGAN, JIJI, GANJI_60, 
        DAY_STEM_TO_TIME_STEM_START_INDEX, 
        YEAR_STEM_TO_MONTH_STEM_INDEX,
        O_HAENG_MAP,
        TEN_GAN_PERSONA
    )
except ImportError:
    print("🚨 오류: saju_data.py 파일이 없거나 상수가 누락되었습니다.")
    raise

# --------------------------------------------------------------------------
# 2. 임상 데이터 로드 함수
# --------------------------------------------------------------------------
def load_clinical_data(file_path: str = "saju-study-data-all.txt") -> str:
    """
    saju-study-data-all.txt 파일을 읽어와 AI 프롬프트에 삽입할 수 있는 문자열로 반환합니다.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data_content = f.read().strip()
            return data_content
            
    except FileNotFoundError:
        return "🚨 임상 데이터 파일 (saju-study-data-all.txt)을 찾을 수 없습니다. 분석의 깊이가 제한됩니다."
    except Exception as e:
        return f"🚨 임상 데이터 로드 중 오류 발생: {e}"

# --------------------------------------------------------------------------
# 3. 십성 계산 관련 상수 및 함수 추가 (app.py의 calculate_sewoon_sipsin 호환)
# --------------------------------------------------------------------------

# 천간 십성 인덱스 (일간 기준)
# 🚨 십성 관계는 saju_data.py에 없으므로 여기에 임시로 정의합니다.
TEN_GODS_MAP_STEM = {
    # (일간_인덱스, 타천간_인덱스): 십성
    (0, 0): '일원', (0, 1): '겁재', (0, 2): '식신', (0, 3): '상관', (0, 4): '편재', (0, 5): '정재', (0, 6): '편관', (0, 7): '정관', (0, 8): '편인', (0, 9): '정인', 
    (1, 0): '겁재', (1, 1): '일원', (1, 2): '상관', (1, 3): '식신', (1, 4): '정재', (1, 5): '편재', (1, 6): '정관', (1, 7): '편관', (1, 8): '정인', (1, 9): '편인', 
    (2, 0): '편인', (2, 1): '정인', (2, 2): '비견', (2, 3): '겁재', (2, 4): '식신', (2, 5): '상관', (2, 6): '편재', (2, 7): '정재', (2, 8): '편관', (2, 9): '정관', 
    (3, 0): '정인', (3, 1): '편인', (3, 2): '겁재', (3, 3): '일원', (3, 4): '상관', (3, 5): '식신', (3, 6): '정재', (3, 7): '편재', (3, 8): '정관', (3, 9): '편관', 
    (4, 0): '편관', (4, 1): '정관', (4, 2): '편인', (4, 3): '정인', (4, 4): '일원', (4, 5): '겁재', (4, 6): '식신', (4, 7): '상관', (4, 8): '편재', (4, 9): '정재', 
    (5, 0): '정관', (5, 1): '편관', (5, 2): '정인', (5, 3): '편인', (5, 4): '겁재', (5, 5): '일원', (5, 6): '상관', (5, 7): '식신', (5, 8): '정재', (5, 9): '편재', 
    (6, 0): '편재', (6, 1): '정재', (6, 2): '편관', (6, 3): '정관', (6, 4): '편인', (6, 5): '정인', (6, 6): '일원', (6, 7): '겁재', (6, 8): '식신', (6, 9): '상관', 
    (7, 0): '정재', (7, 1): '편재', (7, 2): '정관', (7, 3): '편관', (7, 4): '정인', (7, 5): '편인', (7, 6): '겁재', (7, 7): '일원', (7, 8): '상관', (7, 9): '식신', 
    (8, 0): '식신', (8, 1): '상관', (8, 2): '편재', (8, 3): '정재', (8, 4): '편관', (8, 5): '정관', (8, 6): '편인', (8, 7): '정인', (8, 8): '일원', (8, 9): '겁재', 
    (9, 0): '상관', (9, 1): '식신', (9, 2): '정재', (9, 3): '편재', (9, 4): '정관', (9, 5): '편관', (9, 6): '정인', (9, 7): '편인', (9, 8): '겁재', (9, 9): '일원', 
}

# 지지 십성 인덱스 (지장간을 고려하지 않은, 지지의 대표 오행 기준)
JIJI_TO_STEM_INDEX = {
    '子': 9, '丑': 5, '寅': 0, '卯': 1, '辰': 4, '巳': 2, '午': 3, '未': 5, '申': 6, '酉': 7, '戌': 4, '亥': 8
}
# 🚨 壬(8), 癸(9)의 일원 인덱스가 0~9 기준으로 '비견'이 아닌 '일원'으로 처리되도록 TEN_GODS_MAP_STEM도 수정되었습니다.

def calculate_pillar_sipsin(day_master: str, ganji: str) -> Dict:
    """
    일간을 기준으로 특정 간지(柱)의 천간(Stem)과 지지(Branch)의 십성(Ten Gods)을 계산합니다.
    """
    if len(ganji) != 2 or day_master not in CHEONGAN:
        return {'stem_ten_god': 'N/A', 'branch_ten_god': 'N/A'}

    day_idx = CHEONGAN.index(day_master)
    stem = ganji[0]
    branch = ganji[1]

    # 1. 천간 십성 계산
    stem_idx = CHEONGAN.index(stem)
    stem_sipsin = TEN_GODS_MAP_STEM.get((day_idx, stem_idx), 'N/A')
    
    # 2. 지지 십성 계산 (대표 오행의 십성)
    # 지지에 해당하는 천간 인덱스를 가져와서 일간과 비교
    branch_stem_idx = JIJI_TO_STEM_INDEX.get(branch)
    if branch_stem_idx is not None:
        branch_sipsin = TEN_GODS_MAP_STEM.get((day_idx, branch_stem_idx), 'N/A')
    else:
        branch_sipsin = 'N/A'

    return {'stem_ten_god': stem_sipsin, 'branch_ten_god': branch_sipsin}

# app.py에서 calculate_sewoon_sipsin 이름으로 호환되도록 래핑
calculate_sewoon_sipsin = calculate_pillar_sipsin


# --------------------------------------------------------------------------
# 4. AI 프롬프트 및 분석 함수 추가 (app.py 오류 해결)
# --------------------------------------------------------------------------

def get_system_instruction() -> str:
    """AI 모델의 역할과 응답 형식을 정의하는 시스템 지침을 반환합니다."""
    return """
    당신은 '희구소(Hidden Luck Lab)'의 사주 전문 AI 멘토입니다. 당신의 임무는 고객의 만세력 데이터를 바탕으로 현실적이고 심리 명리 기반의 따뜻한 조언을 제공하는 것입니다.
    
    [응답 형식]:
    모든 분석은 오직 하나의 JSON 객체로 출력해야 합니다. JSON의 스키마는 다음과 같습니다:
    {
        "summary_card": {
            "keyword": "2026년 운세의 핵심 키워드",
            "best_month": "양력 X월 (최고의 달)",
            "risk": "가장 주의해야 할 리스크",
            "action_item": "핵심 실천 전략 한 문장"
        },
        "detailed_analysis": {
            "wealth_luck": "재물운 (전문 용어 사용, 상세 설명)",
            "career_luck": "직업/사업운 (전문 용어 사용, 상세 설명)",
            "love_family_luck": "애정/가정운 (전문 용어 사용, 상세 설명)",
            "change_luck": "변동운 (전문 용어 사용, 상세 설명)",
            "health_advice": "건강 조언 (전문 용어 사용, 상세 설명)"
        },
        "customer_analysis": {
            "wealth_luck": "재물운 (쉬운 말, 감성적 설명)",
            "career_luck": "직업/사업운 (쉬운 말, 감성적 설명)",
            "love_family_luck": "애정/가정운 (쉬운 말, 감성적 설명)",
            "change_luck": "변동운 (쉬운 말, 감성적 설명)",
            "health_advice": "건강 조언 (쉬운 말, 감성적 설명 - 전문 용어 없이 일상적인 표현 사용)"
        },
        "qa_section": {
            "q1": "고객 질문 1 (그대로)",
            "a1": "고객 질문 1에 대한 명쾌하고 실전적인 답변 (쉬운 말, 전문 용어 없이, 300자 이내)",
            "q2": "고객 질문 2 (그대로)",
            "a2": "고객 질문 2에 대한 명쾌하고 실전적인 답변 (쉬운 말, 전문 용어 없이, 300자 이내)"
        },
        "final_message": "고객의 일간 페르소나를 반영한 최종 격려 메시지 (100자 이내)",
        "radar_chart": {
            "labels": ["추진력", "수익화", "협상력", "안정성", "리더십"],
            "current": [8, 5, 6, 7, 7],
            "future": [7, 8, 9, 7, 8]
        },
        "monthly_flow": [70, 75, 80, 65, 85, 50, 60, 70, 95, 80, 75, 70],
        "monthly_guide": {
            "1": {"title": "월별 테마", "wealth": "재물운 등급/조언", "career": "직업운 조언", "love": "애정운 조언", "focus": "핵심 집중점", "caution": "주의사항", "action": "실천 행동"}
            // ... 2월부터 12월까지
        },
        "key_actions": ["30일 이내 실전 행동 1", "30일 이내 실전 행동 2", "30일 이내 실전 행동 3"]
    }

    [응답 지침]:
    1. 모든 응답 텍스트는 **따뜻하고 감성적인** 문체(고객용)와 **전문적인 용어**(전문가용)를 구분하여 작성하십시오.
    2. detailed_analysis의 내용은 **전문 용어를 상세히 풀어서** 설명해야 합니다. (운영자/전문가 참고용)
    3. customer_analysis의 내용은 **쉬운 말**로 감성적이고 공감할 수 있도록 작성하십시오. 명리학 전문 용어(십성, 편관, 정재 등)를 사용하지 마십시오.
    4. 텍스트 내에서 줄 바꿈이 필요한 경우 반드시 '\\n' 문자열을 사용하십시오.
    5. '일원'을 제외하고 십성 용어 앞에 이중 별표를 붙이지 마십시오. (사용자 요구사항 반영)
    6. 고객의 질문(q1, q2)에 대해 명리학적 근거를 바탕으로 구체적인 행동 지침을 제시하되, **qa_section의 답변(a1, a2)은 쉬운 일상 언어로 작성**하십시오. 전문 용어를 피하고 누구나 이해할 수 있게 설명하십시오.
    7. customer_analysis의 health_advice는 반드시 포함해야 하며, 전문 용어 없이 일상적인 건강 조언으로 작성하십시오.
    """


def get_final_ai_prompt(ilgan: str, saju_data: Dict, daewoon_info: Dict, sewoon_info: Dict, q: str, events: str, clinical_data_str: str) -> str:
    """
    최종 통합된 AI 분석 요청 프롬프트를 생성합니다.
    """
    # (TEN_GAN_PERSONA는 saju_data.py에서 가져온다고 가정)
    persona = TEN_GAN_PERSONA.get(ilgan, {"style": "따뜻함", "instruction": "공감"}) 
    
    prompt = f"""
# Role: [희구소] 사주 분석 AI - 심리/명리 기반의 따뜻한 공감 및 실전 전략 멘토

# Core Principles (AI의 태도 - 유지):
1. [공감적 이해] 분석 서론은 고객의 일간 페르소나('style')를 반영하여 따뜻하고 감동적인 공감 문구로 시작해야 합니다.
2. [실속 있는 결과] 조언의 본론과 결론에서는 명리학적 근거를 기반으로 '실패 원인 진단' 및 '현실적인 행동 지침'을 명확하고 간결하게 제시합니다.
3. [맞춤형 문체] 모든 답변은 입력된 TEN_GAN_PERSONA의 'instruction'과 'style'을 엄격하게 따릅니다.

[입력 명식 및 운세 데이터]:
- 명식: {saju_data['년주']} {saju_data['월주']} {saju_data['일주']} {saju_data['시주']}
- 일간: {ilgan}
- 십성: {saju_data['십성_결과_배열']}
- 대운 정보: {daewoon_info['대운수']}세 시작, {daewoon_info['대운_간지_배열'][:3]}...
- 세운 정보: {sewoon_info[0]['year']}년 세운: {sewoon_info[0]['ganji']}

[고객 페르소나 및 문체 정보]:
- 일간 Style: {persona['style']} 
- 어조 Instruction: {persona['instruction']}

[고객 제공 임상/과거 사건 이력]:
- {events}

[AI 참고용 임상 통계 자료 (절대 출력 금지)]:
---START OF REFERENCE DATA---
{clinical_data_str}
---END OF REFERENCE DATA---

[분석 요구사항]:
1. [Emotional Opening] 첫 문단은 일간 Style을 활용하여 고객의 본질을 칭찬하고 따뜻하게 시작할 것.
2. [Core Diagnosis] 고객의 과거 사건 이력과 참고 자료를 교차 분석하여, 실패/정체 원인을 명리학적 관점에서 진단할 것.
3. [Practical Strategy] 고객층(3050 여성, N잡/육아/창업)의 현실적 문제(수익화, 루틴, 지속력)에 초점을 맞춰 구체적인 해결책을 제시할 것.
4. [Key Actions] '30일 이내 시작할 실전 행동 3가지'를 명확하게 도출할 것.

[고객의 질문]: {q}
"""
    return prompt


def analyze_ai_report(manse_info: Dict, daewoon_info: Dict, full_q: str, profile_data: Dict, events: str, engine_instance, api_key: str) -> Dict:
    """
    Gemini API를 호출하여 최종 사주 분석 JSON 리포트를 생성합니다.
    """
    
    # 1. AI 프롬프트 생성에 필요한 데이터 준비
    ilgan = manse_info['일주'][0]
    clinical_data_str = load_clinical_data()
    sewoon_info = engine_instance.get_sewoon(datetime.datetime.now().year, 1) # 현재 연도 세운 1년치

    # 2. 최종 프롬프트 생성 (get_final_ai_prompt는 이미 정의되어 있음)
    prompt = get_final_ai_prompt(
        ilgan=ilgan, 
        saju_data=manse_info, 
        daewoon_info=daewoon_info, 
        sewoon_info=sewoon_info, 
        q=full_q, 
        events=events, 
        clinical_data_str=clinical_data_str
    )
    
    # 3. AI API 호출 및 응답 처리
    try:
        genai.configure(api_key=api_key)
        
        response = genai.GenerativeModel(
            'gemini-2.5-flash',
            system_instruction=get_system_instruction()
        ).generate_content(
            contents=[prompt],
            # 수정 완료: 'config'를 'generation_config'로 변경
            generation_config={
                "temperature": 0.5,
                "response_mime_type": "application/json",
            }
        )
        
        response_text = response.text.strip()
        
        # JSON 파싱 시 오류 방지
        clean_json_str = re.sub(r'```json|```', '', response_text, flags=re.IGNORECASE).strip()
        
        try:
            result_json = json.loads(clean_json_str)
        except json.JSONDecodeError as e:
             return {
                 "summary_card": {"keyword": f"❌ AI 응답 파싱 실패 (JSON 오류)", "best_month": "N/A", "risk": "N/A", "action_item": "N/A"},
                 "raw_response": clean_json_str
             }
        
        return result_json

    except Exception as e:
        return {
            "summary_card": {"keyword": f"❌ API 호출 실패 - {type(e).__name__}", "best_month": "N/A", "risk": "N/A", "action_item": "N/A"},
            "raw_response": f"API 호출 또는 응답 생성 중 예상치 못한 오류 발생: {str(e)}"
        }

# --------------------------------------------------------------------------
# 5. 핵심 엔진 클래스 (SajuEngine) - 원국, 대운, 세운 계산 통합
# --------------------------------------------------------------------------

# astropy, numpy 등 필요한 라이브러리 임포트는 이 파일 상단에 이미 있습니다.
try:
    from astropy.time import Time
    from astropy.coordinates import solar_system_ephemeris, EarthLocation, get_sun, SkyCoord
    import astropy.units as u
    solar_system_ephemeris.set('de432s') 
except ImportError:
    # 이 환경에서 astropy가 불가능할 경우, SajuEngine은 작동하지 않습니다.
    pass


class SajuEngine:
    
    JEOLGI_DEGREES = {
        0: '立春', 30: '驚蟄', 60: '淸明', 90: '立夏',
        120: '芒種', 150: '小暑', 180: '立秋', 210: '白露',
        240: '寒露', 270: '立冬', 300: '大雪', 330: '小寒'
    }

    def __init__(self):
        self.ganji_60 = GANJI_60
        self.cheongan = CHEONGAN
        self.jiji = JIJI

    def _find_jeolgi_time(self, target_degree: int, target_year: int) -> datetime.datetime:
        """astropy를 사용하여 특정 황경 도달 시각 (KST)을 계산합니다. (기존 로직 유지)"""
        # ... (로직 생략)
        time_start = Time(f'{target_year}-01-01 00:00:00', format='iso', scale='utc')
        time_end = Time(f'{target_year+1}-03-01 00:00:00', format='iso', scale='utc')
        times = time_start + np.linspace(0, (time_end - time_start).to_value(u.day), 5000) * u.day
        sun_pos = get_sun(times)
        sun_ecliptic_lon = sun_pos.barycentrictrueecliptic.lon.to(u.deg).value
        target_lon = target_degree
        
        lon_diff = sun_ecliptic_lon - target_lon
        lon_diff[lon_diff > 180] -= 360
        lon_diff[lon_diff < -180] += 360
        
        crossing_index = np.where(np.diff(np.sign(lon_diff)))[0]
        
        if len(crossing_index) == 0:
             return self._find_jeolgi_time(target_degree, target_year + 1)

        idx = crossing_index[0]
        t1, t2 = times[idx], times[idx+1]
        l1, l2 = sun_ecliptic_lon[idx], sun_ecliptic_lon[idx+1]
        
        time_frac = (target_lon - l1) / (l2 - l1)
        time_jeolgi_utc = t1 + (t2 - t1) * time_frac
        
        return time_jeolgi_utc.to_datetime(timezone=TIME_ZONE)

    def _get_all_jeolgi_for_year(self, target_year: int) -> List[Dict]:
        """주어진 연도에 필요한 모든 '절(節)' 시각을 계산합니다. (기존 로직 유지)"""
        calculated_jeolgi = []
        for degree, name in self.JEOLGI_DEGREES.items():
            time_kst = self._find_jeolgi_time(degree, target_year)
            if time_kst and time_kst.year in [target_year, target_year + 1, target_year - 1]:
                 calculated_jeolgi.append({'datetime': time_kst, 'name': name, 'degree': degree})
        
        calculated_jeolgi.sort(key=lambda x: x['datetime'])
        return calculated_jeolgi

    def _get_day_ganji(self, dt: datetime.datetime) -> str:
        """일주 (日柱) 계산 함수 (기준일 甲戌日로 최종 변경, 기존 로직 유지)"""
        REF_DATE = datetime.date(1900, 1, 1) 
        REF_DAY_GANJI_INDEX = 10 
        date_obj = dt.date()
        days_passed = (date_obj - REF_DATE).days
        day_ganji_index = (REF_DAY_GANJI_INDEX + days_passed) % 60
        return self.ganji_60[day_ganji_index]

    def _get_shi_ganji(self, day_gan: str, birth_hour: int) -> str:
        """시주 (時柱) 계산 함수 (시두법 기반, 기존 로직 유지)"""
        hour_index = (birth_hour + 1) % 24 // 2
        shi_zhi = self.jiji[hour_index % 12] 
        start_stem_index = DAY_STEM_TO_TIME_STEM_START_INDEX[day_gan]
        shi_gan_index = (start_stem_index + hour_index) % 10
        shi_gan = self.cheongan[shi_gan_index]
        return shi_gan + shi_zhi
        
    def generate_saju_palja(self, birth_dt: datetime.datetime, gender: str) -> Dict:
        """
        최종 사주팔자 8글자 및 대운 계산에 필요한 정보 반환
        🚨 십성 결과를 포함하도록 최종 반환 구조를 수정했습니다.
        """
        
        if birth_dt.tzinfo is None:
             birth_dt = birth_dt.replace(tzinfo=TIME_ZONE)
             
        day_ganji = self._get_day_ganji(birth_dt)
        day_gan = day_ganji[0]
        shi_ganji = self._get_shi_ganji(day_gan, birth_dt.hour)

        try:
            jeolgi_db_current = self._get_all_jeolgi_for_year(birth_dt.year)
            jeolgi_db_prev = self._get_all_jeolgi_for_year(birth_dt.year - 1)
            jeolgi_db_full = sorted(jeolgi_db_current + jeolgi_db_prev, key=lambda x: x['datetime'])
        except Exception as e:
            raise ValueError(f"절기 계산 중 오류 발생: {e}")

        past_jeolgi = None
        future_jeolgi = None
        
        for dt_info in jeolgi_db_full:
            dt = dt_info['datetime']
            if dt <= birth_dt:
                past_jeolgi = dt_info
            elif dt > birth_dt:
                future_jeolgi = dt_info
                break

        if past_jeolgi is None:
             raise ValueError("절기 DB에 출생 시점보다 이전 데이터가 없습니다.")

        # 년주 확정 (立春 기준)
        lipchun_dt = next((j['datetime'] for j in jeolgi_db_full if j['name'] == '立春' and j['datetime'].year == birth_dt.year), None)
        year_index_naive = (birth_dt.year - 1900 + 33) % 60
        
        if lipchun_dt and birth_dt < lipchun_dt:
            year_ganji_final = GANJI_60[(year_index_naive - 1 + 60) % 60]
        else:
            year_ganji_final = GANJI_60[year_index_naive]

        # 월주 확정 (월건법, 년간 기준)
        month_zhi_index = (past_jeolgi['degree'] // 30) % 12
        month_zhi = JIJI[(month_zhi_index + 2) % 12]
        year_gan = year_ganji_final[0]
        month_stem_start_idx = YEAR_STEM_TO_MONTH_STEM_INDEX[year_gan]
        month_stem_idx = (month_stem_start_idx + month_zhi_index) % 10 
        month_gan = CHEONGAN[month_stem_idx]
        month_ganji = month_gan + month_zhi

        # 대운 정보 계산
        daewoon_info = self._calculate_full_daewoon(year_ganji_final, month_ganji, birth_dt, gender, past_jeolgi['datetime'], future_jeolgi['datetime'])
        
        # 십성 계산 (추가된 부분)
        pillars_ganji = [year_ganji_final, month_ganji, day_ganji, shi_ganji]
        ten_gods_array = [calculate_pillar_sipsin(day_gan, g) for g in pillars_ganji]

        return {
            "년주": year_ganji_final, "월주": month_ganji, "일주": day_ganji, "시주": shi_ganji,
            "대운_정보": daewoon_info,
            "출생일": birth_dt.strftime("%Y-%m-%d %H:%M:%S"),
            "일간": day_gan,
            "십성_결과_배열": ten_gods_array
        }

    def _calculate_full_daewoon(self, year_ganji: str, month_ganji: str, birth_dt: datetime.datetime, gender: str, past_jeolgi: datetime.datetime, future_jeolgi: datetime.datetime) -> Dict:
        """대운수, 순/역행, 대운 간지 배열을 계산"""
        year_gan = year_ganji[0]
        # 년간의 음양 판단: 甲丙戊庚壬(양), 乙丁己辛癸(음)
        is_yang = year_gan in ['甲', '丙', '戊', '庚', '壬']
        
        # 순행/역행 결정: 양년생 남/음년생 여 = 순행, 양년생 여/음년생 남 = 역행
        is_forward = (is_yang and gender == 'M') or (not is_yang and gender == 'F')
        기준_절기 = future_jeolgi if is_forward else past_jeolgi
        
        if 기준_절기 is None: return {"error": "기준 절기 데이터 부족"}
        
        time_diff = abs(기준_절기 - birth_dt)
        days_diff = time_diff.total_seconds() / (24 * 3600)
        
        # 🚨 [수정 1] 대운수 계산 오버플로우 방지 및 올림 처리
        days_per_age = days_diff / 3.0
        
        # math.ceil 함수를 사용하여 무조건 올림 (대운수 계산 표준)
        # days_diff가 0보다 클 경우에만 ceil 적용, days_diff=0일 경우 1로 처리
        if days_diff > 0:
            daewoon_su = int(ceil(days_per_age))
        else:
            daewoon_su = 1

        # 최소 1, 최대 10세 범위로 강제 (100세 이상 오버플로우 방지)
        daewoon_su = max(1, min(10, daewoon_su)) 
            
        m_s_idx, m_b_idx = self.cheongan.index(month_ganji[0]), self.jiji.index(month_ganji[1])
        daewoon_list = []
        for i in range(1, 9): 
            # 🚨 [수정 2] 대운 시작 나이 계산 시 오버플로우 방지
            age_start = daewoon_su + (i - 1) * 10
            
            if is_forward:
                # 순행 (인덱스 증가)
                s_idx = (m_s_idx + i) % 10
                b_idx = (m_b_idx + i) % 12
            else:
                # 역행 (인덱스 감소)
                # 丙戌(2, 10)에서 역행하면 i=1일 때 乙酉(1, 9)가 됩니다.
                s_idx = (m_s_idx - i + 10) % 10
                b_idx = (m_b_idx - i + 12) % 12

            daewoon_list.append({"age": age_start, "ganji": self.cheongan[s_idx] + self.jiji[b_idx]})
        
        return {
            "대운수": daewoon_su,
            "순행_역행": "순행" if is_forward else "역행",
            "대운_간지_배열": daewoon_list
        }
        
    def get_sewoon(self, current_year: int, count: int = 10) -> List[Dict]:
        """세운 (歲運) 계산 함수 (기존 로직 유지)"""
        sewoon_list = []
        start_index = (33 + (current_year - 1900)) % 60
        
        for i in range(count):
            year = current_year + i
            index = (start_index + i) % 60
            ganji = self.ganji_60[index]
            sewoon_list.append({"year": year, "ganji": ganji})
            
        return sewoon_list

# --------------------------------------------------------------------------
# 이 아래에 get_final_ai_prompt, analyze_ai_report 함수 정의가 이어집니다.
# (위쪽 4. AI 프롬프트 및 분석 함수 추가 섹션에 이미 정의되어 있습니다.)
# --------------------------------------------------------------------------