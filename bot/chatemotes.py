import yaml

# Loading configurations from config.yaml
with open('../configuration/config.yaml', 'r') as f:
    doc = yaml.load(f)

prefix = doc['BOT']['command_prefix']

# Chat emotes list starts from here-----------------------------------------------
async def main(self, message):
    if message.content.startswith(prefix+'kappa'):
        await self.send_message(message.channel, 'http://i.imgur.com/N5RzfBB.png')

    if message.content.startswith(prefix+'feelsbadman'):
        await self.send_message(message.channel, 'http://i.imgur.com/DfURIfh.png')

    if message.content.startswith(prefix+'feelsgoodman'):
        await self.send_message(message.channel, 'http://i.imgur.com/9Ggf2vs.png')

    if message.content.startswith(prefix+'lapz'):
        await self.send_message(message.channel, 'http://i.imgur.com/I0Lqf3w.png')
