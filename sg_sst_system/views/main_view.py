import flet as ft
from .incident_view import IncidentView
from agent.graph import SgsstAgent

class MainView(ft.UserControl):
    def __init__(self):
        super().__init__(expand=True)

        # Instantiate the SG-SST agent
        self.agent = SgsstAgent()

        # Pass the agent to the incident view
        self.incident_view = IncidentView(agent=self.agent)

        # In a real app, you might have more navigation destinations
        self.content_area = ft.Container(
            content=self.incident_view,
            expand=True,
            padding=ft.padding.all(20),
        )

    def build(self):
        # A simple layout for now, can be expanded with NavigationRail etc.
        return self.content_area
