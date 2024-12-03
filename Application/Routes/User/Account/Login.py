import time

from Routes.Base import Base

from Erebus.Networking.UserTypes.UserAccount import UserAccount
# from Erebus.Console.ConsoleOutput import ConsoleOutput

class Route(Base):

    def __init__(self):
        self.configuration = {
            "requirements": {
                "username": str,
                "password": str
            }
        }
        self._user_account = UserAccount()

    async def main(self):
        if not self.user_account.exists(username = self.username):
            return await self.websocket.send(
                success = False,
                message = "Invalid login credentials",
                type = self.constants.INVALID_USER_LOGIN
            )

        account = self.user_account.get(username = self.username)
        password_validation = await self.user_account.verify_password(self.request["password"])

        if not password_validation:
            return await self.websocket.send(
                success = False,
                message = "Invalid login credentials",
                type = self.constants.INVALID_USER_LOGIN
            )

        if not account["status"]:
            return await self.websocket.send(
                success = False,
                message = "Your account has not been activated yet. Please confirm your email address.",
                type = self.constants.INACTIVE_ACCOUNT
            )

        self.websocket.account = self.user_account

        await self.context.connection_handler.register_connection(self.websocket, "user")

        token = await self.context.jwt_controller.encode({
            "id": self.user_account.id,
            "expire_time": int(time.time() + 7200),
            "type": "user"
        })

        await self.websocket.send(
            success = True,
            message = "You have been logged in.",
            token = token,
            type = self.constants.USER_SUCCESSFUL_LOGIN
        )

        # ConsoleOutput.print("{} has logged in ({}).".format(self.websocket.account.username, self.websocket.ip_address))

    @property
    def username(self):
        return self.request["username"]

    @property
    def user_account(self):
        return self._user_account