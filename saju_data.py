# =================================================================
# [필수 상수 정의] - analysis_core_final.py가 참조하는 핵심 데이터
# =================================================================

# 1. 10천간 (十天干)
CHEONGAN = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']

# 2. 12지지 (十二地支)
JIJI = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']

# 3. 60갑자 (六十甲子)
GANJI = [
    '甲子', '乙丑', '丙寅', '丁卯', '戊辰', '己巳', '庚午', '辛未', '壬申', '癸酉',
    '甲戌', '乙亥', '丙子', '丁丑', '戊寅', '己卯', '庚辰', '辛巳', '壬午', '癸未',
    '甲申', '乙酉', '丙戌', '丁亥', '戊子', '己丑', '庚寅', '辛卯', '壬辰', '癸巳',
    '甲午', '乙未', '丙申', '丁酉', '戊戌', '己亥', '庚子', '辛丑', '壬寅', '癸卯',
    '甲辰', '乙巳', '丙午', '丁未', '戊申', '己酉', '庚戌', '辛亥', '壬子', '癸丑'
]

# 4. 월두법 상수 (년간 기준 월간 시작 천간 인덱스)
# (甲己:丙寅, 乙庚:戊寅, 丙辛:庚寅, 丁壬:壬寅, 戊癸:甲寅)
YEAR_STEM_TO_MONTH_STEM_INDEX = {
    '甲': 2, '己': 2, # 丙寅 시작 (丙의 인덱스)
    '乙': 4, '庚': 4, # 戊寅 시작
    '丙': 6, '辛': 6, # 庚寅 시작
    '丁': 8, '壬': 8, # 壬寅 시작
    '戊': 0, '癸': 0  # 甲寅 시작
}

# 5. 오행 맵 (간단 버전, 오류 방지용)
O_HAENG_MAP = {
    '甲': '木', '乙': '木', '丙': '火', '丁': '火', '戊': '土', 
    '己': '土', '庚': '金', '辛': '金', '壬': '水', '癸': '水', 
    '子': '水', '丑': '土', '寅': '木', '卯': '木', '辰': '土', 
    '巳': '火', '午': '火', '未': '土', '申': '金', '酉': '金', 
    '戌': '土', '亥': '水'
}

# (이 아래에 기존에 수정하신 DAY_STEM_TO_TIME_STEM_START_INDEX 코드가 있어야 합니다.)
# saju_data.py
# 희구소(Hidden Luck Lab) 사주 데이터 모듈
# 역할: 만세력 계산 및 분석에 필요한 모든 상수와 커스터마이징된 점수 및 규칙을 보관합니다.
# 이 파일은 CSV 파일 없이 독립적으로 작동하도록 모든 점수표(딕셔너리)를 내장합니다.

# 1. 기본 매핑 상수
CHEONGAN = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
JIJI = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
GANJI_60 = [c + j for c in CHEONGAN for j in JIJI][:60]

# DAY_STEM_TO_TIME_STEM_START_INDEX: 일간을 기준으로 子時(자시)의 천간 인덱스 (甲=0)
# (甲己:甲, 乙庚:丙, 丙辛:戊, 丁壬:庚, 戊癸:壬)
DAY_STEM_TO_TIME_STEM_START_INDEX = {
    '甲': 0, # 甲子時 시작 (甲의 인덱스)
    '乙': 2, # 丙子時 시작 (丙의 인덱스)
    '丙': 4, # 戊子時 시작 (戊의 인덱스)
    '丁': 6, # 庚子時 시작 (庚의 인덱스)
    '戊': 8, # 🚨 최종 수정: 壬子時 시작 (壬의 인덱스)
    '己': 0, # 甲子時 시작
    '庚': 2, # 丙子時 시작
    '辛': 4, # 戊子時 시작
    '壬': 6, # 庚子時 시작
    '癸': 8, # 壬子時 시작
}

