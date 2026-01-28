import time
import board
import busio
import gpiozero
import os
import textwrap
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306
import ollama

# --- 1. OLED Hardware Setup ---
oled_reset_pin = gpiozero.OutputDevice(4, active_high=False)
oled_reset_pin.on()
time.sleep(0.1)
oled_reset_pin.off()
time.sleep(0.1)
oled_reset_pin.on()

i2c = board.I2C()
oled = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c, addr=0x3C)
image = Image.new("1", (oled.width, oled.height))
draw = ImageDraw.Draw(image)

# Load Font
try:
    font = ImageFont.truetype('PixelOperator.ttf', 14)
except:
    font = ImageFont.load_default()

# --- 2. Helper Functions ---
def display_on_oled(text):
    """Clears screen and draws wrapped text."""
    draw.rectangle((0, 0, oled.width, oled.height), outline=0, fill=0)
    # width=20 is usually good for a 128px wide screen with 14pt font
    lines = textwrap.wrap(text, width=20)
    y = 0
    for line in lines:
        if y < 64:
            draw.text((0, y), line, font=font, fill=255)
            y += 15
    oled.image(image)
    oled.show()

def get_ai_response(user_input):
    """Sends prompt to TinyDolphin."""
    try:
        response = ollama.chat(model='tinydolphin', messages=[
            {'role': 'user', 'content': user_input},
        ])
        return response.get('message', {}).get('content', "No reply.")
    except Exception as e:
        return f"Error: {str(e)}"

# --- 3. Main Terminal Loop ---
print("-" * 30)
print("TinyDolphin Terminal Controller")
print("Type your message and press Enter.")
print("Type 'exit' or 'quit' to stop.")
print("-" * 30)

display_on_oled("Ready for terminal input...")

while True:
    # This happens in the terminal
    user_prompt = input("\nYOU: ")
    
    # Check if user wants to quit
    if user_prompt.lower() in ['exit', 'quit']:
        display_on_oled("Shutting down...")
        print("Exiting...")
        time.sleep(2)
        break
    
    if user_prompt.strip():
        # Update OLED so you know it's working
        display_on_oled(f"Thinking about: {user_prompt[:15]}...")
        
        # Get AI Response
        answer = get_ai_response(user_prompt)
        
        # Show on OLED
        display_on_oled(answer)
        
        # Also print to terminal so you can read it there too
        print(f"DOLPHIN: {answer}")
    else:
        print("Please enter a question!")
