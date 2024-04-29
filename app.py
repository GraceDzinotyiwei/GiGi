
import io
from flask import Flask, render_template, request, send_file
from PIL import Image, ImageDraw, ImageFont



app = Flask(__name__)

# Function to generate the styled invoice image
def generate_invoice_image(name, email, phone, services, price_list, total_amount):
    # Define image dimensions and colors
    image_width = 600
    image_height = 800
    background_color = (255, 255, 255)
    text_color = (0, 0, 0)
    header_color = (102, 204, 255)  # Pastel shade of blue

    # Create a new image with a white background
    image = Image.new("RGB", (image_width, image_height), background_color)
    draw = ImageDraw.Draw(image)

    # Load the Kunstler Script Regular font for the header
    font_path = "C:/Windows/Fonts/kunstler.ttf"  # Replace with the actual font file path
    header_font_size = 48
    header_font = ImageFont.truetype(font_path, header_font_size)

    # Load Arial font for other text
    arial_font_path = "C:/Windows/Fonts/Bell.ttf"  # Replace with the actual font file path
    font_size = 24
    arial_font = ImageFont.truetype(arial_font_path, font_size)

    # Define the starting position for drawing text
    x = 50
    y = 50

    # Draw the invoice header
    header_text = "GiGi Hairstyles - Invoice"
    draw.text((x, y), header_text, font=header_font, fill=header_color)
    y += 50
    
    # Draw the customer details
    customer_text = f"\nCustomer Name: {name}\nEmail: {email}\nPhone: {phone}"
    draw.text((x, y), customer_text, font=arial_font, fill=text_color)
    y += 100

    # Draw the selected services
    services_text = "\nSelected Services:\n"
    for service in services:
        services_text += f"- {service} (${price_list[service]})\n"
    draw.text((x, y), services_text, font=arial_font, fill=text_color)
    y += 150

    # Draw the total amount
    total_text = f"\nTotal Amount: ${total_amount}"
    draw.text((x, y), total_text, font=arial_font, fill=text_color)

    return image

@app.route('/')
def index():
    return render_template('/index.html')

@app.route('/generate_invoice', methods=['POST'])
def generate_invoice():
    name = request.form['name']
    email = request.form['email']
    phone = request.form['phone']
    services = request.form.getlist('services')

    # Price list for services
    price_list = {
        'Wig Sewing': 11,
        '2" by 4" Closure': 10,
        '2" by 6" Closure': 15,
        'Wig Sewing with Fringe/Bangs/No Part': 4,
        'Washing': 10,
        'Styling': 10,
        'Deconstruction & Reconstruction': 15,
        'Knot Bleaching': 10,
        'Plucking': 5,
        'Highlights (Bleaching)': 20,
        'Wig Satin Storage Bag': 1,
        'Addition of Adjustable Band': 2
    }

    # Calculate the total amount based on the selected services
    total_amount = sum(price_list[service] for service in services)

    # Generate the styled invoice image
    invoice_image = generate_invoice_image(name, email, phone, services, price_list, total_amount)

    # Save the invoice image to a temporary file
    #with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as temp_file:
       # invoice_image.save(temp_file.name)

    # Specify the filename and folder path for the saved invoice
    #filename = f"{name.replace(' ', '_')}_invoice.png"
    #folder_path = r'C:\Users\grace\Downloads\GiGi\invoices'

    # Check if the file already exists
    #counter = 1
    
    #while os.path.exists(os.path.join(folder_path, filename)):
    #    filename = f"{filename.split('.')[0]}_{counter}.png"
    #    counter += 1

    #file_path = os.path.join(folder_path, filename)

    # Move the temporary file to the specified folder path
    #os.replace(temp_file.name, file_path)
    # Save the invoice image
    #invoice_image.save(file_path)
    # Send the invoice image as a response to display on the client's screen
    # Clear selected items and client informatio
    image_io = io.BytesIO()
    invoice_image.save(image_io, 'PNG')
    image_io.seek(0)
    return send_file(image_io, mimetype='image/png')
    # Send the invoice image as an attachment
    #return send_file(io.BytesIO(invoice_image.getvalue()), mimetype='image/png')
    


if __name__ == '__main__':
    app.run()