# 2. 일간별 맞춤 문체 (Persona) - 기존 내용 유지
TEN_GAN_PERSONA = {
    # ... (기존 TEN_GAN_PERSONA 내용은 생략)
    "甲": {"style": "직진하는 용기와 강한 성장의 힘! 새로운 시작을 자신 있게 응원합니다.", "instruction": "청자(User)는 '갑목(甲)' 성향입니다. 서론을 길게 끌지 말고, 두괄식으로 진취적인 비전을 제시하세요. '성장', '시작', '도전'과 같은 긍정적이고 미래지향적인 어휘를 사용하고, 망설임 없이 등을 떠밀어주는 힘찬 어조를 유지하세요."},
    "乙": {"style": "따뜻한 마음과 배려, 모두의 행복을 챙기는 모습이 인상적이에요.", "instruction": "청자(User)는 '을목(乙)' 성향입니다. 부드러운 언어를 사용하되, 핵심 메시지는 확고하고 정확하게 전달하세요. '연결', '유연성', '조화' 같은 어휘를 사용하며, 주변의 도움을 활용하는 방법을 구체적으로 조언하세요."},
    "丙": {"style": "밝고 긍정적인 에너지로 주변을 환하게 만드는 태양이네요.", "instruction": "청자(User)는 '병화(丙)' 성향입니다. 명쾌하고 자신감 넘치는 어조를 사용하세요. '비전', '확산', '밝음' 같은 어휘를 활용하여, 대중적 영향력과 시야 확장에 초점을 맞춘 조언을 제시하세요."},
    "丁": {"style": "세밀한 통찰력과 강한 집중력으로 빛을 만들어내는 분입니다.", "instruction": "청자(User)는 '정화(丁)' 성향입니다. 사려 깊지만 결론은 명확한 어조를 사용하세요. '집중', '통찰', '정밀함' 같은 어휘를 활용하여, 내실 다지기와 정확한 목표 설정의 중요성을 강조하세요."},
    "戊": {"style": "묵묵히 큰 것을 담아내며 믿음을 주는 안정적인 산과 같습니다.", "instruction": "청자(User)는 '무토(戊)' 성향입니다. 신뢰감을 주는 무게감 있는 어조를 사용하세요. '중심', '안정', '축적' 같은 어휘를 활용하여, 장기적인 계획과 흔들리지 않는 중심을 잡는 방법을 조언하세요."},
    "己": {"style": "세상의 모든 것을 품고 키워내는 포용력과 실질적인 힘이 있습니다.", "instruction": "청자(User)는 '기토(己)' 성향입니다. 공감 능력이 느껴지는 친근한 어조를 사용하세요. '조율', '실속', '포용' 같은 어휘를 활용하여, 현실적인 이익과 타인과의 관계에서 균형을 잡는 방법을 제시하세요."},
    "庚": {"style": "강한 의지와 결단력으로 목표를 쟁취하는 금속의 리더십이 있네요.", "instruction": "청자(User)는 '경금(庚)' 성향입니다. 단호하고 논리적인 어조를 사용하세요. '개혁', '실행', '결단' 같은 어휘를 활용하여, 불필요한 것을 잘라내고 핵심에 집중하는 전략을 강조하세요."},
    "辛": {"style": "세상에 꼭 필요한 가치를 만들고 세밀한 아름다움을 완성하는 보석입니다.", "instruction": "청자(User)는 '신금(辛)' 성향입니다. 정제되고 섬세한 어조를 사용하세요. '가치', '정밀', '완성' 같은 어휘를 활용하여, 전문성을 높이고 자신의 가치를 인정받는 방법을 구체적으로 조언하세요."},
    "壬": {"style": "넓은 시야와 유연함으로 세상을 탐험하는 바다와 같습니다.", "instruction": "청자(User)는 '임수(壬)' 성향입니다. 지혜롭고 개방적인 어조를 사용하세요. '스케일', '흐름', '지혜' 같은 어휘를 활용하여, 큰 그림을 보고 다방면으로 정보를 수집하는 전략을 제시하세요."},
    "癸": {"style": "어둠 속에서도 생명을 키워내는 깊은 지혜와 영감을 가진 분입니다.", "instruction": "청자(User)는 '계수(癸)' 성향입니다. 차분하고 통찰력 있는 어조를 사용하세요. '영감', '잠재력', '은밀함' 같은 어휘를 활용하여, 직관을 따르고 내면의 힘을 기르는 방법을 조언하세요."},
}

# 3. 십이운성 (12-Star) - 기존 내용 유지
TWELVE_STAR = ["장생", "목욕", "관대", "건록", "제왕", "쇠", "병", "사", "묘", "절", "태", "양"]


# ====================================================================================================
# [4. '희구소' AI 사주 점수화 로직 (Scoring Tables & Functions)]
# 목표: 커스터마이징된 점수와 가중치를 적용하여 운세 그래프 기반 점수 산출
# ====================================================================================================

# --------------------------------------------------------------------------------
# 4.1. 점수 테이블 (Scoring Tables) - CSV 데이터를 Dictionary로 변환하여 내장 (완전한 형태로 구현)
# --------------------------------------------------------------------------------

