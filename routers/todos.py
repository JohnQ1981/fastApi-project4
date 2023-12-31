from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path, Request, Form
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from starlette import status
from starlette.responses import RedirectResponse

import models
from models import Todos
from database import SessionLocal, engine
from .auth import get_current_user
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

# engine,
# from routers import auth

router = APIRouter()

models.Base.metadata.create_all(bind=engine)
templates = Jinja2Templates(directory="templates")


# app.include_router(auth.router)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/todos", response_class=HTMLResponse)
async def read_all_by_user(request: Request, db: Session = Depends(get_db)):
    todos = db.query(models.Todos).filter(models.Todos.owner_id == 1).all()
    return templates.TemplateResponse("home.html", {"request": request, "todos": todos})


@router.get("/add-todo", response_class=HTMLResponse)
async def add_new_todo(request: Request):
    return templates.TemplateResponse("add-todo.html", {"request": request})


@router.post("/add-todo", response_class=HTMLResponse)
async def create_todo(request: Request, title: str = Form(...), description: str = Form(...),
                      priority: int = Form(...), db: Session = Depends(get_db)):
    todo_model = models.Todos()
    todo_model.title = title
    todo_model.description = description
    todo_model.priority = priority
    todo_model.complete = False
    todo_model.owner_id = 1

    db.add(todo_model)
    db.commit()
    return RedirectResponse(url="/todos", status_code=status.HTTP_302_FOUND)


@router.get("/edit-todo/{todo_id}", response_class=HTMLResponse)
async def edit_todo(request: Request, todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(models.Todos).filter(models.Todos.id == todo_id).first()
    return templates.TemplateResponse("edit-todo.html", {"request": request, "todo": todo})


@router.post("/edit-todo/{todo_id}", response_class=HTMLResponse)
async def edit_todo_commit(request: Request, todo_id: int, title: str = Form(...),
                           description: str = Form(...), priority: int = Form(...), db: Session = Depends(get_db)):
    todo_model = db.query(models.Todos).filter(models.Todos.id == todo_id).first()

    todo_model.title = title
    todo_model.description = description
    todo_model.priority = priority

    db.add(todo_model)
    db.commit()

    return RedirectResponse(url="/todos", status_code=status.HTTP_302_FOUND)


@router.delete("/delete/{todo_id}")
async def delete_todo(request: Request, todo_id: int, db: Session = Depends(get_db)):

    todo_model = db.query(models.Todos).filter(models.Todos.id == todo_id).filter(models.Todos.owner_id == 1).first()

    if todo_model is None:
        return RedirectResponse(url="/todos", status_code=status.HTTP_302_FOUND)

    db.query(models.Todos).filter(models.Todos.id == todo_id).delete()

    db.commit()

    return RedirectResponse(url="/todos", status_code=status.HTTP_302_FOUND)
