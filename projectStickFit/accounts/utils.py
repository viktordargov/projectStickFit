import asyncio
from django.core.mail import send_mail


async def send_async_email(subject, message, recipient_list):
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(
        None,
        send_mail,
        subject,
        message,
        None,
        recipient_list,
    )
