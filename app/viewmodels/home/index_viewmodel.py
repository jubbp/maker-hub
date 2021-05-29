from typing import List

from starlette.requests import Request

from app.schema.part import PartPublic
from app.services import part_service, project_service, storage_service
from app.viewmodels.shared.viewmodel import ViewModelBase


class IndexViewModel(ViewModelBase):
    def __init__(self, request: Request):
        super().__init__(request)

        self.part_count: int = 0
        self.location_count: int = 0
        self.project_count: int = 0
        self.latest_parts: List[PartPublic] = []
        self.latest_projects: List[
            PartPublic
        ] = []  # Todo: Change to correct Type once Project schema has been completed

    async def load(self):
        self.part_count = await part_service.get_part_count()
        self.location_count = await storage_service.get_location_count()
        self.project_count = await project_service.get_project_count()
        self.latest_parts = await part_service.get_latest_parts(limit=7)
        self.latest_projects = await project_service.get_latest_projects(limit=7)
