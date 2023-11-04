import asyncio
from datetime import datetime
from pprint import pprint

import aiohttp
import requests
from more_itertools import chunked

from models import engine, Base, SwapiPeople, Session

CHUNK_SIZE = 5


def count_people():
    response = requests.get(url='https://swapi.dev/api/people/').json()
    return response['count']


async def chunked_async(async_iter, size):
    list_items = []
    while True:
        try:
            item = await async_iter.__anext__()
        except StopAsyncIteration:
            break
        list_items.append(item)
        if len(list_items) == size:
            yield list_items
            list_items = []


async def get_data_from_url(url: str, key, client: aiohttp.ClientSession):
    response = await client.get(url)
    data = await response.json()
    return data[key]


async def get_list_urls(urls: list, key: str, client: aiohttp.ClientSession):
    tasks = (asyncio.create_task(get_data_from_url(url, key, client)) for url in urls)
    for task in tasks:
        yield await task


async def get_info_people(urls: list, key: str, client: aiohttp.ClientSession):
    items = []
    async for item in get_list_urls(urls, key, client):
        items.append(item)
    return ', '.join(items)


async def get_person_json(people_id: int, client: aiohttp.ClientSession):
    async with client.get(f"https://swapi.dev/api/people/{people_id}/") as response:
        if response.status == 404:
            return {'status_code': 404}
        person_json = await response.json()
        return person_json


async def insert_people(people_pattern):
    async with Session() as session:
        async with aiohttp.ClientSession() as client:
            for json in people_pattern:
                if json.get('status_code') == 404:
                    break
                title_films = await get_info_people(json['films'], 'title', client)
                homeworld = await get_info_people([json['homeworld']], 'name', client)
                species = await get_info_people(json['species'], 'name', client)
                starships = await get_info_people(json['starships'], 'name', client)
                vehicles = await get_info_people(json['vehicles'], 'name', client)
                person = SwapiPeople(
                    birth_year=json['birth_year'],
                    eye_color=json['eye_color'],
                    films=title_films,
                    gender=json['gender'],
                    hair_color=json['hair_color'],
                    height=json['height'],
                    homeworld=homeworld,
                    mass=json['mass'],
                    name=json['name'],
                    skin_color=json['skin_color'],
                    species=species,
                    starships=starships,
                    vehicles=vehicles
                )
                session.add(person)
                await session.commit()


async def get_all_people():
    async with aiohttp.ClientSession() as client:
        for ids_chunk in chunked(range(1, count_people() + 1), CHUNK_SIZE):
            coroutines = [get_person_json(i, client) for i in ids_chunk]
            results = await asyncio.gather(*coroutines)
            for item in results:
                yield item


async def main():
    async with engine.begin() as con:
        await con.run_sync(Base.metadata.drop_all)
        await con.run_sync(Base.metadata.create_all)
        await con.commit()
    async for chunk in chunked_async(get_all_people(), CHUNK_SIZE):
        asyncio.create_task(insert_people(chunk))
    tasks = set((asyncio.all_tasks())) - {asyncio.current_task()}
    for task in tasks:
        await task


if __name__ == '__main__':
    start = datetime.now()
    pprint(asyncio.run(main()))
    print(datetime.now() - start)
