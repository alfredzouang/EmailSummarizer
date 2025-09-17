from fastapi import APIRouter, Depends, HTTPException, Query, status
from typing import List, Optional

from email_summarizer.app.utils.exchange_client import ExchangeClient
from email_summarizer.api.dependencies import get_exchange_client
from email_summarizer.api.models.email import EmailResponse, TargetEmailRequest

router = APIRouter(
    prefix="/emails",
    tags=["emails"],
    responses={
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Exchange server error"},
        status.HTTP_400_BAD_REQUEST: {"description": "Invalid request parameters"}
    }
)

def get_client_from_request(request: TargetEmailRequest) -> ExchangeClient:
    return get_exchange_client(request.target_email)

@router.post("/all", response_model=List[EmailResponse])
async def get_all_emails(
    request: TargetEmailRequest,
    client: ExchangeClient = Depends(get_client_from_request)
):
    """
    获取指定邮箱中的所有邮件
    
    - **target_email**: 必选参数，指定要查询的目标邮箱地址
    """
    try:
        emails = client.fetch_all_emails()
        return emails
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch all emails: {str(e)}"
        )
    
@router.post("/today", response_model=List[EmailResponse])
async def get_today_emails(
    request: TargetEmailRequest,
    client: ExchangeClient = Depends(get_client_from_request)
):
    """
    获取指定邮箱中最近 24 小时内的邮件
    
    - **target_email**: 必选参数，指定要查询的目标邮箱地址
    """
    try:
        emails = client.fetch_today_emails()
        return emails
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch today's emails: {str(e)}"
        )
    
@router.post("/timerange", response_model=List[EmailResponse])
async def get_emails_in_time_range(
    request: TargetEmailRequest,
    start_time: str = Query(..., description="起始时间，格式为 YYYY-MM-DDTHH:MM:SS"),
    end_time: str = Query(..., description="结束时间，格式为 YYYY-MM-DDTHH:MM:SS"),
    client: ExchangeClient = Depends(get_client_from_request)
):
    """
    获取指定邮箱中在给定时间范围内的邮件
    
    - **target_email**: 必选参数，指定要查询的目标邮箱地址
    - **start_time**: 必选参数，指定查询的起始时间，格式为 YYYY-MM-DDTHH:MM:SS
    - **end_time**: 必选参数，指定查询的结束时间，格式为 YYYY-MM-DDTHH:MM:SS
    """
    try:
        # Convert string parameters to datetime objects
        from datetime import datetime
        start_datetime = datetime.fromisoformat(start_time)
        end_datetime = datetime.fromisoformat(end_time)
        
        emails = client.fetch_emails(since=start_datetime, until=end_datetime)
        return emails
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid datetime format: {str(e)}. Use YYYY-MM-DDTHH:MM:SS format."
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch emails in time range: {str(e)}"
        )