# 1. 천간 점수 테이블 (S_Plan, 20% 비중) - 일간 vs. 운천간 상호작용
CHUNGAN_SCORES_LOOKUP = {('甲', '甲'): 45, ('甲', '乙'): 35, ('甲', '丙'): 100, ('甲', '丁'): 50, ('甲', '戊'): 75, ('甲', '己'): 0, ('甲', '庚'): 35, ('甲', '辛'): 50, ('甲', '壬'): 75, ('甲', '癸'): 75, ('乙', '甲'): 75, ('乙', '乙'): 45, ('乙', '丙'): 75, ('乙', '丁'): 100, ('乙', '戊'): 75, ('乙', '己'): 50, ('乙', '庚'): 35, ('乙', '辛'): 0, ('乙', '壬'): 75, ('乙', '癸'): 75, ('丙', '甲'): 75, ('丙', '乙'): 75, ('丙', '丙'): 45, ('丙', '丁'): 35, ('丙', '戊'): 100, ('丙', '己'): 75, ('丙', '庚'): 50, ('丙', '辛'): 0, ('丙', '壬'): 35, ('丙', '癸'): 75, ('丁', '甲'): 75, ('丁', '乙'): 75, ('丁', '丙'): 35, ('丁', '丁'): 45, ('丁', '戊'): 75, ('丁', '己'): 100, ('丁', '庚'): 75, ('丁', '辛'): 50, ('丁', '壬'): 0, ('丁', '癸'): 35, ('戊', '甲'): 35, ('戊', '乙'): 35, ('戊', '丙'): 75, ('戊', '丁'): 75, ('戊', '戊'): 45, ('戊', '己'): 35, ('戊', '庚'): 75, ('戊', '辛'): 75, ('戊', '壬'): 50, ('戊', '癸'): 0, ('己', '甲'): 0, ('己', '乙'): 35, ('己', '丙'): 75, ('己', '丁'): 75, ('己', '戊'): 35, ('己', '己'): 45, ('己', '庚'): 75, ('己', '辛'): 75, ('己', '壬'): 0, ('己', '癸'): 50, ('庚', '甲'): 35, ('庚', '乙'): 0, ('庚', '丙'): 50, ('庚', '丁'): 50, ('庚', '戊'): 75, ('庚', '己'): 75, ('庚', '庚'): 45, ('庚', '辛'): 35, ('庚', '壬'): 100, ('庚', '癸'): 75, ('辛', '甲'): 50, ('辛', '乙'): 35, ('辛', '丙'): 50, ('辛', '丁'): 50, ('辛', '戊'): 75, ('辛', '己'): 75, ('辛', '庚'): 35, ('辛', '辛'): 50, ('辛', '壬'): 100, ('辛', '癸'): 75, ('壬', '甲'): 45, ('壬', '乙'): 45, ('壬', '丙'): 75, ('壬', '丁'): 0, ('壬', '戊'): 50, ('壬', '己'): 0, ('壬', '庚'): 75, ('壬', '辛'): 75, ('壬', '壬'): 45, ('壬', '癸'): 35, ('癸', '甲'): 75, ('癸', '乙'): 75, ('癸', '丙'): 75, ('癸', '丁'): 50, ('癸', '戊'): 0, ('癸', '己'): 50, ('癸', '庚'): 75, ('癸', '辛'): 75, ('癸', '壬'): 35, ('癸', '癸'): 45}
# ---------------------------------------------------------------------------------

