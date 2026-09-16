from fastapi import APIRouter, Form, Header
from utils.db import get_db
from utils.enc_dec import hash_password,verify_password
from utils.jwtutil import create_access_token, decode_access_token

router=APIRouter()

#회원가입 만들기
@router.post("/regiser")#<- 요게 주소
def regiser(
    username=Form("")
    ,password=Form("")
    ,email=Form("")
    ,gender=Form("m")
    ,address=Form("")
):
    result={"success":True
            ,"data":None
            ,"msg":""}
    try:
        password=hash_password(password)
        with get_db() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO t_user
                    (username,password,email,gender,address)
                    VALUES
                    (%s,%s,%s,%s,%s)
                    RETURNING id, username, email, gender, created_dt, address
                """
                    ,(username,password,email,gender,address)
                )
                row=cursor.fetchone()
                columns = [
                    desc[0]
                    for desc in cursor.description
                ]
                #위에 회원가입 코드를 data에 저장한다.
                data = dict(zip(columns, row))
                data["created_dt"] = data["created_dt"].isoformat()
        data["password"]=""
        token=create_access_token(data=data)
        result["data"]={
            "token":token
            ,"userinfo":data
        }
    except Exception as e:
        result["success"]=False
        result["msg"]=str(e)
    return result
#ㄴ서버 돌리는 패턴

#로그인 만들기
@router.post("/login")
def login(username:str=Form("")
            ,password:str=Form("")
            ):
    result={"success":True,
                "data":None,
                "msg":""}
    try:
        with get_db() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    SELECT
                    u.id
                    ,u.username
                    ,u.password
                    ,u.email
                    ,u.gender
                    ,u.created_dt
                    ,address
                    FROM t_user AS u
                    WHERE u.username = %s
                """
                    ,(username,)
                )
                row=cursor.fetchone()
                columns = [
                    desc[0]
                    for desc in cursor.description
                ]
                data = dict(zip(columns, row))
                data["created_dt"] = data["created_dt"].isoformat()
        bcheck=verify_password(password,data["password"])
        if not bcheck:
           raise Exception("password not match")
        data["password"]=""
        token=create_access_token(data=data)
        result["data"]={
            "token":token
            ,"userinfo":data
        }
    except Exception as e:
        result["success"]=False
        result["msg"]=str(e)
    return result