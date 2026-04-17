from fastapi import APIRouter


class Item:
    def __init__(self):
        self.router = APIRouter(prefix='/items', tags=['Items'])
        self._setup_routes()

    def _setup_routes(self):
        self.router.add_api_route('/', self.get_home, methods=['GET'])

    def get_home(self):
        return {'message': 'Welcome to items routes'}
