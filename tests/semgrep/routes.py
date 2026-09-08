from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends

app = FastAPI()

# ok: fastapi-route-missing-auth
@app.get('/protected')
def protected(auth: dict = Depends(verify_jwt_token)):
    pass

# ok: fastapi-route-missing-auth
@app.post('/protected')
async def protected_async(auth: dict = Depends(verify_jwt_token)):
    pass

# ruleid: fastapi-route-missing-auth
@app.get('/private')
def unprotected():
    pass

# ruleid: fastapi-route-missing-auth
@app.post('/private')
async def unprotected_async():
    pass

# ruleid: fastapi-route-missing-auth
@app.put('/private')
def unprotected_put():
    pass

# ruleid: fastapi-route-missing-auth
@app.patch('/private')
async def unprotected_patch():
    pass

# ruleid: fastapi-route-missing-auth
@app.delete('/private')
def unprotected_delete():
    pass

# ok: fastapi-route-missing-auth
@app.get('/healthz')
def health():
    pass

# ok: fastapi-route-missing-auth
@app.get('/healthz')
async def health_async():
    pass

# ruleid: fastapi-route-missing-auth
@app.post('/healthz')
def health_mutation():
    pass

# ruleid: fastapi-route-missing-auth
@app.get('/healthz/details')
def health_details():
    pass

# ok: fastapi-route-missing-auth
@asynccontextmanager
async def lifespan(app):
    yield

# ok: fastapi-route-missing-auth
@app.middleware('http')
async def middleware(request, call_next):
    return await call_next(request)
