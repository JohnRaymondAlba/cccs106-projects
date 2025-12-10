"""Weather Application using Flet v0.28.3"""

import flet as ft
from weather_service import WeatherService
from config import Config
import json
from pathlib import Path


class WeatherApp:
    """Main Weather Application class."""
    
    def __init__(self, page: ft.Page):
        self.page = page
        self.weather_service = WeatherService()
        self.history_file = Path("search_history.json")
        self.search_history = self.load_history()
        self.setup_page()
        self.build_ui()
    
    def load_history(self):
        """Load search history from file."""
        if self.history_file.exists():
            with open(self.history_file, 'r') as f:
                return json.load(f)
        return []
    
    def save_history(self):
        """Save search history to file."""
        with open(self.history_file, 'w') as f:
            json.dump(self.search_history, f)
    
    def add_to_history(self, city: str):
        """Add city to search history."""
        if city not in self.search_history:
            self.search_history.insert(0, city)
            self.search_history = self.search_history[:5]  # Keep last 5
            self.save_history()
            self.update_history_dropdown()
        
    def setup_page(self):
        """Configure page settings."""
        self.page.title = Config.APP_TITLE
        
        # Use system theme (respects OS dark mode settings)
        self.page.theme_mode = ft.ThemeMode.SYSTEM
        
        # Custom theme with blue color scheme
        self.page.theme = ft.Theme(
            color_scheme_seed=ft.Colors.BLUE,
        )
        
        self.page.padding = 20
        self.page.scroll = ft.ScrollMode.AUTO
        
        # Window properties (accessed via page.window in Flet 0.28.3)
        self.page.window.width = Config.APP_WIDTH
        self.page.window.height = Config.APP_HEIGHT
        self.page.window.resizable = False
        
        # Center the window on desktop
        self.page.window.center()
    
    def build_ui(self):
        """Build the user interface."""
        # Title with gradient effect (using blue theme)
        self.title = ft.Text(
            "Weather App",
            size=36,
            weight=ft.FontWeight.BOLD,
            color=ft.Colors.BLUE_700,
        )
        
        # Theme toggle button with hover effect
        self.theme_button = ft.IconButton(
            icon=ft.Icons.DARK_MODE,
            tooltip="Toggle theme",
            on_click=self.toggle_theme,
            icon_size=24,
        )
        
        # Title row with theme button
        self.title_row = ft.Row(
            [
                self.title,
                self.theme_button,
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        )
        
        # History dropdown with enhanced styling
        self.history_dropdown = ft.Dropdown(
            label="Recent Searches",
            options=[ft.dropdown.Option(city) for city in self.search_history],
            on_change=self.load_from_history,
            width=300,
            border_color=ft.Colors.BLUE_300,
        )
        
        # City input field with enhanced styling
        self.city_input = ft.TextField(
            label="Enter city name",
            hint_text="e.g., London, Tokyo, New York",
            border_color=ft.Colors.BLUE_300,
            prefix_icon=ft.Icons.LOCATION_CITY,
            autofocus=True,
            on_submit=self.on_search,
            width=300,
        )
        
        # Container for input and dropdown
        self.input_container = ft.Column(
            [
                self.city_input,
                self.history_dropdown,
            ],
            spacing=8,
        )
        
        # Search button with enhanced styling and hover effect
        self.search_button = ft.ElevatedButton(
            "Get Weather",
            icon=ft.Icons.SEARCH,
            on_click=self.on_search,
            style=ft.ButtonStyle(
                color=ft.Colors.WHITE,
                bgcolor=ft.Colors.BLUE_700,
                padding=ft.padding.symmetric(horizontal=32, vertical=12),
                elevation=4,
            ),
        )
        
        # Weather display container with enhanced styling
        self.weather_container = ft.Container(
            visible=False,
            bgcolor=ft.Colors.LIGHT_BLUE_50,
            border_radius=15,
            padding=25,
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=8,
                color=ft.Colors.LIGHT_BLUE_100,
            ),
            border=ft.border.all(1, ft.Colors.LIGHT_BLUE_200),
        )
        
        # Error message with enhanced styling
        self.error_message = ft.Text(
            "",
            color=ft.Colors.RED_700,
            visible=False,
            size=14,
            weight=ft.FontWeight.W_500,
        )
        
        # Loading indicator with size adjustment
        self.loading = ft.ProgressRing(
            visible=False,
            value=None,
            stroke_width=4,
        )
        
        # Create alert banner
        self.alert_banner = ft.Container(
            visible=False,
            bgcolor=ft.Colors.AMBER_100,
            padding=15,
            border_radius=10,
            border=ft.border.all(2, ft.Colors.AMBER),
            content=ft.Row(
                [
                    ft.Icon(ft.Icons.WARNING, color=ft.Colors.AMBER, size=32),
                    ft.Column(
                        [
                            ft.Text("Alert", weight=ft.FontWeight.BOLD, size=16),
                            ft.Text("Alert message", size=12),
                        ],
                        expand=True,
                    ),
                    ft.IconButton(
                        ft.Icons.CLOSE,
                        on_click=self.dismiss_alert_banner,
                    ),
                ],
                spacing=10,
            ),
        )
        
        # Add all components to page
        self.page.add(
            ft.Column(
                [
                    self.alert_banner,
                    self.title_row,
                    ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
                    self.input_container,
                    self.search_button,
                    ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
                    self.loading,
                    self.error_message,
                    self.weather_container,
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=10,
            )
        )
    
    def update_history_dropdown(self):
        """Update the history dropdown options."""
        self.history_dropdown.options = [
            ft.dropdown.Option(city) for city in self.search_history
        ]
        self.history_dropdown.value = None  # Clear selection
        self.page.update()
    
    def load_from_history(self, e):
        """Load a city from history dropdown."""
        if e.control.value:
            self.city_input.value = e.control.value
            self.page.run_task(self.get_weather)
            # Clear dropdown selection after loading
            e.control.value = None
            self.page.update()
    
    def on_search(self, e):
        """Handle search button click or enter key press."""
        self.page.run_task(self.get_weather)
    
    def toggle_theme(self, e):
        """Toggle between light and dark theme."""
        if self.page.theme_mode == ft.ThemeMode.LIGHT:
            self.page.theme_mode = ft.ThemeMode.DARK
            self.theme_button.icon = ft.Icons.LIGHT_MODE
        else:
            self.page.theme_mode = ft.ThemeMode.LIGHT
            self.theme_button.icon = ft.Icons.DARK_MODE
        self.page.update()
    
    async def get_weather(self):
        """Fetch and display weather data with comprehensive error handling."""
        city = self.city_input.value.strip()
        
        # Validate input - empty city name
        if not city:
            self.show_error("Please enter a city name")
            return
        
        # Validate input - check for valid characters (optional but recommended)
        if len(city) > 50:
            self.show_error("City name is too long (max 50 characters)")
            return
        
        # Show loading state, hide previous results
        self.loading.visible = True
        self.error_message.visible = False
        self.weather_container.visible = False
        self.page.update()
        
        try:
            # Fetch weather data from service
            weather_data = await self.weather_service.get_weather(city)
            
            # Add successful search to history
            self.add_to_history(city)
            
            # Display the weather data (with animation)
            await self.display_weather(weather_data)
            
        except Exception as e:
            # Catch and display any errors (WeatherServiceError or unexpected)
            self.show_error(str(e))
        
        finally:
            # Always hide loading indicator, regardless of success or failure
            self.loading.visible = False
            self.page.update()
    
    def check_weather_alerts(self, temp: float, wind_speed: float, humidity: float):
        """Check for extreme weather conditions and display alerts."""
        print(f"DEBUG: Checking alerts - temp: {temp}, wind: {wind_speed}, humidity: {humidity}")
        
        alert_triggered = False
        alert_title = ""
        alert_msg = ""
        alert_color = ft.Colors.AMBER
        bg_color = ft.Colors.AMBER_100
        border_color = ft.Colors.AMBER
        
        # High temperature alert
        if temp > 35:
            alert_triggered = True
            alert_title = "⚠️ High Temperature Alert!"
            alert_msg = "Temperature exceeds 35°C"
            alert_color = ft.Colors.ORANGE
            bg_color = ft.Colors.ORANGE_100
            border_color = ft.Colors.ORANGE
        
        # Extreme wind alert
        elif wind_speed > 15:
            alert_triggered = True
            alert_title = "💨 Strong Wind Alert!"
            alert_msg = f"Wind speed: {wind_speed} m/s"
            alert_color = ft.Colors.RED
            bg_color = ft.Colors.RED_100
            border_color = ft.Colors.RED
        
        # Low humidity alert
        elif humidity < 30:
            alert_triggered = True
            alert_title = "💧 Low Humidity Alert!"
            alert_msg = f"Humidity: {humidity}%"
            alert_color = ft.Colors.AMBER
            bg_color = ft.Colors.AMBER_100
            border_color = ft.Colors.AMBER
        
        # High humidity alert
        elif humidity > 80:
            alert_triggered = True
            alert_title = "💧 High Humidity Alert!"
            alert_msg = f"Humidity: {humidity}%"
            alert_color = ft.Colors.BLUE
            bg_color = ft.Colors.BLUE_100
            border_color = ft.Colors.BLUE
        
        # Update banner
        if alert_triggered:
            print(f"DEBUG: Alert triggered - {alert_title}")
            self.alert_banner.bgcolor = bg_color
            self.alert_banner.border = ft.border.all(2, border_color)
            self.alert_banner.content = ft.Row(
                [
                    ft.Icon(ft.Icons.WARNING, color=alert_color, size=32),
                    ft.Column(
                        [
                            ft.Text(alert_title, weight=ft.FontWeight.BOLD, size=16, color=alert_color),
                            ft.Text(alert_msg, size=12, color=ft.Colors.BLACK),
                        ],
                        expand=True,
                    ),
                    ft.IconButton(
                        ft.Icons.CLOSE,
                        on_click=self.dismiss_alert_banner,
                    ),
                ],
                spacing=10,
            )
            self.alert_banner.visible = True
            print("DEBUG: Banner visible set to True")
        else:
            print("DEBUG: No alert triggered")
            self.alert_banner.visible = False
        
        self.page.update()
    
    def dismiss_banner(self, e):
        """Dismiss the alert banner."""
        self.page.banner.open = False
        self.page.update()
    
    def dismiss_alert_banner(self, e):
        """Dismiss the alert container."""
        self.alert_banner.visible = False
        self.page.update()
    
    async def display_weather(self, data: dict):

        """Display weather information with animation."""
        # Extract data
        city_name = data.get("name", "Unknown")
        country = data.get("sys", {}).get("country", "")
        temp = data.get("main", {}).get("temp", 0)
        feels_like = data.get("main", {}).get("feels_like", 0)
        humidity = data.get("main", {}).get("humidity", 0)
        description = data.get("weather", [{}])[0].get("description", "").title()
        icon_code = data.get("weather", [{}])[0].get("icon", "01d")
        wind_speed = data.get("wind", {}).get("speed", 0)
        
        # Check for extreme weather conditions and display alerts
        self.check_weather_alerts(temp, wind_speed, humidity)
        
        # Build weather display with enhanced styling
        self.weather_container.content = ft.Column(
            [
                # Location header with enhanced styling
                ft.Text(
                    f"{city_name}, {country}",
                    size=28,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.BLUE_900,
                ),
                
                ft.Divider(height=10, color=ft.Colors.LIGHT_BLUE_200),
                
                # Weather icon and description
                ft.Row(
                    [
                        ft.Image(
                            src=f"https://openweathermap.org/img/wn/{icon_code}@2x.png",
                            width=100,
                            height=100,
                        ),
                        ft.Column(
                            [
                                ft.Text(
                                    description,
                                    size=18,
                                    weight=ft.FontWeight.W_600,
                                    color=ft.Colors.BLUE_700,
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=10,
                ),
                
                ft.Divider(height=10, color=ft.Colors.LIGHT_BLUE_200),
                
                # Temperature with enhanced styling
                ft.Column(
                    [
                        ft.Text(
                            f"{temp:.1f}°C",
                            size=56,
                            weight=ft.FontWeight.BOLD,
                            color=ft.Colors.BLUE_900,
                        ),
                        
                        ft.Text(
                            f"Feels like {feels_like:.1f}°C",
                            size=14,
                            color=ft.Colors.BLUE_600,
                            weight=ft.FontWeight.W_500,
                        ),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=5,
                ),
                
                ft.Divider(height=15, color=ft.Colors.LIGHT_BLUE_200),
                
                # Additional info with better spacing
                ft.Row(
                    [
                        self.create_info_card(
                            ft.Icons.WATER_DROP,
                            "Humidity",
                            f"{humidity}%"
                        ),
                        self.create_info_card(
                            ft.Icons.AIR,
                            "Wind Speed",
                            f"{wind_speed} m/s"
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_AROUND,
                    spacing=10,
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=12,
        )
        
        # Setup animation - start with opacity 0
        self.weather_container.animate_opacity = 300  # 300ms animation duration
        self.weather_container.opacity = 0
        self.weather_container.visible = True
        self.error_message.visible = False
        self.page.update()
        
        # Small delay to ensure container is rendered before animation
        import asyncio
        await asyncio.sleep(0.05)
        
        # Fade in animation
        self.weather_container.opacity = 1
        self.page.update()
    
    def create_info_card(self, icon, label, value):
        """Create an enhanced info card for weather details."""
        return ft.Container(
            content=ft.Column(
                [
                    ft.Icon(icon, size=32, color=ft.Colors.BLUE_700),
                    ft.Text(label, size=11, color=ft.Colors.BLUE_600, weight=ft.FontWeight.W_500),
                    ft.Text(
                        value,
                        size=18,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.BLUE_900,
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=6,
            ),
            bgcolor=ft.Colors.WHITE,
            border_radius=12,
            padding=18,
            width=140,
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=4,
                color=ft.Colors.LIGHT_BLUE_100,
            ),
            border=ft.border.all(1, ft.Colors.LIGHT_BLUE_200),
        )
    
    def show_error(self, message: str):
        """
        Display error message to user with enhanced visual feedback.
        
        Args:
            message: Error message to display
        """
        # Ensure message is a string and not None
        message = str(message) if message else "An unexpected error occurred"
        
        # Format error message with visual indicator
        self.error_message.value = f"❌ {message}"
        self.error_message.visible = True
        
        # Hide weather container to show error prominently
        self.weather_container.visible = False
        
        # Update page to display error immediately
        self.page.update()


def main(page: ft.Page):
    """Main entry point."""
    WeatherApp(page)


if __name__ == "__main__":
    ft.app(target=main)