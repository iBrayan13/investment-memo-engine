import io
import logging
import datetime

from fastapi import APIRouter, Request, status, BackgroundTasks, HTTPException
from fastapi.responses import StreamingResponse

from src.langg.nodes import Nodes
from src.langg.state import MemoState
from src.langg.graph import WorkFlow, StateGraph
from src.models.router import MemoGenerateRequest
from src.services.docx_service import DOCXService
from src.services.memos_manager import MemosManager
from src.services.pchain.chainable import MinimalChainable
from src.core.settings import DevelopmentSettings as Settings
from src.services.pchain.chain_prompt_manager import ChainPromptManager

logger = logging.getLogger(__name__)
settings = Settings()

memo_router = APIRouter(prefix="/memo", tags=["Memo"])


@memo_router.get("/")
def list_memos():
    memos_manager = MemosManager()
    memos = memos_manager.get_memos()
    return {"data": memos}

@memo_router.get("/{memo_id}")
def get_memo(memo_id: str):
    memos_manager = MemosManager()
    memo = memos_manager.get_memo_by_id(memo_id)
    if not memo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Memo not found")
    return {"data": memo}

@memo_router.get("/docx/{memo_id}")
def get_memo(memo_id: str):
    memos_manager = MemosManager()
    memo = memos_manager.get_memo_by_id(memo_id)
    if not memo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Memo not found")
    
    if not memo.get("memo_file_path"):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Memo file not found")
    
    with open(memo["memo_file_path"], "rb") as f:
        file_content = f.read()
        return StreamingResponse(
            io.BytesIO(file_content),
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            headers={"Content-Disposition": f'attachment; filename="{memo_id}.docx"'},
        )

@memo_router.delete("/{memo_id}")
def delete_memo(memo_id: str):
    memos_manager = MemosManager()
    success = memos_manager.delete_memo(memo_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Memo not found")
    return {"message": "Memo deleted successfully"}

@memo_router.post("/generate", status_code=status.HTTP_201_CREATED)
async def generate_memo(request: MemoGenerateRequest, background_tasks: BackgroundTasks):
    logger.info("Received request to generate memo")

    workflow = WorkFlow(
        nodes=Nodes(
            settings=settings,
            minimal_chainable=MinimalChainable(settings=settings),
            prompt_manager=ChainPromptManager(),
            memos_manager=MemosManager(),
            docx_service=DOCXService(),
        ),
        state_graph=StateGraph(MemoState)
    )

    memo_id = f"memo-{int(datetime.datetime.now().timestamp())}"
    background_tasks.add_task(
        workflow.app.ainvoke,
        input={"memo_id": memo_id, "raw_inputs": request.raw_inputs},
    )

    return {
        "memo_id": memo_id,
        "message": "Memo generation started in the background",
    }