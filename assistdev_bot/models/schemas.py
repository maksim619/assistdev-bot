"""
Модели данных (Pydantic) для валидации и типизации.
"""

from typing import Optional
from pydantic import BaseModel, Field

# ========== МОДЕЛИ ПОЛЬЗОВАТЕЛЯ ==========

class UserBase(BaseModel):
    user_id: int
    username: Optional[str] = None
    full_name: Optional[str] = None

class UserCreate(UserBase):
    pass

class UserResponse(UserBase):
    created_at: str

    class Config:
        from_attributes = True

# ========== МОДЕЛИ ДИАЛОГА ==========

class DialogStateBase(BaseModel):
    user_id: int
    state: str
    service_name: Optional[str] = None
    service_price: Optional[int] = None
    ai_model: Optional[str] = None
    extra_setup: bool = False
    extra_price: int = 0
    total_price: Optional[int] = None
    details: Optional[str] = None
    contact: Optional[str] = None
    history: Optional[str] = None  # JSON строка

class DialogStateCreate(DialogStateBase):
    pass

class DialogStateResponse(DialogStateBase):
    updated_at: str

    class Config:
        from_attributes = True

# ========== МОДЕЛИ ЗАКАЗА ==========

class OrderBase(BaseModel):
    user_id: int
    service_name: str = Field(..., min_length=1)
    service_price: int = Field(..., gt=0)
    ai_model: Optional[str] = None
    extra_setup: bool = False
    extra_price: int = 0
    total_price: int = Field(..., gt=0)
    details: Optional[str] = None
    contact: Optional[str] = None
    status: str = "new"

class OrderCreate(OrderBase):
    pass

class OrderResponse(OrderBase):
    id: int
    created_at: str

    class Config:
        from_attributes = True

# ========== ПОДТВЕРЖДЕНИЕ ЗАКАЗА ==========

class OrderConfirmation(BaseModel):
    """Данные для подтверждения заказа."""
    service_name: str
    service_price: int
    ai_model: Optional[str]
    extra_setup: bool
    extra_price: int
    total_price: int
    details: Optional[str]

    @property
    def service_display_name(self) -> str:
        names = {
            "faq_bot": "FAQ-бот",
            "hr_screener": "HR-бот-скринер",
            "sentiment_analysis": "Сентимент-анализ",
            "appointment_bot": "Бот записи",
            "rag_assistant": "RAG-ассистент"
        }
        return names.get(self.service_name, self.service_name)

    @property
    def ai_model_display(self) -> str:
        if not self.ai_model:
            return "Не выбран"
        return "OpenRouter (бесплатно)" if self.ai_model == "openrouter" else "DeepSeek (платно)"

    @property
    def extra_setup_display(self) -> str:
        return "✅ Да (+1 500 ₽)" if self.extra_setup else "❌ Нет"
