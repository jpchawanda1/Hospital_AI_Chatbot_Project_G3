#!/usr/bin/env python3
"""
Simple PDF Generator using browser print functionality
Creates a PDF-optimized HTML version that can be printed to PDF
"""

import os
import webbrowser
from pathlib import Path

def create_pdf_optimized_html():
    """Create a PDF-optimized version of the poster"""
    
    # Read the original HTML
    html_file = Path(__file__).parent / "project_poster.html"
    pdf_html_file = Path(__file__).parent / "project_poster_pdf.html"
    
    print("📄 Creating PDF-optimized HTML version...")
    
    with open(html_file, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # Add PDF-specific styles and print instructions
    pdf_optimized_content = html_content.replace(
        '<title>Hospital AI Agent - Project Poster</title>',
        '''<title>Hospital AI Agent - Project Poster (PDF Version)</title>
    <style>
        /* PDF Print Optimization */
        @media print {
            * {
                -webkit-print-color-adjust: exact !important;
                color-adjust: exact !important;
                print-color-adjust: exact !important;
            }
            
            body {
                margin: 0 !important;
                padding: 0 !important;
            }
            
            .poster {
                box-shadow: none !important;
                margin: 0 !important;
                page-break-inside: avoid !important;
                width: 100% !important;
                height: 100vh !important;
                transform: scale(0.95) !important;
                transform-origin: top left !important;
            }
            
            @page {
                size: A1 landscape;
                margin: 0.5in;
            }
        }
        
        /* PDF Notice Banner */
        .pdf-notice {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            background: #2C3E50;
            color: white;
            padding: 10px;
            text-align: center;
            z-index: 1000;
            font-family: Arial, sans-serif;
        }
        
        .pdf-instructions {
            background: #3498DB;
            color: white;
            padding: 15px;
            margin: 10px;
            border-radius: 5px;
            font-size: 14px;
        }
        
        .poster {
            margin-top: 80px;
        }
        
        @media print {
            .pdf-notice,
            .pdf-instructions {
                display: none !important;
            }
            
            .poster {
                margin-top: 0 !important;
            }
        }
    </style>'''
    )
    
    # Add PDF instructions banner
    pdf_optimized_content = pdf_optimized_content.replace(
        '<body>',
        '''<body>
    <div class="pdf-notice">
        🏥 Hospital AI Agent Project Poster - PDF Version
    </div>
    
    <div class="pdf-instructions">
        <strong>📄 To generate PDF:</strong><br>
        1. Press <strong>Ctrl+P</strong> (Windows) or <strong>Cmd+P</strong> (Mac)<br>
        2. Select <strong>"Save as PDF"</strong> as destination<br>
        3. Choose <strong>Landscape</strong> orientation<br>
        4. Select <strong>A1</strong> or <strong>A0</strong> paper size for best quality<br>
        5. Enable <strong>"More settings" → "Graphics"</strong> for colors<br>
        6. Click <strong>"Save"</strong> and name it <strong>"Hospital_AI_Agent_Poster.pdf"</strong>
    </div>'''
    )
    
    # Save the PDF-optimized version
    with open(pdf_html_file, 'w', encoding='utf-8') as f:
        f.write(pdf_optimized_content)
    
    print(f"✅ PDF-optimized HTML created: {pdf_html_file}")
    return pdf_html_file

def open_in_browser(file_path):
    """Open the PDF-optimized HTML in default browser"""
    file_url = f"file:///{file_path.absolute()}"
    print(f"🌐 Opening in browser: {file_url}")
    webbrowser.open(file_url)

def main():
    """Main function"""
    print("🏥 Hospital AI Agent Project - Simple PDF Generator")
    print("=" * 60)
    
    # Create PDF-optimized HTML
    pdf_html_file = create_pdf_optimized_html()
    
    # Open in browser for manual PDF generation
    open_in_browser(pdf_html_file)
    
    print("\n🎯 PDF Generation Instructions:")
    print("1. A browser window will open with the poster")
    print("2. Press Ctrl+P (Windows) or Cmd+P (Mac)")
    print("3. Select 'Save as PDF' as destination")
    print("4. Choose Landscape orientation")
    print("5. Select A1 or A0 paper size")
    print("6. Enable Graphics/Background colors")
    print("7. Save as 'Hospital_AI_Agent_Poster.pdf'")
    print("\n📄 The PDF will be saved to your Downloads folder")
    print("✨ High-quality poster ready for printing!")

if __name__ == "__main__":
    main()
