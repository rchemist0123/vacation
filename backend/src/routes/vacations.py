from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status, Response,Request
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session, load_only
from starlette.routing import Router
from src.auth.users import validate_user
from src.auth.jwthandler import get_current_user
from src.schemas.token import Status
from src.schemas.users import ShowUser, User
from src.schemas.vacations import Vacation, VacationBase, VacationList
from src.database.models import get_db, Vacations
import pandas as pd
from src.database.models import Users, get_db
from typing import List
import re
import datetime

router = APIRouter(
  tags=['vacations']
)

connect_db = get_db

@router.post('/submit')
async def submitVacations(request:List[Vacation], current_user:ShowUser=Depends(get_current_user),db:Session=Depends(connect_db)):
    for i in request:
        data = Vacations(
            userid=current_user.rid,
            vdate = i.vdate,
            vtype = i.vtype,
            vhour = i.vhour,
            vcheck= False,
            boss="정세영"
        )
        if not data:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="휴가 신청 불가.")
        db.add(data)
        db.commit()
        db.refresh(data)

    return "휴가 신청 완료."

@router.get('/vacations')
async def getVacations(db:Session=Depends(connect_db), current_user:ShowUser=Depends(get_current_user)):
    rawData = db.query(Vacations)\
                .filter(Vacations.userid==current_user.rid)
                #   .join(Users, Users.rid == Vacations.userid)\
    vacations = pd.read_sql(rawData.statement, rawData.session.bind)
    dateArr = []
    for i in range(vacations.shape[0]):
        # print(vacations.iloc[i,:]['vdate'])
        temp= []
        x= vacations.iloc[i,:]['vdate'].split(" ")
        for j in range(2):
            rst = re.findall('\d+',x[j])
            y="".join(rst)
            temp.append(y)
        now = datetime.datetime.now()
        date = pd.Timestamp(now.year,  int(temp[0]), int(temp[1]),0,0,0).date()
        dateArr.append(str(date))
    vacations['vymd']=dateArr
    json = vacations.to_json(orient="records")
    return Response(content=json, media_type='application/json')