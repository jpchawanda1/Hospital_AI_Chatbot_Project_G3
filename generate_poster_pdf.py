#!/usr/bin/env python3
"""
Hospital AI Agent Project Poster PDF Generator
Converts the HTML poster to a high-quality PDF document
"""

import os
import sys
from pathlib import Path

def generate_pdf_with_weasyprint():
    """Generate PDF using WeasyPrint (best quality)"""
    try:
        import weasyprint
        
        # Get absolute paths
        html_file = Path(__file__).parent / "project_poster.html"
        pdf_file = Path(__file__).parent / "Hospital_AI_Agent_Poster.pdf"
        
        print("🎨 Generating PDF with WeasyPrint...")
        print(f"📄 Source: {html_file}")
        print(f"📄 Target: {pdf_file}")
        
        # Read HTML content
        with open(html_file, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # Generate PDF
        html_doc = weasyprint.HTML(string=html_content, base_url=str(html_file.parent))
        css = weasyprint.CSS(string='''
            @page {
                size: A0 landscape;
                margin: 0.5in;
            }
            .poster {
                width: 100%;
                height: 100%;
                box-shadow: none;
                margin: 0;
                page-break-inside: avoid;
            }
            body {
                margin: 0;
                padding: 0;
            }
        ''')
        
        html_doc.write_pdf(str(pdf_file), stylesheets=[css])
        
        print(f"✅ PDF generated successfully: {pdf_file}")
        return True
        
    except ImportError:
        print("❌ WeasyPrint not found. Installing...")
        return False
    except Exception as e:
        print(f"❌ Error with WeasyPrint: {e}")
        return False

def generate_pdf_with_pdfkit():
    """Generate PDF using pdfkit (wkhtmltopdf)"""
    try:
        import pdfkit
        
        # Get absolute paths
        html_file = Path(__file__).parent / "project_poster.html"
        pdf_file = Path(__file__).parent / "Hospital_AI_Agent_Poster.pdf"
        
        print("🎨 Generating PDF with pdfkit...")
        print(f"📄 Source: {html_file}")
        print(f"📄 Target: {pdf_file}")
        
        # PDF options for poster quality
        options = {
            'page-size': 'A0',
            'orientation': 'Landscape',
            'margin-top': '0.5in',
            'margin-right': '0.5in',
            'margin-bottom': '0.5in',
            'margin-left': '0.5in',
            'encoding': "UTF-8",
            'no-outline': None,
            'enable-local-file-access': None,
            'print-media-type': None,
            'disable-smart-shrinking': None,
            'zoom': 1.0
        }
        
        # Generate PDF
        pdfkit.from_file(str(html_file), str(pdf_file), options=options)
        
        print(f"✅ PDF generated successfully: {pdf_file}")
        return True
        
    except ImportError:
        print("❌ pdfkit not found. Installing...")
        return False
    except Exception as e:
        print(f"❌ Error with pdfkit: {e}")
        return False

def generate_pdf_with_playwright():
    """Generate PDF using Playwright (browser-based)"""
    try:
        from playwright.sync_api import sync_playwright
        
        # Get absolute paths
        html_file = Path(__file__).parent / "project_poster.html"
        pdf_file = Path(__file__).parent / "Hospital_AI_Agent_Poster.pdf"
        
        print("🎨 Generating PDF with Playwright...")
        print(f"📄 Source: {html_file}")
        print(f"📄 Target: {pdf_file}")
        
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            
            # Load the HTML file
            page.goto(f"file://{html_file.absolute()}")
            
            # Wait for content to load
            page.wait_for_load_state('networkidle')
            
            # Generate PDF with poster settings
            page.pdf(
                path=str(pdf_file),
                format='A0',
                landscape=True,
                margin={
                    'top': '0.5in',
                    'right': '0.5in', 
                    'bottom': '0.5in',
                    'left': '0.5in'
                },
                print_background=True,
                prefer_css_page_size=True
            )
            
            browser.close()
        
        print(f"✅ PDF generated successfully: {pdf_file}")
        return True
        
    except ImportError:
        print("❌ Playwright not found. Installing...")
        return False
    except Exception as e:
        print(f"❌ Error with Playwright: {e}")
        return False

def install_dependencies():
    """Install required dependencies"""
    import subprocess
    
    print("📦 Installing PDF generation dependencies...")
    
    packages = [
        "weasyprint",
        "pdfkit", 
        "playwright"
    ]
    
    for package in packages:
        try:
            print(f"Installing {package}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f"✅ {package} installed successfully")
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install {package}: {e}")
    
    # Install playwright browsers if playwright was installed
    try:
        print("Installing Playwright browsers...")
        subprocess.check_call([sys.executable, "-m", "playwright", "install", "chromium"])
        print("✅ Playwright browsers installed")
    except subprocess.CalledProcessError:
        print("❌ Failed to install Playwright browsers")

def main():
    """Main function to generate PDF poster"""
    print("🏥 Hospital AI Agent Project - PDF Poster Generator")
    print("=" * 60)
    
    # Check if HTML file exists
    html_file = Path(__file__).parent / "project_poster.html"
    if not html_file.exists():
        print(f"❌ HTML file not found: {html_file}")
        return
    
    # Try different PDF generation methods
    methods = [
        ("WeasyPrint", generate_pdf_with_weasyprint),
        ("Playwright", generate_pdf_with_playwright),
        ("pdfkit", generate_pdf_with_pdfkit)
    ]
    
    success = False
    for method_name, method_func in methods:
        print(f"\n🔄 Trying {method_name}...")
        if method_func():
            success = True
            break
        else:
            print(f"❌ {method_name} failed, trying next method...")
    
    if not success:
        print("\n❌ All PDF generation methods failed.")
        print("📦 Installing dependencies and retrying...")
        install_dependencies()
        
        # Retry after installation
        print("\n🔄 Retrying PDF generation...")
        for method_name, method_func in methods:
            print(f"\n🔄 Trying {method_name} (after installation)...")
            if method_func():
                success = True
                break
    
    if success:
        print("\n🎉 PDF poster generated successfully!")
        print("📄 File: Hospital_AI_Agent_Poster.pdf")
        print("🖨️  Ready for printing and presentation!")
    else:
        print("\n❌ Failed to generate PDF. Please install dependencies manually:")
        print("   pip install weasyprint")
        print("   pip install playwright")
        print("   playwright install chromium")

if __name__ == "__main__":
    main()
