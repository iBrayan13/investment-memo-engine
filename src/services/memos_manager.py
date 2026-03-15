import json
from typing import Dict, List, Optional

from src.models.manager import Memo, StatusEnum

class MemosManager:
    def __init__(self, memos_file="memos.json"):
        self.memos_file = memos_file

    def save_new_memo(self, memo_id: str) -> bool:
        try:
            memos = self._load_memos()
            new_memo: Memo = {
                "memo_id": memo_id,
                "status": StatusEnum.started,
                "status_message": "Iniciando generación del memo",
                "memo_object": {},
                "memo_file_path": None
            }
            memos.append(new_memo)
            self._save_memos(memos)
            return True
        except Exception as e:
            print(f"Error saving new memo: {e}")
            return False
    
    def get_memos(self) -> List[Memo]:
        return self._load_memos()
    
    def get_memo_by_id(self, memo_id: str) -> Optional[Memo]:
        memos = self._load_memos()
        for memo in memos:
            if memo["memo_id"] == memo_id:
                return memo
        return None
    
    def update_memo_status(self, memo_id: str, status: StatusEnum, status_message: str = "", memo_object: Dict = None, memo_file_path: str = None) -> bool:
        try:
            memos = self._load_memos()
            for memo in memos:
                if memo["memo_id"] == memo_id:
                    memo["status"] = status
                    memo["status_message"] = status_message
                    if memo_object is not None:
                        memo["memo_object"] = memo_object
                    if memo_file_path is not None:
                        memo["memo_file_path"] = memo_file_path
                    self._save_memos(memos)
                    return True
            return False
        except Exception as e:
            print(f"Error updating memo status: {e}")
            return False
        
    def delete_memo(self, memo_id: str) -> bool:
        try:
            memos = self._load_memos()
            memos = [memo for memo in memos if memo["memo_id"] != memo_id]
            self._save_memos(memos)
            return True
        except Exception as e:
            print(f"Error deleting memo: {e}")
            return False
        
    def update_memo_message(self, memo_id: str, status_message: str) -> bool:
        try:
            memos = self._load_memos()
            for memo in memos:
                if memo["memo_id"] == memo_id:
                    memo["status_message"] = status_message
                    self._save_memos(memos)
                    return True
            return False
        except Exception as e:
            print(f"Error updating memo message: {e}")
            return False
        
    def update_memo_object(self, memo_id: str, memo_object: Dict) -> bool:
        try:
            memos = self._load_memos()
            for memo in memos:
                if memo["memo_id"] == memo_id:
                    memo["memo_object"] = memo_object
                    self._save_memos(memos)
                    return True
            return False
        except Exception as e:
            print(f"Error updating memo object: {e}")
            return False

    def _load_memos(self) -> List[Memo]:
        try:
            with open(self.memos_file, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return []

    def _save_memos(self, memos: List[Memo]):
        with open(self.memos_file, "w") as f:
            json.dump(memos, f)