class OAuthInfo:
    def __init__(self):
        self.client_id = ''
        self.client_secret = ''
        self.user_agent = ''
        self.is_set = False

    def set_info(self, id, secret, agent):
        if id is '' or secret is '' or agent is '':
            return

        self.client_id = id
        self.client_secret = secret
        self.user_agent = agent
        self.is_set = True

    def set_info_by_input(self):
        self.client_id = input('Input your client id: ')
        self.client_secret = input('Input your client secret: ')
        self.user_agent = input('Input your authenticated user name: ')
        self.is_set = True
