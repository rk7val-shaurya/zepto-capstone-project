from pathlib import Path

DOCS = Path(__file__).resolve().parent / "docs"
DOCS.mkdir(exist_ok=True)

documents = {
    "doc_01": (
        "Zepto delivers grocery and household essentials to serviceable "
        "pin codes within 10 to 30 minutes of order confirmation, depending "
        "on the customer's delivery zone and current order volume. "
        "Standard delivery is free on orders over INR 149; orders below "
        "this threshold incur a flat INR 25 delivery fee. Priority delivery, "
        "which reserves the next available rider slot, is available at "
        "checkout for an additional INR 15. Zepto does not currently deliver "
        "to addresses outside its listed serviceable pin codes."
    ),
    "doc_02": (
        "Grocery and perishable items may be reported for a return within "
        "24 hours of delivery if damaged, spoiled, or incorrect; "
        "non-perishable packaged items may be returned within 7 days of "
        "delivery in unopened, resalable condition. Approved refunds are "
        "credited to the original payment method within 3–5 business days, "
        "or instantly to the Zepto wallet if the customer opts for wallet "
        "credit. Personal care items that have been opened are "
        "non-returnable except in the case of a manufacturing defect. "
        "Return pickup, where required, is arranged free of cost by Zepto."
    ),
    "doc_03": (
        "Zepto offers three account tiers: Basic (free, default tier, "
        "standard delivery fees apply), Zepto Pass (INR 49 per month, "
        "free standard delivery on all orders and 5% off select categories), "
        "and Zepto Pass+ (INR 99 per month, free priority delivery, "
        "10% off select categories, and early access to limited-time deals "
        "24 hours before they go live to Basic and Pass members). "
        "Membership can be cancelled at any time from account settings; "
        "cancelling stops the next billing cycle but does not refund the "
        "current membership period."
    ),
    "doc_04": (
        "Every Zepto order shows a live rider-tracking map from the moment "
        "it is packed until delivery, accessible from the 'Track Order' "
        "screen. Estimated delivery time updates automatically as the "
        "rider moves. If an order's status shows no movement for more than "
        "20 minutes past its original estimated delivery time, customers "
        "should contact support directly rather than continue waiting, "
        "since this indicates a likely delivery issue."
    ),
    "doc_05": (
        "Orders can be cancelled free of cost any time before the order "
        "status changes to 'Packed', typically within the first 2 minutes "
        "of placing the order. Once an order has been packed, it can no "
        "longer be cancelled through the app, since the rider is dispatched "
        "immediately after packing given Zepto's quick-delivery model. "
        "If a packed order cannot be delivered due to a Zepto-side issue "
        "(for example, rider unavailability), the order is auto-cancelled "
        "and fully refunded without any cancellation fee."
    ),
    "doc_06": (
        "If an order arrives with damaged, spoiled, or missing items, "
        "customers must report it within 24 hours of delivery through "
        "the 'Report an Issue' button on the order page. Zepto ships a "
        "free replacement or issues a full refund for damaged, spoiled, "
        "or missing items without requiring the customer to return the "
        "original item, unless the order value exceeds INR 1000, "
        "in which case a photo of the issue must be submitted through "
        "the report form before a replacement or refund is processed."
    ),
    "doc_07": (
        "Zepto gift cards are available in fixed denominations of "
        "INR 100, INR 250, INR 500, and INR 1000, and are delivered by "
        "email or SMS within minutes of purchase. Gift cards are valid "
        "for 1 year from the date of issue and carry no maintenance fees. "
        "Gift card balance can be combined with one other payment method "
        "at checkout but cannot be combined with another gift card in "
        "the same transaction. Gift card balance cannot be redeemed "
        "for cash except where required by law."
    ),
    "doc_08": (
        "Zepto customer support is available via in-app chat 24 hours a "
        "day, 7 days a week, given the time-sensitive nature of quick "
        "commerce deliveries. Average in-app chat response time is under "
        "2 minutes. Email support is also available for non-urgent queries "
        "and is answered within 24 hours on business days. Phone support "
        "is not offered."
    ),
}

for document_id, content in documents.items():
    path = DOCS / f"{document_id}.txt"
    path.write_text(content, encoding="utf-8")
    print(f"Created {path.name}")

print(f"\nCreated {len(documents)} policy documents.")