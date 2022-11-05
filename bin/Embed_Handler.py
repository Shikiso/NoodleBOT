import discord

class embed:

	def __init__(self, title, description=None, color=discord.Colour.default(), url=None, icon=None, author=None, footer=None, fields=None):
		self.e = None

		if url and description:
			self.e = discord.Embed(title=title, description=description, url=url, color=color)
		elif url:
			self.e = discord.Embed(title=title, url=url, color=color)
		elif description:
			self.e = discord.Embed(title=title, description=description, color=color)
		else:
			self.e = discord.Embed(title=title, color=color)
		
		if author:
			name, link, icon_url = author
			if link and icon_url:
				self.e.set_author(name=name, url=link, icon_url=icon_url)
			elif link:
				self.e.set_author(name=name, url=link)
			elif icon_url:
				self.e.set_author(name=name, icon_url=icon_url)
		
		if icon:
			self.e.set_thumbnail(url=icon)
		
		if footer:
			self.e.set_footer(text=footer)
		
		if fields:
			# [(Name='', Value='', Inline=True), (Name='', Value=None, Inline=False)]
			for field in fields:
				name, value, inline = field
				self.field(name, value, inline)			
	
	def field(self, name, value, inline=False):
		self.e.add_field(name=name, value=value, inline=inline)
	
	def get_embed(self):
		return self.e