from typing import Dict
import json

# --------------------------------------------------------------------------------
# [HTML 템플릿] (수정된 킬러힐러_희구소_2026_리포트.html 전체 내용 반영)
# 사용자님이 수정하신 최종 디자인과 JavaScript 렌더링 로직이 포함된 템플릿입니다.
# --------------------------------------------------------------------------------
HTML_TEMPLATE = r"""
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>희구소: 2026 마스터 리포트</title>
    <!-- 폰트: 고운바탕, Noto Sans KR -->
    <link href="https://fonts.googleapis.com/css2?family=Gowun+Batang:wght@400;700&family=Noto+Sans+KR:wght@300;400;500;700&display=swap" rel="stylesheet">
    <!-- 아이콘 -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <!-- 차트 라이브러리 -->
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <!-- 캡처 라이브러리 (html2canvas) -->
    <script src="https://html2canvas.hertzen.com/dist/html2canvas.min.js"></script>
    <!-- 축하 폭죽 효과 (Confetti) -->
    <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.6.0/dist/confetti.browser.min.js"></script>
    
    <style>
        /* CSS 변수 정의 */
        :root { 
            --bg-color: #FFFDF7; 
            --card-bg: #FFFFFF; 
            --text-main: #555555; 
            --text-sub: #8D8580; 
            --primary: #B0E0D5; /* Soft Mint */
            --accent: #FFCBA4; /* Warm Peach */
            --border: 1px solid #E6E6E6; 
            --shadow: 0 5px 20px rgba(176, 224, 213, 0.3);
            /* 오행 색상 */
            --wood: #A8D5BA; --fire: #FFB7B2; --earth: #E6CEAC; --metal: #D3D3D3; --water: #A2C2E0; 
            --nav-height: 70px; /* 네비게이션 높이 */
        }
        
        /* 기본 스타일 */
        * { margin: 0; padding: 0; box-sizing: border-box; } 
        html { scroll-behavior: smooth; }
        
        body { 
            font-family: 'Gowun Batang', serif;
            background: var(--bg-color); 
            color: var(--text-main); 
            line-height: 1.8; 
            padding-top: var(--nav-height); /* 플로팅 네비게이션바를 위한 공간 확보 */
        }
        h1, h2, h3, .serif { 
            font-family: 'Gowun Batang', serif; 
            font-weight: 700; 
            line-height: 1.2;
        } 
        
        /* 앵커 위치 조정 (네비게이션바 아래로 오도록) */
        section {
            scroll-margin-top: calc(var(--nav-height) + 20px);
        }

        /* 네비게이션 바 (고정) */
        .nav-bar { 
            position: fixed; top: 0; left: 0; width: 100%; 
            background: rgba(255, 255, 255, 0.95); 
            border-bottom: 1px solid var(--border); 
            z-index: 1000; padding: 15px 0; display: flex; 
            justify-content: center; gap: 20px; 
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
            backdrop-filter: blur(3px);
            height: var(--nav-height);
        }
        .nav-item { 
            text-decoration: none; color: var(--text-sub); 
            font-size: 0.9rem; font-weight: 500; padding: 0 10px; 
            transition: 0.3s; font-family: 'Gowun Batang', serif;
        }
        .nav-item:hover, .nav-item.active { 
            color: #333; 
            border-bottom: 2px solid var(--primary); 
            padding-bottom: 3px; 
        }
        
        .container { max-width: 800px; margin: 0 auto; padding: 0 20px 100px 20px; }
        
        /* 헤더 */
        header { text-align: center; padding: 40px 0 40px 0; }
        .brand { color: var(--accent); letter-spacing: 3px; font-size: 0.9rem; display: block; margin-bottom: 10px; font-family: 'Gowun Batang', serif;}
        .main-title { 
            font-size: 3rem; 
            color: #333; 
            margin-bottom: 10px; 
            line-height: 1.2;
        }
        .sub-title { font-size: 1.2rem; color: var(--accent); font-family: 'Gowun Batang', serif; font-weight: 400; }
        
        /* 카드 스타일 */
        .card { 
            background: var(--card-bg); 
            border-radius: 20px; padding: 30px; 
            margin-bottom: 40px; 
            box-shadow: var(--shadow); 
            border: var(--border); 
        }
        .section-title { 
            font-size: 2.2rem; 
            margin-bottom: 25px; 
            text-align: center; 
            color: #333; 
            border-bottom: 2px dashed var(--primary); 
            padding-bottom: 15px; 
        }
        
        /* 사주 명식 테이블 레이아웃 */
        .saju-wrapper { display: flex; flex-direction: column; gap: 10px; margin-bottom: 30px; }
        .saju-row { display: grid; grid-template-columns: repeat(4, 1fr); gap: 8px; text-align: center; }
        .saju-header { font-size: 0.8rem; color: #999; font-family: 'Gowun Batang', serif; }
        
        /* 사주 셀 디자인 */
        .saju-cell, .ten-god-top, .ten-god-bottom { border-radius: 15px; padding: 10px 5px; min-height: 40px; display: flex; flex-direction: column; justify-content: center; transition: background 0.2s; }
        .saju-cell { cursor: default; padding: 15px 5px; } /* 천간/지지는 호버 X */
        .ten-god-top, .ten-god-bottom { cursor: pointer; background: rgba(176, 224, 213, 0.2); } /* 십성만 호버 O */

        /* 오행 색상 배경 */
        .bg-wood { background: var(--wood); color: #383; } 
        .bg-fire { background: var(--fire); color: #833; } 
        .bg-earth { background: var(--earth); color: #763; } 
        .bg-metal { background: var(--metal); color: #555; } 
        .bg-water { background: var(--water); color: #338; }

        /* 간지 크기 */
        .saju-hanja { font-size: 1.8rem; font-weight: bold; font-family: 'Gowun Batang', serif; margin-bottom: 0px;} 
        .saju-korean { font-size: 0.9rem; color: #333; opacity: 0.8; margin-top: 0px;} 
        .ten-god-top, .ten-god-bottom { font-family: 'Gowun Batang', serif; color: var(--text-main); font-size: 0.9rem; }
        .ten-god-tag.master { background: var(--accent); color: white; border-radius: 8px; padding: 5px 0; font-size: 0.9rem; cursor: default; } /* 일간 */

        /* 대운 스타일 */
        .daewoon-timeline { display: flex; justify-content: space-between; overflow-x: auto; padding: 10px 0; margin-top: 20px; border-top: 1px dashed #eee; border-bottom: 1px dashed #eee; }
        .dw-node { display: flex; flex-direction: column; align-items: center; min-width: 60px; position: relative; opacity: 0.5; transition: 0.3s; padding: 5px 0;}
        .dw-node.current { opacity: 1; transform: scale(1.1); font-weight: bold; }
        .dw-node.current::after { content: '▼'; position: absolute; top: -15px; color: var(--primary); font-size: 0.8rem; animation: bounce 1s infinite; }
        .dw-age { font-size: 0.75rem; color: #888; margin-bottom: 2px; }
        .dw-ganji { font-size: 1rem; font-family: 'Gowun Batang'; color: #333; }
        .dw-sipsin { font-size: 0.75rem; color: var(--text-sub); cursor: pointer; }
        @keyframes bounce { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(-3px); } }
        
        /* 대운 진행 바 */
        .daewoon-progress-box { background: #FAF7F5; padding: 15px; border-radius: 10px; margin-top: 20px; }
        .daewoon-bar-bg { width: 100%; height: 8px; background: #e0e0e0; border-radius: 4px; overflow: hidden; margin: 8px 0; }
        .daewoon-bar-fill { height: 100%; background: linear-gradient(90deg, var(--primary), var(--accent)); width: 0%; border-radius: 4px; transition: width 1s ease-out; }
        .daewoon-info { display: flex; justify-content: space-between; font-size: 0.8rem; color: #666; }

        /* 요약 카드 그리드 */
        .summary-grid { 
            display: grid; 
            grid-template-columns: 1fr 1fr; 
            gap: 15px; 
            padding: 15px; 
        }
        .summary-box { 
            background: #F8F8F8; 
            padding: 15px; 
            border-radius: 15px; 
            text-align: center; 
            border: 1px solid var(--primary); 
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        }

        /* 스탯 변화 차트 */
        .flow-chart-box { height: 200px; width: 100%; margin-bottom: 20px; padding: 10px; background: #fff; border-radius: 15px; }

        /* 월별 가이드 버튼 */
        .month-btn-grid { 
            display: grid; 
            grid-template-columns: repeat(6, 1fr); /* 6개씩 2줄 배치 */
            justify-items: center; 
            gap: 8px; 
            margin-bottom: 20px; 
            padding: 0 5px;
        }
        .month-btn { 
            flex-grow: 0; flex-shrink: 0; padding: 8px 12px; border-radius: 10px; 
            border: 1px solid #C0C0C0; background: #FFFFFF; color: var(--text-main);
            font-size: 0.9rem; cursor: pointer; text-align: center; font-weight: 700; 
            transition: all 0.2s;
        }
        .month-btn:hover { background: #F0F0F0; }
        .month-btn.active { 
            background: var(--primary); color: #333; border-color: '#387669'; 
            font-weight: 700; box-shadow: 0 2px 5px rgba(176, 224, 213, 0.5); 
        }

        /* 월별 대시보드 */
        .monthly-dashboard { background: #FEF7E7; padding: 25px; border-radius: 20px; border: 1px dashed var(--accent); animation: fadeIn 0.5s; }
        .monthly-luck-block {
            background: #FFFFFF; padding: 15px 20px; border-radius: 12px; margin-bottom: 12px;
            text-align: center; box-shadow: 0 1px 5px rgba(0,0,0,0.05); line-height: 1.5;
        }
        .luck-icon-large { font-size: 1.8rem; display: block; margin-bottom: 5px; }
        .luck-label-small { font-size: 0.85rem; color: var(--text-sub); display: block; margin-bottom: 5px; }
        .luck-value { font-family: 'Gowun Batang', serif; font-weight: 700; font-size: 1.1rem; }

        .guide-horizontal-grid {
            display: flex; justify-content: space-around; align-items: flex-start;
            gap: 10px; margin-top: 25px; flex-wrap: wrap; padding: 0 5px;
        }
        .guide-item { flex: 1 1 30%; max-width: 33%; text-align: center; min-width: 150px; }
        .guide-label-btn {
            display: inline-block; background: var(--primary); color: #333; font-weight: 700; 
            padding: 5px 10px; border-radius: 15px; font-size: 0.9rem; margin-bottom: 8px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
        .guide-content-box {
            background: #FFFFFF; padding: 15px 10px; border-radius: 10px; min-height: 80px;
            display: flex; justify-content: center; align-items: center; font-size: 0.95rem;
            line-height: 1.4; font-weight: 500; box-shadow: 0 1px 5px rgba(0,0,0,0.05);
        }
        
        /* 상세 분석 텍스트 스타일 */
        .detail-box { 
            background-color: var(--card-bg); 
            border: 1px solid var(--primary); 
            border-radius: 15px; 
            padding: 25px; 
            margin-bottom: 25px; 
            box-shadow: 0 4px 10px rgba(176, 224, 213, 0.2); 
        }
        .detail-title { 
            font-family: 'Gowun Batang', serif; 
            font-size: 1.8rem; 
            color: #333; 
            margin-bottom: 15px; 
            border-bottom: 2px dashed var(--accent); 
            padding-bottom: 5px; 
        }
        .detail-content { 
            line-height: 1.9; 
            font-size: 1.05rem; 
            color: var(--text-main); 
            font-family: 'Gowun Batang', serif; 
            white-space: pre-wrap;
        }

        /* Q&A 스타일 */
        .qa-container { 
            background-color: #F8F8F8; 
            border-radius: 20px; 
            padding: 30px; 
            border: 1px dashed var(--accent);
        }
        
        /* 개운법 섹션 스타일 (Key Actions) */
        .key-action-box {
            background-color: #F7FFF7; 
            border: 2px solid var(--primary); 
            border-radius: 15px; 
            padding: 25px; 
            margin-top: 30px; 
            box-shadow: 0 4px 10px rgba(176, 224, 213, 0.4);
        }
        .key-action-box h3 {
            font-family: 'Gowun Batang', serif;
            font-size: 2rem;
            color: #387669; /* Darker Mint */
            margin-bottom: 20px;
            text-align: center;
            padding-bottom: 10px;
            border-bottom: 2px solid #387669;
        }
        .key-action-list {
            list-style: none;
            padding: 0;
        }
        .key-action-list li {
            margin-bottom: 15px;
            padding-left: 25px;
            position: relative;
            font-size: 1.05rem;
            line-height: 1.6;
            font-family: 'Gowun Batang', serif;
        }
        .key-action-list li::before {
            content: "💡";
            position: absolute;
            left: 0;
            color: var(--accent);
            font-size: 1.2rem;
        }
        
        /* 최종 메시지 */
        #final-message { 
            color: var(--primary); 
            font-size: 1.5rem; 
            font-weight: 700;
            white-space: pre-wrap; 
        }

        /* 모달 스타일 (팝업창) */
        .modal-overlay {
            position: fixed; top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(0, 0, 0, 0.5); display: none; /* 초기 숨김 */
            justify-content: center; align-items: center; z-index: 10000;
        }
        .modal-content {
            background: var(--card-bg); padding: 30px; border-radius: 20px;
            max-width: 400px; width: 90%; box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
            font-family: 'Gowun Batang', serif;
            animation: modalFadeIn 0.3s;
            position: relative;
        }
        .close-modal {
            position: absolute; top: 15px; right: 20px; font-size: 1.5rem;
            color: var(--text-sub); cursor: pointer;
        }
        @keyframes modalFadeIn { from { opacity: 0; transform: translateY(-20px); } to { opacity: 1; transform: translateY(0); } }

        /* 포토카드 푸터 스타일 (수정 1, 2, 3 반영) */
        .brand-footer {
            margin-top: 15px; /* 간격 축소 (수정 3) */
            text-align: center;
            font-size: 0.9rem;
            font-family: 'Gowun Batang', serif;
            display: flex;
            align-items: center;
            justify-content: center; /* 가운데 정렬 (수정 2) */
        }
        .brand-footer a {
            color: #387669; /* 진한 민트 색상 (수정 2) */
            text-decoration: none;
            font-weight: 700;
            display: flex;
            align-items: center;
            gap: 5px;
        }
        .brand-footer a:hover {
            text-decoration: underline;
        }
        .brand-footer .fab.fa-instagram {
            font-size: 1.2em; /* 아이콘 크기 조정 */
        }

        /* 반응형 디자인 (모바일 최적화) */
        @media (max-width: 600px) {
            .main-title { font-size: 2.2rem; }
            .section-title { font-size: 1.8rem; }
            .saju-row { gap: 4px; }
            .saju-hanja { font-size: 1.5rem; }
            .summary-grid { grid-template-columns: 1fr; }
            .guide-item { max-width: 100%; min-width: 100%; margin-bottom: 10px; }
            .nav-bar { gap: 10px; overflow-x: auto; padding: 15px 10px; }
            .nav-item { font-size: 0.8rem; padding: 0 5px; flex-shrink: 0; }
            .month-btn-grid { grid-template-columns: repeat(4, 1fr); }
            .brand-footer { margin-top: 15px; font-size: 0.8rem; }
        }
    </style>
    
    <script>
        // 1. Mock Data (테스트 및 폴백용으로 HTML 내부에 유지)
        const MOCK_REPORT_DATA = {
            "analysis": {
                "summary_card": {
                    "keyword": "직설적이고 냉철한 판단으로 사업의 기반을 단단히 다지는 해", 
                    "best_month": "양력 9월 (酉月)", 
                    "risk": "아이디어 과잉과 실행력 분산", 
                    "action_item": "수익 모델 구조화 및 자동화 시스템 구축에 집중"
                },
                "detailed_analysis": {
                    "wealth_luck": "경금(庚)에게 현재 재물운은 명예(火)로 인해 지출을 동반합니다. 돈을 벌기보다 명예와 기반을 다지는 투자에 집중하는 것이 실속을 챙기는 길입니다.\\n\\n이는 장기적인 브랜딩과 콘텐츠 IP 확보에 필수적인 투자입니다. 단기적인 수익에 집착하지 마십시오.", 
                    "career_luck": "냉철한 분석력과 판단력이 빛을 발하는 시기입니다. 다만, 조직 내 갈등이나 예상치 못한 압박이 올 수 있으니, 꼼꼼한 문서 처리와 협상력이 중요합니다.\\n\\n특히, 파트너십 계약 시에는 경금 일간의 강한 주체성을 바탕으로 명확한 선을 그어야 합니다.", 
                    "love_family_luck": "가정 내에서는 리더십이 과도해져 가족 구성원과의 관계에서 충돌이 발생할 수 있습니다. 각자의 역할을 명확히 하고 존중하는 태도가 필요합니다.\\n\\n가장 중요한 것은 '결과'가 아닌 '과정'을 존중하는 부드러움을 보여주는 것입니다.", 
                    "change_luck": "사업장 확장이나 이사 변동운이 강하게 들어옵니다. 모든 계약 과정에서 전문가의 조언을 반드시 구하고 꼼꼼하게 검토해야 리스크를 줄일 수 있습니다.\\n\\n불안정성이 높은 달(월별 가이드 참고)에는 큰 계약을 피하십시오.", 
                    "health_advice": "강한 관살(火) 운으로 스트레스와 과로로 인한 심혈관 및 호흡기 계통에 주의해야 합니다. 규칙적인 운동과 휴식으로 기운을 통제하세요.\\n\\n금(金) 기운의 날카로움을 해소하기 위해 심리적 안정감을 주는 루틴을 확보하십시오."
                },
                "customer_analysis": {
                    "wealth_luck": "돈을 벌 기회보다는 명성을 얻고 기반을 닦는 데 돈이 나갈 해입니다. 당장의 수익보다는 브랜드를 키우는 데 필요한 '성장형 지출'에 투자하고, 장기적인 성공에 집중하세요.", 
                    "career_luck": "판단력이 매우 날카로워집니다. 다만 주변의 압력이나 경쟁이 강해질 수 있으니, 계약서나 중요한 문서 처리는 실수 없이 꼼꼼하게 진행해야 합니다. 사업에서는 명확한 기준을 세우는 것이 중요합니다.", 
                    "love_family_luck": "집이나 가족에게는 강한 리더가 되기보다, 가족 구성원 각자의 의견을 존중하고 부드럽게 대화하는 태도가 필요합니다. 강한 주장을 내려놓고 편안한 관계를 유지하는 것이 좋습니다.", 
                    "change_luck": "이동하거나 거주지를 바꿀 운이 있습니다. 이사나 새로운 사업을 위한 계약을 할 때는, 주변의 조언을 듣고 신중하게 결정해야 손해를 줄일 수 있습니다."
                },
                "qa_section": {
                    "q1": "새 사업(희구소)의 수익 모델을 언제 확정하는 것이 좋을까요?", 
                    "a1": "경금(庚) 일간에게 지금은 수익화 모델을 완성하는 금(金) 기운이 약합니다. 늦가을(양력 9월~10월)에 금 기운이 강해지니, 그때까지 콘텐츠와 구조를 완성하고, 가을 이후에 수익 모델을 확정하여 공격적으로 실행하십시오.",
                    "q2": "아이디어 과잉을 시스템으로 묶는 구체적인 방법은 무엇인가요?",
                    "a2": "아이디어(水)를 생산하는 것에 20%, 이를 상품화하고 시스템으로 묶는 구조화(金)에 80%의 시간을 투자하세요. 특히, Gemini AI 프롬프트에 '주체성 강한 일간'의 필터를 강제 주입하여, AI가 아이디어의 필터 역할을 하도록 훈련하는 것이 핵심 솔루션입니다."
                },
                "final_message": "당신이 설정한 논리적인 시스템만이 당신의 뛰어난 추진력을 완성시킬 수 있습니다.\\n\\n오직 실속과 결과에 집중하십시오.", 
                "radar_chart": {
                    "labels": ["추진력", "수익화", "협상력", "안정성", "리더십"],
                    "current": [8, 5, 6, 7, 7],
                    "future": [7, 8, 9, 7, 8]
                },
                "monthly_flow": [70, 75, 80, 65, 85, 50, 60, 70, 95, 80, 75, 70],
                "monthly_guide": {
                    "1": {"title": "내부 정비 및 구조화 시작", "wealth": "보통", "career": "내부 정비와 문서 작업에 유리.", "love": "차분한 관계 유지", "focus": "업무/사업 프로세스 정립", "caution": "급격한 투자 금지", "action": "회계/정산 시스템 완성"},
                    "9": {"title": "금 기운 발동! 수익 모델 극대화", "wealth": "매우 좋음", "career": "수익 모델 확정 및 공격적 영업 시작.", "love": "관계의 결실을 맺는 시기", "focus": "실적 관리 및 계약 체결", "caution": "자만심 경계", "action": "새로운 상품 출시 및 브랜딩 강화"}
                },
                "key_actions": [
                    "분산된 아이디어를 '수익화 파이프라인'이라는 단 하나의 틀 안에 넣는 시스템 구축에 80%의 시간을 투자하십시오.",
                    "재물운은 장기적 명예 투자에 집중되니, 단기 수익보다 브랜딩, IP 확보, 콘텐츠 품질 향상에 필요한 '실속 지출'만 허용하십시오.",
                    "강한 리더십이 충돌을 만들 수 있습니다. 가정에서는 '결과'가 아닌 '과정'을 존중하는 부드러운 태도를 보여야 합니다."
                ]
            }
        }; 
        
        // Mock 만세력 데이터 (예시 구조를 맞추기 위해 추가)
        const MOCK_MANSE_DATA = {
            day_master: '庚금', // 일간
            curr_age: 36, 
            current_dw_start_year: 2017,
            pillars: [
                { stem: '乙', branch: '亥' }, // 년주
                { stem: '己', branch: '卯' }, // 월주
                { stem: '庚', branch: '午' }, // 일주 (일간은 庚)
                { stem: '丁', branch: '巳' }  // 시주
            ],
            ten_gods_result: [
                { stem_ten_god: '겁재', branch_ten_god: '식신' }, // Mock Data의 구조에 따라 임시 지정
                { stem_ten_god: '정인', branch_ten_god: '정재' },
                { stem_ten_god: '비견', branch_ten_god: '편관' }, // 일간은 비견으로
                { stem_ten_god: '정관', branch_ten_god: '정인' }
            ],
            daewoon_list: [
                { age: 6, ganji: '戊子' }, { age: 16, ganji: '丁亥' }, 
                { age: 26, ganji: '丙戌' }, { age: 36, ganji: '乙酉' }, // 현재 대운
                { age: 46, ganji: '甲申' }, { age: 56, ganji: '癸未' }
            ],
            daewoon_sipsin: {
                '戊子': { stem: '편인', branch: '상관' }, '丁亥': { stem: '정관', branch: '식신' }, 
                '丙戌': { stem: '편관', branch: '편인' }, '乙酉': { stem: '정재', branch: '겁재' }, // 36세: 정재(乙) + 겁재(酉)
                '甲申': { stem: '편재', branch: '비견' }, '癸未': { stem: '상관', branch: '정인' }
            },
            sewoon_ganji: {
                2024: '甲辰', 2025: '乙巳', 2026: '丙午', 2027: '丁未', 2028: '戊申', 2029: '己酉', 
                2030: '庚戌', 2031: '辛亥', 2032: '壬子', 2033: '癸丑'
            },
            sewoon_sipsin_map: {
                2024: { stem: '편재', branch: '편인' }, 2025: { stem: '정재', branch: '정관' }, 
                2026: { stem: '편관', branch: '정관' }, // 2026년: 편관(丙) + 정관(午)
                2027: { stem: '정관', branch: '정인' }, 2028: { stem: '편인', branch: '비견' }, 
                2029: { stem: '정인', branch: '겁재' }, 2030: { stem: '비견', branch: '편인' }, 
                2031: { stem: '겁재', branch: '식신' }, 2032: { stem: '식신', branch: '상관' },
                2033: { stem: '상관', branch: '편재' }
            }
        };

        // window.reportDataPackage에 Python 데이터가 할당될 예정입니다.
        // 데이터가 주입되지 않을 경우를 대비하여 Mock Data로 초기화합니다.
        if (typeof window.reportDataPackage === 'undefined') {
            window.reportDataPackage = {
                analysis: MOCK_REPORT_DATA.analysis,
                manse: MOCK_MANSE_DATA
            };
        }

        let analysisData = {}; 
        let manseData = {};
        let monthlyFlowChart = null;
        
        // 2. 사주 용어 사전 (십성, 간지, 대운 용어 통합)
        const SAJU_DICT = {
            // 십성 (Ten Gods)
            '비견': '친구, 형제처럼 내 편이 되는 존재', '겁재': '내 몫을 뺏는 경쟁자',
            '식신': '재능·표현, 먹고사는 힘', '상관': '자유분방, 튀는 성향',
            '정재': '성실히 모은 정직한 재물', '편재': '우연히 얻는 뜻밖의 재물',
            '정관': '규칙, 명예, 안정적인 직업', '편관': '권력, 도전, 변화 많은 일',
            '정인': '대인관계, 배움, 조력자', '편인': '독립적 조력자, 특별한 배움',
            '일원': '일간(나) 자신',
            
            // 12신살 및 12운성 (예시를 위한 최소한의 데이터만 포함)
            '장생': '생명의 시작, 힘이 왕성함', '제왕': '힘의 절정, 최고의 왕성함',
            '건록': '사회 진출, 안정된 직업운', '쇠': '기운이 약해지고 힘이 줄어듦',
            '도화살': '매력적이고 인기가 많아 대인관계가 원활함',
            '역마살': '자주 이동하고 변화가 많은 운세',
            
            // 간지 및 대운 간지 (만세력 데이터에서 사용된 값 위주)
            '巳': '지지의 사화(巳)는 역마살과 관련이 있으며, 변화와 확장을 의미합니다.',
            '午': '지지의 오화(午)는 제왕의 기운으로, 가장 강한 에너지와 리더십을 의미합니다.',
            '卯': '지지의 묘목(卯)은 도화살과 관련되며, 대인 관계에서의 인기와 매력을 의미합니다.',
            '亥': '지지의 해수(亥)는 지살(地殺)과 관련되며, 이동과 활동성을 의미합니다.',
            '丙午': '2026년 세운 간지입니다. 강한 불(火) 기운으로 명예, 권력, 관재에 대한 압박이 강해지는 해를 의미합니다.',
            '乙酉': '현재 대운 간지입니다. 정재(乙)의 안정적인 재물과 겁재(酉)의 경쟁적 결실을 의미합니다.'
        };
        
        // 오행 컬러 매핑 함수
        function getGanjiElementColor(hanja) { 
            const elements = {'甲':'wood', '乙':'wood', '寅':'wood', '卯':'wood', '丙':'fire', '丁':'fire', '巳':'fire', '午':'fire', '戊':'earth', '己':'earth', '辰':'earth', '戌':'earth', '丑':'earth', '未':'earth', '庚':'metal', '辛':'metal', '申':'metal', '酉':'metal', '壬':'water', '癸':'water', '亥':'water', '子':'water'}; 
            return elements[hanja] ? `bg-${elements[hanja]}` : ''; 
        }
        
        // 한자 → 한글 매핑
        const HANJA_TO_KR = {
            '甲':'갑', '乙':'을', '丙':'병', '丁':'정', '戊':'무', '己':'기', '庚':'경', '辛':'신', '壬':'임', '癸':'계',
            '子':'자', '丑':'축', '寅':'인', '卯':'묘', '辰':'진', '巳':'사', '午':'오', '未':'미', '申':'신', '酉':'유', '戌':'술', '亥':'해'
        };

        // DOM 로드 후 렌더링 시작 (이 부분이 누락되어 빈 화면이 보였을 수 있습니다.)
        document.addEventListener('DOMContentLoaded', function() {
            // Chart.js 로딩 및 캔버스 요소 준비 확인
            if (typeof Chart === 'undefined') {
                console.error("Chart.js 라이브러리가 로드되지 않았습니다.");
                return;
            }

            if (window.reportDataPackage && window.reportDataPackage.analysis && window.reportDataPackage.manse) {
                renderReport(window.reportDataPackage.analysis, window.reportDataPackage.manse);
            } else {
                // 폴백: Mock 데이터 사용 (파이썬에서 데이터 주입 실패 시 대비)
                 renderReport(MOCK_REPORT_DATA.analysis, MOCK_MANSE_DATA);
            }
            
            // 네비게이션바 활성 상태 초기화
            window.addEventListener('scroll', updateNavActiveState);
            updateNavActiveState();
        });

        // === 핵심 렌더링 함수 ===
        function renderReport(data, manse) {
            analysisData = data; 
            manseData = manse;
            
            const dayMaster = manse.day_master; 
            const summaryCard = data.summary_card || {};
            const currentAge = manse.curr_age;
            
            // 1. Header & Title 업데이트
            const headerTitle = summaryCard.keyword || '당신의 빛나는 계절이 조용히 다가옵니다';
            const fixedHeaderTitle = headerTitle.replace('판단으로 사업의 기반을', '판단으로<br>사업의 기반을'); // 디자인 유지 위한 줄바꿈 처리
            const customerName = manse.customer_name || '고객';
            // 사용자 HTML 파일의 문자열 주입을 위해 '께' 대신 '님은,'을 사용함.
            // 하지만 사용자 요청이 '따뜻하고 감성적'이므로 '님께'로 수정합니다.
            document.getElementById('dynamic-title').innerHTML = `2026년 ${dayMaster}일간 ${customerName}님께,<br>${fixedHeaderTitle}`;
            
            // 2. 만세력 & 대운
            renderManse(manseData); 
            renderDaewoon(manse.daewoon_list, currentAge, manse.current_dw_start_year); 
            renderSewoonTimeline(manse.current_dw_start_year); 

            // 3. 핵심 요약 (포토카드)
            document.getElementById('card-main-title').innerHTML = summaryCard.keyword || '2026년 운세 분석';
            renderSummary(summaryCard); 

            // 4. 스탯 변화, 월별 가이드 통합
            if (data.radar_chart) updateRadarChart(data.radar_chart);
            if (data.monthly_flow) updateMonthlyFlowChart(data.monthly_flow); 
            
            renderMonthButtons(); 
            // 베스트 월이 있으면 해당 월을 기본 선택, 없으면 1월
            // AI가 '양력 9월 (酉月)' 형태로 줄 수 있으므로, 숫자만 추출
            const bestMonthMatch = summaryCard.best_month ? summaryCard.best_month.match(/\d+/) : null;
            const initialMonth = bestMonthMatch ? parseInt(bestMonthMatch[0]) : 1; 
            selectMonth(initialMonth); 

            // 5. 상세 분석 & Q&A & 개운법
            renderDetailedAnalysis(data.detailed_analysis, data.qa_section, data.final_message, data.key_actions);
            
            // 6. 푸터 메시지 업데이트 (fixedHeaderTitle 사용)
            const footerMsg = document.getElementById('footer-message');
            if (footerMsg && headerTitle) {
                footerMsg.innerHTML = `<strong>"${headerTitle}"</strong>`;
            }
        }

        // 만세력 명식 렌더링
        function renderManse(manse) {
            // manse.pillars: [년주, 월주, 일주, 시주] 순서 (0, 1, 2, 3)
            // 렌더링 순서: 시주(3), 일주(2), 월주(1), 년주(0)
            const pillarsIndex = [3, 2, 1, 0]; 
            
            let tenGodTopHtml = '', stemHtml = '', branchHtml = '', tenGodBottomHtml = '';
            
            for(let i of pillarsIndex) {
                const p = manse.pillars[i];
                const ten = manse.ten_gods_result[i];
                const stem = p.stem; 
                const branch = p.branch;
                const topGod = ten.stem_ten_god; 
                const bottomGod = ten.branch_ten_god;
                const isDayMaster = topGod === '일원';

                const stemColor = getGanjiElementColor(stem); 
                const branchColor = getGanjiElementColor(branch);

                // 천간 십성
                tenGodTopHtml += `<div class="ten-god-top ${isDayMaster ? 'ten-god-tag master' : ''}" onclick="openInfo('${topGod}')">${topGod}</div>`;
                
                // 천간 블록 (Stem)
                stemHtml += `<div class="saju-cell ${stemColor}">
                                <div class="saju-hanja">${stem}</div><div class="saju-korean">${HANJA_TO_KR[stem] || ''}</div>
                             </div>`;
                             
                // 지지 블록 (Branch)
                branchHtml += `<div class="saju-cell ${branchColor}" onclick="openInfo('${branch}')">
                                <div class="saju-hanja">${branch}</div><div class="saju-korean">${HANJA_TO_KR[branch] || ''}</div>
                             </div>`;
                             
                // 지지 십성
                tenGodBottomHtml += `<div class="ten-god-bottom" onclick="openInfo('${bottomGod}')">${bottomGod}</div>`;
            }
            
            document.getElementById('saju-ten-god-top').innerHTML = tenGodTopHtml;
            document.getElementById('saju-stem').innerHTML = stemHtml;
            document.getElementById('saju-branch').innerHTML = branchHtml;
            document.getElementById('saju-ten-god-bottom').innerHTML = tenGodBottomHtml;
        }
        
        // 대운 타임라인 및 진행바 렌더링
        function renderDaewoon(daewoonList, currAge, currentDwStartYear) {
            let dwHtml = ''; 
            let currentDw = null;

            daewoonList.forEach(item => {
                const isCurrent = (currAge >= item.age && currAge < item.age + 10);
                const activeClass = isCurrent ? 'current' : '';
                const dwSipsin = manseData.daewoon_sipsin[item.ganji] || {};
                const stemGod = dwSipsin.stem_ten_god || dwSipsin.stem || 'N/A';
                const branchGod = dwSipsin.branch_ten_god || dwSipsin.branch || 'N/A';
                
                if (isCurrent) {
                    currentDw = item;
                }

                dwHtml += `
                    <div class="dw-node ${activeClass}">
                        <span class="dw-age">${item.age}세</span>
                        <span class="dw-sipsin" onclick="openInfo('${stemGod}')">${stemGod}</span>
                        <span class="dw-ganji">${item.ganji}</span>
                        <span class="dw-sipsin" onclick="openInfo('${branchGod}')">${branchGod}</span>
                    </div>
                `;
            });
            document.getElementById('daewoon-timeline').innerHTML = dwHtml;
            
            // 대운 진행 바 로직
            if (currentDw) {
                const dwStartAge = currentDw.age; 
                const dwStartYear = currentDwStartYear; 
                const dwEndYear = dwStartYear + 9;

                const progressInYears = new Date().getFullYear() - dwStartYear;
                const progressPercent = Math.min(100, (progressInYears / 10) * 100);

                document.getElementById('dw-current-ganji').innerHTML = `
                    <strong style="color:var(--text-main);">${currentDw.ganji} 대운</strong>이 ${currentDw.age}세(${dwStartYear}년)부터 진행 중입니다.
                `;

                document.getElementById('daewoon-progress-area').innerHTML = `
                    <div class="daewoon-progress-box">
                        <div style="display:flex; justify-content:space-between; align-items:center;">
                            <strong>${currentDw.ganji} 대운 (${currentDw.age}세~)</strong>
                            <span style="font-size:0.8rem; color:var(--primary);">인생의 여정</span>
                        </div>
                        <div class="daewoon-bar-bg"><div id="dw-fill" class="daewoon-bar-fill" style="width: ${progressPercent}%;"></div></div>
                        <div class="daewoon-info"><span id="dw-start-year">${dwStartYear}년</span><span id="dw-progress">${Math.floor(progressPercent)}% 진행</span><span id="dw-end-year">${dwEndYear}년 종료</span></div>
                    </div>
                `;
            }
        }

        // 세운 흐름 렌더링 함수
        function renderSewoonTimeline(currentDwStartYear) {
            const currentYear = new Date().getFullYear();
            let swHtml = '';
            
            // 세운은 현재 대운 시작년도부터 10년치 (예시: 2024~2033) 또는 현재년도 근처 10년치 표시
            // 여기서는 manseData에 저장된 세운 정보를 사용합니다. (app.py에서 10년치 계산하여 주입)
            const sortedYears = Object.keys(manseData.sewoon_ganji).map(Number).sort((a, b) => a - b);
            
            for (let year of sortedYears) {
                const isCurrent = year === currentYear;
                const swGanji = manseData.sewoon_ganji[year] || 'N/A';
                const swSipsin = manseData.sewoon_sipsin_map[year] || {};
                
                const style = isCurrent ? 'font-weight: bold; color: var(--accent);' : '';
                
                const swStemGod = swSipsin.stem_ten_god || swSipsin.stem || 'N/A';
                const swBranchGod = swSipsin.branch_ten_god || swSipsin.branch || 'N/A';
                
                swHtml += `
                    <div class="sw-node" style="opacity: ${isCurrent ? 1 : 0.7}; border-bottom: ${isCurrent ? '3px solid var(--accent)' : 'none'}; min-width: 50px; display: flex; flex-direction: column; align-items: center; font-size: 0.8rem; flex-shrink: 0;">
                        <span style="font-size: 0.7rem; color:#999;">${year}</span>
                        <span style="font-size: 0.8rem; ${style}" onclick="openInfo('${swStemGod}')">${swStemGod}</span>
                        <span class="sw-ganji" style="${style}" onclick="openInfo('${swGanji}')">${swGanji}</span>
                        <span style="font-size: 0.7rem; ${style}" onclick="openInfo('${swBranchGod}')">${swBranchGod}</span>
                    </div>
                `;
            }
            
            document.getElementById('sewoon-timeline').innerHTML = swHtml;
        }

        // 핵심 요약 카드 렌더링
        function renderSummary(summary) {
             // Mock Data에 맞게 동적 업데이트
            const gridHtml = `
                <div class="summary-box"><i class="fas fa-crown" style="color:#FFCBA4; font-size:1.5rem; margin-bottom:5px;"></i><div class="summary-label"><strong>올해의 테마</strong></div><div class="summary-val">"${summary.keyword || '...'}"</div></div>
                <div class="summary-box" onclick="triggerConfetti(event)"><i class="fas fa-star" style="color:var(--primary); font-size:1.5rem; margin-bottom:5px;"></i><div class="summary-label"><strong>가장 빛날 때</strong></div><div class="summary-val">${summary.best_month || 'N월'} (Best) ✨</div></div>
                <div class="summary-box"><i class="fas fa-shield-alt" style="color:#A2C2E0; font-size:1.5rem; margin-bottom:5px;"></i><div class="summary-label"><strong>나를 지키는 것</strong></div><div class="summary-val">${summary.risk || '...'}</div></div>
                <div class="summary-box"><i class="fas fa-leaf" style="color:#E6CEAC; font-size:1.5rem; margin-bottom:5px;"></i><div class="summary-label"><strong>성장을 위한 씨앗</strong></div><div class="summary-val">${summary.action_item || '...'}</div></div>
            `;
            document.getElementById('summary-grid').innerHTML = gridHtml;
        }
        
        // 상세 분석, Q&A, 최종 메시지 렌더링
        function renderDetailedAnalysis(details, qa, final_msg, key_actions) {
            
            // 🚨🚨🚨 핵심 수정: HTML 리포트에는 고객용 쉬운 설명을 사용
            const customerDetails = analysisData.customer_analysis || details; 
            
            // 🔧 건강 조언: customer_analysis에 있으면 그것을 사용, 없으면 detailed_analysis 것 사용
            const healthAdvice = customerDetails.health_advice || details.health_advice; 
            
            const sections = [
                {id: 'wealth', title: '💰 재물운', data: customerDetails.wealth_luck},
                {id: 'career', title: '👔 직업/사업운', data: customerDetails.career_luck},
                {id: 'love', title: '💖 애정/가정운', data: customerDetails.love_family_luck},
                {id: 'change', title: '🏠 변동운 (이사/부동산)', data: customerDetails.change_luck},
                {id: 'health', title: '🏥 건강 조언', data: healthAdvice} 
            ];
            
            // 상세 분석 에세이 렌더링
            let detailHtml = sections.map(sec => {
                const content = sec.data || "AI 분석 중입니다. 데이터가 유효하지 않을 수 있습니다.";
                return `
                    <div class="detail-box">
                        <h3 class="detail-title">${sec.title}</h3>
                        <div class="detail-content" style="white-space: pre-wrap; font-size: 1.05rem;">${content.replace(/\\n/g, '<br><br>')}</div>
                    </div>
                `;
            }).join('');
            
            // 개운법 블록 생성
            if (key_actions && key_actions.length > 0) {
                const actionListHtml = key_actions.map(action => `<li>${action}</li>`).join('');
                detailHtml += `
                    <div class="key-action-box">
                        <h3 class="serif">2026 개운법 (Key Actions)</h3>
                        <ul class="key-action-list">
                            ${actionListHtml}
                        </ul>
                    </div>
                `;
            }

            document.getElementById('detail-content-area').innerHTML = detailHtml;
            
            // Q&A 렌더링
            let qaHtml = '';
            const renderQaItem = (q, a) => {
                if (!q || !a) return '';
                // 이스케이프된 줄바꿈 문자열 처리 (\n -> <br><br>)
                const formattedAnswer = a.replace(/\\n/g, '<br><br>');
                return `
                    <div style="margin-bottom:20px;">
                        <div class="qa-question" style="font-weight:700; margin-bottom:10px;"><i class="fas fa-question-circle" style="color:var(--primary); margin-right:8px;"></i> ${q}</div>
                        <div class="qa-answer" style="white-space: pre-wrap; font-size: 1rem; line-height: 1.8; background: #FFFFFF; padding: 15px; border-radius: 10px;">${formattedAnswer}</div>
                    </div>
                `;
            };

            qaHtml += renderQaItem(qa.q1, qa.a1);
            qaHtml += renderQaItem(qa.q2, qa.a2);

            document.getElementById('qa-content').innerHTML = qaHtml;
            
            // 최종 메시지 렌더링
            const fixedFinalMessage = final_msg.replace('시스템만이 당신의 뛰어난 추진력을', '시스템만이<br>당신의 뛰어난 추진력을').replace(/\\n/g, '<br><br>');
            document.getElementById('final-message').innerHTML = fixedFinalMessage;
        }

        // 레이더 차트 (스탯 변화) 렌더링
        function updateRadarChart(chartData) {
            if (!chartData || !document.getElementById('radarChart')) return;
            // 기존 차트가 있다면 파괴
            if (Chart.getChart('radarChart')) {
                Chart.getChart('radarChart').destroy();
            }

            new Chart(document.getElementById('radarChart'), { 
                type: 'radar', 
                data: { 
                    labels: chartData.labels, 
                    datasets: [
                        { label: '기본 글자', data: chartData.current, backgroundColor: 'rgba(176, 224, 213, 0.4)', borderColor: '#B0E0D5', borderWidth: 2 }, 
                        { label: '2026 변화', data: chartData.future, backgroundColor: 'rgba(255, 203, 164, 0.4)', borderColor: '#FFCBA4', borderWidth: 2 }
                    ] 
                }, 
                options: { 
                    responsive: true, 
                    maintainAspectRatio: false, 
                    scales: { 
                        r: { 
                            min:0, max:10, ticks:{display:false}, 
                            pointLabels:{font:{size:12, family:"'Gowun Batang'"}} 
                        } 
                    }, 
                    plugins: { legend: { position: 'bottom', labels: { font: { family: "'Gowun Batang'" } } } } 
                } 
            });
        }
        
        // 월별 흐름 차트 렌더링
        function updateMonthlyFlowChart(flowData) {
            if (!flowData || !document.getElementById('monthlyFlowChart')) return;
            // 기존 차트가 있다면 파괴
            if (Chart.getChart('monthlyFlowChart')) {
                Chart.getChart('monthlyFlowChart').destroy();
            }

            const flowCtx = document.getElementById('monthlyFlowChart').getContext('2d');
            monthlyFlowChart = new Chart(flowCtx, { 
                type: 'line', 
                data: { 
                    labels: ['1월', '2월', '3월', '4월', '5월', '6월', '7월', '8월', '9월', '10월', '11월', '12월'], 
                    datasets: [
                        { 
                            data: flowData, 
                            borderColor: '#387669', // Darker Mint
                            backgroundColor: (context) => { 
                                const ctx = context.chart.ctx; 
                                const gradient = ctx.createLinearGradient(0, 0, 0, 200); 
                                gradient.addColorStop(0, 'rgba(176, 224, 213, 0.7)');
                                gradient.addColorStop(1, 'rgba(176, 224, 213, 0)'); 
                                return gradient; 
                            }, 
                            fill: true, tension: 0.4, 
                            pointBackgroundColor: '#fff', 
                            pointBorderColor: '#8C6A5A',
                            pointRadius: 5, 
                            pointHoverRadius: 7 
                        }
                    ] 
                }, 
                options: { 
                    responsive: true, 
                    maintainAspectRatio: false, 
                    onClick: (e, activeEls) => { if(activeEls.length > 0) { selectMonth(activeEls[0].index + 1); } },
                    plugins: { legend: { display: false } }, 
                    scales: { y: { display: false, min: 0, max: 100 }, x: { grid: { display: false } } } 
                } 
            });
        }

        // 월별 버튼 렌더링 (6개씩 2줄 그리드)
        function renderMonthButtons() {
            const grid = document.getElementById('month-btn-grid'); 
            grid.innerHTML = '';
            for(let m=1; m<=12; m++) { 
                const btn = document.createElement('div'); 
                btn.className = 'month-btn'; 
                btn.innerText = `${m}월`; 
                btn.onclick = () => selectMonth(m); 
                grid.appendChild(btn); 
            }
        }
        
        // 월별 가이드 선택 및 대시보드 업데이트
        function selectMonth(m) {
            document.querySelectorAll('.month-btn').forEach(b => b.classList.remove('active'));
            const btn = document.querySelectorAll('.month-btn')[m-1]; 
            if(btn) btn.classList.add('active');
            
            const d = analysisData.monthly_guide ? analysisData.monthly_guide[String(m)] : null;
            
            const defaultData = {
                title: `${m}월: 월별 데이터 준비 중`,
                wealth: '보통', career: '월별 흐름에 맞춰 유연하게 대처', 
                love: '안정적인 관계 유지', focus: '핵심 목표 재점검', 
                caution: '문서/금전 거래 주의', action: '일상 루틴 유지'
            };
            
            const dataToRender = d || defaultData;

            const titleElem = document.getElementById('m-title'); 
            titleElem.style.animation = 'none'; titleElem.offsetHeight; titleElem.style.animation = 'fadeIn 0.5s';
            
            document.getElementById('m-title').innerText = dataToRender.title;
            updateLuck('t-wealth', dataToRender.wealth); 
            updateLuck('t-career', dataToRender.career); 
            updateLuck('t-love', dataToRender.love);
            
            document.getElementById('m-focus').innerText = dataToRender.focus; 
            document.getElementById('m-caution').innerText = dataToRender.caution; 
            document.getElementById('m-action').innerText = dataToRender.action;
        }

        // 운세 등급에 따른 텍스트 색상 업데이트
        function updateLuck(id, val) { 
            const el = document.getElementById(id); 
            el.innerText = val; 
            el.style.color = "#555555";
            if(val.includes('매우 좋음') || val.includes('대길')) el.style.color = "#2E7D32"; 
            else if(val.includes('주의') || val.includes('흉')) el.style.color = "#C62828"; 
            else if(val.includes('보통')) el.style.color = "#F5A623"; 
            else el.style.color = "#555555";
        }
        
        // 폭죽 효과
        function triggerConfetti(event) { 
            event.stopPropagation();
            confetti({ 
                particleCount: 150, 
                spread: 70, 
                origin: { 
                    x: event.clientX / window.innerWidth,
                    y: event.clientY / window.innerHeight
                }, 
                colors: ['#B0E0D5', '#FFCBA4', '#A8D5BA'] 
            }); 
        }
        
        // 용어 팝업 모달 함수
        function openInfo(key) { 
            document.getElementById('info-title').innerText = key;
            
            let content = SAJU_DICT[key] || "용어 설명 준비 중입니다.";
            
            document.getElementById('info-content').innerHTML = `
                <p style="font-size: 1rem; color: #333; font-weight: 700;">${key}의 의미</p>
                <p style="margin-top: 10px; line-height: 1.6;">${content}</p>
            `;
            document.getElementById('infoModal').style.display = 'flex'; 
        }
        
        // 모달 닫기
        function closeModal(e, force = false) { 
            if (force || !e || e.target.classList.contains('modal-overlay') || e.target.classList.contains('close-modal')) { 
                document.querySelectorAll('.modal-overlay').forEach(m => m.style.display = 'none'); 
            } 
        }
        
        // 포토카드 캡처
        function savePhotoCard() { 
            const target = document.getElementById('capture-area');
            html2canvas(target, { 
                scale: 2, 
                logging: false,
                useCORS: true 
            }).then(canvas => { 
                const link = document.createElement('a'); 
                link.download = 'HEEGUSO_AI_THEME_CARD.png'; 
                link.href = canvas.toDataURL('image/png'); 
                link.click(); 
            }); 
        }
        
        // 네비게이션바 활성 상태 업데이트
        function updateNavActiveState() {
            const sections = document.querySelectorAll('section');
            const navItems = document.querySelectorAll('.nav-item');
            let currentActive = null;

            sections.forEach(section => {
                const rect = section.getBoundingClientRect();
                // 네비게이션 높이만큼 보정
                if (rect.top <= 80 && rect.bottom >= 80) { 
                    currentActive = section.id;
                }
            });

            navItems.forEach(item => {
                item.classList.remove('active');
                if (currentActive && item.getAttribute('href').substring(1) === currentActive) {
                    item.classList.add('active');
                }
            });
        }
    </script>
</head>
<body>
    <!-- 고정 네비게이션 바 -->
    <nav class="nav-bar">
        <a href="#sec-my" class="nav-item active">나의 원국</a>
        <a href="#sec-summary" class="nav-item">핵심 요약</a>
        <a href="#sec-chart" class="nav-item">스탯 변화</a>
        <a href="#sec-monthly" class="nav-item">월별 가이드</a>
        <a href="#sec-detail" class="nav-item">상세 분석</a>
        <a href="#sec-qa" class="nav-item">솔루션 Q&A</a>
    </nav>

    <div class="container">
        <header>
            <span class="brand">HEEGUSO | Hidden Luck Lab</span>
            <!-- 동적 타이틀 (스크립트에서 업데이트됨) -->
            <h1 class="main-title" id="dynamic-title">2026년 庚금일간에게,<br>직설적이고 냉철한 판단으로<br>사업의 기반을 단단히 다지는 해</h1>
            <div class="sub-title" id="dynamic-sub"></div>
        </header>

        <!-- 1. 나의 사주 명식 섹션 -->
        <section id="sec-my" class="card">
            <h2 class="section-title">나의 사주 명식 (My Energy)</h2>
            <div class="saju-wrapper">
                <div class="saju-row" id="saju-ten-god-top">
                    <!-- 십성 데이터는 스크립트에서 렌더링됩니다. -->
                </div> 
                <div class="saju-row" id="saju-stem">
                    <!-- 천간 데이터는 스크립트에서 렌더링됩니다. -->
                </div>      
                <div class="saju-row" id="saju-branch">
                    <!-- 지지 데이터는 스크립트에서 렌더링됩니다. -->
                </div>    
                <div class="saju-row" id="saju-ten-god-bottom">
                    <!-- 십성 데이터는 스크립트에서 렌더링됩니다. -->
                </div> 
                <div class="saju-row" style="margin-top:10px;">
                    <div class="saju-header">시주 (말년)</div>
                    <div class="saju-header">일주 (나)</div>
                    <div class="saju-header">월주 (청년)</div>
                    <div class="saju-header">년주 (초년)</div>
                </div>
            </div>
            
            <div style="padding-top:20px; border-top:1px dashed #eee; text-align:center;">
                <h3 class="serif" style="font-size:1.8rem; margin-bottom:15px; color:#333;">인생의 흐름 (Life Path)</h3>
                
                <div class="daewoon-timeline" id="daewoon-timeline">
                    <!-- 대운 데이터는 스크립트에서 렌더링됩니다. -->
                </div>
                <div id="dw-current-ganji" style="font-weight:bold; color:var(--text-main); margin-top:15px; font-family: 'Gowun Batang', serif;">현재: 乙酉 대운 (36세~)</div>
                
                <div id="daewoon-progress-area">
                    <!-- 대운 진행 바는 스크립트에서 렌더링됩니다. -->
                </div>

                <div id="sewoon-timeline-container">
                    <h4 style="font-size:1.2rem; margin-top:20px; color:var(--primary); font-weight:700;">현재 대운의 세운 흐름 (2024~2033)</h4>
                    <div style="display: flex; justify-content: space-between; overflow-x: auto; padding: 10px 0; border-top: 1px dashed #eee; margin-top: 15px;" id="sewoon-timeline">
                        <!-- 세운 데이터는 스크립트에서 렌더링됩니다. -->
                    </div>
                </div>
            </div>
        </section>

        <!-- 2. 핵심 실행 테마 섹션 (포토카드 캡처 영역) -->
        <section id="sec-summary" class="card">
            <h2 class="section-title">2026 나의 핵심 실행 테마</h2>
            <div style="text-align:right;"><button onclick="savePhotoCard()" style="font-family: 'Gowun Batang', serif; font-size:0.8rem; padding:8px 15px; background:var(--accent); color:var(--text-main); border:none; border-radius:15px; cursor:pointer; box-shadow: 0 3px 10px rgba(0,0,0,0.1);"><i class="fas fa-camera"></i> 캡처하여 공유</button></div>
            
            <div id="capture-area" style="aspect-ratio: 1 / 1; max-width: 600px; margin: 20px auto 0 auto; border: 2px dashed var(--primary); border-radius: 25px; background: #FFFFFF; box-shadow: 0 10px 30px rgba(176, 224, 213, 0.4);">
                <div class="photo-card-wrapper" style="padding: 30px;">
                    <div class="header-info" style="text-align:center;">
                        <span class="brand">Execution Report for 2026</span>
                        <h3 id="card-main-title" style="font-family: 'Gowun Batang', serif; font-size: 2rem; color: #333; margin: 10px 0 20px 0;">직설적이고 냉철한 판단으로<br>사업의 기반을 단단히 다지는 해</h3>
                    </div>

                    <div class="summary-grid" id="summary-grid">
                        <!-- 요약 데이터는 스크립트에서 렌더링됩니다. -->
                    </div>

                    <div style="text-align:center; margin-top:30px;">
                        <p id="footer-message" style="font-family: 'Gowun Batang', serif; font-size:1.25rem; color:#8D8580;">
                            <strong>"오직 실속과 결과에 집중하십시오."</strong>
                        </p>
                    </div>
                    
                    <!-- 수정된 푸터 (수정 1, 2, 3 반영) -->
                    <div class="brand-footer">
                        <a href="https://www.instagram.com/hiddenluck_lab" target="_blank">
                            <i class="fab fa-instagram"></i>
                            희구소 | HiddenLuck_Lab
                        </a>
                    </div>
                </div>
            </div>
        </section>

        <!-- 3. 스탯 변화 섹션 (레이더 차트) -->
        <section id="sec-chart" class="card">
            <h2 class="section-title">2026 나의 스탯 변화</h2>
            <div style="height: 300px; width: 100%;"><canvas id="radarChart"></canvas></div>
            <div style="text-align:center; margin-top:20px; font-size:0.9rem; color:#8D8580;">
                <p id="chart-description">
                    AI가 분석한 현재 기질(기본)과 2026년 운세 변화(미래)의 스탯을 비교합니다.<br><strong>&apos;기본 글자&apos;,&apos;2026 변화&apos;</strong>글자를 눌러 변화를 확인하세요.</p>
                </p>
            </div>
        </section>
        
        <!-- 4. 월별 실전 실행 가이드 섹션 -->
        <section id="sec-monthly" class="card">
            <h2 class="section-title">월별 실전 실행 가이드</h2>
            <div class="flow-chart-box"><canvas id="monthlyFlowChart"></canvas></div>
            
            <div class="month-btn-grid" id="month-btn-grid">
                <!-- 월별 버튼 (1월~12월)은 스크립트에서 렌더링됩니다. -->
            </div>
            
            <div class="monthly-dashboard">
                <h3 id="m-title" style="margin-bottom:20px; color:var(--accent); text-align:center; font-size:1.3rem; font-weight:700;">월별 타이틀</h3>
                
                <div class="monthly-luck-block">
                    <span class="luck-icon-large">💰</span>
                    <span class="luck-label-small">재물운</span>
                    <strong class="luck-value" id="t-wealth">보통</strong>
                </div>
                <div class="monthly-luck-block">
                    <span class="luck-icon-large">👔</span>
                    <span class="luck-label-small">직업/사업운</span>
                    <strong class="luck-value" id="t-career">내용</strong>
                </div>
                <div class="monthly-luck-block">
                    <span class="luck-icon-large">❤️</span>
                    <span class="luck-label-small">애정/관계운</span>
                    <strong class="luck-value" id="t-love">내용</strong>
                </div>

                <div class="guide-horizontal-grid">
                    <div class="guide-item">
                        <div class="guide-label-btn">Focus</div>
                        <div class="guide-content-box" id="m-focus">내용</div>
                    </div>
                    <div class="guide-item">
                        <div class="guide-label-btn" style="background: var(--accent);">Caution</div>
                        <div class="guide-content-box" id="m-caution">내용</div>
                    </div>
                    <div class="guide-item">
                        <div class="guide-label-btn" style="background: #A8D5BA;">Action Quest</div>
                        <div class="guide-content-box" id="m-action">내용</div>
                    </div>
                </div>
                
            </div>
        </section>

        <!-- 5. 상세 분석 에세이 섹션 -->
        <section id="sec-detail" class="card">
            <h2 class="section-title">상세 분석 에세이</h2>
            <div id="detail-content-area">
                <!-- 상세 분석 내용 및 개운법은 스크립트에서 렌더링됩니다. -->
            </div>
        </section>

        <!-- 6. 솔루션 Q&A 섹션 및 최종 메시지 -->
        <section id="sec-qa" class="card">
            <div class="qa-container">
                <h3 style="font-size: 2rem; color: var(--accent); margin-bottom: 25px; text-align: center;">가장 필요한 해답: Solution Q&A</h3>
                <div class="qa-content" id="qa-content">
                    <!-- Q&A 내용은 스크립트에서 렌더링됩니다. -->
                </div>
            </div>
            
            <div style="margin-top:30px; text-align:center;">
                <h3 id="final-message" class="serif">최종 메시지</h3>
            </div>
        </section>
        
        <!-- 십성/간지 정보 모달 (팝업) -->
        <div id="infoModal" class="modal-overlay" onclick="closeModal(event)">
            <div class="modal-content">
                <span class="close-modal" onclick="closeModal(null, true)">&times;</span>
                <h3 id="info-title">용어 설명</h3>
                <div id="info-content" style="margin-top:20px;">
                    <!-- 내용 -->
                </div>
            </div>
        </div>

        <!-- 푸터 CTA -->
        <div style="margin-top: 50px; text-align: center;">
            <a href="https://link.inpock.co.kr/hiddenluck" target="_blank" class="btn-link" style="
                display: inline-block; 
                background: var(--primary); 
                color: var(--text-main); 
                border: 1px solid #96CFC1;
                padding: 15px 30px; 
                border-radius: 12px; 
                font-weight: bold; 
                text-decoration: none; 
                transition: 0.2s; 
                box-shadow: 0 5px 15px rgba(176, 224, 213, 0.4); 
                font-family: 'Gowun Batang', serif; 
            ">
                <i class="fas fa-comment-dots"></i> 깊은 상담 요청하기
            </a>
        </div>
        
        <footer style="text-align:center; color:var(--text-sub); font-size:0.8rem; margin-top: 50px; font-family: 'Gowun Batang', serif;">
            Private Analysis by HEEGUSO
        </footer>
    </div>

</body>
</html>
"""

