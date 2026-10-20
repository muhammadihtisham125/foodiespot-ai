# Project Document: FoodieSpot AI - Smart Range & Budget Finder

## 1. Project Overview & Problem Statement
Students, hostelites, and budget travelers often struggle to find affordable dining options within a specific distance and budget range. This application solves this problem by using AI to dynamically locate and recommend budget-friendly food spots near any given campus or location.

## 2. Domain & Key Features
- **Domain:** Food + Location (Range & Budget Filtering)
- **Dynamic Spot Retrieval:** Fetches real-time, realistic local food spots based on user location, distance limit, and budget cap.
- **Smart AI Recommendations:** Provides customized meal recommendations and menu advice based on user prompts (e.g., high protein options, night cravings).

## 3. Tech Stack
- **Frontend & UI:** Python + Streamlit (with Custom CSS glassmorphism UI)
- **LLM Engine:** Gemini 3.8 Flash (`google-genai` SDK)
- **Data Processing:** Pandas & JSON parsing

## 4. Rules & Regulations
- API keys are handled securely via input components without hardcoding.
- No sensitive user data or personal location history is stored or tracked.
- Output is rendered strictly using structured DataFrames, metric cards, and clean markdown tables.

## 5. Competitor Analysis
- **Foodpanda / Zomato:** Focuses primarily on commercial delivery with high service fees, lacking hyper-local range sliders for budget travelers.
- **Google Maps:** Provides places but doesn't easily filter by specific student meal budget caps simultaneously with range.
- **Our Edge:** Instant, lightweight filtering tailored strictly for student budget constraints and AI-powered advice.