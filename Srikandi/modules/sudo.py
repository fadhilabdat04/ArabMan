from pyrogram import filters
from pyrogram.types import Message

from Srikandi import BOT_ID, SUDOERS, app, eor
from Srikandi.core.decorators.errors import capture_err
from Srikandi.utils.dbfunctions import add_sudo, get_sudoers, remove_sudo
from Srikandi.utils.functions import restart

__MODULE__ = "Sudo"
__HELP__ = """
**THIS MODULE IS ONLY FOR DEVS**

.useradd - To Add A User In Sudoers.
.userdel - To Remove A User From Sudoers.
.sudoers - To List Sudo Users.

**NOTE:**

Never add anyone to sudoers unless you trust them,
sudo users can do anything with your account, they
can even delete your account.
"""


@app.on_message(filters.command("useradd") & filters.user(SUDOERS))
@capture_err
async def useradd(_, message: Message):
    if not message.reply_to_message:
        return await eor(
            message,
            text="Reply to someone's message to add him to sudoers.",
        )
    user_id = message.reply_to_message.from_user.id
    umention = (await app.get_users(user_id)).mention
    sudoers = await get_sudoers()
    if user_id in sudoers:
        return await eor(message, text=f"{umention} is already in sudoers.")
    if user_id == BOT_ID:
        return await eor(
            message, text="You can't add assistant bot in sudoers."
        )
    added = await add_sudo(user_id)
    if added:
        await eor(
            message,
            text=f"Successfully added {umention} in sudoers, Bot will be restarted now.",
        )
        return await restart(None)
    await eor(message, text="Something wrong happened, check logs.")


@app.on_message(filters.command("userdel") & filters.user(SUDOERS))
@capture_err
async def userdel(_, message: Message):
    if not message.reply_to_message:
        return await eor(
            message,
            text="Reply to someone's message to remove him to sudoers.",
        )
    user_id = message.reply_to_message.from_user.id
    umention = (await app.get_users(user_id)).mention
    if user_id not in await get_sudoers():
        return await eor(message, text=f"{umention} is not in sudoers.")
    removed = await remove_sudo(user_id)
    if removed:
        await eor(
            message,
            text=f"Successfully removed {umention} from sudoers, Bot will be restarted now.",
        )
        return await restart(None)
    await eor(message, text="Something wrong happened, check logs.")


@app.on_message(filters.command("sudoers") & filters.user(SUDOERS))
@capture_err
async def sudoers_list(_, message: Message):
    sudoers = await get_sudoers()
    text = ""
    for count, user_id in enumerate(sudoers, 1):
        user = await app.get_users(user_id)
        user = user.first_name if not user.mention else user.mention
        text += f"{count}. {user}\n"
    await eor(message, text=text)
