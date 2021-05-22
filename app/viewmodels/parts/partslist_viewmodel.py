from starlette.requests import Request


from app.services import part_service
from app.viewmodels.shared.viewmodel import ViewModelBase


class PartslistViewModel(ViewModelBase):
    def __init__(self, request: Request):
        super().__init__(request)

        self.part_count: int = part_service.part_count()
        self.parts = part_service.latest_parts(limit=30)