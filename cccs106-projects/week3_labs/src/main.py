<<<<<<< HEAD
# 1. Import necessary libraries.
import flet as ft
import mysql.connector
from db_connection import connect_db

# 2. Define the main function and configure the page.
def main(page: ft.Page):
    
    page.window.center()
    page.window.frameless = True
    page.title = "User Login"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.window.height = 350
    page.window.width = 400
    page.bgcolor = ft.Colors.AMBER_ACCENT
    
    # If the device is in darkmode, this will set the app to light mode.
    page.theme_mode = ft.ThemeMode.LIGHT
    
# 3. Create the UI controls.
    # Login Title
    login_title = ft.Text(
                    "User Login",
                    text_align=ft.TextAlign.CENTER,
                    size=20,
                    weight=ft.FontWeight.BOLD,
                    font_family="Arial"
                    )
    
    # Username Input Field
    username_field = ft.TextField(
                        label="User name",
                        hint_text="Enter your username",
                        helper_text="This is your unique identifier",
                        width=300,
                        autofocus=True,
                        disabled=False,
                        icon = ft.Icons.PERSON,
                        bgcolor=ft.Colors.LIGHT_BLUE_ACCENT
                        )
    
    # Password Input Field
    password_field = ft.TextField(
                        label="Password",
                        hint_text="Enter your password",
                        helper_text="This is your secret key",
                        width=300,
                        disabled=False,
                        password=True,
                        can_reveal_password=True,
                        icon = ft.Icons.PASSWORD,
                        bgcolor=ft.Colors.LIGHT_BLUE_ACCENT
                    )

# 1. Create the login_click function.
    def login_click(e):
# 2. Create dialogs for feedback.
        # Success Dialog
        success_dialog = ft.AlertDialog(
            icon=ft.Icon(ft.Icons.CHECK_CIRCLE, color=ft.Colors.GREEN),
            title=ft.Text("Login Successful!", text_align=ft.TextAlign.CENTER),
            content=ft.Text("Welcome, " + username_field.value + "!", text_align=ft.TextAlign.CENTER),
            actions=[
                    ft.TextButton("OK", on_click=lambda e: page.close(success_dialog))
                    ]
        )
        
        # Failure Dialog
        failure_dialog = ft.AlertDialog(
            icon=ft.Icon(ft.Icons.ERROR, color=ft.Colors.RED),
            title=ft.Text("Login Failed", text_align=ft.TextAlign.CENTER),
            content=ft.Text("Invalid username or password", text_align=ft.TextAlign.CENTER),
            actions=[
                    ft.TextButton("OK", on_click=lambda e: page.close(failure_dialog))
                    ]
        )
        
        # Invalid Input Dialog
        invalid_input_dialog = ft.AlertDialog(
            icon=ft.Icon(ft.Icons.INFO_ROUNDED, color=ft.Colors.BLUE),
            title=ft.Text("Input Error", text_align=ft.TextAlign.CENTER),
            content=ft.Text("Please enter username and password", text_align=ft.TextAlign.CENTER),
            actions=[
                    ft.TextButton("OK", on_click=lambda e: page.close(invalid_input_dialog))
                    ]
        )
        
        # Database Error Dialog
        database_error_dialog = ft.AlertDialog(
            title=ft.Text("Database Error"),
            content=ft.Text("An error occurred while connecting to the database"),
            actions=[
                    ft.TextButton("OK", on_click=lambda e: page.close(database_error_dialog))
                    ]
        )
    
# 3. Add Validation and Database Logic.
        # Check if username or password are empty. If so, open invalid_input_dialog and return.
        if username_field.value == "" or password_field.value == "":
            page.open(invalid_input_dialog)
            return
        
        # Using a try-except block to handle mysql.connector.Error.
        try:
            connect = connect_db()                                              # Establish a database connection using connect_db().
            if connect is None:
                page.open(database_error_dialog)
                page.update()
                return
            
            cursor = connect.cursor()                                           # Create a cursor.

            query = "SELECT * FROM users WHERE username = %s AND password = %s" # Execute a parameterized SQL query to select a user where username and password match the input values. Crucially, emphasize the use of parameterized queries to prevent SQL injection.
            cursor.execute(query, (username_field.value, password_field.value))

            result = cursor.fetchone() is not None                              # Fetch the result.

            cursor.close()
            connect.close()                                                     # Close the database connection.

            if result:                                                          # If a result is found, open success_dialog; otherwise, open failure_dialog.
                page.open(success_dialog)
            else:
                page.open(failure_dialog)

            page.update()                                                       # Call page.update().

        # Inside the except block, open database_error_dialog and call page.update().
        except mysql.connector.Error as e:
            print(f"Database error: {e}")
            page.open(database_error_dialog)
            page.update()

# 4. Createt Login Button
    login_button = ft.ElevatedButton("Login",
                        on_click = login_click,
                        width = 100,
                        icon = ft.Icons.LOGIN
                        )

# 1. Add all controls to the page.
    page.add(login_title)
    page.add(ft.Container(content = ft.Column(controls=[username_field, password_field],
                            spacing = 20)))
    page.add(ft.Container(content = login_button,
                            alignment = ft.alignment.top_right,
                            margin = ft.Margin(0, 20, 40, 0)))

# 2. Start the Flet app.
ft.app(target=main)