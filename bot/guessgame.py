import random

async def guess(self, message):
    await self.send_message(message.channel, 'Guess a number between 1 to 10')

    def guess_check(m1):
        return m1.content.isdigit()

    guesst = await self.wait_for_message(timeout=5.0, author=message.author, check=guess_check)
    answer = random.randint(1, 10)
    if guesst is None:
        fmt = 'Sorry, you took too long. It was {}.'
        await self.send_message(message.channel, fmt.format(answer))
        return
    if int(guesst.content) == answer:
        await self.send_message(message.channel, 'You are right!')
    else:
        await self.send_message(message.channel, 'Sorry. It is actually {}.'.format(answer))
