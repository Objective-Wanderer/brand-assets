#!/usr/bin/env python3
"""
matemplates.com cover image generator
Produces 1280x720 (16:9) cover PNGs with the unified brand style:
  - Diagonal gradient: orange (top-left) → dark navy (center/bottom-right)
  - Centered title text (white, bold)
  - Small subtitle text (light gray, below title)
  - "matemplates" branding at bottom-left
  - Subtle n8n logo accent at top-right
"""
import math
import os
import sys
from PIL import Image, ImageDraw, ImageFont

W, H = 1280, 720
FONT_DIR = "C:/Windows/Fonts"
OUT_DIR = os.path.join(os.path.dirname(__file__), "brand-assets", "covers") if len(sys.argv) < 3 else sys.argv[2]

# Brand colors
ORANGE = (255, 122, 0)
DARK_BG = (19, 32, 50)
NAVY = (25, 36, 57)
WHITE = (255, 255, 255)
LIGHT_GRAY = (180, 195, 215)
ACCENT_ORANGE = (164, 86, 16)

# Cover data: (filename, title, subtitle)
COVERS = [
    # Template products
    ("real-estate-lead-enrichment.png", "Real Estate\nLead Enrichment", "Scrape, AI-score, and route hot leads"),
    ("gumroad-sales-notifier.png", "Gumroad\nSales Notifier", "Instant alerts for every new sale"),
    ("invoice-followup.png", "Invoice\nFollow-Up", "From overdue to paid, on autopilot"),
    ("cold-outreach.png", "Cold\nOutreach", "Personalized sequences at scale"),
    ("support-triage.png", "Customer Support\nTriage", "Auto-tag and route inbound requests"),
    # Blog posts
    ("auto-chase-overdue-invoices-n8n.png", "Auto-Chase\nOverdue Invoices", "n8n sends polite nudges until they pay"),
    ("cold-outreach-that-converts.png", "Cold Outreach\nThat Converts", "Why most outreach fails and how to fix it"),
    ("gumroad-sale-telegram-alert.png", "Gumroad Sale\nTelegram Alert", "Get notified the second a sale lands"),
    ("n8n-vs-zapier-solopreneur.png", "n8n vs Zapier\nfor Solopreneurs", "Which automation tool is worth your time"),
    ("n8n-webhook-telegram-trigger.png", "n8n Webhook +\nTelegram Trigger", "Two-way messaging from any API"),
    ("no-code-crm-google-sheets-n8n.png", "No-Code CRM\nin Google Sheets", "Build a pipeline without SaaS bills"),
    ("real-estate-lead-enrichment-n8n.png", "Real Estate\nLead Enrichment", "n8n workflow for lead scoring and routing"),
    ("solopreneur-n8n-automations.png", "n8n for\nSolopreneurs", "Automate without engineers"),
    # Special products
    ("automation-club.png", "n8n\nAutomation Club", "Premium workflows and community access"),
    ("free-lead-sampler.png", "Free Lead\nEnrichment Sampler", "Try the workflow before you buy"),
    ("starter-pack.png", "n8n\nStarter Pack", "Five essential workflows to get going"),
]


def make_gradient(w, h):
    """Create the diagonal gradient background: orange top-left → navy bottom-right."""
    import numpy as np
    xs = np.linspace(0, 1, w)
    ys = np.linspace(0, 1, h)
    xx, yy = np.meshgrid(xs, ys)
    diag = np.clip(xx * 0.6 + yy * 0.4, 0, 1)

    orange_w = np.clip(1.0 - diag * 3.5, 0, 1)
    dark = 0.85 + 0.15 * diag

    r = ((ORANGE[0] * orange_w + DARK_BG[0] * (1 - orange_w)) * dark).astype(np.uint8)
    g = ((ORANGE[1] * orange_w + DARK_BG[1] * (1 - orange_w)) * dark).astype(np.uint8)
    b = ((ORANGE[2] * orange_w + DARK_BG[2] * (1 - orange_w)) * dark).astype(np.uint8)

    arr = np.stack([r, g, b], axis=2)
    return Image.fromarray(arr, "RGB")


def draw_text_centered(draw, text, y, font, fill, max_width=1100):
    """Draw multi-line text centered horizontally."""
    lines = text.split("\n")
    total_height = 0
    line_sizes = []
    for line in lines:
        bbox = font.getbbox(line)
        lw = bbox[2] - bbox[0]
        lh = bbox[3] - bbox[1]
        line_sizes.append((lw, lh, line))
        total_height += lh + 8

    cy = y
    for lw, lh, line in line_sizes:
        x = (W - lw) // 2
        draw.text((x, cy), line, font=font, fill=fill)
        cy += lh + 8
    return cy


def generate_cover(filename, title, subtitle):
    """Generate a single cover image."""
    img = make_gradient(W, H)
    draw = ImageDraw.Draw(img)

    # Load fonts
    try:
        title_font = ImageFont.truetype(os.path.join(FONT_DIR, "arialbd.ttf"), 86)
    except Exception:
        title_font = ImageFont.truetype(os.path.join(FONT_DIR, "bahnschrift.ttf"), 86)

    try:
        sub_font = ImageFont.truetype(os.path.join(FONT_DIR, "arial.ttf"), 34)
    except Exception:
        sub_font = ImageFont.truetype(os.path.join(FONT_DIR, "bahnschrift.ttf"), 34)

    try:
        brand_font = ImageFont.truetype(os.path.join(FONT_DIR, "arial.ttf"), 26)
    except Exception:
        brand_font = ImageFont.truetype(os.path.join(FONT_DIR, "bahnschrift.ttf"), 26)

    # Draw title centered vertically
    lines = title.split("\n")
    title_height = sum(title_font.getbbox(l)[3] - title_font.getbbox(l)[1] + 8 for l in lines) - 8
    title_y = (H - title_height) // 2 - 20  # slightly above center
    draw_text_centered(draw, title, title_y, title_font, WHITE)

    # Draw subtitle below title
    sub_y = title_y + title_height + 20
    bbox = sub_font.getbbox(subtitle)
    sw = bbox[2] - bbox[0]
    draw.text(((W - sw) // 2, sub_y), subtitle, font=sub_font, fill=LIGHT_GRAY)

    # Draw "matemplates" branding at bottom-left — split-color: mate=white, mplates=accent
    bx, by = 90, H - 55
    mate_bbox = brand_font.getbbox("mate")
    mate_w = mate_bbox[2] - mate_bbox[0]
    draw.text((bx, by), "mate", font=brand_font, fill=(255, 255, 255))
    draw.text((bx + mate_w, by), "mplates", font=brand_font, fill=(255, 122, 0))

    # Subtle n8n accent dot (top-right area)
    draw.ellipse([W - 120, 50, W - 80, 90], fill=ACCENT_ORANGE)

    return img


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    for filename, title, subtitle in COVERS:
        img = generate_cover(filename, title, subtitle)
        path = os.path.join(OUT_DIR, filename)
        img.save(path, "PNG", optimize=True)
        print(f"  ✓ {filename}")

    print(f"\n{len(COVERS)} covers generated → {OUT_DIR}")


if __name__ == "__main__":
    main()
