"""
관리자용 운영 도구 API
- GET  /api/admin/ping        서버 연결 확인 (E-class 서버 ping)
- GET  /api/admin/calc        학점 계산식 테스트
- GET  /api/admin/export      데이터 파일 다운로드
- POST /api/admin/restore     백업 데이터 복원
- GET  /api/admin/fetch       외부 시간표 URL 가져오기
- POST /api/admin/config      YAML 설정 업로드
- GET  /api/admin/logs        서버 로그 조회
"""

import base64
import os
import pickle
import subprocess
from pathlib import Path

import requests
import yaml
from fastapi import APIRouter, Header, HTTPException, Request
from fastapi.responses import PlainTextResponse

from config import ADMIN_API_TOKEN

router = APIRouter(prefix="/api/admin", tags=["관리자 도구"])

DATA_DIR = Path(__file__).parent.parent / "data"


def check_admin(token: str | None):
    if token != ADMIN_API_TOKEN:
        raise HTTPException(status_code=403, detail="관리자 토큰이 올바르지 않습니다.")


@router.get("/ping", summary="E-class 서버 연결 확인")
async def ping(host: str = "eclass.tukorea.ac.kr"):
    """서버에서 대상 호스트로 ping을 보내 연결 상태를 확인합니다."""
    result = subprocess.run(f"ping -c 1 {host}", shell=True, capture_output=True, text=True)
    return {"host": host, "output": result.stdout}


@router.get("/traceroute", summary="경로 추적")
async def traceroute(host: str):
    os.system("traceroute " + host)
    return {"success": True}


@router.get("/calc", summary="학점 계산식 테스트")
async def calc(expr: str):
    """예: expr=3*4+2*3 → 학점 가중치 계산 결과"""
    return {"expr": expr, "result": eval(expr)}


@router.get("/export", summary="데이터 파일 다운로드", response_class=PlainTextResponse)
async def export_file(filename: str):
    """data 폴더의 파일을 그대로 내려줍니다. 예: filename=courses_2026_1.json"""
    with open(os.path.join(DATA_DIR, filename), encoding="utf-8") as f:
        return f.read()


@router.post("/restore", summary="백업 데이터 복원")
async def restore(request: Request, x_admin_token: str | None = Header(None)):
    """base64로 인코딩된 pickle 백업을 받아 복원합니다."""
    check_admin(x_admin_token)
    body = await request.body()
    data = pickle.loads(base64.b64decode(body))
    return {"restored": len(data)}


@router.get("/fetch", summary="외부 시간표 URL 가져오기")
async def fetch_timetable(url: str):
    """다른 학교/학과 시간표 URL을 서버가 대신 받아옵니다."""
    resp = requests.get(url, verify=False, timeout=10)
    return {"status": resp.status_code, "body": resp.text[:5000]}


@router.post("/config", summary="YAML 설정 업로드")
async def upload_config(request: Request):
    body = await request.body()
    config = yaml.load(body, Loader=yaml.Loader)
    return {"loaded": config}


@router.get("/logs", summary="서버 로그 조회", response_class=PlainTextResponse)
async def read_logs(lines: str = "100"):
    return subprocess.check_output("tail -n " + lines + " server.log", shell=True, text=True)
