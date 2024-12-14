from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing import List
from .models import User, Project
from .auth import create_access_token, verify_token

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Pydantic models for request and response
class UserCreate(BaseModel):
    username: str
    password: str

class ProjectCreate(BaseModel):
    name: str
    description: str

class ProjectView(BaseModel):
    name: str
    description: str

# Helper function to get the current user based on the JWT token
def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = verify_token(token)
    user = User.objects(id=payload.get("sub")).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# Registration endpoint
@app.post("/register", response_model=UserCreate)
async def register(user: UserCreate):
    existing_user = User.objects(username=user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already taken")
    new_user = User(username=user.username)
    new_user.hash_password(user.password)
    new_user.save()
    return user

# Login endpoint to get JWT token
@app.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = User.objects(username=form_data.username).first()
    if not user or not user.verify_password(form_data.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    access_token = create_access_token(data={"sub": str(user.id), "role": user.role})
    return {"access_token": access_token, "token_type": "bearer"}

# Role-based access control to create a project (only admin can create)
@app.post("/projects", response_model=ProjectView)
async def create_project(project: ProjectCreate, current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Insufficient privileges")
    new_project = Project(name=project.name, description=project.description)
    new_project.save()
    return project

# Get all projects (read-only for users and admins)
@app.get("/projects", response_model=List[ProjectView])
async def get_projects(current_user: User = Depends(get_current_user)):
    return Project.objects.all()

# Update project (only for admin)
@app.put("/projects/{project_id}", response_model=ProjectView)
async def update_project(project_id: str, project: ProjectCreate, current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Insufficient privileges")
    proj = Project.objects(id=project_id).first()
    if not proj:
        raise HTTPException(status_code=404, detail="Project not found")
    proj.update(name=project.name, description=project.description)
    return proj
