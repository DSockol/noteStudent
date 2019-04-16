from application.modules.managers.BaseManager import BaseManager


class WSManager(BaseManager):

    def __init__(self, options):
        super().__init__(options)
        self.socket.on(self.SOCKET_EVENTS['START_CONNECTION'], self.connect)
        self.socket.on(self.SOCKET_EVENTS['SEND_MESSAGE'], self.getMessage)

    def getUser(self, token):
        users = self.mediator.get(self.TRIGGERS['GET_ACTIVE_USERS'])
        if token in users.keys():
            return users[token]

    def getUserBySocketId(self, socketId):
        users = self.mediator.get(self.TRIGGERS['GET_ACTIVE_USERS'])
        for u in users:
            if users[u].socketId == socketId:
                return users[u]

    # Поднять сокетное соединение
    async def connect(self, data, ws):
        if data['id']:
            user = self.getUser(data['token'])
            self.socket.wss[data['id']] = ws  # запомнить сокет клиента в список сокетов
            user.socketId = data['id']
            await self.socket.emit(self.SOCKET_EVENTS['SEND_MESSAGE_TO_ALL'],
                                   {'text': 'Пользователь ' + user.name + ' подключился!', 'id': data['id'], 'name': user.name})
            print('START_CONNECTION: ' + data['id'])

    async def getMessage(self, data, ws):
        user = self.getUserBySocketId(data['id'])
        await self.socket.emit(self.SOCKET_EVENTS['SEND_MESSAGE_TO_ALL'], {'text': data['text'], 'id': data['id'], 'name': user.name})