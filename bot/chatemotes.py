
async def main(self, message):
    if message.content.startswith('!kappa'):
        await self.send_message(message.channel, 'http://i.imgur.com/N5RzfBB.png')

    if message.content.startswith('!feelsbadman'):
        await self.send_message(message.channel, 'http://i.imgur.com/DfURIfh.png')

    if message.content.startswith('!feelsgoodman'):
        await self.send_message(message.channel, 'http://i.imgur.com/9Ggf2vs.png')

    if message.content.startswith('!lapz'):
        await self.send_message(message.channel, 'http://i.imgur.com/I0Lqf3w.png')