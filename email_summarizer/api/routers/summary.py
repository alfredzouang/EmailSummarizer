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

@router.post("", response_model=SummaryResponse)
async def generate_summary(
    request: SummaryRequest,
    client: ExchangeClient = Depends(get_client_from_summary_request),
    summarizer: EmailSummarizerAgentsGraph = Depends(get_summarizer_from_request)
):
    # Get the date directly from the request
    date = get_formatted_date(request)
    """
    根据指定邮箱中的邮件生成摘要报告
    
    - **target_email**: 必选，指定要查询的目标邮箱地址
    - **selected_analysts**: 可选，指定要使用的分析器列表
    - **date**: 可选，指定摘要日期，默认为今天
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