# 2. 지지 점수 테이블 (S_Result, S_General_ChoHou, S_ShinJung_ChoHou) (50%, 30% 비중)
# 지지대지지 상호작용 점수 (Key: 지지1+지지2)
JIJI_SCORES_LOOKUP = {'寅寅': {'Result_Jiji': 45, 'General_ChoHou': 75, 'ShinJung_ChoHou': 60}, '寅卯': {'Result_Jiji': 25, 'General_ChoHou': 75, 'ShinJung_ChoHou': 60}, '寅辰': {'Result_Jiji': 75, 'General_ChoHou': 75, 'ShinJung_ChoHou': 60}, '寅巳': {'Result_Jiji': 75, 'General_ChoHou': 90, 'ShinJung_ChoHou': 35}, '寅午': {'Result_Jiji': 100, 'General_ChoHou': 100, 'ShinJung_ChoHou': 35}, '寅未': {'Result_Jiji': 75, 'General_ChoHou': 90, 'ShinJung_ChoHou': 35}, '寅申': {'Result_Jiji': 45, 'General_ChoHou': 45, 'ShinJung_ChoHou': 60}, '寅酉': {'Result_Jiji': 45, 'General_ChoHou': 60, 'ShinJung_ChoHou': 60}, '寅戌': {'Result_Jiji': 75, 'General_ChoHou': 75, 'ShinJung_ChoHou': 75}, '寅亥': {'Result_Jiji': 95, 'General_ChoHou': 60, 'ShinJung_ChoHou': 75}, '寅子': {'Result_Jiji': 75, 'General_ChoHou': 35, 'ShinJung_ChoHou': 75}, '寅丑': {'Result_Jiji': 45, 'General_ChoHou': 50, 'ShinJung_ChoHou': 75}, '卯寅': {'Result_Jiji': 45, 'General_ChoHou': 75, 'ShinJung_ChoHou': 60}, '卯卯': {'Result_Jiji': 45, 'General_ChoHou': 75, 'ShinJung_ChoHou': 60}, '卯辰': {'Result_Jiji': 75, 'General_ChoHou': 75, 'ShinJung_ChoHou': 60}, '卯巳': {'Result_Jiji': 75, 'General_ChoHou': 90, 'ShinJung_ChoHou': 35}, '卯午': {'Result_Jiji': 75, 'General_ChoHou': 100, 'ShinJung_ChoHou': 35}, '卯未': {'Result_Jiji': 100, 'General_ChoHou': 90, 'ShinJung_ChoHou': 35}, '卯申': {'Result_Jiji': 45, 'General_ChoHou': 45, 'ShinJung_ChoHou': 60}, '卯酉': {'Result_Jiji': 25, 'General_ChoHou': 25, 'ShinJung_ChoHou': 60}, '卯戌': {'Result_Jiji': 45, 'General_ChoHou': 75, 'ShinJung_ChoHou': 75}, '卯亥': {'Result_Jiji': 95, 'General_ChoHou': 60, 'ShinJung_ChoHou': 75}, '卯子': {'Result_Jiji': 45, 'General_ChoHou': 35, 'ShinJung_ChoHou': 75}, '卯丑': {'Result_Jiji': 45, 'General_ChoHou': 50, 'ShinJung_ChoHou': 75}, '辰寅': {'Result_Jiji': 75, 'General_ChoHou': 75, 'ShinJung_ChoHou': 60}, '辰卯': {'Result_Jiji': 75, 'General_ChoHou': 75, 'ShinJung_ChoHou': 60}, '辰辰': {'Result_Jiji': 45, 'General_ChoHou': 75, 'ShinJung_ChoHou': 60}, '辰巳': {'Result_Jiji': 75, 'General_ChoHou': 90, 'ShinJung_ChoHou': 35}, '辰午': {'Result_Jiji': 75, 'General_ChoHou': 100, 'ShinJung_ChoHou': 35}, '辰未': {'Result_Jiji': 75, 'General_ChoHou': 90, 'ShinJung_ChoHou': 35}, '辰申': {'Result_Jiji': 95, 'General_ChoHou': 60, 'ShinJung_ChoHou': 60}, '辰酉': {'Result_Jiji': 45, 'General_ChoHou': 60, 'ShinJung_ChoHou': 60}, '辰戌': {'Result_Jiji': 25, 'General_ChoHou': 50, 'ShinJung_ChoHou': 75}, '辰亥': {'Result_Jiji': 75, 'General_ChoHou': 60, 'ShinJung_ChoHou': 75}, '辰子': {'Result_Jiji': 95, 'General_ChoHou': 35, 'ShinJung_ChoHou': 75}, '辰丑': {'Result_Jiji': 45, 'General_ChoHou': 50, 'ShinJung_ChoHou': 75}, '巳寅': {'Result_Jiji': 75, 'General_ChoHou': 90, 'ShinJung_ChoHou': 35}, '巳卯': {'Result_Jiji': 75, 'General_ChoHou': 90, 'ShinJung_ChoHou': 35}, '巳辰': {'Result_Jiji': 75, 'General_ChoHou': 90, 'ShinJung_ChoHou': 35}, '巳巳': {'Result_Jiji': 45, 'General_ChoHou': 90, 'ShinJung_ChoHou': 35}, '巳午': {'Result_Jiji': 75, 'General_ChoHou': 100, 'ShinJung_ChoHou': 35}, '巳未': {'Result_Jiji': 75, 'General_ChoHou': 100, 'ShinJung_ChoHou': 35}, '巳申': {'Result_Jiji': 25, 'General_ChoHou': 45, 'ShinJung_ChoHou': 60}, '巳酉': {'Result_Jiji': 75, 'General_ChoHou': 60, 'ShinJung_ChoHou': 60}, '巳戌': {'Result_Jiji': 75, 'General_ChoHou': 75, 'ShinJung_ChoHou': 75}, '巳亥': {'Result_Jiji': 25, 'General_ChoHou': 40, 'ShinJung_ChoHou': 75}, '巳子': {'Result_Jiji': 25, 'General_ChoHou': 35, 'ShinJung_ChoHou': 75}, '巳丑': {'Result_Jiji': 75, 'General_ChoHou': 50, 'ShinJung_ChoHou': 75}, '午寅': {'Result_Jiji': 100, 'General_ChoHou': 100, 'ShinJung_ChoHou': 35}, '午卯': {'Result_Jiji': 75, 'General_ChoHou': 100, 'ShinJung_ChoHou': 35}, '午辰': {'Result_Jiji': 75, 'General_ChoHou': 100, 'ShinJung_ChoHou': 35}, '午巳': {'Result_Jiji': 75, 'General_ChoHou': 100, 'ShinJung_ChoHou': 35}, '午午': {'Result_Jiji': 45, 'General_ChoHou': 100, 'ShinJung_ChoHou': 35}, '午未': {'Result_Jiji': 75, 'General_ChoHou': 100, 'ShinJung_ChoHou': 35}, '午申': {'Result_Jiji': 45, 'General_ChoHou': 45, 'ShinJung_ChoHou': 60}, '午酉': {'Result_Jiji': 45, 'General_ChoHou': 60, 'ShinJung_ChoHou': 60}, '午戌': {'Result_Jiji': 100, 'General_ChoHou': 100, 'ShinJung_ChoHou': 75}, '午亥': {'Result_Jiji': 45, 'General_ChoHou': 40, 'ShinJung_ChoHou': 75}, '午子': {'Result_Jiji': 25, 'General_ChoHou': 35, 'ShinJung_ChoHou': 75}, '午丑': {'Result_Jiji': 75, 'General_ChoHou': 50, 'ShinJung_ChoHou': 75}, '未寅': {'Result_Jiji': 75, 'General_ChoHou': 90, 'ShinJung_ChoHou': 35}, '未卯': {'Result_Jiji': 100, 'General_ChoHou': 90, 'ShinJung_ChoHou': 35}, '未辰': {'Result_Jiji': 75, 'General_ChoHou': 90, 'ShinJung_ChoHou': 35}, '未巳': {'Result_Jiji': 75, 'General_ChoHou': 100, 'ShinJung_ChoHou': 35}, '未午': {'Result_Jiji': 75, 'General_ChoHou': 100, 'ShinJung_ChoHou': 35}, '未未': {'Result_Jiji': 45, 'General_ChoHou': 100, 'ShinJung_ChoHou': 35}, '未申': {'Result_Jiji': 45, 'General_ChoHou': 45, 'ShinJung_ChoHou': 60}, '未酉': {'Result_Jiji': 75, 'General_ChoHou': 60, 'ShinJung_ChoHou': 60}, '未戌': {'Result_Jiji': 45, 'General_ChoHou': 75, 'ShinJung_ChoHou': 75}, '未亥': {'Result_Jiji': 95, 'General_ChoHou': 60, 'ShinJung_ChoHou': 75}, '未子': {'Result_Jiji': 35, 'General_ChoHou': 35, 'ShinJung_ChoHou': 75}, '未丑': {'Result_Jiji': 25, 'General_ChoHou': 50, 'ShinJung_ChoHou': 75}, '申寅': {'Result_Jiji': 25, 'General_ChoHou': 45, 'ShinJung_ChoHou': 60}, '申卯': {'Result_Jiji': 45, 'General_ChoHou': 45, 'ShinJung_ChoHou': 60}, '申辰': {'Result_Jiji': 95, 'General_ChoHou': 60, 'ShinJung_ChoHou': 60}, '申巳': {'Result_Jiji': 25, 'General_ChoHou': 45, 'ShinJung_ChoHou': 60}, '申午': {'Result_Jiji': 45, 'General_ChoHou': 45, 'ShinJung_ChoHou': 60}, '申未': {'Result_Jiji': 45, 'General_ChoHou': 45, 'ShinJung_ChoHou': 60}, '申申': {'Result_Jiji': 45, 'General_ChoHou': 45, 'ShinJung_ChoHou': 60}, '申酉': {'Result_Jiji': 45, 'General_ChoHou': 60, 'ShinJung_ChoHou': 60}, '申戌': {'Result_Jiji': 45, 'General_ChoHou': 75, 'ShinJung_ChoHou': 75}, '申亥': {'Result_Jiji': 25, 'General_ChoHou': 40, 'ShinJung_ChoHou': 75}, '申子': {'Result_Jiji': 95, 'General_ChoHou': 35, 'ShinJung_ChoHou': 75}, '申丑': {'Result_Jiji': 75, 'General_ChoHou': 50, 'ShinJung_ChoHou': 75}, '酉寅': {'Result_Jiji': 45, 'General_ChoHou': 60, 'ShinJung_ChoHou': 60}, '酉卯': {'Result_Jiji': 25, 'General_ChoHou': 25, 'ShinJung_ChoHou': 60}, '酉辰': {'Result_Jiji': 45, 'General_ChoHou': 60, 'ShinJung_ChoHou': 60}, '酉巳': {'Result_Jiji': 75, 'General_ChoHou': 60, 'ShinJung_ChoHou': 60}, '酉午': {'Result_Jiji': 45, 'General_ChoHou': 60, 'ShinJung_ChoHou': 60}, '酉未': {'Result_Jiji': 75, 'General_ChoHou': 60, 'ShinJung_ChoHou': 60}, '酉申': {'Result_Jiji': 45, 'General_ChoHou': 60, 'ShinJung_ChoHou': 60}, '酉酉': {'Result_Jiji': 45, 'General_ChoHou': 60, 'ShinJung_ChoHou': 60}, '酉戌': {'Result_Jiji': 75, 'General_ChoHou': 75, 'ShinJung_ChoHou': 75}, '酉亥': {'Result_Jiji': 45, 'General_ChoHou': 40, 'ShinJung_ChoHou': 75}, '酉子': {'Result_Jiji': 45, 'General_ChoHou': 35, 'ShinJung_ChoHou': 75}, '酉丑': {'Result_Jiji': 75, 'General_ChoHou': 50, 'ShinJung_ChoHou': 75}, '戌寅': {'Result_Jiji': 75, 'General_ChoHou': 75, 'ShinJung_ChoHou': 75}, '戌卯': {'Result_Jiji': 45, 'General_ChoHou': 75, 'ShinJung_ChoHou': 75}, '戌辰': {'Result_Jiji': 25, 'General_ChoHou': 50, 'ShinJung_ChoHou': 75}, '戌巳': {'Result_Jiji': 75, 'General_ChoHou': 75, 'ShinJung_ChoHou': 75}, '戌午': {'Result_Jiji': 100, 'General_ChoHou': 100, 'ShinJung_ChoHou': 75}, '戌未': {'Result_Jiji': 45, 'General_ChoHou': 75, 'ShinJung_ChoHou': 75}, '戌申': {'Result_Jiji': 45, 'General_ChoHou': 75, 'ShinJung_ChoHou': 75}, '戌酉': {'Result_Jiji': 75, 'General_ChoHou': 75, 'ShinJung_ChoHou': 75}, '戌戌': {'Result_Jiji': 45, 'General_ChoHou': 75, 'ShinJung_ChoHou': 75}, '戌亥': {'Result_Jiji': 45, 'General_ChoHou': 40, 'ShinJung_ChoHou': 75}, '戌子': {'Result_Jiji': 35, 'General_ChoHou': 100, 'ShinJung_ChoHou': 75}, '戌丑': {'Result_Jiji': 25, 'General_ChoHou': 50, 'ShinJung_ChoHou': 75}, '亥寅': {'Result_Jiji': 95, 'General_ChoHou': 60, 'ShinJung_ChoHou': 75}, '亥卯': {'Result_Jiji': 95, 'General_ChoHou': 60, 'ShinJung_ChoHou': 75}, '亥辰': {'Result_Jiji': 75, 'General_ChoHou': 60, 'ShinJung_ChoHou': 75}, '亥巳': {'Result_Jiji': 25, 'General_ChoHou': 40, 'ShinJung_ChoHou': 75}, '亥午': {'Result_Jiji': 45, 'General_ChoHou': 40, 'ShinJung_ChoHou': 75}, '亥未': {'Result_Jiji': 95, 'General_ChoHou': 60, 'ShinJung_ChoHou': 75}, '亥申': {'Result_Jiji': 25, 'General_ChoHou': 40, 'ShinJung_ChoHou': 75}, '亥酉': {'Result_Jiji': 45, 'General_ChoHou': 40, 'ShinJung_ChoHou': 75}, '亥戌': {'Result_Jiji': 45, 'General_ChoHou': 40, 'ShinJung_ChoHou': 75}, '亥亥': {'Result_Jiji': 45, 'General_ChoHou': 40, 'ShinJung_ChoHou': 75}, '亥子': {'Result_Jiji': 45, 'General_ChoHou': 20, 'ShinJung_ChoHou': 75}, '亥丑': {'Result_Jiji': 75, 'General_ChoHou': 50, 'ShinJung_ChoHou': 75}, '子寅': {'Result_Jiji': 75, 'General_ChoHou': 35, 'ShinJung_ChoHou': 75}, '子卯': {'Result_Jiji': 45, 'General_ChoHou': 35, 'ShinJung_ChoHou': 75}, '子辰': {'Result_Jiji': 95, 'General_ChoHou': 35, 'ShinJung_ChoHou': 75}, '子巳': {'Result_Jiji': 25, 'General_ChoHou': 35, 'ShinJung_ChoHou': 75}, '子午': {'Result_Jiji': 25, 'General_ChoHou': 35, 'ShinJung_ChoHou': 75}, '子未': {'Result_Jiji': 35, 'General_ChoHou': 35, 'ShinJung_ChoHou': 75}, '子申': {'Result_Jiji': 95, 'General_ChoHou': 35, 'ShinJung_ChoHou': 60}, '子酉': {'Result_Jiji': 45, 'General_ChoHou': 35, 'ShinJung_ChoHou': 60}, '子戌': {'Result_Jiji': 35, 'General_ChoHou': 100, 'ShinJung_ChoHou': 75}, '子亥': {'Result_Jiji': 45, 'General_ChoHou': 20, 'ShinJung_ChoHou': 75}, '子子': {'Result_Jiji': 45, 'General_ChoHou': 20, 'ShinJung_ChoHou': 75}, '子丑': {'Result_Jiji': 75, 'General_ChoHou': 50, 'ShinJung_ChoHou': 75}, '丑寅': {'Result_Jiji': 45, 'General_ChoHou': 50, 'ShinJung_ChoHou': 75}, '丑卯': {'Result_Jiji': 45, 'General_ChoHou': 50, 'ShinJung_ChoHou': 75}, '丑辰': {'Result_Jiji': 45, 'General_ChoHou': 50, 'ShinJung_ChoHou': 75}, '丑巳': {'Result_Jiji': 75, 'General_ChoHou': 50, 'ShinJung_ChoHou': 75}, '丑午': {'Result_Jiji': 75, 'General_ChoHou': 50, 'ShinJung_ChoHou': 75}, '丑未': {'Result_Jiji': 25, 'General_ChoHou': 50, 'ShinJung_ChoHou': 75}, '丑申': {'Result_Jiji': 75, 'General_ChoHou': 50, 'ShinJung_ChoHou': 60}, '丑酉': {'Result_Jiji': 75, 'General_ChoHou': 50, 'ShinJung_ChoHou': 60}, '丑戌': {'Result_Jiji': 25, 'General_ChoHou': 50, 'ShinJung_ChoHou': 75}, '丑亥': {'Result_Jiji': 75, 'General_ChoHou': 50, 'ShinJung_ChoHou': 75}, '丑子': {'Result_Jiji': 75, 'General_ChoHou': 50, 'ShinJung_ChoHou': 75}, '丑丑': {'Result_Jiji': 45, 'General_ChoHou': 50, 'ShinJung_ChoHou': 75}}
# ---------------------------------------------------------------------


