## SECTION 1 : PROJECT TITLE
## Rental Recommendation Systems in Singapore

<img src="SystemCode/Rental-Recommendation-System-in-Singapore/app/static/img/Rental.jpg"
     style="float: left; margin-right: 0px;" />

---

## SECTION 2 : EXECUTIVE SUMMARY / PAPER ABSTRACT
Amid the rapid urbanization and globalization of Singapore, the housing market has been at the forefront of these changes. With the influx of professionals, both local and international, seeking the dynamic opportunities Singapore offers, the rental market has witnessed substantial growth and transformation. Residents and newcomers are on the hunt for residential spaces that not only fit their budget but also align with their preferences and lifestyle.

In today's digital era, where convenience and precision are paramount, potential tenants face the daunting task of sifting through an overwhelming number of property listings across various platforms. The sheer volume of options often results in decision fatigue, extended search durations, and potential mismatches between renters and their ideal homes.

To address this inefficiency, our team has meticulously crafted a Rental Recommendation System. Envisioned as a comprehensive platform, our system alleviates the cumbersome process of property hunting. By understanding a tenant's unique needs and preferences, it offers tailored property suggestions that resonate with individual requirements.
Our system is anchored on comprehensive data mining from property listing platforms Airbnb and github. Central to our system is the recommendation reasoning mechanism which harnesses a specialized content-based filtering approach, enriched by certain algorithmic strategies, to offer pinpointed property recommendations. On the frontend, our team has adeptly employed Bootstrap as the foundational framework, enhanced by Jinja2 integration, ensuring both adaptability and aesthetic coherence. Features like interactive drop-down menus powered by JavaScript ajax further elevate the user experience. Seamlessly uniting this frontend with our backend is the Python Flask-wtf application, which not only streamlines data interactions but also ensures swift and accurate response to user queries.

Our project team hopes that with our solution, people in need will be able to find the house that suits their specific requirements most.


---

## SECTION 3 : CREDITS / PROJECT CONTRIBUTION

| Official Full Name  | Student ID (MTech Applicable)  | Work Items (Who Did What) | Email (Optional) |
| :------------ |:---------------:| :-----| :-----|
| Li Linze | A0285963L | Market research<br>System design<br>Integration<br>Team collaboration| e1221775@u.nus.edu |
| Pan Shuyi | A0286033H | Ideation & Data<br>Data Preprocessing<br>Algorithm&Optimization<br>Report & Video| panshuyi08@u.nus.edu |
| Cai Xichen | A0285786E | System Design<br>Front-end Development<br>CSS Collaboration<br>Backend Demo<br>| e1221598@u.nus.edu |
| Liu Yifeng | A0285847J | Backend Integration<br>System Facilitation<br>Algorithm Involvement<br>Database Design| e1221659@u.nus.edu |
| Li Jiaxuan | A0285821Y | UI Development<br>Design Collaboration<br>Front-end Harmony<br>Technical Contributions| e1221633@u.nus.edu |

---

## SECTION 4 : VIDEO OF SYSTEM MODELLING & USE CASE DEMO

### Business Presentation
[![Rental Recommendation Systems in Singapore(Business)](http://img.youtube.com/vi/mn_TUcbrk2E/0.jpg)](https://www.youtube.com/watch?v=mn_TUcbrk2E  "Rental Recommendation Systems in Singapore")


### Technical Presentation
[![Rental Recommendation Systems in Singapore(Technical)](http://img.youtube.com/vi/dCElCLCmM4k/0.jpg)](https://youtu.be/dCElCLCmM4k?si=FR2ZjpwK_1keAHZv  "Rental Recommendation Systems in Singapore")

Here is our promotion [video.](https://www.youtube.com/watch?v=mn_TUcbrk2E "promotion video")

---

## SECTION 5 : USER GUIDE


### [ 1 ] Clone Project Sourcecode
```
git clone https://github.com/Leelinze/Rental-Recommendation-Systems-in-Singapore-.git
```


### [ Optional ] Create New Conda Environment
```
conda create --name pjrent python=3.11
conda activate pjrent
```

### [ 2 ] Install Required Packages via pip
```
cd SystemCode/Rental-Recommendation-System-in-Singapore
conda install --file requirements.txt
```

### [ 3 ] Set Your Google GeoCoding API Key
```
cd SystemCode/Rental-Recommendation-System-in-Singapore
touch app/.env
echo 'GEOCODING_APIKEY="Your API Key"' > app/.env
```

### [ 4 ] Strat Flask Server
```
python run.py
```


> **Go to URL using web browser** http://0.0.0.0:5000 or http://127.0.0.1:5000 or http://localhost:5000

---
## SECTION 6 : PROJECT REPORT / PAPER


**Recommended Sections for Project Report / Paper:**
- Executive Summary
- Problem Description
  - Problem Statement
  - Market research
  - Project scope
- Project Solution
  - Project Deliverables/ System architecture
  - Knowledge Representation/ Data
- System implementation
  - System Frontend
  - User Interface
  - System Backend
    - Backend System Architecture and Functional Modules
    - Backend Database Tables and Relationships
    - User Authentication and Authorization
  - Recommendation Algorithm
    - Feature Selection
    - Recommendation Module
      - Content-based recommendation algorithm
      - Matrix Factorization recommendation algorithm
      - Hybrid recommendation algorithm
      - Output
    - User Rating Estimation
- Challenge & Future Improvement
  - Challenge
  - Future Improvement

---
