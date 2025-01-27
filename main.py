from fastapi import FastAPI, Depends, HTTPException, Query
from service.scraperService import ScraperService
from auth.authService import AuthService
from models.person import Person
from typing import Optional

app = FastAPI()

@app.get("/")
async def root():
    # add instructions to hit /auth to generate user token
    return {
        "message": "Welcome to the web scraper app :)", 
        "First Step": "Generate auth token for authentication | endpoint: /auth",
        "Endpoints": "single page: /page/{page} || multiple pages: /pages?end_page={endPageNo}&start_page={startPageNo}"
    }

@app.post("/auth")
async def generate_user_token(person: Person):
    if not person.name.strip():
        raise HTTPException(status_code=400, detail="Name cannot be empty or null")
    auth_service = AuthService()
    token = auth_service.generate_user_token(person)
    return {"token": token}

@app.post("/page/{page_no}")
async def scrap_single_page(page_no: int = 1, authenticated: bool = Depends(AuthService.authenticate)):
    scraper_service = ScraperService()
    result_message = scraper_service.run(page_no, page_no)
    return {"message": result_message}

@app.post("/pages")
async def scrape_pages(start_page: Optional[int] = Query(1), end_page: int = Query(...), authenticated: bool = Depends(AuthService.authenticate)):
    scraper_service = ScraperService()
    result_message = scraper_service.run(start_page, end_page)
    return {"message": result_message}
