from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime, date

class SummaryRequest(BaseModel):
    """
    邮件摘要请求模型
    """
    target_email: str = Field(..., description="目标邮箱地址，用于获取邮件")
    selected_analysts: Optional[List[str]] = Field(
        default=["briefing_analyst", "status_updates"],
        description="要使用的分析器列表，默认为简报分析和状态更新"
    )
    date: Optional[str] = Field(
        default=None, 
        description="摘要日期，格式为 YYYY-MM-DD，默认为今天"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "target_email": "alfredzou@thebig1.biz",
                "selected_analysts": ["briefing_analyst", "status_updates"],
                "date": "2025-09-17"
            }
        }

class SummaryResponse(BaseModel):
    """
    邮件摘要响应模型
    """
    summary: str = Field(..., description="生成的邮件摘要报告")
    date: str = Field(..., description="摘要生成日期")
    target_email: str = Field(..., description="目标邮箱地址")
    analysts_used: List[str] = Field(..., description="使用的分析器列表")
    
    class Config:
        schema_extra = {
            "example": {
                "summary": "# 邮件摘要报告\n\n## 今日概览\n- 收到5封重要邮件\n- 2个待处理事项\n\n## 详细内容\n...",
                "date": "2025-09-17",
                "target_email": "alfredzou@thebig1.biz",
                "analysts_used": ["briefing_analyst", "status_updates"]
            }
        }