def generate_report_html(report_data: Dict) -> str:
    """
    Tier 2의 역할을 수행: 분석 결과를 HTML 템플릿에 주입하여 최종 HTML 문자열을 반환합니다.
    [핵심 수정]: JSON 직렬화 시 특수문자 탈출(Escaping) 처리를 강화하여 JS 에러를 방지합니다.
    """
    import json

    try:
        # 1. Python 객체를 JSON 문자열로 변환 (한글 보존)
        json_str = json.dumps(report_data, ensure_ascii=False)
        
        # 2. JavaScript 문자열 내부에 들어갈 때 깨지지 않도록 이스케이프 처리
        # Backslash(\) -> Double Backslash(\\)
        # Single Quote(') -> Escaped Single Quote(\')
        # 이 과정이 없으면 JS에서 'Uncaught SyntaxError'가 발생하여 화면이 하얗게 뜹니다.
        # 참고: r""" 문자열에서는 백슬래시 이스케이프가 복잡해지므로,
        # 원본 HTML에서 </head> 태그를 찾고 그 앞에 주입하는 방식으로 유지합니다.
        safe_json_str = json_str.replace('\\', '\\\\').replace("'", "\\'")
        
    except Exception as e:
        # 에러 발생 시에도 빈 JSON을 넣어주어 페이지가 멈추지 않게 함
        print(f"JSON Serialization Error: {e}")
        safe_json_str = "{}"

    # 3. HTML 템플릿 내의 데이터 주입구에 안전하게 삽입
    # 수정된 HTML 파일의 데이터 주입 위치(</head> 바로 앞)에 맞춥니다.
    injection_script = f"""
    <script>
        // Python에서 안전하게 처리된 JSON 데이터를 파싱합니다.
        try {{
            window.reportDataPackage = JSON.parse('{safe_json_str}');
            console.log("Report Data Loaded Successfully");
        }} catch (e) {{
            console.error("JSON Parsing Error:", e);
            // 에러 발생 시 Mock Data라도 보여주도록 처리 가능
        }}
    </script>
    """
    
    # 템플릿의 </head>를 찾아 주입 스크립트를 삽입합니다.
    final_html = HTML_TEMPLATE.replace("</head>", injection_script + "</head>")
    
    return final_html
