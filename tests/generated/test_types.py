from dataclasses import dataclass, field
from typing import Optional, List, Union
from decimal import Decimal
from datetime import date

class MissingType:
    pass

@dataclass
class ActionSource:
    name: str
    
@dataclass
class HistoryItem:
    title: str
    description: str
    source: ActionSource
    timestamp: int
    
@dataclass
class LineItem:
    description: str
    amount: int
    id: str
    
@dataclass
class TicketEntry:
    email: str
    ticket_number: str
    access: List[int]
    active: bool
    checkout_session: str
    full_name: str
    line_items: List[LineItem]
    purchase_date: int
    status: str
    student_ticket: bool
    ticket_used: bool
    history: List[HistoryItem]= []
    schedule: Union[List[str], MissingType]= MissingType()
    phone: Union[str, MissingType]= MissingType()
    promo_code: Union[str, MissingType]= MissingType()
    