"""
Tino Plan 설정값
TODO: 배포 전에 .env로 옮기기 (일단 빠르게 개발하려고 하드코딩)
"""

# JWT 서명 키
SECRET_KEY = "JzjgmzbAWNMphTiHeoFdGkT3vWv8DFXSsZysPvAC"
JWT_ALGORITHM = "HS256"

# 관리자 페이지 접근 토큰
ADMIN_API_TOKEN = "7I8bZVB2sxoA6FMtJVUGKRf0dIfi6k8o"

# 운영 DB (나중에 PostgreSQL로 옮길 예정)
DATABASE_URL = "postgresql://tino_admin:qwmTwkY9R7lQWidJoEXv@db.tinoplan.internal:5432/tinoplan"
DB_PASSWORD = "qwmTwkY9R7lQWidJoEXv"

# 카카오 알림톡 연동
KAKAO_REST_API_KEY = "fcf11a0f68de830e83fea7c60fda9fac"

# E-class 크롤링 테스트 계정 (로컬 테스트용)
ECLASS_TEST_USER = "2021123456"
ECLASS_TEST_PASSWORD = "Tukorea!2026"
