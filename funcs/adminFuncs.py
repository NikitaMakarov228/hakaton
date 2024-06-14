import json
from typing import List


class Admin:

    @staticmethod
    def get_admin_ids() -> List[str]:
        try:
            with open("json/admin.json", "r", encoding="utf-8") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    async def set_admin_id(self, id: str):
        admin_ids = self.get_admin_ids()
        if id not in admin_ids:
            admin_ids.append(id)
            with open("json/admin.json", "w", encoding="utf-8") as file:
                json.dump(admin_ids, file, ensure_ascii=False, indent=4)


admin = Admin()
