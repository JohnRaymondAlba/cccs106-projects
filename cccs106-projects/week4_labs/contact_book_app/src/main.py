import flet as ft
from database import init_db
from app_logic import display_contacts, add_contact, search_contacts

def main(page: ft.Page):
    page.title = "Contact Book"
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.window.width = 430
    page.window.height = 700
    
    # Initialize database
    db_conn = init_db()
    
    # Input fields
    name_input = ft.TextField(label="Name", width=380)
    phone_input = ft.TextField(label="Phone", width=380)
    email_input = ft.TextField(label="Email", width=380)
    
    inputs = (name_input, phone_input, email_input)
    
    # Search field
    search_input = ft.TextField(
        label="Search contacts...",
        width=380,
        prefix_icon=ft.Icons.SEARCH
    )
    
    # Contacts list view
    contacts_list_view = ft.ListView(expand=1, spacing=10, auto_scroll=True)
    
    # Add contact button
    add_button = ft.ElevatedButton(
        text="Add Contact",
        icon=ft.Icons.PERSON_ADD,
        on_click=lambda e: add_contact(page, inputs, contacts_list_view, db_conn, search_input)
    )
    
    # Theme toggle switch
    def toggle_theme(e):
        if page.theme_mode == ft.ThemeMode.LIGHT:
            page.theme_mode = ft.ThemeMode.DARK
            theme_switch.label = "Light Mode"
            theme_switch.icon = ft.Icons.LIGHT_MODE
        else:
            page.theme_mode = ft.ThemeMode.LIGHT
            theme_switch.label = "Dark Mode"
            theme_switch.icon = ft.Icons.DARK_MODE
        page.update()
    
    theme_switch = ft.ElevatedButton(
        text="Dark Mode",
        icon=ft.Icons.DARK_MODE,
        on_click=toggle_theme
    )
    
    # Search functionality
    def on_search_change(e):
        search_contacts(page, contacts_list_view, db_conn, search_input.value)
    
    search_input.on_change = on_search_change
    
    # Main layout
    page.add(
        ft.Container(
            content=ft.Column(
                [
                    # Header with theme toggle
                    ft.Row(
                        [
                            ft.Text("Contact Book", size=24, weight=ft.FontWeight.BOLD),
                            theme_switch
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                    ),
                    ft.Divider(),
                    
                    # Add contact section
                    ft.Text("Add New Contact:", size=18, weight=ft.FontWeight.W_500),
                    name_input,
                    phone_input,
                    email_input,
                    add_button,
                    ft.Divider(height=20),
                    
                    # Search and contacts section
                    ft.Text("Your Contacts:", size=18, weight=ft.FontWeight.W_500),
                    search_input,
                    ft.Container(height=10),  # Spacing
                    contacts_list_view,
                ],
                spacing=5,
                scroll=ft.ScrollMode.AUTO  # Enable scrolling
            ),
            padding=20,
            expand=True  # Take full height
        )
    )
    
    # Load initial contacts
    display_contacts(page, contacts_list_view, db_conn)

if __name__ == "__main__":
    ft.app(target=main)