# --------------------------------------------------------------------------------
# 4.2. 보조 함수 (Helper Functions for Logic)
# --------------------------------------------------------------------------------

# 지지 오행 매핑 (토 지지 내장 오행 미포함, 대표 오행 기준)
JIJI_O_HENG = {
    '寅': '木', '卯': '木', '辰': '土', '巳': '火', '午': '火', '未': '土', 
    '申': '金', '酉': '金', '戌': '土', '亥': '水', '子': '水', '丑': '土'
}

def get_oheng(jiji: str) -> str:
    """지지 글자의 대표 오행을 반환 (Returns the representative element of the earthly branch)"""
    return JIJI_O_HENG.get(jiji, '')

def check_geuk(oheng1: str, oheng2: str) -> bool:
    """오행1이 오행2를 극(剋)하는지 확인 (Checks if Element 1 clashes with Element 2)"""
    geuk_map = {
        '木': '土', '火': '金', '土': '水', '金': '木', '水': '火'
    }
    return geuk_map.get(oheng1) == oheng2

def get_cheongan_score(stem1: str, stem2: str) -> float:
    """천간 점수(0~100)를 딕셔너리에서 조회 (50점은 기본값/평) (Look up Heavenly Stem score)"""
    return CHUNGAN_SCORES_LOOKUP.get((stem1, stem2), 50.0)

