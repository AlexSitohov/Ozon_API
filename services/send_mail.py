from fastapi import APIRouter, BackgroundTasks, Depends, status
from back_task_send_email import send_email

from JWT import get_current_user

router = APIRouter(tags=['mail'], prefix="/report")


def create_background_task(background_tasks: BackgroundTasks, user, order):
    background_tasks.add_task(send_email, user, order)

