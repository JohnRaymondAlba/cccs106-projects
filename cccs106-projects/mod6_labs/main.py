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
        self.temp_pref_file = Path("temp_preference.json")
        self.search_history = self.load_history()
        self.temp_unit = self.load_temp_preference()  # "C" or "F"
        self.current_weather_data = None  # Store current weather data for unit conversion
        self.setup_page()
        self.build_ui()
    
    def load_history(self):
        """Load search history from file."""
        if self.history_file.exists():
            with open(self.history_file, 'r') as f:
                return json.load(f)
        return []
    
    def load_temp_preference(self):
        """Load temperature unit preference from file."""
        if self.temp_pref_file.exists():
            with open(self.temp_pref_file, 'r') as f:
                data = json.load(f)
                return data.get("unit", "C")
        return "C"  # Default to Celsius
    
    def save_temp_preference(self):
        """Save temperature unit preference to file."""
        with open(self.temp_pref_file, 'w') as f:
            json.dump({"unit": self.temp_unit}, f)
    
    def save_history(self):
        """Save search history to file."""
        with open(self.history_file, 'w') as f:
            json.dump(self.search_history, f)
    
    def celsius_to_fahrenheit(self, celsius: float) -> float:
        """Convert Celsius to Fahrenheit."""
        return (celsius * 9/5) + 32
    
    def fahrenheit_to_celsius(self, fahrenheit: float) -> float:
        """Convert Fahrenheit to Celsius."""
        return (fahrenheit - 32) * 5/9
    
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
        
        self.page.padding = 16
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
            "🌤️ Weather",
            size=32,
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
        
        # Temperature unit toggle button
        self.temp_unit_button = ft.IconButton(
            icon=ft.Icons.THERMOSTAT,
            tooltip=f"Temperature: {self.temp_unit}°",
            on_click=self.toggle_temp_unit,
            icon_size=24,
        )
        
        # Title row with theme button and temperature button
        self.title_row = ft.Row(
            [
                self.title,
                ft.Row(
                    [
                        self.temp_unit_button,
                        self.theme_button,
                    ],
                    spacing=5,
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        )
        
        # History dropdown with enhanced styling
        self.history_dropdown = ft.Dropdown(
            label="Recent Searches",
            options=[ft.dropdown.Option(city) for city in self.search_history],
            on_change=self.load_from_history,
            width=450,
            border_color=ft.Colors.BLUE_300,
            dense=True,
        )
        
        # City input field with enhanced styling
        self.city_input = ft.TextField(
            label="Search City",
            hint_text="e.g., London, Tokyo, New York",
            border_color=ft.Colors.BLUE_300,
            prefix_icon=ft.Icons.LOCATION_CITY,
            autofocus=True,
            on_submit=self.on_search,
            width=450,
            dense=True,
        )
        
        # Container for input and dropdown
        self.input_container = ft.Column(
            [
                self.city_input,
                self.history_dropdown,
            ],
            spacing=4,
        )
        
        # Search button with enhanced styling and hover effect
        self.search_button = ft.ElevatedButton(
            "Search",
            icon=ft.Icons.SEARCH,
            on_click=self.on_search,
            style=ft.ButtonStyle(
                color=ft.Colors.WHITE,
                bgcolor=ft.Colors.BLUE_700,
                padding=ft.padding.symmetric(horizontal=48, vertical=14),
                elevation=6,
            ),
            width=200,
        )
        
        # Weather display container with enhanced styling
        self.weather_container = ft.Container(
            visible=False,
            bgcolor=ft.Colors.LIGHT_BLUE_50,
            border_radius=20,
            padding=18,
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=12,
                color=ft.Colors.LIGHT_BLUE_200,
            ),
            border=ft.border.all(1, ft.Colors.LIGHT_BLUE_200),
        )
        
        # 5-day forecast container
        self.forecast_container = ft.Container(
            visible=False,
            bgcolor=ft.Colors.LIGHT_BLUE_50,
            border_radius=20,
            padding=14,
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=12,
                color=ft.Colors.LIGHT_BLUE_200,
            ),
            border=ft.border.all(1, ft.Colors.LIGHT_BLUE_200),
        )
        
        # Forecast header
        self.forecast_header = ft.Text(
            "📅 5-Day Forecast",
            size=20,
            weight=ft.FontWeight.BOLD,
            color=ft.Colors.BLUE_700,
            visible=False,
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
            padding=12,
            border_radius=12,
            border=ft.border.all(1, ft.Colors.AMBER),
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=8,
                color=ft.Colors.AMBER_200,
            ),
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
                    ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
                    self.input_container,
                    ft.Row(
                        [self.search_button],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
                    self.loading,
                    self.error_message,
                    # Current weather
                    self.weather_container,
                    # Forecast section
                    ft.Divider(height=8, color=ft.Colors.TRANSPARENT),
                    self.forecast_header,
                    self.forecast_container,
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=8,
                expand=True,
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
    
    def toggle_temp_unit(self, e):
        """Toggle between Celsius and Fahrenheit."""
        if self.temp_unit == "C":
            self.temp_unit = "F"
        else:
            self.temp_unit = "C"
        
        # Save preference
        self.save_temp_preference()
        
        # Update button tooltip
        self.temp_unit_button.tooltip = f"Temperature: {self.temp_unit}°"
        
        # Redisplay weather if data exists
        if self.current_weather_data:
            self.page.run_task(self.redisplay_weather)
        
        self.page.update()
    
    async def redisplay_weather(self):
        """Redisplay current weather with new temperature unit."""
        if self.current_weather_data:
            await self.display_weather(self.current_weather_data)
    
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
        self.forecast_container.visible = False
        self.forecast_header.visible = False
        self.page.update()
        
        try:
            # Fetch current weather and forecast data from service
            weather_data = await self.weather_service.get_weather(city)
            forecast_data = await self.weather_service.get_forecast(city)
            
            # Add successful search to history
            self.add_to_history(city)
            
            # Display the weather data (with animation)
            await self.display_weather(weather_data)
            
            # Display the forecast
            self.display_forecast(forecast_data)
            
            # Show forecast header
            self.forecast_header.visible = True
            self.error_message.visible = False
            self.page.update()
            
        except Exception as e:
            # Catch and display any errors (WeatherServiceError or unexpected)
            self.show_error(str(e))
        
        finally:
            # Always hide loading indicator, regardless of success or failure
            self.loading.visible = False
            self.page.update()
    
    def check_weather_alerts(self, temp_celsius: float, wind_speed: float, humidity: float, temp_unit: str):
        """Check for extreme weather conditions and display alerts."""
        alert_triggered = False
        alert_title = ""
        alert_msg = ""
        alert_color = ft.Colors.AMBER
        bg_color = ft.Colors.AMBER_100
        border_color = ft.Colors.AMBER
        
        # High temperature alert (>35°C or >95°F)
        if temp_celsius > 35:
            alert_triggered = True
            alert_title = "⚠️ High Temperature Alert!"
            if temp_unit == "F":
                display_temp = self.celsius_to_fahrenheit(temp_celsius)
                alert_msg = f"Temperature exceeds 95°F ({display_temp:.1f}°F)"
            else:
                alert_msg = f"Temperature exceeds 35°C ({temp_celsius:.1f}°C)"
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
        else:
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
        # Store current weather data for unit conversion
        self.current_weather_data = data
        
        # Extract data
        city_name = data.get("name", "Unknown")
        country = data.get("sys", {}).get("country", "")
        temp_celsius = data.get("main", {}).get("temp", 0)
        feels_like_celsius = data.get("main", {}).get("feels_like", 0)
        humidity = data.get("main", {}).get("humidity", 0)
        description = data.get("weather", [{}])[0].get("description", "").title()
        icon_code = data.get("weather", [{}])[0].get("icon", "01d")
        wind_speed = data.get("wind", {}).get("speed", 0)
        
        # Convert temperatures if Fahrenheit is selected
        if self.temp_unit == "F":
            temp = self.celsius_to_fahrenheit(temp_celsius)
            feels_like = self.celsius_to_fahrenheit(feels_like_celsius)
            temp_unit_display = "°F"
        else:
            temp = temp_celsius
            feels_like = feels_like_celsius
            temp_unit_display = "°C"
        
        # Check for extreme weather conditions and display alerts (always use Celsius for thresholds)
        self.check_weather_alerts(temp_celsius, wind_speed, humidity, self.temp_unit)
        
        # Build weather display with enhanced styling
        self.weather_container.content = ft.Column(
            [
                # Location header with enhanced styling
                ft.Text(
                    f"{city_name}, {country}",
                    size=24,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.BLUE_900,
                ),
                
                ft.Divider(height=6, color=ft.Colors.LIGHT_BLUE_200),
                
                # Weather icon and description in a row
                ft.Row(
                    [
                        ft.Image(
                            src=f"https://openweathermap.org/img/wn/{icon_code}@2x.png",
                            width=80,
                            height=80,
                        ),
                        ft.Column(
                            [
                                ft.Text(
                                    description,
                                    size=16,
                                    weight=ft.FontWeight.W_600,
                                    color=ft.Colors.BLUE_700,
                                ),
                                ft.Text(
                                    f"{temp:.1f}{temp_unit_display}",
                                    size=32,
                                    weight=ft.FontWeight.BOLD,
                                    color=ft.Colors.BLUE_900,
                                ),
                                ft.Text(
                                    f"Feels like {feels_like:.1f}{temp_unit_display}",
                                    size=12,
                                    color=ft.Colors.BLUE_600,
                                    weight=ft.FontWeight.W_500,
                                ),
                            ],
                            spacing=2,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.START,
                    spacing=10,
                ),
                
                ft.Divider(height=6, color=ft.Colors.LIGHT_BLUE_200),
                
                # Additional info cards in a more compact grid
                ft.Row(
                    [
                        self.create_info_card(
                            ft.Icons.WATER_DROP,
                            "Humidity",
                            f"{humidity}%"
                        ),
                        self.create_info_card(
                            ft.Icons.AIR,
                            "Wind",
                            f"{wind_speed} m/s"
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_AROUND,
                    spacing=8,
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.START,
            spacing=4,
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
    
    def display_forecast(self, data: dict):
        """Display 5-day weather forecast."""
        try:
            from datetime import datetime
            
            # Extract forecast data
            forecast_list = data.get("list", [])
            
            if not forecast_list:
                print("No forecast data available")
                return
            
            # Group forecasts by day (take one entry per day at noon)
            daily_forecasts = {}
            for item in forecast_list:
                dt = datetime.fromtimestamp(item["dt"])
                day = dt.date()
                
                # Take the entry closest to noon
                hour = dt.hour
                if day not in daily_forecasts or abs(hour - 12) < abs(datetime.fromtimestamp(daily_forecasts[day]["dt"]).hour - 12):
                    daily_forecasts[day] = item
            
            # Get the next 5 days
            forecast_days = sorted(list(daily_forecasts.items()))[:5]
            
            if not forecast_days:
                print("No forecast days found")
                return
            
            # Create forecast cards
            forecast_row = ft.Column(
                [
                    self.create_forecast_card(day, forecast_data)
                    for day, forecast_data in forecast_days
                ],
                spacing=6,
            )
            
            self.forecast_container.content = forecast_row
            self.forecast_container.visible = True
            print(f"Forecast displayed with {len(forecast_days)} days")
            
        except Exception as e:
            print(f"Error displaying forecast: {e}")
            import traceback
            traceback.print_exc()
    
    def create_forecast_card(self, day, forecast_data):
        """Create a forecast card for a specific day."""
        from datetime import datetime
        
        # Extract data
        temp_min = forecast_data.get("main", {}).get("temp_min", 0)
        temp_max = forecast_data.get("main", {}).get("temp_max", 0)
        description = forecast_data.get("weather", [{}])[0].get("description", "").title()
        icon_code = forecast_data.get("weather", [{}])[0].get("icon", "01d")
        humidity = forecast_data.get("main", {}).get("humidity", 0)
        
        # Convert temperatures if Fahrenheit is selected
        if self.temp_unit == "F":
            temp_min = self.celsius_to_fahrenheit(temp_min)
            temp_max = self.celsius_to_fahrenheit(temp_max)
            temp_unit = "°F"
        else:
            temp_unit = "°C"
        
        # Format day name
        day_name = day.strftime("%a, %b %d")
        
        return ft.Container(
            content=ft.Row(
                [
                    ft.Column(
                        [
                            ft.Text(day_name, size=12, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_900),
                            ft.Text(description, size=10, color=ft.Colors.BLUE_600),
                        ],
                        spacing=2,
                        expand=True,
                    ),
                    ft.Image(
                        src=f"https://openweathermap.org/img/wn/{icon_code}.png",
                        width=50,
                        height=50,
                    ),
                    ft.Column(
                        [
                            ft.Text(f"{temp_max:.0f}{temp_unit}", size=12, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_900),
                            ft.Text(f"{temp_min:.0f}{temp_unit}", size=10, color=ft.Colors.BLUE_600),
                        ],
                        spacing=1,
                        horizontal_alignment=ft.CrossAxisAlignment.END,
                    ),
                ],
                spacing=10,
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            bgcolor=ft.Colors.WHITE,
            border_radius=14,
            padding=12,
            border=ft.border.all(1, ft.Colors.LIGHT_BLUE_200),
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=4,
                color=ft.Colors.LIGHT_BLUE_100,
            ),
        )
    
    def create_info_card(self, icon, label, value):
        """Create an enhanced info card for weather details."""
        return ft.Container(
            content=ft.Column(
                [
                    ft.Icon(icon, size=32, color=ft.Colors.BLUE_700),
                    ft.Text(label, size=11, color=ft.Colors.BLUE_600, weight=ft.FontWeight.W_600),
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
            border_radius=14,
            padding=14,
            width=150,
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=6,
                color=ft.Colors.LIGHT_BLUE_200,
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