def get_jiji_interaction_score(jiji1: str, jiji2: str, score_type: str) -> float:
    """지지 점수(0~100)를 딕셔너리에서 조회 (50점은 기본값/평) (Look up Earthly Branch interaction score)"""
    key = jiji1 + jiji2 
    return JIJI_SCORES_LOOKUP.get(key, {}).get(score_type, 50.0)


# --------------------------------------------------------------------------------
# 4.3. 최종 운세 점수 계산 함수 (Total Luck Score Calculation)
# --------------------------------------------------------------------------------

def calculate_total_luck_score(sa_ju_data: dict, luck_data: dict) -> float:
    """
    확정된 가중치 (환경 50%, 계획 20%, 결과 30%)를 사용하여 최종 종합 운세 점수(0~100)를 산출합니다.
    (Calculates the final total luck score based on confirmed weights.)
    sa_ju_data = {'일간': '辛', '월지': '午', '일지': '子', '시지': '寅'}
    luck_data = {'천간': '壬', '지지': '寅', '운의종류': '대운'}
    """
    ilgan = sa_ju_data.get('일간', '')
    wol_jiji = sa_ju_data.get('월지', '')
    il_jiji = sa_ju_data.get('일지', '')
    luck_cheongan = luck_data.get('천간', '')
    luck_jiji = luck_data.get('지지', '')

    # 1. 계획 점수 (천간, 20%) - 일간 vs. 운천간
    s_plan_score = get_cheongan_score(ilgan, luck_cheongan)
    s_plan = s_plan_score * 0.20
    
    # 2. 결과 점수 (지지, 30%) - 일지 vs. 운지지 (Result_Jiji 컬럼 사용)
    # 일지: 거주/결혼 운. 지지 컬럼 점수가 결과(Result)를 반영.
    s_result_score = get_jiji_interaction_score(il_jiji, luck_jiji, 'Result_Jiji')
    s_result = s_result_score * 0.30
    
    # 3. 환경 점수 (조후, 50%) - 월지 vs. 운지지
    s_general_cho_hou_score = get_jiji_interaction_score(wol_jiji, luck_jiji, 'General_ChoHou')
    
    if ilgan in ['辛', '丁']:
        # 신금/정화 일간 로직: 일반 10% + 신정 40% (Work/수익성 강조)
        s_shinjung_cho_hou_score = get_jiji_interaction_score(wol_jiji, luck_jiji, 'ShinJung_ChoHou')
        s_environment = (s_general_cho_hou_score * 0.1) + (s_shinjung_cho_hou_score * 0.4)
    else:
        # 일반 일간 로직: 일반 조후 50%
        s_environment = s_general_cho_hou_score * 0.5

    s_total = s_environment + s_plan + s_result
    return round(s_total, 2)


