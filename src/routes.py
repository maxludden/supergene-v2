from typing import List

from fastapi import APIRouter, HTTPException, Depends
from beanie.odm.fields import PydanticObjectId

from chapter import Chapter

chapter_router = APIRouter()

async def get_chapter(chapter_id: PydanticObjectId) -> Chapter:
    '''Helper function to get a chapter by id.'''

    chapter = await Chapter.get(chapter_id)
    if chapter is None:
        raise HTTPException(status_code=404, detail="Chapter not found")
    return chapter

@chapter_router.get("/chapters/{chapter_id}", response_model=Chapter)
async def get_chapter_by_id(chapter: Chapter = Depends(get_chapter)):
    '''Get a chapter by id.'''
    return chapter

@chapter_router.get("/chapters", response_model=List[Chapter])
async def list_chapters():
    return await Chapter.find_all().to_list()

@chapter_router.post("/chapters/", response_model=Chapter)
async def create_chapter(chapter: Chapter):
    return await chapter.create()