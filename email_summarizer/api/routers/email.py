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