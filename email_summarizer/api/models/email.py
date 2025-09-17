from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class EmailResponse(BaseModel):
    """
    邮件响应模型，对应 ExchangeClient 返回的邮件数据结构
    """
    sender: str = Field(..., description="发件人信息，格式为 'Name: 姓名, Email: 邮箱地址'")
    to_recipients: str = Field("", description="收件人列表，多个收件人以分号分隔，每个格式为 'Name: 姓名, Email: 邮箱地址'")
    cc_recipients: str = Field("", description="抄送人列表，多个抄送人以分号分隔，每个格式为 'Name: 姓名, Email: 邮箱地址'")
    bcc_recipients: str = Field("", description="密送人列表，多个密送人以分号分隔，每个格式为 'Name: 姓名, Email: 邮箱地址'")
    author: str = Field(..., description="邮件作者信息，格式为 'Name: 姓名, Email: 邮箱地址'")
    message_id: str = Field("", description="邮件唯一标识符")
    is_read: bool = Field(False, description="邮件是否已读")
    main_content: str = Field(..., description="邮件正文内容（Markdown 格式）")
    datetime_received: Optional[str] = Field(None, description="邮件接收时间 ISO 格式字符串")
    subject: Optional[str] = Field(None, description="邮件主题")
    importance: Optional[str] = Field(None, description="邮件重要性")

    class Config:
        schema_extra = {
            "example": {
                "sender": "Name: John Doe, Email: john.doe@example.com",
                "to_recipients": "Name: Jane Smith, Email: jane.smith@example.com",
                "cc_recipients": "Name: Bob Johnson, Email: bob@example.com",
                "bcc_recipients": "",
                "author": "Name: John Doe, Email: john.doe@example.com",
                "message_id": "ABCD1234@example.com",
                "is_read": False,
                "main_content": "# Meeting Summary\n\nHello team,\n\nHere are the key points from our meeting...",
                "datetime_received": "2025-09-17T10:30:00+08:00",
                "subject": "Meeting Summary - Project X",
                "importance": "normal"
            }
        }

class TargetEmailRequest(BaseModel):
    """
    目标邮箱请求模型，用于指定要查询的邮箱
    """
    target_email: str = Field(..., description="目标邮箱地址")

    class Config:
        schema_extra = {
            "example": {
                "target_email": "user@example.com"
            }
        }