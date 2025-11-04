"""
Public URL QR Code Generator
Generates QR code with a public URL (ngrok, cloudflare tunnel, etc.)
"""

import qrcode
import sys

def generate_public_qr(url):
    """Generate QR code for public URL"""
    
    print("\n" + "="*70)
    print("  🌐 PUBLIC URL QR CODE GENERATOR")
    print("="*70)
    print(f"\n🔗 Creating QR code for: {url}")
    
    # Create QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    
    qr.add_data(url)
    qr.make(fit=True)
    
    # Create image
    img = qr.make_image(fill_color="black", back_color="white")
    img.save("phishing_qr_public.png")
    
    print(f"✅ QR code saved as: phishing_qr_public.png")
    
    # Try to create poster
    try:
        from PIL import Image, ImageDraw, ImageFont
        
        width, height = 800, 1000
        poster = Image.new('RGB', (width, height), color='white')
        draw = ImageDraw.Draw(poster)
        
        # Gradient background
        for y in range(height):
            r = int(102 + (118 - 102) * y / height)
            g = int(126 + (75 - 126) * y / height)
            b = int(234 + (162 - 234) * y / height)
            draw.rectangle([(0, y), (width, y+1)], fill=(r, g, b))
        
        # Load and paste QR
        qr_img = Image.open("phishing_qr_public.png")
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
        
        # CTA
        cta = "Scan the QR code with your phone"
        cta_bbox = draw.textbbox((0, 0), cta, font=text_font)
        cta_width = cta_bbox[2] - cta_bbox[0]
        draw.text(((width - cta_width) // 2, 850), cta, fill='white', font=text_font)
        
        poster.save("phishing_poster_public.png")
        print(f"✅ Poster saved as: phishing_poster_public.png")
        
    except Exception as e:
        print(f"⚠️  Poster creation skipped: {e}")
    
    print("\n" + "="*70)
    print("✅ PUBLIC QR CODE CREATED!")
    print("="*70)
    print(f"\n📱 QR code redirects to: {url}")
    print(f"\n✅ This URL works from ANY network/location!")
    print(f"\n⚠️  SECURITY REMINDERS:")
    print(f"   - Keep tunnel running only during demo")
    print(f"   - Close tunnel immediately after session")
    print(f"   - Don't share URL publicly")
    print(f"   - Monitor admin dashboard for activity")
    print("="*70 + "\n")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        url = sys.argv[1]
    else:
        print("\n🌐 Enter your public URL")
        print("Examples:")
        print("  - https://abc123.ngrok.io")
        print("  - https://your-tunnel.loca.lt")
        print("  - https://random.trycloudflare.com")
        print()
        url = input("Enter public URL: ").strip()
    
    if not url:
        print("❌ No URL provided!")
        sys.exit(1)
    
    generate_public_qr(url)
