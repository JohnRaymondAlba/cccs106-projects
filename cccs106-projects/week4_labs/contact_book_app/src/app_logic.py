import flet as ft
from database import update_contact_db, delete_contact_db, add_contact_db, get_all_contacts_db

def display_contacts(page, contacts_list_view, db_conn, search_term=None):
    """Fetches and displays all contacts in the ListView with modern card design."""
    contacts_list_view.controls.clear()
    contacts = get_all_contacts_db(db_conn, search_term)
    
    if not contacts:
        # Show message when no contacts found
        message = "No contacts found." if search_term else "No contacts yet. Add your first contact!"
        contacts_list_view.controls.append(
            ft.Container(
                content=ft.Text(
                    message,
                    size=16,
                    color=ft.Colors.GREY_600,
                    text_align=ft.TextAlign.CENTER
                ),
                alignment=ft.alignment.center,
                padding=20
            )
        )
    else:
        for contact in contacts:
            contact_id, name, phone, email = contact
            
            # Create contact card 
            card = ft.Card(
                content=ft.Container(
                    content=ft.Column([
                        ft.Row([
                            ft.Icon(ft.Icons.PERSON, color=ft.Colors.BLUE_400, size=20),
                            ft.Text(name, size=18, weight=ft.FontWeight.BOLD),
                            ft.PopupMenuButton(
                                icon=ft.Icons.MORE_VERT,
                                items=[
                                    ft.PopupMenuItem(
                                        text="Edit",
                                        icon=ft.Icons.EDIT,
                                        on_click=lambda _, c=contact: open_edit_dialog(page, c, db_conn, contacts_list_view)
                                    ),
                                    ft.PopupMenuItem(),  # Divider
                                    ft.PopupMenuItem(
                                        text="Delete",
                                        icon=ft.Icons.DELETE,
                                        on_click=lambda _, cid=contact_id, n=name: show_delete_confirmation(page, cid, n, db_conn, contacts_list_view)
                                    ),
                                ],
                            ),
                        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                        
                        # Phone number row
                        ft.Row([
                            ft.Icon(ft.Icons.PHONE, color=ft.Colors.GREEN_400, size=16),
                            ft.Text(phone or "No phone", size=14, color=ft.Colors.GREY_700),
                        ]) if phone else ft.Row([
                            ft.Icon(ft.Icons.PHONE_DISABLED, color=ft.Colors.GREY_400, size=16),
                            ft.Text("No phone", size=14, color=ft.Colors.GREY_500),
                        ]),
                        
                        # Email row
                        ft.Row([
                            ft.Icon(ft.Icons.EMAIL, color=ft.Colors.ORANGE_400, size=16),
                            ft.Text(email or "No email", size=14, color=ft.Colors.GREY_700),
                        ]) if email else ft.Row([
                            ft.Icon(ft.Icons.EMAIL_OUTLINED, color=ft.Colors.GREY_400, size=16),
                            ft.Text("No email", size=14, color=ft.Colors.GREY_500),
                        ]),
                    ], spacing=8),
                    padding=15
                ),
                elevation=2
            )
            
            contacts_list_view.controls.append(card)
    
    page.update()

def add_contact(page, inputs, contacts_list_view, db_conn, search_input=None):
    """Adds a new contact with input validation and refreshes the list."""
    name_input, phone_input, email_input = inputs
    
    # Clear previous error
    name_input.error_text = None
    
    # Validate name input
    if not name_input.value or not name_input.value.strip():
        name_input.error_text = "Name cannot be empty"
        page.update()
        return
    
    # Add the contact to database
    add_contact_db(db_conn, name_input.value.strip(), phone_input.value.strip(), email_input.value.strip())
    
    # Clear all input fields
    for field in inputs:
        field.value = ""
    
    # Clear search to show all contacts including the new one
    if search_input:
        search_input.value = ""
    
    # Refresh the contacts list
    display_contacts(page, contacts_list_view, db_conn)
    
    # Show success message
    page.open(
        ft.SnackBar(
            content=ft.Text("Contact added successfully!"),
            bgcolor=ft.Colors.GREEN_400
        )
    )

def show_delete_confirmation(page, contact_id, contact_name, db_conn, contacts_list_view):
    """Shows a confirmation dialog before deleting a contact."""
    def confirm_delete(e):
        delete_contact_db(db_conn, contact_id)
        display_contacts(page, contacts_list_view, db_conn)
        confirmation_dialog.open = False
        page.update()
        page.open(
            ft.SnackBar(
                content=ft.Text(f"Contact '{contact_name}' deleted successfully!"),
                bgcolor=ft.Colors.RED_400
            )
        )
    
    def cancel_delete(e):
        confirmation_dialog.open = False
        page.update()
    
    confirmation_dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("Confirm Delete"),
        content=ft.Text(f"Are you sure you want to delete '{contact_name}'?\nThis action cannot be undone."),
        actions=[
            ft.TextButton("Cancel", on_click=cancel_delete),
            ft.TextButton(
                "Delete", 
                on_click=confirm_delete,
                style=ft.ButtonStyle(color=ft.Colors.RED_400)
            ),
        ],
    )
    
    page.open(confirmation_dialog)

def delete_contact(page, contact_id, db_conn, contacts_list_view):
    """Deletes a contact and refreshes the list."""
    delete_contact_db(db_conn, contact_id)
    display_contacts(page, contacts_list_view, db_conn)

def open_edit_dialog(page, contact, db_conn, contacts_list_view):
    """Opens a dialog to edit a contact's details with improved UI."""
    contact_id, name, phone, email = contact
    
    edit_name = ft.TextField(label="Name", value=name, width=300)
    edit_phone = ft.TextField(label="Phone", value=phone or "", width=300)
    edit_email = ft.TextField(label="Email", value=email or "", width=300)

    def save_and_close(e):
        # Validate name
        if not edit_name.value or not edit_name.value.strip():
            edit_name.error_text = "Name cannot be empty"
            page.update()
            return
        
        edit_name.error_text = None
        update_contact_db(db_conn, contact_id, edit_name.value.strip(), 
                         edit_phone.value.strip(), edit_email.value.strip())
        dialog.open = False
        page.update()
        display_contacts(page, contacts_list_view, db_conn)
        page.open(
            ft.SnackBar(
                content=ft.Text("Contact updated successfully!"),
                bgcolor=ft.Colors.BLUE_400
            )
        )

    def cancel_edit(e):
        dialog.open = False
        page.update()

    dialog = ft.AlertDialog(
        modal=True,
        title=ft.Row([
            ft.Icon(ft.Icons.EDIT, color=ft.Colors.BLUE_400),
            ft.Text("Edit Contact")
        ]),
        content=ft.Column([
            edit_name,
            edit_phone,
            edit_email
        ], width=300, spacing=10),
        actions=[
            ft.TextButton("Cancel", on_click=cancel_edit),
            ft.TextButton(
                "Save Changes", 
                on_click=save_and_close,
                style=ft.ButtonStyle(color=ft.Colors.BLUE_400)
            ),
        ],
    )

    page.open(dialog)

def search_contacts(page, contacts_list_view, db_conn, search_term):
    """Filters contacts based on search term."""
    display_contacts(page, contacts_list_view, db_conn, search_term)