"""
QR Code Generator for Phishing Demonstration
Generates a QR code that points to your local phishing server
"""

import qrcode
import socket

def get_local_ip():
    """Get the local IP address of the machine"""
    try:
        # Create a socket to determine the local IP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except Exception:
        return "localhost"

def generate_qr_code(url, filename="phishing_qr.png"):
    """Generate QR code for the given URL"""
    # Create QR code
    qr = qrcode.QRCode(
        version=1,  # Controls the size of the QR code
        error_correction=qrcode.constants.ERROR_CORRECT_H,  # High error correction
        box_size=10,  # Size of each box in pixels
        border=4,  # Border thickness
    )
    
    qr.add_data(url)
    qr.make(fit=True)
    
    # Create an image
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(filename)
    print(f"✅ QR code saved as: {filename}")
    return filename

def create_poster(qr_filename="phishing_qr.png", poster_filename="phishing_poster.png"):
    """Create an attractive poster with the QR code"""
    try:
        from PIL import Image, ImageDraw, ImageFont
        
        # Create a poster image
        width, height = 800, 1000
        poster = Image.new('RGB', (width, height), color='white')
        draw = ImageDraw.Draw(poster)
        
        # Add gradient background
        for y in range(height):
            r = int(102 + (118 - 102) * y / height)
            g = int(126 + (75 - 126) * y / height)
            b = int(234 + (162 - 234) * y / height)
            draw.rectangle([(0, y), (width, y+1)], fill=(r, g, b))
        
        # Load and paste QR code
        qr_img = Image.open(qr_filename)
        qr_img = qr_img.resize((500, 500))
        poster.paste(qr_img, ((width - 500) // 2, 300))
        
        # Add text
        try:
            title_font = ImageFont.truetype("arial.ttf", 60)
            subtitle_font = ImageFont.truetype("arial.ttf", 30)
            text_font = ImageFont.truetype("arial.ttf", 25)
        except:
            title_font = ImageFont.load_default()
            subtitle_font = ImageFont.load_default()
            text_font = ImageFont.load_default()
        
        # Title
        title = "🎁 EXCLUSIVE GIVEAWAY!"
        title_bbox = draw.textbbox((0, 0), title, font=title_font)
        title_width = title_bbox[2] - title_bbox[0]
        draw.text(((width - title_width) // 2, 100), title, fill='white', font=title_font)
        
        # Subtitle
        subtitle = "Scan to claim your prize"
        subtitle_bbox = draw.textbbox((0, 0), subtitle, font=subtitle_font)
        subtitle_width = subtitle_bbox[2] - subtitle_bbox[0]
        draw.text(((width - subtitle_width) // 2, 200), subtitle, fill='white', font=subtitle_font)
        
        # Call to action
        cta = "Scan the QR code with your phone"
        cta_bbox = draw.textbbox((0, 0), cta, font=text_font)
        cta_width = cta_bbox[2] - cta_bbox[0]
        draw.text(((width - cta_width) // 2, 850), cta, fill='white', font=text_font)
        
        poster.save(poster_filename)
        print(f"✅ Poster saved as: {poster_filename}")
        return poster_filename
        
    except ImportError:
        print("⚠️ PIL/Pillow not installed. Install with: pip install pillow")
        print("   Skipping poster creation, using QR code only.")
        return qr_filename

def main():
    print("\n" + "="*70)
    print("  🎣 PHISHING QR CODE GENERATOR - EDUCATIONAL USE ONLY")
    print("="*70)
    
    # Get local IP
    local_ip = get_local_ip()
    
    print(f"\n📱 Your local IP address: {local_ip}")
    print(f"🌐 Make sure your Flask server is running on: http://{local_ip}:5000")
    
    # Option to use custom URL or IP
    print("\nOptions:")
    print(f"1. Use local IP: {local_ip}")
    print("2. Use localhost (for testing on same machine)")
    print("3. Enter custom IP/domain")
    
    choice = input("\nSelect option (1-3) [1]: ").strip() or "1"
    
    if choice == "2":
        url = "http://localhost:5000"
    elif choice == "3":
        custom = input("Enter custom IP or domain: ").strip()
        url = f"http://{custom}:5000"
    else:
        url = f"http://{local_ip}:5000"
    
    print(f"\n🔗 QR code will redirect to: {url}")
    
    # Generate QR code
    qr_file = generate_qr_code(url)
    
    # Try to create poster
    poster_file = create_poster(qr_file)
    
    print("\n" + "="*70)
    print("✅ QR CODE GENERATION COMPLETE!")
    print("="*70)
    print(f"\n📄 Files created:")
    print(f"   - {qr_file}")
    if poster_file != qr_file:
        print(f"   - {poster_file}")
    
    print(f"\n📋 Next steps:")
    print(f"   1. Start the Flask server: python app.py")
    print(f"   2. Print or display the QR code/poster")
    print(f"   3. Participants scan with their phones")
    print(f"   4. Monitor captures at: http://{local_ip}:5000/admin")
    
    print(f"\n⚠️  IMPORTANT:")
    print(f"   - Ensure your device and participants' phones are on the same network")
    print(f"   - Check firewall settings if connection fails")
    print(f"   - Use only for authorized security awareness training!")
    print("="*70 + "\n")

if __name__ == "__main__":
    main()
