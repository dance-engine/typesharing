interface ActionSource {
    name: string;
    
}
interface HistoryItem {
    title: string;
    description: string;
    source: ActionSource;
    timestamp: number;
    
}
interface LineItem {
    description: string;
    amount: number;
    id: string;
    
}
interface TicketEntry {
    email: string;
    ticketNumber: string;
    access: number[];
    active: boolean;
    checkoutSession: string;
    fullName: string;
    history: HistoryItem[];
    lineItems: LineItem[];
    purchaseDate: number;
    status: string;
    studentTicket: boolean;
    ticketUsed: boolean;
    schedule?: null | undefined | string[];
    phone?: null | undefined | string;
    promoCode?: null | undefined | string;
    
}