# --------------------------------------------------------------------------------
# 4.4. 특수 구조 해석 플래그 함수 (Interpretation Flags)
# --------------------------------------------------------------------------------

def generate_interpretation_flags(sa_ju_data: dict, luck_data: dict, child_data: dict = None) -> dict:
    """
    점수 외의 특수 구조 및 관계/건강 관련 해석 플래그를 생성합니다.
    (Generates interpretation flags for AI prompt injection.)
    """
    flags = {}
    wol_jiji = sa_ju_data.get('월지', '')
    il_jiji = sa_ju_data.get('일지', '')
    si_jiji = sa_ju_data.get('시지', '')
    
    # A. 토 월지 선용신 플래그 (辰戌丑未)
    if wol_jiji in ['辰', '戌', '丑', '未']:
        flags['용신_선순위'] = "土 월지: 木(목) 선 용신 적용. 구조화 및 수익화에 필요한 시작의 힘(木)을 중점 평가."
    
    # B. 위치 기반 해석 (AI 분석 프롬프트에 활용)
    flags['사업_투자_관점'] = f"시 지지({si_jiji})와 운({luck_data.get('지지', '')})의 상호작용 분석"
    flags['거주_결혼_관점'] = f"일 지지({il_jiji})와 운({luck_data.get('지지', '')})의 상호작용 분석"
    
    # C. 배우자 건강 위험 플래그 (시/월 지지가 일 지지를 동시에 극할 때)
    oheng_si = get_oheng(si_jiji)
    oheng_wol = get_oheng(wol_jiji)
    oheng_il = get_oheng(il_jiji)
    
    # 시와 월의 오행이 같고, 그 오행이 일지를 극하는 경우
    if oheng_si and oheng_wol and oheng_il:
        if oheng_si == oheng_wol and check_geuk(oheng_si, oheng_il):
            flags['배우자_건강_위험'] = "시/월 지지의 동시 극으로 인한 일지 피극. 배우자 건강 주의 및 물리적 거리 권장."
        
    # D. 자녀 천간합 플래그 (대운에 한해)
    if child_data and luck_data.get('운의종류') == '대운':
        # 이 로직은 child_data['월천간']과 luck_data['천간']의 천간합 관계 맵을 확인해야 합니다.
        # flags['부모님_건강_주의'] = "자녀 월천간과 대운 천간합. 부모님 건강 관리 및 체크 필수 시기."
        pass 
    
    # E. 부부 비교 플래그 (외부에서 비교 데이터가 들어올 경우 활성화)
    # 예시: if flags.get('배우자_일지_피극') and other_spouse_data['일지_운합']:
    #     flags['부부_건강_비교_조언'] = "극 당하는 배우자(고객 혹은 파트너)의 건강 및 심리적 안정에 집중할 시기."

    return flags