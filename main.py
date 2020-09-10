import time
from telethon.sync import TelegramClient
from telethon.tl.functions.channels import GetParticipantsRequest, InviteToChannelRequest
from telethon.tl.types import ChannelParticipantsSearch

API_ID = int(input("Введите API ID: telegram"))
API_HASH = input("Введите API HASH telegram: ")
USERNAME = "db"

client = TelegramClient(USERNAME, API_ID, API_HASH)
client.start()


async def parseChat(channel):
    offset_user = 0  
    limit_user = 100 

    all_participants = []
    filter_user = ChannelParticipantsSearch('')

    while True:
        participants = await client(GetParticipantsRequest(channel, filter_user, offset_user, limit_user, hash=0))
        if not participants.users:
            break
        for user in participants.users:
            all_participants.append(user.id)
        offset_user += len(participants.users)

    return all_participants

async def inviteChannel(ch, users):
    limitUser = 20
    while len(users) > 0:
        part = []
        for i in range(limitUser):
            if len(users) == 0:
                break
            part.append(users.pop())
        print(part)
        await client(InviteToChannelRequest(ch, part))
        print(" [X] Add new group users")
        time.sleep(30)


async def main():
    url = input("Введите ссылку на канал или чат донора: ")
    ch = input("Введите ссылку на канал или чат куда добавлять: ")
    channel = await client.get_entity(url)
    users = await parseChat(channel)
    await inviteChannel(ch, users)


with client:
    client.loop.run_until_complete(main())
