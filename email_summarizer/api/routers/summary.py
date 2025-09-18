from fastapi import APIRouter, Depends, HTTPException, status
from datetime import datetime, date
from typing import List, Optional, Tuple

from email_summarizer.app.utils.exchange_client import ExchangeClient
from email_summarizer.app.agents.graph.email_summarizer_graph import EmailSummarizerAgentsGraph
from email_summarizer.api.dependencies import get_exchange_client, get_email_summarizer
from email_summarizer.api.models.summary import SummaryRequest, SummaryResponse

router = APIRouter(
    prefix="/summary",
    tags=["summary"],
    responses={
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "处理摘要时出错"},
        status.HTTP_400_BAD_REQUEST: {"description": "无效的请求参数"}
    }
)

def get_client_from_summary_request(request: SummaryRequest) -> ExchangeClient:
    return get_exchange_client(request.target_email)

def get_summarizer_from_request(request: SummaryRequest) -> EmailSummarizerAgentsGraph:
    return get_email_summarizer(request.selected_analysts)

def get_formatted_date(request: SummaryRequest) -> str:
    if request.date:
        return request.date
    return datetime.now().strftime("%Y-%m-%d")

@router.post("/today", response_model=SummaryResponse)
async def generate_summary(
    request: SummaryRequest,
    client: ExchangeClient = Depends(get_client_from_summary_request),
    summarizer: EmailSummarizerAgentsGraph = Depends(get_summarizer_from_request)
):
    # Get the date directly from the request
    date = get_formatted_date(request)
    """
    根据指定邮箱中的邮件生成今日邮件摘要报告
    
    - **target_email**: 必选，指定要查询的目标邮箱地址
    - **selected_analysts**: 可选，指定要使用的分析器列表
    """
    try:
        # 获取邮件
        emails = client.fetch_today_emails()
        
        # 生成摘要
        final_state = summarizer.propagate(emails, date)
        
        # 构建响应
        return SummaryResponse(
            summary=final_state["email_summary_report"],
            date=date,
            target_email=request.target_email,
            analysts_used=request.selected_analysts
        )
    except KeyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"摘要生成失败：缺少关键结果 ({str(e)})"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"摘要生成失败：{str(e)}"
        )

@router.post("/timerange", response_model=SummaryResponse)
async def generate_summary_in_time_range(
    request: SummaryRequest,
    start_time: str,
    end_time: str,
    client: ExchangeClient = Depends(get_client_from_summary_request),
    summarizer: EmailSummarizerAgentsGraph = Depends(get_summarizer_from_request)
):
    # Get the date directly from the request
    date = get_formatted_date(request)
    """
    根据指定邮箱中在给定时间范围内的邮件生成摘要报告
    
    - **target_email**: 必选，指定要查询的目标邮箱地址
    - **selected_analysts**: 可选，指定要使用的分析器列表
    - **start_time**: 必选，查询的起始时间，格式为 YYYY-MM-DDTHH:MM:SS
    - **end_time**: 必选，查询的结束时间，格式为 YYYY-MM-DDTHH:MM:SS
    """
    try:
        # Convert string parameters to datetime objects
        start_datetime = datetime.fromisoformat(start_time)
        end_datetime = datetime.fromisoformat(end_time)
        
        # 获取邮件
        emails = client.fetch_emails(since=start_datetime, until=end_datetime)
        
        # 生成摘要
        final_state = summarizer.propagate(emails, date)
        
        # 构建响应
        return SummaryResponse(
            summary=final_state["email_summary_report"],
            date=date,
            target_email=request.target_email,
            analysts_used=request.selected_analysts
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"无效的日期格式：{str(e)}"
        )
    except KeyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"摘要生成失败：缺少关键结果 ({str(e)})"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"摘要生成失败：{str(e)}"
        )