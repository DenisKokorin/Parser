from sqlalchemy import select, insert, delete, update, text
from src.parse_functions import get_link_vacancy, get_vacancy
from fastapi import FastAPI, Depends
from models.tables import request, vacancy
from src.database import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession

app = FastAPI()

@app.get("/")
async def write_request_vacancy():
    return "Напишите ваш запрос"

@app.get("/all")
async def show_all(session: AsyncSession = Depends(get_async_session)):
    data = []
    query = await session.execute(select(vacancy))
    for row in query:
        vac = {
            "title": row[1],
            "salary": row[2],
            "city": row[3],
            "company": row[4],
            "experience": row[5],
            "type_of_employment": row[6],
            "schedule": row[7],
            "viewers_count": row[8],
            "link": row[9]
        }
        data.append(vac)
    return data


@app.get("/{req}")
async def find_vacancy(req: str, num: int, session: AsyncSession = Depends(get_async_session)):
    check_request = await session.execute(select(request).where(request.c.request == req))
    if check_request.scalar() is None:
        ins1 = insert(request).values(request=req, num=num)
        await session.execute(ins1)
        await session.commit()
        count = 0
        for link in get_link_vacancy(req):
            res = get_vacancy(link)
            if "adsrv" in res["link"]:
                continue
            ins2 = insert(vacancy).values(request = req, title = res["title"], salary = res["salary"], city = res["city"], company = res["company"], experience = res["experience"], typeofemployment = res["type_of_employment"], schedule = res["schedule"], viewers_count = res["viewers_count"], link = res["link"])
            await session.execute(ins2)
            await session.commit()
            if count+1 == num:
                break
            else:
                count += 1
        check_vacancy = await session.execute(select(vacancy).where(vacancy.c.request == req))
        if check_vacancy.scalar() is None:
            del_stmt = delete(request).where(request.c.request == req)
            await session.execute(del_stmt)
            await session.commit()
            return "К сожалению парсер не смог найти никаких вакансий. Попробуйте сделать другой запрос"
        else:
            return "Есть подходящие вакансии"

    else:
        check_num = await session.execute(select(request.c.num).where(request.c.request == req))
        res = check_num.scalars().first()
        if num > int(res):
            del_stmt = delete(vacancy).where(vacancy.c.request == req)
            upd_stmt = update(request).where(request.c.request == req).values(num=num)
            await session.execute(del_stmt)
            await session.execute(upd_stmt)
            await session.commit()
            count = 0
            for link in get_link_vacancy(req):
                res = get_vacancy(link)
                if "adsrv" in res["link"]:
                    continue
                ins3 = insert(vacancy).values(request=req, title=res["title"], salary=res["salary"], city=res["city"],
                                              company=res["company"], experience=res["experience"],
                                              typeofemployment=res["type_of_employment"], schedule=res["schedule"],
                                              viewers_count=res["viewers_count"], link=res["link"])
                await session.execute(ins3)
                await session.commit()
                if count + 1 == num:
                    break
                else:
                    count += 1
            check_vacancy = await session.execute(select(vacancy).where(vacancy.c.request == req))
            if check_vacancy.scalar() is None:
                del_stmt = delete(request).where(request.c.request == req)
                await session.execute(del_stmt)
                await session.commit()
                return "К сожалению парсер не смог найти никаких вакансий. Попробуйте сделать другой запрос"
            else:
                return "Есть подходящие вакансии"

        else:
            return "Вакансии уже есть в базе"

@app.get("/{req}/filtered")
async def filter_request(req: str, num: int, city: str, experience: str, type_of_employment: str, schedule: str,  session: AsyncSession = Depends(get_async_session)):
    if city == "Не имеет значения":
        cit = "city"
    else:
        cit = f"'{city}'"
    if experience == "Не имеет значения":
        exp = "experience"
    else:
        exp = f"'{experience}'"
    if type_of_employment == "Не имеет значения" :
        type = "typeofemployment"
    else:
        type = f"'{type_of_employment}'"
    if schedule == "Не имеет значения":
        sch= "schedule"
    else:
        sch = f"'{schedule}'"
    query = text(f"SELECT * from vacancy WHERE vacancy.request = '{req}' and vacancy.city = {cit} and vacancy.experience = {exp} and vacancy.typeofemployment = {type} and vacancy.schedule = {sch}")
    res = await session.execute(query)
    data = []
    count = 0
    for row in res:
        vac = {
            "title": row[1],
            "salary": row[2],
            "city": row[3],
            "company": row[4],
            "experience": row[5],
            "type_of_employment": row[6],
            "schedule": row[7],
            "viewers_count": row[8],
            "link": row[9]
        }
        data.append(vac)
        if count + 1 == num:
            break
        else:
            count += 1
    return data

