from Members.Member import check_if_user_in_database, add_user_to_database, User
from bin.quick_access import Users
from bin.needed_vars import *

def create_user_object(member):
    User_data = check_if_user_in_database(member.id)
    UserObj = None
    
    if User_data:
        UserObj = User(DiscordID=member.id, Money=User_data[0], Items=User_data[1])
    else:
        UserObj = User(member.id)
        add_user_to_database(UserObj)
    
    Users[member.id] = UserObj
    
def start(client):
    log.info("[+] Creating User objects...")
    for guild in client.guilds:
        for member in guild.members:
            if not member.bot:
                create_user_object(member)