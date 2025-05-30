import tkinter as tk
from tkinter import messagebox
from models.data_models import load_users

class AccountController:
    def __init__(self, view):
        self.view = view
        self.users = load_users()

    

