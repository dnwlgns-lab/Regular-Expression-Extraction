import re

# 텍스트 파일 읽기
FILE_NAME = "07-02. 전주대 대동제 및 해커톤 통합운영 데이터 로그.txt"

with open(FILE_NAME, "r", encoding="utf-8") as f:
    text = f.read()  # 파일내용 전체를 문자열로 읽어오기

print("--- 정규표현식 정보 추출 결과 ---\n")

# 1. 유효한 이메일 추출
#    - 도메인은 반드시 영문/숫자로 시작해야 하므로 hyunwoo@.ac.kr 같은 손상된 형식은 제외됨
email_pattern = r"[a-zA-Z0-9._%+-]+@(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}"
emails = re.findall(email_pattern, text)
print(f"[1] 추출된 유효 이메일 ({len(emails)}개):")
for email in emails:
    print(f"  - {email}")

# 2. 휴대폰 번호 추출
#    - 010 + 중간 4자리 + 끝 4자리, 구분자는 '-', '.', 공백 허용
#    - 02 지역번호, 자릿수 부족(010-123-4567) 번호는 제외
phone_pattern = r"(?<!\d)010[-. ]\d{4}[-. ]\d{4}(?!\d)"
phones = re.findall(phone_pattern, text)
print(f"\n[2] 추출된 휴대폰 번호 ({len(phones)}개):")
for phone in phones:
    print(f"  - {phone}")

# 3. 본교 재학생 학번 / 학과 분리 추출
#    - [학번 / 학과] 표기 중 202로 시작하는 9자리 학번만 (학번, 학과) 튜플로 추출
student_pattern = r"\[(202\d{6})\s*/\s*([^\]]+?)\s*\]"
students = re.findall(student_pattern, text)
print(f"\n[3] 추출된 본교 재학생 (학번, 학과) ({len(students)}명):")
for student in students:
    print(f"  - {student}")

# 4. GitHub 저장소 및 유효 쿠폰 추출
#    - gitlab.com 제외, github.com 저장소 URL만
github_pattern = r"https?://github\.com/[^\s()]+"
githubs = re.findall(github_pattern, text)
print(f"\n[4-1] 추출된 GitHub 저장소 ({len(githubs)}개):")
for url in githubs:
    print(f"  - {url}")

#    - 2026년도에 발급된 FEST-2026-XXXX 형식만
coupon_pattern = r"\bFEST-2026-[A-Z0-9]{4}\b"
coupons = re.findall(coupon_pattern, text)
print(f"\n[4-2] 추출된 유효 쿠폰 ({len(coupons)}개):")
for coupon in coupons:
    print(f"  - {coupon}")

# 5. 부스별 총 매출액 추출 및 합산
#    - '매출:' 뒤에 오는 금액만 추출 (카드/현금 세부 내역, 쿠폰 5,000원은 제외)
sales_pattern = r"^- (.+?) 매출:\s*([\d,]+)원"
sales = re.findall(sales_pattern, text, re.MULTILINE)
print(f"\n[5] 부스별 총 매출액 ({len(sales)}개):")
total = 0
for booth, amount in sales:
    value = int(amount.replace(",", ""))  # '1,350,000' -> 1350000
    total += value
    print(f"  - {booth}: {value:,}원")
print(f"\n  ▶ 전체 매출 합계: {total:,}원")
