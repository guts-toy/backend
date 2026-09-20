from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from core.clients import http_client
from datetime import datetime, timezone, timedelta
import json

# Weather API
router = APIRouter(prefix="/weather", tags=["weather"])


# 날씨 검색 테스트 API
@router.get("/test")
async def test(appid: str, area: str):
    try:
        if area == '서울':
            area = "Seoul,kr"
        elif area == '런던':
            area = "London,uk"
        else:
            return {"response": "해당 지역을 찾을수 없습니다. 런던, 서울만 가능"}

        url = f"https://api.openweathermap.org/data/2.5/weather?q={area}&APPID={appid}&lang=kr&units=metric"
        response = await http_client.client.get(url)
        response_json = json.load(response)

        # 한국 시간대(UTC+9) 정의
        KST = timezone(timedelta(hours=9))

        # KST 기준으로 날씨 형식 수정
        sunrise = datetime.fromtimestamp(response_json.get('sys').get('sunrise'), tz = KST).strftime('%X')
        sunset  = datetime.fromtimestamp(response_json.get('sys').get('sunset'), tz = KST).strftime('%X')

        # 날씨 데이터 업데이트
        response_json.get('sys').update({'sunrise': sunrise})
        response_json.get('sys').update({'sunset': sunset})

        return {
            "response": response_json
        }
    except Exception:
        raise HTTPException(status_code=404, detail="API KEY 또는 요청 URL을 확인해주세요.")


# 지역 좌표 검색 API
@router.get("/area")
async def area(appid: str, area: str):
    try:
        url = f"https://api.openweathermap.org/geo/1.0/direct?q={area}&limit=1&appid={appid}"
        response = await http_client.client.get(url)

        import json
        return {
            "response": json.load(response)
        }
    except Exception:
        raise HTTPException(status_code=404, detail="API KEY 또는 요청 URL을 확인해주세요.")

