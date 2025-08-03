# JIJI KENYA CHATBOT - DATA COLLECTION PLAN

## Project Summary
**Goal**: Business chatbot for Jiji Kenya marketplace  
**Target**: 10K+ listings across major categories  

## Data Source
- **Platform**: Jiji.co.ke (Kenya's largest marketplace)
- **Scope**: National coverage, 2020-2025 listings
- **Categories**: Cars, Electronics, Property, Fashion, Services, Jobs, Agriculture, etc.

## Technical Approach
- **Tools**: Python, BeautifulSoup, Pandas
- **Method**: Multi-selector scraping with fallback strategies
- **Data**: Title, price, location, URL, description
- **Quality**: Duplicate removal, validation, cleaning

## Dataset Output
- **Records**: 3,256+ unique business listings
- **Format**: CSV (UTF-8)
- **Size**: ~1.5MB
- **Completeness**: 100% titles, 65% prices, 80% locations

## Chatbot Applications
- Business discovery and search
- Price comparison insights
- Location-based recommendations
- Category navigation assistance

## Common Customer Inquiries & FAQs

### Product/Service Discovery
- "Find cars under 500K in Nairobi"
- "Show me electronics shops near me"
- "What properties are available for rent?"
- "I need a laptop under 50K"
- "Find fashion stores in Mombasa"

### Price & Comparison
- "What's the average price for Toyota Corolla?"
- "Compare prices for Samsung phones"
- "Is this price negotiable?"
- "Show cheapest options in this category"
- "What's the market rate for this item?"

### Location & Contact
- "Where is this seller located?"
- "How do I contact the seller?"
- "What's the exact address?"
- "Are there similar items nearby?"
- "Show me sellers in my area"

### Category Navigation
- "What categories are available?"
- "Show me all car brands"
- "Find jobs in IT sector"
- "Browse home furniture options"
- "What services are offered?"

### Transaction Support
- "Is this seller verified?"
- "How do I make payment?"
- "What's the return policy?"
- "Is delivery available?"
- "Can I view the item first?"

### Technical Questions
- "How do I post an ad?"
- "Why can't I see images?"
- "How to search effectively?"
- "Filter by price range"
- "Sort by newest listings"

**Deliverable**: `jiji_kenya_10k.csv` & `data_collection_plan`
