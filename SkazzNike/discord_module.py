from dhooks import Webhook, Embed


class DiscordModule:
    def __init__(self):
        pass

    def send_to_discord(self, product, kind):
        embed = Embed(
            title="{}on Destroyer".format(product['name']),
            url='https://www.destroyshop.ru',
            color=2544107,
            timestamp='now'
        )
        embed.add_field(name='**Status**', value='NEW ' + kind, inline=False)
        embed.add_field(name='**Stock Status**', value=product['status'], inline=False)
        embed.add_field(name='**Price**', value=product['price'], inline=False)
        if product['status'] != 'OUT OF STOCK': embed.add_field(
            name='**Sizes**', value=''.join(product['sizes']),
            inline=False)
        embed.set_thumbnail('https://www.destroyshop.ru' + product['img'])

        embed.set_footer(text="Skazz for PP ", icon_url="https://i.imgur.com/5FvrLXq.png")

        for webhook in self.webhooks:
            try:
                hook = Webhook(webhook)
                hook.username = "Destroyer Monitor"
                hook.avatar_url = "https://upload.wikimedia.org/wikipedia/commons/6/60/Brandshop-usual-logo.png"
                hook.send(embed=embed)
                self.log("Posted status update to Discord webhook {}".format(webhook))
            except Exception as e:
                self.log("Error sending to Discord webhook {}".format(e))