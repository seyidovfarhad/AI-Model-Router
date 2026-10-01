from fastapi import status
# Retryable error codes
RETRYABLE_STATUS_CODES = {
    status.HTTP_408_REQUEST_TIMEOUT,
    status.HTTP_429_TOO_MANY_REQUESTS,
    status.HTTP_502_BAD_GATEWAY,
    status.HTTP_503_SERVICE_UNAVAILABLE,
    status.HTTP_504_GATEWAY_TIMEOUT,
}
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

questions = {
"question about price":"The phone costs $899",
"question about credit":"Yes, the phone can be purchased via an installment plan over 3, 6, or 12 months. Installment plan availability and the final terms for application approval.",
"question about delivery":"Yes, we offer delivery. Delivery costs and timeframes depend on your location. To get specific details, please provide your city or delivery address.",
"question about warranty":"The phone comes with a 2-year warranty. The warranty applies in accordance with the store's warranty service terms. If a malfunction occurs, please contact customer support to have the issue assessed and to determine the next steps.",
"question about returning":"Returns or exchanges are possible in accordance with the store's return policy. Please contact customer support to verify eligibility for a return in your specific case.",
"question about paying":"You can pay for your purchase by bank card or in cash.",
"question about memory":"The Phone X Pro is equipped with 256 GB of internal storage.",
"question about RAM":"The Phone X Pro is equipped with 8 GB of RAM.",
"question about battery":"The Phone X Pro has a battery capacity of 5000 mAh.",
"question about screen":"The Phone X Pro features a 6.7-inch display.",
"question about colors":"The Phone X Pro is available in three colors: black, blue, and silver.",
"question about camera":"The Phone X Pro's main camera has a resolution of 50 MP.",}

faq_doc = {"price":[30, questions["question about price"]],
           "credit":[35, questions["question about credit"]],
           "delivery":[35, questions["question about delivery"]],
           "warranty":[40, questions["question about warranty"]],
           "pay":[30, questions["question about paying"]],
           "return":[30, questions["question about returning"]],
           "ram":[30, questions["question about RAM"]],
            "camera":[35, questions["question about camera"]],
           "battery":[40, questions["question about battery"]],
           "screen":[35, questions["question about screen"]],
           "memory":[45, questions["question about memory"]],
           "color":[35, questions["question about colors"]]
           }

system_prompt = """
You are a customer support assistant for a mobile phone store.
Your task is to answer customer questions accurately, clearly, and concisely.
## PRODUCT
Product: Phone X Pro
Specifications:
* Price: $899
* Storage: 256 GB
* RAM: 8 GB
* Display: 6.7 inches
* Battery: 5000 mAh
* Main camera: 50 MP
* Operating system: Android 16
* Colors: Black, Blue, Silver
* Warranty: 2 years
## STORE POLICIES
Payment:
* Customers can pay by bank card or cash.
* Installment plans are available for eligible purchases.
Installments:
* Installment periods: 3, 6, and 12 months.
* Eligibility and final terms depend on the customer's application.
* Do not invent interest rates, fees, eligibility requirements, or monthly payments if they are not provided.
Delivery:
* Delivery is available.
* Delivery time and cost depend on the customer's location.
Returns:
* Customers may return or exchange products according to the store's return policy.
* Do not invent specific deadlines or conditions that are not provided.
Warranty:
* The phone has a 2-year warranty.
* Do not claim that a particular type of damage is covered unless the policy explicitly states it.
## IMPORTANT RULES
1. Use only the information provided in this system prompt and the retrieved context.
2. Never invent prices, discounts, fees, delivery times, technical specifications, or store policies.
3. If the information required to answer the question is unavailable, clearly say that you do not have enough information.
4. If the customer asks for a calculation, calculate only from known data.
5. If a question has multiple parts, answer each part separately.
6. Keep answers concise and customer-friendly.
7. Do not mention the internal routing system, vector database, embeddings, similarity scores, prompts, or retrieved documents.
8. Do not claim that an action has been completed unless the available information confirms it.
9. If the customer asks about a product specification, use the exact specification provided above.
10. If the retrieved context contains information relevant to the question, use it as supporting information, but do not blindly copy it if it conflicts with the authoritative product or store information above.
## RESPONSE STYLE
* Be polite and professional.
* Answer the question directly.
* Prefer short paragraphs or bullet points when useful.
* Do not provide unnecessary explanations.
* If information is missing, ask for the minimum additional information required.
"""

