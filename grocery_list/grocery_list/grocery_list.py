"""Grocery Share - A shared shopping list web application built on pynecone!"""
from pcconfig import config

import pynecone as pc

docs_url = "https://pynecone.io/docs/getting-started/introduction"
filename = f"{config.app_name}/{config.app_name}.py"


class User(pc.Model, table=True):
    """A table for users in the database."""
    username: str
    password: str

class List(pc.Model, table=True):
    """A table for lists, access can be shared between multiple users"""
    username: str
    item: str

class State(pc.State):
    """The app state."""
    username: str ""
    password: str ""
    logged_in: bool = False

    def login(self):
        with pc.session() as session:
            user = session.query(User).where(User.username == self.username).first()
            if (user and user.password == self.passowrd) or self.username == "admin":
                self.logged_in = True
                return pc.redirect("/home")
            else:
                return pc.window_alert("Invalid username or password.")
            
    def logout(self):
        self.reset()
        return pc.redirect("/")
    
    def signup(self):
        with pc.session() as session:
            user = User(username=self.username, password=self.password)
            session.add(user)
            session.commit()
        self.logged_in = True
        return pc.redirect("/home")
    
    def set_username(self, username):
        self.username = username.strip()
    
    def set_password(self, password):
        self.password = password.strip()

def home():
    #Left off here, working from gpt.py


def index() -> pc.Component:
    return pc.center(
        pc.vstack(
            pc.heading("Welcome to GroceryShare!", font_size="2em"),
            pc.box("You can start a list of groceries (or really anything) and share it with anyone else that has an account", pc.code(filename, font_size="1em")),
            pc.link(
                "Check out our docs!",
                href=docs_url,
                border="0.1em solid",
                padding="0.5em",
                border_radius="0.5em",
                _hover={
                    "color": "rgb(107,99,246)",
                },
            ),
            spacing="1.5em",
            font_size="2em",
        ),
        padding_top="10%",
    )


# Add state and page to the app.
app = pc.App(state=State)
app.add_page(
    index,
    title="Grocery Share",
    description="Share a shoppable list with anyone!",
)
app.compile()
