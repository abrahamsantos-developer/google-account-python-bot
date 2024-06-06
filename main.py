import argparse
import time
from playwright.sync_api import sync_playwright

def get_month_in_english(spanish_month):
    months_mapping = {
        "enero": "January", "febrero": "February", "marzo": "March",
        "abril": "April", "mayo": "May", "junio": "June",
        "julio": "July", "agosto": "August", "septiembre": "September",
        "octubre": "October", "noviembre": "November", "diciembre": "December"
    }
    return months_mapping.get(spanish_month.lower(), spanish_month)

def get_gender_normalized(gender):
    gender_mapping = {
        "masculino": "Male", "hombre": "Male", "male": "Male",
        "femenino": "Female", "mujer": "Female", "female": "Female"
    }
    return gender_mapping.get(gender.lower(), gender)

def run(playwright, first_name, last_name, birth_month, birth_day, birth_year, gender):
    browser = playwright.chromium.launch(channel="chrome", headless=False)
    context = browser.new_context()
    page = context.new_page()

    # Navegar a la página de creación de cuenta de Google
    page.goto("https://accounts.google.com/signup")

    # Esperar a que los campos estén disponibles y llenarlos en la primera pantalla
    page.wait_for_selector("input[name='firstName']")
    page.fill("input[name='firstName']", first_name)
    
    page.wait_for_selector("input[name='lastName']")
    page.fill("input[name='lastName']", last_name)
    
    # Clic en el botón de siguiente en la primera pantalla
    page.wait_for_selector("button[jsname='LgbsSe']")
    page.click("button[jsname='LgbsSe']")

    # Esperar a que la segunda pantalla cargue
    try:
        page.wait_for_selector("#month", timeout=60000)
        
        # Obtener el mes en inglés
        birth_month_english = get_month_in_english(birth_month)
        
        # Seleccionar mes de nacimiento
        page.click("#month")
        page.select_option("#month", birth_month_english)
        
        # Llenar día y año de nacimiento
        page.wait_for_selector("#day")
        page.fill("#day", birth_day)
        
        page.wait_for_selector("#year")
        page.fill("#year", birth_year)

        # Normalizar género
        gender_normalized = get_gender_normalized(gender)
        if gender_normalized not in ["Male", "Female"]:
            raise ValueError("Género no reconocido. Usa 'Masculino/Hombre/Male' o 'Femenino/Mujer/Female'.")

        # Seleccionar género
        page.wait_for_selector("#gender")
        page.click("#gender")
        page.select_option("#gender", label=gender_normalized)

        # Clic en el botón de siguiente en la segunda pantalla usando XPath para ambos idiomas
        page.wait_for_selector("//span[text()='Siguiente' or text()='Next']/ancestor::button")
        page.click("//span[text()='Siguiente' or text()='Next']/ancestor::button")

        # Espera adicional para verificar que la acción se complete
        time.sleep(5)

    except Exception as e:
        print(f"Error: {e}")
        page.screenshot(path="error_screenshot.png")
    
    # Aquí podrías agregar más lógica para manejar el flujo completo del registro

    # Espera adicional para depuración antes de cerrar el navegador
    time.sleep(10)
    browser.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Automatizar la creación de una cuenta de Google.")
    parser.add_argument("--first_name", required=True, help="Nombre")
    parser.add_argument("--last_name", required=True, help="Apellido")
    parser.add_argument("--birth_month", required=True, help="Mes de nacimiento (Enero, Febrero, etc.)")
    parser.add_argument("--birth_day", required=True, help="Día de nacimiento")
    parser.add_argument("--birth_year", required=True, help="Año de nacimiento")
    parser.add_argument("--gender", required=True, choices=["Masculino", "Hombre", "Male", "Femenino", "Mujer", "Female"], help="Género (Masculino/Hombre/Male, Femenino/Mujer/Female)")

    args = parser.parse_args()

    with sync_playwright() as playwright:
        run(playwright, args.first_name, args.last_name, get_month_in_english(args.birth_month), args.birth_day, args.birth_year, get_gender_normalized(args.gender))
