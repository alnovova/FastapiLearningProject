from fastapi import FastAPI, Query, Body
import uvicorn


app = FastAPI()


hotels = [
    {"id": 1, "title":"Sochi", "name": "sochi"},
    {"id": 2, "title":"Dubai", "name": "dubai"},
]


@app.get("/hotels")
def get_hotels(
        id: int | None = Query(None, description="Идентификатор"),
        title: str | None = Query(None, description="Название отеля"),
):
    hotels_ = []
    for hotel in hotels:
        if id and hotel["id"] != id:
            continue
        if title and hotel["title"] != title:
            continue
        hotels_.append(hotel)

    return hotels_


@app.delete("/hotels/{hotel_id}")
def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"status": "OK"}


@app.post("/hotels")
def create_hotel(
        title: str = Body(embed=True),   # embed=True обязательно прописывать, если параметр всего один
        name: str = Body(embed=True)
):
    global hotels
    hotels.append({
        "id": hotels[-1]["id"] + 1,
        "title": title,
        "name": name
    })
    return {"status": "OK"}


@app.put("/hotels/{hotel_id}")
def update_hotel(
        hotel_id: int,
        title: str = Body(embed=True),
        name: str = Body(embed=True)
):
    global hotels
    for i, hotel in enumerate(hotels):
        if hotel["id"] == hotel_id:
            hotels[i]["title"] = title
            hotels[i]["name"] = name
            return {"status": "OK"}
        return {"status": "ERROR", "message": "Элемент не найден"}


@app.patch("/hotels/{hotel_id}")
def patch_hotel(
        hotel_id: int,
        title: str | None = Body(None, embed=True),
        name: str | None = Body(None, embed=True)
):
    global hotels
    for i, hotel in enumerate(hotels):
        if hotel["id"] == hotel_id:
            if title is not None:
                hotels[i]["title"] = title
            if name is not None:
                hotels[i]["name"] = name
            return {"status": "OK"}
        return {"status": "ERROR", "message": "Элемент не найден"}



if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
