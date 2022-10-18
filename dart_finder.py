import pandas as pd
import requests


class Dart:
    def __init__(self, 사업연도, 분기, corp_code, crtfc_key):
        분기_dic = {1: "11013", 2: "11012", 3: "11014", 4: "11011"}
        self.사업연도 = 사업연도
        self.분기 = 분기_dic[분기]
        self.corp_code = corp_code
        self.crtfc_key = crtfc_key

    def 주요재무제표(self):

        resp = requests.get(
            f"https://opendart.fss.or.kr/api/fnlttSinglAcnt.json?crtfc_key={self.crtfc_key}&corp_code={self.corp_code}\
                &bsns_year={self.사업연도}&reprt_code={self.분기}&fs_div=OFS"
        )
        resp.json()
        dict = resp.json()
        df3 = pd.DataFrame(dict["list"])
        df4 = df3[df3["fs_nm"] == "재무제표"][
            ["sj_nm", "account_nm", "thstrm_amount", "frmtrm_amount"]
        ]
        df4 = df4.rename(
            columns={
                "sj_nm": "재무제표종류",
                "account_nm": "계정구분",
                "thstrm_amount": "당기",
                "frmtrm_amount": "전기",
            }
        )
        df4 = df4.set_index("재무제표종류")
        return df4

    def 기업개황(self):
        기업개황 = requests.get(
            f"https://opendart.fss.or.kr/api/company.json?crtfc_key={self.crtfc_key}&corp_code={self.corp_code}"
        )
        기업개황2 = 기업개황.json()
        기업개황 = pd.DataFrame.from_dict(기업개황2, orient="index")
        기업개황3 = 기업개황.rename(
            index={
                "status": "상태",
                "message": "에러메시지",
                "corp_name": "회사명",
                "adres": "주소",
                "corp_name_eng": "영문명",
                "stock_name": "종목명",
                "stock_code": "종목코드",
                "ceo_nm": "대표자명",
                "hm_url": "홈페이지",
                "ir_url": "IR페이지",
                "phn_no": "전화번호",
                "fax_no": "팩스번호",
                "est_dt": "설립일",
                "acc_mt": "결산월",
            }
        )
        기업개황3 = 기업개황3.iloc[[5, 6, 7, 11, 12, 14, 15, 17, 18]]

        return 기업개황3

    def 조건부자본증권미상환잔액(self):

        조건부자본증권미상환잔액 = requests.get(
            f"https://opendart.fss.or.kr/api/cndlCaplScritsNrdmpBlce.json?crtfc_key={self.crtfc_key}\
                &corp_code={self.corp_code}&bsns_year={self.사업연도}&reprt_code={self.분기}"
        )
        조건부자본증권미상환잔액2 = 조건부자본증권미상환잔액.json()
        조건부자본증권미상환잔액3 = pd.DataFrame(조건부자본증권미상환잔액2["list"])
        조건부자본증권미상환잔액4 = 조건부자본증권미상환잔액3[
            [
                "corp_name",
                "remndr_exprtn1",
                "remndr_exprtn2",
                "yy1_below",
                "yy1_excess_yy2_below",
                "yy2_excess_yy3_below",
                "yy3_excess_yy4_below",
                "yy4_excess_yy5_below",
                "yy5_excess_yy10_below",
                "yy10_excess_yy20_below",
                "yy20_excess_yy30_below",
                "yy30_excess",
                "sm",
            ]
        ]
        조건부자본증권미상환잔액5 = 조건부자본증권미상환잔액4.rename(
            columns={
                "corp_name": "회사명",
                "remndr_exprtn1": "잔여만기",
                "remndr_exprtn2": "잔여만기",
                "yy1_below": "1년 이하",
                "yy1_excess_yy2_below": "1년초과 2년이하",
                "yy2_excess_yy3_below": "2년초과 3년이하",
                "yy3_excess_yy4_below": "3년초과 4년이하",
                "yy4_excess_yy5_below": "4년초과 5년이하",
                "yy5_excess_yy10_below": "5년초과 10년이하",
                "yy10_excess_yy20_below": "10년초과 20년이하",
                "yy20_excess_yy30_below": "20년초과 30년이하",
                "yy30_excess": "30년초과",
                "sm": "합계",
            }
        )
        # 조건부자본증권미상환잔액5=조건부자본증권미상환잔액5.set_index('회사명')
        return 조건부자본증권미상환잔액5

    def 미등기임원보수현황(self):
        미등기임원보수현황 = requests.get(
            f"https://opendart.fss.or.kr/api/unrstExctvMendngSttus.json?crtfc_key={self.crtfc_key}&corp_code={self.corp_code}&bsns_year={self.사업연도}&reprt_code={self.분기}"
        )
        미등기임원보수현황2 = 미등기임원보수현황.json()
        미등기임원보수현황3 = pd.DataFrame(미등기임원보수현황2["list"])
        미등기임원보수현황4 = 미등기임원보수현황3[
            ["corp_name", "se", "nmpr", "fyer_salary_totamt", "jan_salary_am", "rm"]
        ]
        미등기임원보수현황5 = 미등기임원보수현황4.rename(
            columns={
                "corp_name": "회사명",
                "se": "구분",
                "nmpr": "인원수",
                "fyer_salary_totamt": "연간급여총액",
                "jan_salary_am": "1인평균 급여액",
                "rm": "비고",
            }
        )
        # 미등기임원보수현황5=미등기임원보수현황5.set_index('회사명')
        return 미등기임원보수현황5

    def 회사채미상환잔액(self):
        회사채미상환잔액 = requests.get(
            f"https://opendart.fss.or.kr/api/cprndNrdmpBlce.json?crtfc_key={self.crtfc_key}\
                &corp_code={self.corp_code}&bsns_year={self.사업연도}&reprt_code={self.분기}"
        )
        회사채미상환잔액2 = 회사채미상환잔액.json()
        회사채미상환잔액3 = pd.DataFrame(회사채미상환잔액2["list"])
        회사채미상환잔액4 = 회사채미상환잔액3[
            [
                "corp_name",
                "remndr_exprtn1",
                "remndr_exprtn2",
                "yy1_below",
                "yy1_excess_yy2_below",
                "yy2_excess_yy3_below",
                "yy3_excess_yy4_below",
                "yy4_excess_yy5_below",
                "yy5_excess_yy10_below",
                "yy10_excess",
                "sm",
            ]
        ]
        회사채미상환잔액5 = 회사채미상환잔액4.rename(
            columns={
                "corp_name": "회사명",
                "remndr_exprtn1": "잔여만기",
                "remndr_exprtn2": "잔여만기",
                "yy1_below": "1년 이하",
                "yy1_excess_yy2_below": "1년초과 2년이하",
                "yy2_excess_yy3_below": "2년초과 3년이하",
                "yy3_excess_yy4_below": "3년초과 4년이하",
                "yy4_excess_yy5_below": "4년초과 5년이하",
                "yy5_excess_yy10_below": "5년초과 10년이하",
                "yy10_excess": "10년초과",
                "sm": "합계",
            }
        )
        # 회사채미상환잔액5=회사채미상환잔액5.set_index('회사명')
        return 회사채미상환잔액5

    def 단기사채미상환잔액(self):
        단기사채미상환잔액 = requests.get(
            f"https://opendart.fss.or.kr/api/srtpdPsndbtNrdmpBlce.json?crtfc_key=\
                {self.crtfc_key}&corp_code={self.corp_code}&bsns_year={self.사업연도}&reprt_code={self.분기}"
        )
        단기사채미상환잔액2 = 단기사채미상환잔액.json()
        단기사채미상환잔액3 = pd.DataFrame(단기사채미상환잔액2["list"])
        단기사채미상환잔액4 = 단기사채미상환잔액3[
            [
                "corp_name",
                "remndr_exprtn1",
                "remndr_exprtn2",
                "de10_below",
                "de10_excess_de30_below",
                "de30_excess_de90_below",
                "de90_excess_de180_below",
                "de180_excess_yy1_below",
                "sm",
                "isu_lmt",
                "remndr_lmt",
            ]
        ]
        단기사채미상환잔액5 = 단기사채미상환잔액4.rename(
            columns={
                "corp_name": "회사명",
                "remndr_exprtn1": "잔여만기",
                "remndr_exprtn2": "잔여만기",
                "de10_below": "10일 이하",
                "de10_excess_de30_below": "10일초과 30일이하",
                "de30_excess_de90_below": "30일초과 90일이하",
                "de90_excess_de180_below": "90일초과 180일이하",
                "de180_excess_yy1_below": "180일초과 1년이하",
                "sm": "합계",
                "isu_lmt": "발행 한도",
                "remndr_lmt": "잔여 한도",
            }
        )
        # 단기사채미상환잔액5=단기사채미상환잔액5.set_index('회사명')
        return 단기사채미상환잔액5

    def 기업어음증권미상환잔액(self):
        기업어음증권미상환잔액 = requests.get(
            f"https://opendart.fss.or.kr/api/entrprsBilScritsNrdmpBlce.json?crtfc_key=\
                {self.crtfc_key}&corp_code={self.corp_code}&bsns_year={self.사업연도}&reprt_code={self.분기}"
        )
        기업어음증권미상환잔액2 = 기업어음증권미상환잔액.json()
        기업어음증권미상환잔액3 = pd.DataFrame(기업어음증권미상환잔액2["list"])
        기업어음증권미상환잔액4 = 기업어음증권미상환잔액3[
            [
                "corp_name",
                "remndr_exprtn1",
                "remndr_exprtn2",
                "de10_below",
                "de10_excess_de30_below",
                "de30_excess_de90_below",
                "de90_excess_de180_below",
                "de180_excess_yy1_below",
                "yy1_excess_yy2_below",
                "yy2_excess_yy3_below",
                "yy3_excess",
                "sm",
            ]
        ]
        기업어음증권미상환잔액5 = 기업어음증권미상환잔액4.rename(
            columns={
                "corp_name": "회사명",
                "remndr_exprtn1": "잔여만기",
                "remndr_exprtn2": "잔여만기",
                "de10_below": "10일 이하",
                "de10_excess_de30_below": "10일초과 30일이하",
                "de30_excess_de90_below": "30일초과 90일이하",
                "de90_excess_de180_below": "90일초과 180일이하",
                "de180_excess_yy1_below": "180일초과 1년이하",
                "yy1_excess_yy2_below": "1년초과 2년이하",
                "yy2_excess_yy3_below": "2년초과 3년이하",
                "yy3_excess": "3년 초과",
                "sm": "합계",
            }
        )
        # 기업어음증권미상환잔액5=기업어음증권미상환잔액5.set_index('회사명')
        return 기업어음증권미상환잔액5

    def 채무증권발행실적(self):
        채무증권발행실적 = requests.get(
            f"https://opendart.fss.or.kr/api/detScritsIsuAcmslt.json?crtfc_key=\
                {self.crtfc_key}&corp_code={self.corp_code}&bsns_year={self.사업연도}&reprt_code={self.분기}"
        )
        채무증권발행실적2 = 채무증권발행실적.json()
        채무증권발행실적3 = pd.DataFrame(채무증권발행실적2["list"])
        채무증권발행실적4 = 채무증권발행실적3[
            [
                "corp_name",
                "isu_cmpny",
                "scrits_knd_nm",
                "isu_mth_nm",
                "isu_de",
                "facvalu_totamt",
                "intrt",
                "evl_grad_instt",
                "mtd",
                "repy_at",
                "mngt_cmpny",
            ]
        ]
        채무증권발행실적5 = 채무증권발행실적4.rename(
            columns={
                "corp_name": "회사명",
                "isu_cmpny": "발행회사",
                "scrits_knd_nm": "증권종류",
                "isu_mth_nm": "발행방법",
                "isu_de": "발행일자",
                "facvalu_totamt": "권면(전자등록)총액",
                "intrt": "이자율",
                "evl_grad_instt": "평가등급(평가기관)",
                "mtd": "만기일",
                "repy_at": "상환여부",
                "mngt_cmpny": "주관회사",
            }
        )
        return 채무증권발행실적5

    def 사모자금의사용내역(self):

        사모자금의사용내역 = requests.get(
            f"https://opendart.fss.or.kr/api/prvsrpCptalUseDtls.json?crtfc_key={self.crtfc_key}&corp_code={self.corp_code}&bsns_year={self.사업연도}&reprt_code={self.분기}"
        )
        사모자금의사용내역2 = 사모자금의사용내역.json()
        사모자금의사용내역3 = pd.DataFrame(사모자금의사용내역2["list"])
        사모자금의사용내역4 = 사모자금의사용내역3[
            [
                "corp_name",
                "se_nm",
                "tm",
                "pay_de",
                "pay_amount",
                "cptal_use_plan",
                "real_cptal_use_sttus",
                "mtrpt_cptal_use_plan_useprps",
                "mtrpt_cptal_use_plan_prcure_amount",
                "real_cptal_use_dtls_cn",
                "real_cptal_use_dtls_amount",
                "dffrnc_occrrnc_resn",
            ]
        ]
        사모자금의사용내역5 = 사모자금의사용내역4.rename(
            columns={
                "corp_name": "회사명",
                "se_nm": "구분",
                "tm": "회차",
                "pay_de": "납입일",
                "pay_amount": "납입금액",
                "cptal_use_plan": "자금사용 계획",
                "real_cptal_use_sttus": "실제 자금사용 현황",
                "mtrpt_cptal_use_plan_useprps": "자금사용 계획(사용용도)",
                "mtrpt_cptal_use_plan_prcure_amount": "자금사용 계획(조달금액)",
                "real_cptal_use_dtls_cn": "실제자금사용내역(내용)",
                "real_cptal_use_dtls_amount": "실제자금사용내역(금액)",
                "dffrnc_occrrnc_resn": "차이발생사유",
            }
        )
        return 사모자금의사용내역5

    def 공모자금의사용내역(self):
        공모자금의사용내역 = requests.get(
            f"https://opendart.fss.or.kr/api/pssrpCptalUseDtls.json?crtfc_key={self.crtfc_key}&corp_code={self.corp_code}&bsns_year={self.사업연도}&reprt_code={self.분기}"
        )
        공모자금의사용내역2 = 공모자금의사용내역.json()
        공모자금의사용내역3 = pd.DataFrame(공모자금의사용내역2["list"])
        공모자금의사용내역4 = 공모자금의사용내역3[
            [
                "corp_name",
                "se_nm",
                "tm",
                "pay_de",
                "pay_amount",
                "on_dclrt_cptal_use_plan",
                "real_cptal_use_sttus",
                "rs_cptal_use_plan_useprps",
                "rs_cptal_use_plan_prcure_amount",
                "real_cptal_use_dtls_cn",
                "real_cptal_use_dtls_amount",
                "dffrnc_occrrnc_resn",
            ]
        ]
        공모자금의사용내역5 = 공모자금의사용내역4.rename(
            columns={
                "corp_name": "회사명",
                "se_nm": "구분",
                "tm": "회차",
                "pay_de": "납입일",
                "pay_amount": "납입금액",
                "on_dclrt_cptal_use_plan": "신고서상 자금사용 계획",
                "real_cptal_use_sttus": "실제 자금사용 현황",
                "rs_cptal_use_plan_useprps": "증권신고서 등의 자금사용 계획(사용용도)",
                "rs_cptal_use_plan_prcure_amount": "증권신고서 등의 자금사용 계획(조달금액)",
                "real_cptal_use_dtls_cn": "실제 자금사용 내역(내용)",
                "real_cptal_use_dtls_amount": "실제 자금사용 내역(금액)",
                "dffrnc_occrrnc_resn": "차이발생 사유 등",
            }
        )
        return 공모자금의사용내역5

    # 주식의 총수 현황
    def 주식의총수현황(self):

        주식의총수현황 = requests.get(
            f"	https://opendart.fss.or.kr/api/stockTotqySttus.json?crtfc_key={self.crtfc_key}&corp_code={self.corp_code}&bsns_year={self.사업연도}&reprt_code={self.분기}"
        )
        주식의총수현황2 = 주식의총수현황.json()
        주식의총수현황3 = pd.DataFrame(주식의총수현황2["list"])
        주식의총수현황4 = 주식의총수현황3[
            [
                "se",
                "isu_stock_totqy",
                "now_to_isu_stock_totqy",
                "now_to_dcrs_stock_totqy",
                "redc",
                "profit_incnr",
                "rdmstk_repy",
                "etc",
                "istc_totqy",
                "tesstk_co",
                "distb_stock_co",
            ]
        ]
        주식의총수현황5 = 주식의총수현황4.rename(
            columns={
                "se": "구분",
                "isu_stock_totqy": "발행할 주식의 총수",
                "now_to_isu_stock_totqy": "현재까지 발행한 주식의 총수",
                "now_to_dcrs_stock_totqy": "현재까지 감소한 주식의 총수",
                "redc": "감자",
                "profit_incnr": "이익소각",
                "rdmstk_repy": "상환주식의 상환",
                "etc": "기타",
                "istc_totqy": "발행주식의 총수",
                "tesstk_co": "자기주식수",
                "distb_stock_co": "유통주식수",
            }
        )

        return 주식의총수현황5

    # 회계감사인의 명칭 및 감사의견
    def 회계감사인의명칭및감사의견(self):
        회계감사인의명칭및감사의견 = requests.get(
            f"https://opendart.fss.or.kr/api/accnutAdtorNmNdAdtOpinion.json?crtfc_key={self.crtfc_key}&corp_code={self.corp_code}&bsns_year={self.사업연도}&reprt_code={self.분기}"
        )
        회계감사인의명칭및감사의견2 = 회계감사인의명칭및감사의견.json()
        회계감사인의명칭및감사의견3 = pd.DataFrame(회계감사인의명칭및감사의견2["list"])
        회계감사인의명칭및감사의견4 = 회계감사인의명칭및감사의견3[
            [
                "bsns_year",
                "adtor",
                "adt_opinion",
                "adt_reprt_spcmnt_matter",
                "emphs_matter",
                "core_adt_matter",
            ]
        ]
        회계감사인의명칭및감사의견5 = 회계감사인의명칭및감사의견4.rename(
            columns={
                "bsns_year": "사업연도",
                "adtor": "감사인",
                "adt_opinion": "감사의견",
                "adt_reprt_spcmnt_matter": "감사보고서 특기사항",
                "emphs_matter": "강조사항 ",
                "core_adt_matter": "핵심감사사항",
            }
        )
        return 회계감사인의명칭및감사의견5

    # 감사용역체결현황
    def 감사용역체결현황(self):
        감사용역체결현황 = requests.get(
            f"https://opendart.fss.or.kr/api/adtServcCnclsSttus.json?crtfc_key={self.crtfc_key}&corp_code={self.corp_code}&bsns_year={self.사업연도}&reprt_code={self.분기}"
        )
        감사용역체결현황2 = 감사용역체결현황.json()
        감사용역체결현황3 = pd.DataFrame(감사용역체결현황2["list"])
        감사용역체결현황4 = 감사용역체결현황3[
            [
                "bsns_year",
                "adtor",
                "cn",
                "mendng",
                "tot_reqre_time",
                "adt_cntrct_dtls_mendng",
                "adt_cntrct_dtls_time",
                "real_exc_dtls_mendng",
                "real_exc_dtls_time",
            ]
        ]
        감사용역체결현황5 = 감사용역체결현황4.rename(
            columns={
                "bsns_year": "사업연도",
                "adtor": "감사인",
                "cn": "내용",
                "mendng": "보수",
                "tot_reqre_time": "총소요시간",
                "adt_cntrct_dtls_mendng": "감사계약내역(보수)",
                "adt_cntrct_dtls_time": "감사계약내역(시간)",
                "real_exc_dtls_mendng": "실제수행내역(보수)",
                "real_exc_dtls_time": "실제수행내역(시간)",
            }
        )
        return 감사용역체결현황5

    # 회계감사인과의 비감사용역 계약체결 현황
    def 회계감사인과의비감사용역계약체결현황(self):
        회계감사인과의비감사용역계약체결현황 = requests.get(
            f"https://opendart.fss.or.kr/api/accnutAdtorNonAdtServcCnclsSttus.json?crtfc_key={self.crtfc_key}&corp_code={self.corp_code}&bsns_year={self.사업연도}&reprt_code={self.분기}"
        )
        회계감사인과의비감사용역계약체결현황 = 회계감사인과의비감사용역계약체결현황.json()
        회계감사인과의비감사용역계약체결현황 = pd.DataFrame(회계감사인과의비감사용역계약체결현황["list"])
        회계감사인과의비감사용역계약체결현황 = 회계감사인과의비감사용역계약체결현황[
            [
                "bsns_year",
                "cntrct_cncls_de",
                "servc_cn",
                "servc_exc_pd",
                "servc_mendng",
                "rm",
            ]
        ]
        회계감사인과의비감사용역계약체결현황 = 회계감사인과의비감사용역계약체결현황.rename(
            columns={
                "bsns_year": "사업연도",
                "cntrct_cncls_de": "계약체결일",
                "servc_cn": "용역내용",
                "servc_exc_pd": "용역수행기간",
                "servc_mendng": "용역보수",
                "rm": "비고",
            }
        )
        return 회계감사인과의비감사용역계약체결현황

    # 사외이사 및 그 변동현황
    def 사외이사및변동현황(self):
        사외이사및변동현황 = requests.get(
            f"https://opendart.fss.or.kr/api/outcmpnyDrctrNdChangeSttus.json?crtfc_key={self.crtfc_key}&corp_code={self.corp_code}&bsns_year={self.사업연도}&reprt_code={self.분기}"
        )
        사외이사및변동현황 = 사외이사및변동현황.json()
        사외이사및변동현황 = pd.DataFrame(사외이사및변동현황["list"])
        사외이사및변동현황 = 사외이사및변동현황[
            [
                "corp_name",
                "drctr_co",
                "otcmp_drctr_co",
                "apnt",
                "rlsofc",
                "mdstrm_resig",
            ]
        ]
        사외이사및변동현황 = 사외이사및변동현황.rename(
            columns={
                "corp_name": "회사명",
                "drctr_co": "이사의 수",
                "otcmp_drctr_co": "사외이사 수",
                "apnt": "사외이사 변동현황(선임)",
                "rlsofc": "사외이사 변동현황(해임)",
                "mdstrm_resig": "사외이사 변동현황(중도퇴임)",
            }
        )

        return 사외이사및변동현황

    # 신종자본증권 미상환 잔액
    def 신종자본증권미상환잔액(self):

        사외이사및변동현황 = requests.get(
            f"https://opendart.fss.or.kr/api/newCaplScritsNrdmpBlce.json?crtfc_key={self.crtfc_key}&corp_code={self.corp_code}&bsns_year={self.사업연도}&reprt_code={self.분기}"
        )
        사외이사및변동현황 = 사외이사및변동현황.json()
        사외이사및변동현황 = pd.DataFrame(사외이사및변동현황["list"])
        사외이사및변동현황 = 사외이사및변동현황[
            [
                "corp_name",
                "remndr_exprtn1",
                "remndr_exprtn2",
                "yy1_below",
                "yy1_excess_yy5_below",
                "yy5_excess_yy10_below",
                "yy10_excess_yy15_below",
                "yy15_excess_yy20_below",
                "yy20_excess_yy30_below",
                "yy30_excess",
                "sm",
            ]
        ]
        사외이사및변동현황 = 사외이사및변동현황.rename(
            columns={
                "corp_name": "회사명",
                "remndr_exprtn1": "잔여만기",
                "remndr_exprtn2": "잔여만기2",
                "yy1_below": "1년 이하",
                "yy1_excess_yy5_below": "1년초과 5년이하",
                "yy5_excess_yy10_below": "5년초과 10년이하",
                "yy10_excess_yy15_below": "10년초과 15년이하",
                "yy15_excess_yy20_below": "15년초과 20년이하",
                "yy20_excess_yy30_below": "20년초과 30년이하",
                "yy30_excess": "30년초과",
                "sm": "합계",
            }
        )

        return 사외이사및변동현황

    def 증자감자_현황(self):
        증자_감자_현황 = requests.get(
            f"https://opendart.fss.or.kr/api/irdsSttus.json?crtfc_key={self.crtfc_key}&corp_code={self.corp_code}&bsns_year={self.사업연도}&reprt_code={self.분기}"
        )
        증자_감자_현황2 = 증자_감자_현황.json()
        증자_감자_현황3 = pd.DataFrame(증자_감자_현황2["list"])
        증자_감자_현황4 = 증자_감자_현황3[
            [
                "isu_dcrs_de",
                "isu_dcrs_stle",
                "isu_dcrs_stock_knd",
                "isu_dcrs_qy",
                "isu_dcrs_mstvdv_fval_amount",
                "isu_dcrs_mstvdv_amount",
            ]
        ]
        증자_감자_현황5 = 증자_감자_현황4.rename(
            columns={
                "isu_dcrs_de": "주식발행일자",
                "isu_dcrs_stle": "발행형태",
                "isu_dcrs_stock_knd": "주식종류",
                "isu_dcrs_qy": "수량",
                "isu_dcrs_mstvdv_fval_amount": "주당 액면 가액",
                "isu_dcrs_mstvdv_amount": "주당 가액",
            }
        )

        return 증자_감자_현황5

    def 배당(self):
        배당 = requests.get(
            f"https://opendart.fss.or.kr/api/alotMatter.json?crtfc_key={self.crtfc_key}&corp_code={self.corp_code}&bsns_year={self.사업연도}&reprt_code={self.분기}"
        )
        배당2 = 배당.json()
        배당3 = pd.DataFrame(배당2["list"])
        배당4 = 배당3.rename(
            columns={"se": "구분", "thstrm": "당기", "frmtrm": "전기", "lwfr": "전전기"}
        )
        배당5 = 배당4[["구분", "당기", "전기", "전전기"]]

        return 배당5

    # 자기주식 취득 및 처분 현황
    def 자기주식(self):
        자기주식 = requests.get(
            f"https://opendart.fss.or.kr/api/tesstkAcqsDspsSttus.json?crtfc_key={self.crtfc_key}&corp_code={self.corp_code}&bsns_year={self.사업연도}&reprt_code={self.분기}"
        )
        자기주식2 = 자기주식.json()
        자기주식3 = pd.DataFrame(자기주식2["list"])

        자기주식3 = 자기주식3[
            [
                "stock_knd",
                "acqs_mth1",
                "acqs_mth2",
                "acqs_mth3",
                "bsis_qy",
                "change_qy_acqs",
                "change_qy_dsps",
                "change_qy_incnr",
                "trmend_qy",
                "rm",
            ]
        ]
        자기주식4 = 자기주식3.rename(
            columns={
                "stock_knd": "주식종류",
                "acqs_mth1": "대분류",
                "acqs_mth2": "중분류",
                "acqs_mth3": "소분류",
                "bsis_qy": "기초수량",
                "change_qy_acqs": "변동수량취득",
                "change_qy_dsps": "변동수량처분",
                "change_qy_incnr": "변동수량소각",
                "trmend_qy": "기말수량",
                "rm": "비고",
            }
        )
        return 자기주식4

    # 최대주주 현황
    def 최대주주현황(self):
        최대주주 = requests.get(
            f"https://opendart.fss.or.kr/api/hyslrSttus.json?crtfc_key={self.crtfc_key}&corp_code={self.corp_code}&bsns_year={self.사업연도}&reprt_code={self.분기}"
        )
        최대주주2 = 최대주주.json()
        최대주주3 = pd.DataFrame(최대주주2["list"])
        최대주주3 = 최대주주3[
            [
                "stock_knd",
                "rm",
                "nm",
                "relate",
                "bsis_posesn_stock_co",
                "bsis_posesn_stock_qota_rt",
                "trmend_posesn_stock_co",
                "trmend_posesn_stock_qota_rt",
            ]
        ]
        최대주주4 = 최대주주3.rename(
            columns={
                "stock_knd": "주식종류",
                "nm": "성명",
                "relate": "관계",
                "bsis_posesn_stock_co": "기초소유주식수",
                "bsis_posesn_stock_qota_rt": "기초소유주식지분율",
                "trmend_posesn_stock_co": "기말소유주식수",
                "trmend_posesn_stock_qota_rt": "기말소유주식지분율",
                "rm": "비고",
            }
        )

        return 최대주주4

    # 최대주주변동현황
    def 최대주주변동(self):
        최대주주변동 = requests.get(
            f"https://opendart.fss.or.kr/api/hyslrChgSttus.json?crtfc_key={self.crtfc_key}&corp_code={self.corp_code}&bsns_year={self.사업연도}&reprt_code={self.분기}"
        )
        최대주주변동2 = 최대주주변동.json()
        최대주주변동3 = pd.DataFrame(최대주주변동2["list"])
        최대주주변동3 = 최대주주변동3[
            [
                "change_on",
                "mxmm_shrholdr_nm",
                "posesn_stock_co",
                "qota_rt",
                "change_cause",
                "rm",
            ]
        ]
        최대주주변동4 = 최대주주변동3.rename(
            columns={
                "change_on": "변동일",
                "mxmm_shrholdr_nm": "최대주주명",
                "posesn_stock_co": "소유주식수",
                "qota_rt": "지분율",
                "change_cause": "변동원인",
                "rm": "비고",
            }
        )
        # 최대주주변동4=최대주주변동4.set_index('변동일')
        return 최대주주변동4

    # 소액주주현황
    def 소액주주현황(self):
        최대주주변동 = requests.get(
            f"https://opendart.fss.or.kr/api/mrhlSttus.json?crtfc_key={self.crtfc_key}&corp_code={self.corp_code}&bsns_year={self.사업연도}&reprt_code={self.분기}"
        )
        최대주주변동2 = 최대주주변동.json()
        최대주주변동3 = pd.DataFrame(최대주주변동2["list"])
        최대주주변동3 = 최대주주변동3[
            [
                "se",
                "shrholdr_co",
                "shrholdr_tot_co",
                "shrholdr_rate",
                "hold_stock_co",
                "stock_tot_co",
                "hold_stock_rate",
            ]
        ]
        최대주주변동4 = 최대주주변동3.rename(
            columns={
                "se": "구분",
                "shrholdr_co": "주주수",
                "shrholdr_tot_co": "전체주주수",
                "shrholdr_rate": "주주비율",
                "hold_stock_co": "보유주식수",
                "stock_tot_co": "총발행주식수",
                "hold_stock_rate": "보유주식비율",
            }
        )

        return 최대주주변동4

    # 임원현황
    def 임원현황(self):

        임원현황 = requests.get(
            f"https://opendart.fss.or.kr/api/exctvSttus.json?crtfc_key={self.crtfc_key}\
                &corp_code={self.corp_code}&bsns_year={self.사업연도}&reprt_code={self.분기}"
        )
        임원현황 = 임원현황.json()
        임원현황 = pd.DataFrame(임원현황["list"])
        임원현황 = 임원현황[["nm", "ofcps", "chrg_job", "main_career", "mxmm_shrholdr_relate"]]
        임원현황 = 임원현황.rename(
            columns={
                "nm": "성명",
                "ofcps": "직위",
                "chrg_job": "담당업무",
                "main_career": "주요경력",
                "mxmm_shrholdr_relate": "최대주주관계",
            }
        )
        return 임원현황

    # 직원현황
    def 직원현황(self):

        직원현황 = requests.get(
            f"https://opendart.fss.or.kr/api/empSttus.json?crtfc_key=\
                {self.crtfc_key}&corp_code={self.corp_code}&bsns_year={self.사업연도}&reprt_code={self.분기}"
        )
        직원현황 = 직원현황.json()
        직원현황 = pd.DataFrame(직원현황["list"])
        직원현황 = 직원현황[
            [
                "sexdstn",
                "fo_bbm",
                "rgllbr_co",
                "rgllbr_abacpt_labrr_co",
                "cnttk_co",
                "cnttk_abacpt_labrr_co",
                "sm",
                "avrg_cnwk_sdytrn",
                "fyer_salary_totamt",
                "jan_salary_am",
                "rm",
            ]
        ]
        직원현황 = 직원현황.rename(
            columns={
                "sexdstn": "성별",
                "fo_bbm": "사업부문",
                "rgllbr_co": "정규직수",
                "rgllbr_abacpt_labrr_co": "정규직단시간근로자수",
                "cnttk_co": "계약직수",
                "cnttk_abacpt_labrr_co": "계약직단시간근로자수",
                "sm": "합계",
                "avrg_cnwk_sdytrn": "평균근속연수",
                "fyer_salary_totamt": "연간급여총액",
                "jan_salary_am": "1인평균급여액",
                "rm": "비고",
            }
        )

        return 직원현황

    # 이사·감사의 개인별 보수 현황
    def 이사감사개인별보수현황(self):

        이사감사 = requests.get(
            f"https://opendart.fss.or.kr/api/hmvAuditIndvdlBySttus.json?crtfc_key=\
                {self.crtfc_key}&corp_code={self.corp_code}&bsns_year={self.사업연도}&reprt_code={self.분기}"
        )
        이사감사 = 이사감사.json()
        이사감사 = pd.DataFrame(이사감사["list"])
        이사감사 = 이사감사[["nm", "ofcps", "mendng_totamt", "mendng_totamt_ct_incls_mendng"]]
        이사감사 = 이사감사.rename(
            columns={
                "nm": "이름",
                "ofcps": "직위",
                "mendng_totamt": "보수총액",
                "mendng_totamt_ct_incls_mendng": "보수총액 비포함보수",
            }
        )

        return 이사감사

    # 이사ㆍ감사의 전체의 보수 현황
    def 이사감사전체의보수현황(self):

        이사감사 = requests.get(
            f"https://opendart.fss.or.kr/api/hmvAuditAllSttus.json?crtfc_key=\
                {self.crtfc_key}&corp_code={self.corp_code}&bsns_year={self.사업연도}&reprt_code={self.분기}"
        )
        이사감사 = 이사감사.json()
        이사감사 = pd.DataFrame(이사감사["list"])
        이사감사 = 이사감사[["nmpr", "jan_avrg_mendng_am", "mendng_totamt", "rm"]]
        이사감사 = 이사감사.rename(
            columns={
                "nmpr": "인원수",
                "jan_avrg_mendng_am": "보수총액",
                "mendng_totamt": "1인평균보수액",
                "rm": "비고",
            }
        )

        return 이사감사

    # 개인별 보수지급 금액(5억이상 상위5인)
    def 고액연봉자(self):
        고액연봉 = requests.get(
            f"https://opendart.fss.or.kr/api/indvdlByPay.json?crtfc_key=\
                {self.crtfc_key}&corp_code={self.corp_code}&bsns_year={self.사업연도}&reprt_code={self.분기}"
        )
        고액연봉 = 고액연봉.json()
        고액연봉 = pd.DataFrame(고액연봉["list"])
        고액연봉 = 고액연봉[["nm", "ofcps", "mendng_totamt", "mendng_totamt_ct_incls_mendng"]]
        고액연봉 = 고액연봉.rename(
            columns={
                "nm": "이름",
                "ofcps": "직위",
                "mendng_totamt": "보수총액",
                "mendng_totamt_ct_incls_mendng": "보수총액 비 포함보수",
            }
        )

        return 고액연봉

    # 타법인출자현황
    def 타법인출자현황(self):

        타법인출자현황 = requests.get(
            f"https://opendart.fss.or.kr/api/otrCprInvstmntSttus.json?crtfc_key=\
                {self.crtfc_key}&corp_code={self.corp_code}&bsns_year={self.사업연도}&reprt_code={self.분기}"
        )
        타법인출자현황 = 타법인출자현황.json()
        타법인출자현황 = pd.DataFrame(타법인출자현황["list"])
        타법인출자현황 = 타법인출자현황[
            [
                "inv_prm",
                "frst_acqs_de",
                "invstmnt_purps",
                "frst_acqs_amount",
                "bsis_blce_qy",
                "bsis_blce_qota_rt",
                "bsis_blce_acntbk_amount",
                "incrs_dcrs_acqs_dsps_qy",
                "incrs_dcrs_acqs_dsps_amount",
                "incrs_dcrs_evl_lstmn",
                "trmend_blce_qy",
                "trmend_blce_qota_rt",
                "trmend_blce_acntbk_amount",
                "recent_bsns_year_fnnr_sttus_tot_assets",
                "recent_bsns_year_fnnr_sttus_thstrm_ntpf",
            ]
        ]
        타법인출자현황 = 타법인출자현황.rename(
            columns={
                "inv_prm": "법인명",
                "frst_acqs_de": "최초취득일자",
                "invstmnt_purps": "출자목적",
                "frst_acqs_amount": "최초취득금액",
                "bsis_blce_qy": "기초잔액수량",
                "bsis_blce_qota_rt": "기초잔액지분율",
                "bsis_blce_acntbk_amount": "기초잔액장부가액",
                "incrs_dcrs_acqs_dsps_qy": "증가감소 취득처분 수량",
                "incrs_dcrs_acqs_dsps_amount": "증가감소 취득처분금액",
                "incrs_dcrs_evl_lstmn": "증가감소 평가손액",
                "trmend_blce_qy": "기말잔액수량",
                "trmend_blce_qota_rt": "기말잔액지분율",
                "trmend_blce_acntbk_amount": "기말잔액장부가액",
                "recent_bsns_year_fnnr_sttus_tot_assets": "최근사업연도 재무현황 총자산",
                "recent_bsns_year_fnnr_sttus_thstrm_ntpf": "최근사업연도 재무현황 당기순이익",
            }
        )

        return 타법인출자현황

    # 대량보유상황보고
    def 대량보유상황보고(self):
        대량보유 = requests.get(
            f"https://opendart.fss.or.kr/api/majorstock.json?crtfc_key={self.crtfc_key}&corp_code={self.corp_code}"
        )
        대량보유 = 대량보유.json()
        대량보유 = pd.DataFrame(대량보유["list"])
        대량보유 = 대량보유[
            [
                "report_tp",
                "repror",
                "stkqy",
                "stkqy_irds",
                "stkrt",
                "stkrt_irds",
                "ctr_stkqy",
                "ctr_stkrt",
                "report_resn",
            ]
        ]
        대량보유 = 대량보유.rename(
            columns={
                "report_tp": "보고구분",
                "repror": "대표보고자",
                "stkqy": "보유주식 수",
                "stkqy_irds": "보유주식 증감",
                "stkrt": "보유비율",
                "stkrt_irds": "보유비율 증감",
                "ctr_stkqy": "주요체결주식 수",
                "ctr_stkrt": "주요체결 보유비율",
                "report_resn": "보고사유",
            }
        )

        return 대량보유

    # 임원주요주주소유보고
    def 임원주요주주소유보고(self):
        임원주요주주소유보고 = requests.get(
            f"https://opendart.fss.or.kr/api/elestock.json?crtfc_key={self.crtfc_key}&corp_code={self.corp_code}"
        )
        임원주요주주소유보고 = 임원주요주주소유보고.json()
        임원주요주주소유보고 = pd.DataFrame(임원주요주주소유보고["list"])
        임원주요주주소유보고 = 임원주요주주소유보고[
            [
                "repror",
                "isu_exctv_rgist_at",
                "isu_exctv_ofcps",
                "isu_main_shrholdr",
                "sp_stock_lmp_cnt",
                "sp_stock_lmp_irds_cnt",
                "sp_stock_lmp_rate",
                "sp_stock_lmp_irds_rate",
            ]
        ]
        임원주요주주소유보고 = 임원주요주주소유보고.rename(
            columns={
                "repror": "보고자",
                "isu_exctv_rgist_at": "발행회사관계임원(등기여부)",
                "isu_exctv_ofcps": "발행회사관계임원직위",
                "isu_main_shrholdr": "발행회사관계주요주주",
                "sp_stock_lmp_cnt": "특정증권등소유수",
                "sp_stock_lmp_irds_cnt": "특정증권등소유증감",
                "sp_stock_lmp_rate": "특정증권등소유비율",
                "sp_stock_lmp_irds_rate": "특정증권등소유증감비율",
            }
        )
        return 임원주요주주소유보고
