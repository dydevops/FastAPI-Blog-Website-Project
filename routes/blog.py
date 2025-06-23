from fastapi import APIRouter, Depends, Request, Form
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Blog, Category
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from slugify import slugify
from starlette.status import HTTP_303_SEE_OTHER

router = APIRouter()
templates = Jinja2Templates(directory="templates")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_class=HTMLResponse)
def show_blog(request: Request, db: Session = Depends(get_db)):
    blogs = db.query(Blog).order_by(Blog.id.desc()).all()
    categories = db.query(Category).all()
    return templates.TemplateResponse("index.html", {"request": request, "blogs": blogs, "categories": categories})

# @router.post("/", response_class=HTMLResponse)
# def add_blog(
#     request: Request,
#     title: str = Form(...),
#     content: str = Form(...),
#     status: int = Form(0),
#     category_id: int = Form(...),
#     db: Session = Depends(get_db)
# ):
#     slug = slugify(title)
#     counter = 1
#     original_slug = slug
#     while db.query(Blog).filter(Blog.slug == slug).first():
#         slug = f"{original_slug}-{counter}"
#         counter += 1

#     new_blog = Blog(title=title, content=content, slug=slug, status=status, category_id=category_id)
#     db.add(new_blog)
#     db.commit()
#     db.refresh(new_blog)
#     return RedirectResponse(url="/", status_code=HTTP_303_SEE_OTHER)
@router.post("/", response_class=HTMLResponse)
def add_blog(
    request: Request,
    title: str = Form(...),
    content: str = Form(...),
    status: int = Form(0),
    category_id: int = Form(...),
    db: Session = Depends(get_db)
):
    slug = slugify(title)
    counter = 1
    original_slug = slug
    while db.query(Blog).filter(Blog.slug == slug).first():
        slug = f"{original_slug}-{counter}"
        counter += 1

    new_blog = Blog(title=title, content=content, slug=slug, status=status, category_id=category_id)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return RedirectResponse(url="/", status_code=HTTP_303_SEE_OTHER)



@router.get("/post/{slug}", response_class=HTMLResponse)
def read_blog_detail(request: Request, slug: str, db: Session = Depends(get_db)):
    blog = db.query(Blog).filter(Blog.slug == slug).first()
    if not blog:
        return templates.TemplateResponse("404.html", {"request": request}, status_code=404)
    return templates.TemplateResponse("detail.html", {"request": request, "blog": blog})

@router.get("/category", response_class=HTMLResponse)
def category_form(request: Request, db: Session = Depends(get_db)):
    return templates.TemplateResponse("category_form.html", {"request": request})

@router.post("/category", response_class=HTMLResponse)
def create_category(
    request: Request,
    name: str = Form(...),
    status: int = Form(0),
    db: Session = Depends(get_db)
):
    category = Category(name=name, status=status)
    db.add(category)
    db.commit()
    return RedirectResponse(url="/category", status_code=HTTP_303_SEE_OTHER)


