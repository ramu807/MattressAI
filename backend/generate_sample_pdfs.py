"""
Generate sample mattress knowledge PDFs for demo purposes.
This creates educational content that can be used to demonstrate the RAG system.

Run: python generate_sample_pdfs.py
From the backend/ directory.
"""
from pathlib import Path

try:
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
    from reportlab.lib.colors import HexColor
except ImportError:
    print("reportlab not installed. Install with: pip install reportlab")
    print("Or place your own PDF files in backend/data/pdfs/")
    exit(1)

OUTPUT_DIR = Path(__file__).parent / "data" / "pdfs"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

styles = getSampleStyleSheet()
title_style = ParagraphStyle(
    'CustomTitle', parent=styles['Title'], fontSize=24, spaceAfter=30,
    textColor=HexColor('#1a1a2e')
)
heading_style = ParagraphStyle(
    'CustomHeading', parent=styles['Heading1'], fontSize=16, spaceAfter=12,
    spaceBefore=20, textColor=HexColor('#16213e')
)
body_style = ParagraphStyle(
    'CustomBody', parent=styles['BodyText'], fontSize=11, spaceAfter=8,
    leading=16
)


def create_buying_guide():
    """Create a comprehensive mattress buying guide PDF."""
    doc = SimpleDocTemplate(
        str(OUTPUT_DIR / "mattress_buying_guide.pdf"),
        pagesize=letter,
        rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=72,
    )

    content = []

    # Title
    content.append(Paragraph("The Complete Mattress Buying Guide", title_style))
    content.append(Paragraph("Everything You Need to Know Before Purchasing a Mattress", styles['Heading2']))
    content.append(Spacer(1, 20))

    # Chapter 1: Types of Mattresses
    content.append(Paragraph("Chapter 1: Types of Mattresses", heading_style))
    content.append(Paragraph(
        "Choosing the right mattress is one of the most important decisions for your sleep quality and overall health. "
        "There are several main types of mattresses available today, each with distinct characteristics, benefits, and drawbacks. "
        "Understanding these differences is crucial for making an informed purchase decision.",
        body_style
    ))
    content.append(Spacer(1, 10))

    content.append(Paragraph("<b>Innerspring Mattresses</b>", body_style))
    content.append(Paragraph(
        "Innerspring mattresses are the most traditional type, using a system of metal coils to provide support. "
        "They typically feature either Bonnell coils (hourglass-shaped, interconnected), offset coils (similar to Bonnell but with flattened tops for better contouring), "
        "or pocketed coils (individually wrapped springs that move independently). Pocketed coil mattresses are generally considered superior "
        "because they minimize motion transfer between sleeping partners. Innerspring mattresses typically range from 300 to over 1,000 coils, "
        "with higher coil counts generally providing better support and durability. They offer excellent breathability due to the open coil structure, "
        "making them a good choice for hot sleepers. However, they may not provide adequate pressure relief for side sleepers "
        "and can develop sagging over time, particularly in the center of the mattress. Average lifespan is 5-7 years.",
        body_style
    ))
    content.append(Spacer(1, 8))

    content.append(Paragraph("<b>Memory Foam Mattresses</b>", body_style))
    content.append(Paragraph(
        "Memory foam (viscoelastic polyurethane foam) was originally developed by NASA in the 1960s to improve seat cushioning and crash protection. "
        "Memory foam mattresses conform closely to the body's shape in response to heat and pressure, distributing weight evenly and relieving pressure points. "
        "This makes them particularly beneficial for people with chronic pain conditions, including back pain, arthritis, and fibromyalgia. "
        "Standard memory foam comes in various densities: low density (3-4 lb/ft³), medium density (4-5 lb/ft³), and high density (5-7 lb/ft³). "
        "Higher density foams tend to be more durable and supportive but may retain more heat. "
        "Gel-infused memory foam was introduced to address heat retention issues, incorporating gel beads or layers that help dissipate body heat. "
        "Open-cell memory foam is another innovation that improves airflow through the foam structure. "
        "Plant-based memory foam replaces a portion of petroleum-based materials with plant-derived oils, typically resulting in a cooler, more responsive feel. "
        "Memory foam mattresses generally last 8-10 years with proper care.",
        body_style
    ))
    content.append(Spacer(1, 8))

    content.append(Paragraph("<b>Latex Mattresses</b>", body_style))
    content.append(Paragraph(
        "Latex mattresses are made from either natural latex (harvested from rubber trees using the Dunlop or Talalay process) "
        "or synthetic latex (made from petrochemicals). Natural latex is highly durable, hypoallergenic, and resistant to dust mites and mold. "
        "The Dunlop process produces denser, firmer latex, while the Talalay process creates a more consistent, slightly softer feel. "
        "Latex mattresses offer excellent responsiveness — they contour to the body like memory foam but spring back more quickly when pressure is removed. "
        "This combination of conforming support and bounce makes latex popular among combination sleepers who change positions frequently. "
        "Natural latex is also one of the most eco-friendly mattress materials available. "
        "Latex mattresses are among the most durable, typically lasting 12-20 years. They are also naturally breathable, sleeping cooler than most memory foam options. "
        "The main drawback is cost — pure natural latex mattresses tend to be significantly more expensive than other types.",
        body_style
    ))
    content.append(Spacer(1, 8))

    content.append(Paragraph("<b>Hybrid Mattresses</b>", body_style))
    content.append(Paragraph(
        "Hybrid mattresses combine an innerspring coil support system with one or more layers of foam (memory foam, latex, or polyfoam) on top. "
        "This design aims to provide the best of both worlds: the responsive support and breathability of coils with the pressure relief "
        "and contouring of foam. Most hybrids use pocketed coils for the support core and 2-3 inches of foam comfort layers. "
        "They tend to work well for a wide range of sleepers, including combination sleepers, couples (due to reduced motion transfer from pocketed coils), "
        "and those who want pressure relief without the 'stuck in the mattress' feeling that some memory foam beds produce. "
        "Hybrid mattresses are typically in the mid to high price range and last 7-10 years. "
        "When shopping for hybrids, pay attention to the coil count (generally 800+ is desirable), "
        "the type and thickness of foam layers, and edge support quality.",
        body_style
    ))

    content.append(PageBreak())

    # Chapter 2: Firmness and Support
    content.append(Paragraph("Chapter 2: Firmness Levels and Support", heading_style))
    content.append(Paragraph(
        "Mattress firmness is typically rated on a scale of 1-10, where 1 is the softest and 10 is the firmest. "
        "Most mattresses fall in the 3-8 range. Understanding firmness is essential because the right firmness level depends on "
        "your sleeping position, body weight, and personal preferences.",
        body_style
    ))
    content.append(Spacer(1, 8))

    content.append(Paragraph(
        "<b>Soft (3-4):</b> Best for side sleepers under 130 pounds. Provides deep contouring and pressure relief for shoulders and hips. "
        "Not recommended for stomach sleepers as it can cause spinal misalignment.",
        body_style
    ))
    content.append(Paragraph(
        "<b>Medium-Soft (4-5):</b> Good for side sleepers between 130-200 pounds. Offers a balance of cushioning and support.",
        body_style
    ))
    content.append(Paragraph(
        "<b>Medium (5-6):</b> The most popular firmness level, suitable for most sleepers. Works well for combination sleepers "
        "who switch between back and side sleeping. Provides adequate support for back sleepers while still offering cushioning for side sleeping.",
        body_style
    ))
    content.append(Paragraph(
        "<b>Medium-Firm (6-7):</b> Ideal for back sleepers and combination sleepers over 200 pounds. Provides strong lumbar support "
        "while still contouring to the body's natural curves. Often recommended by healthcare professionals for people with back pain.",
        body_style
    ))
    content.append(Paragraph(
        "<b>Firm (7-8):</b> Best for stomach sleepers and back sleepers over 230 pounds. "
        "Keeps the spine in a neutral position by preventing excessive sinking. "
        "Stomach sleepers need firmer mattresses to prevent their hips from sinking too deep, which can strain the lower back.",
        body_style
    ))
    content.append(Spacer(1, 12))

    # Chapter 3: Sleeping Positions
    content.append(Paragraph("Chapter 3: Best Mattresses by Sleeping Position", heading_style))

    content.append(Paragraph("<b>Side Sleepers</b>", body_style))
    content.append(Paragraph(
        "Side sleeping is the most common sleep position. Side sleepers need a mattress that cushions the shoulders and hips "
        "— the two primary pressure points in this position. Memory foam and soft-to-medium hybrid mattresses are generally the best options. "
        "Look for mattresses with at least 3 inches of comfort foam to prevent pressure buildup. "
        "The mattress should allow the shoulders and hips to sink in enough to keep the spine aligned horizontally. "
        "A mattress that is too firm for a side sleeper will create pressure points at the shoulders and hips, "
        "potentially leading to numbness, tingling, and pain.",
        body_style
    ))
    content.append(Spacer(1, 8))

    content.append(Paragraph("<b>Back Sleepers</b>", body_style))
    content.append(Paragraph(
        "Back sleepers need a mattress that supports the natural curvature of the spine, particularly the lumbar region. "
        "Medium to medium-firm mattresses are typically ideal. The mattress should be firm enough to prevent the hips from sinking too deep "
        "(which would create a U-shape in the spine) while still contouring enough to fill the gap under the lower back. "
        "Hybrid mattresses and firmer memory foam options work well for back sleepers. "
        "Zoned support systems, which use firmer foam under the hips and softer foam under the shoulders, "
        "can be particularly beneficial for back sleepers.",
        body_style
    ))
    content.append(Spacer(1, 8))

    content.append(Paragraph("<b>Stomach Sleepers</b>", body_style))
    content.append(Paragraph(
        "Stomach sleeping is generally considered the least favorable position for spinal alignment, "
        "but many people find it comfortable. Stomach sleepers need a firm mattress (6-8 on the firmness scale) to prevent the pelvis "
        "from sinking too deeply, which would hyperextend the lower back. Thin, firm mattresses with minimal cushioning on top work best. "
        "Avoid thick pillow-top mattresses and soft memory foam, as these allow too much sinking. "
        "Innerspring and firm hybrid mattresses are popular choices for stomach sleepers.",
        body_style
    ))

    content.append(PageBreak())

    # Chapter 4: Budget Guide
    content.append(Paragraph("Chapter 4: Budget and Value Guide", heading_style))
    content.append(Paragraph(
        "Mattress prices vary enormously, from under $300 to over $5,000. Here is a general breakdown of what to expect at different price points:",
        body_style
    ))
    content.append(Spacer(1, 8))

    content.append(Paragraph(
        "<b>Budget ($300-$600):</b> You can find decent innerspring and basic foam mattresses in this range. "
        "Bed-in-a-box brands have made quality mattresses more accessible at these prices. "
        "Look for CertiPUR-US certified foams and at least a 10-year warranty. "
        "At this price point, expect a lifespan of 5-7 years.",
        body_style
    ))
    content.append(Paragraph(
        "<b>Mid-Range ($600-$1,500):</b> This is where most people find the best value. You can get high-quality memory foam, "
        "latex, or hybrid mattresses with good durability. Many popular online mattress brands offer excellent options in this range. "
        "Expect better materials, improved edge support, and lifespans of 7-10 years.",
        body_style
    ))
    content.append(Paragraph(
        "<b>Premium ($1,500-$3,000):</b> Premium mattresses use higher-grade materials, advanced cooling technologies, "
        "and often feature zoned support systems. Natural latex and premium hybrids dominate this category. "
        "You'll find better motion isolation, edge support, and durability (10-15 years).",
        body_style
    ))
    content.append(Paragraph(
        "<b>Luxury ($3,000+):</b> Luxury mattresses use the finest materials — organic latex, cashmere covers, "
        "hand-tufted construction, and advanced coil systems. Brands like Saatva, Tempur-Pedic, and Stearns & Foster "
        "offer premium options. These mattresses can last 15-20+ years with proper care.",
        body_style
    ))
    content.append(Spacer(1, 12))

    # Chapter 5: Health Considerations
    content.append(Paragraph("Chapter 5: Health and Medical Considerations", heading_style))

    content.append(Paragraph("<b>Back Pain</b>", body_style))
    content.append(Paragraph(
        "For chronic back pain, research consistently shows that medium-firm mattresses provide the best outcomes. "
        "A 2015 study published in the journal Sleep Health found that a medium-firm mattress improved sleep quality "
        "and reduced back pain compared to firm mattresses. The key is proper spinal alignment — the mattress should support "
        "the natural S-curve of the spine without creating pressure points. Memory foam and hybrid mattresses with zoned support "
        "are often recommended by orthopedic specialists. If you have lower back pain, avoid mattresses that are too soft, "
        "as they can cause the hips to sink and misalign the spine.",
        body_style
    ))
    content.append(Spacer(1, 8))

    content.append(Paragraph("<b>Allergies</b>", body_style))
    content.append(Paragraph(
        "For allergy sufferers, latex and memory foam mattresses are generally better than innerspring because they are less hospitable "
        "to dust mites (the most common bedroom allergen). Natural latex is inherently hypoallergenic and antimicrobial. "
        "Look for mattresses with hypoallergenic covers and consider using a mattress protector. "
        "OEKO-TEX and CertiPUR-US certifications ensure the mattress materials are free from harmful chemicals and allergens. "
        "Avoid mattresses with wool or down filling if you have specific material allergies.",
        body_style
    ))
    content.append(Spacer(1, 8))

    content.append(Paragraph("<b>Temperature Regulation</b>", body_style))
    content.append(Paragraph(
        "If you sleep hot, consider mattresses with cooling features. Innerspring and hybrid mattresses naturally sleep cooler "
        "due to airflow through the coil system. For foam mattresses, look for gel-infused memory foam, open-cell foam, "
        "copper-infused foam, or phase-change material (PCM) covers. Latex naturally sleeps cooler than traditional memory foam. "
        "Some mattresses feature active cooling systems with temperature-regulating covers. "
        "Ideal bedroom temperature for sleep is between 60-67°F (15.5-19.4°C).",
        body_style
    ))

    content.append(PageBreak())

    # Chapter 6: Shopping Tips
    content.append(Paragraph("Chapter 6: Smart Shopping Tips", heading_style))
    content.append(Paragraph(
        "1. <b>Try before you buy:</b> If buying in-store, spend at least 15 minutes lying on each mattress in your natural sleeping position. "
        "If buying online, look for brands offering at least 100-night sleep trials.<br/><br/>"
        "2. <b>Read the fine print:</b> Check the return policy, warranty terms, and what voids the warranty. "
        "Most reputable brands offer 10-year limited warranties.<br/><br/>"
        "3. <b>Don't trust firmness labels alone:</b> Firmness perception is subjective and varies between brands. "
        "What one brand calls 'medium' might feel 'firm' to you.<br/><br/>"
        "4. <b>Consider your partner:</b> If sharing with a partner, consider motion isolation (memory foam excels here), "
        "edge support, and possibly a split firmness option.<br/><br/>"
        "5. <b>Replace on schedule:</b> Most mattresses should be replaced every 7-10 years. "
        "Signs it's time for a new mattress include visible sagging, waking with aches, and poor sleep quality.<br/><br/>"
        "6. <b>Foundation matters:</b> Use a proper foundation or platform bed. Box springs are designed for innerspring mattresses; "
        "foam and hybrid mattresses generally work best on a platform base or adjustable frame.<br/><br/>"
        "7. <b>Certifications to look for:</b> CertiPUR-US (foam safety), OEKO-TEX (textile safety), "
        "GOLS (organic latex), GOTS (organic textiles), GREENGUARD Gold (low emissions).",
        body_style
    ))

    doc.build(content)
    print(f"✅ Created: mattress_buying_guide.pdf")


def create_care_guide():
    """Create a mattress care and maintenance guide PDF."""
    doc = SimpleDocTemplate(
        str(OUTPUT_DIR / "mattress_care_maintenance_guide.pdf"),
        pagesize=letter,
        rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=72,
    )

    content = []

    # Title
    content.append(Paragraph("Mattress Care & Maintenance Guide", title_style))
    content.append(Paragraph("Professional Tips for Extending Your Mattress Lifespan", styles['Heading2']))
    content.append(Spacer(1, 20))

    # Chapter 1: Basic Care
    content.append(Paragraph("Chapter 1: Essential Mattress Care Practices", heading_style))
    content.append(Paragraph(
        "Proper mattress care is essential for maintaining comfort, hygiene, and extending the lifespan of your investment. "
        "A well-maintained mattress can last significantly longer than one that is neglected. "
        "Following these essential care practices will help you get the most out of your mattress purchase.",
        body_style
    ))
    content.append(Spacer(1, 8))

    content.append(Paragraph("<b>Use a Mattress Protector</b>", body_style))
    content.append(Paragraph(
        "A quality waterproof mattress protector is the single most important accessory for your mattress. "
        "It creates a barrier against sweat, body oils, dead skin cells, dust mites, and accidental spills. "
        "Without a protector, these substances accumulate in the mattress over time, creating an environment for bacteria, "
        "allergens, and odors. A good protector should be waterproof but breathable — look for protectors made with "
        "polyurethane laminate (PUL) or Tencel fabric. Wash your mattress protector every 1-2 months in warm water. "
        "A mattress protector also helps preserve your warranty, as many manufacturers consider stains a warranty violation.",
        body_style
    ))
    content.append(Spacer(1, 8))

    content.append(Paragraph("<b>Rotate Your Mattress Regularly</b>", body_style))
    content.append(Paragraph(
        "Rotating your mattress 180 degrees (head to foot) every 3-6 months helps distribute wear evenly "
        "and prevents permanent body impressions from forming. This is especially important during the first two years "
        "when the mattress materials are breaking in. Note that most modern mattresses should NOT be flipped (turned upside down) "
        "because they are designed with specific comfort layers on top and support layers on the bottom. "
        "Only rotate (spin) unless the manufacturer specifically states the mattress is flippable. "
        "Some double-sided mattresses are designed to be flipped, in which case alternate between rotating and flipping "
        "every 3 months for optimal wear distribution.",
        body_style
    ))
    content.append(Spacer(1, 8))

    content.append(Paragraph("<b>Ensure Proper Support</b>", body_style))
    content.append(Paragraph(
        "Your mattress needs a solid, even foundation to perform correctly and maintain its warranty. "
        "For innerspring mattresses, a matching box spring or foundation is recommended. "
        "For memory foam, latex, and hybrid mattresses, use a platform bed, slatted frame (with slats no more than 3 inches apart), "
        "or an adjustable base. Placing a mattress on the floor can restrict airflow and promote mold growth. "
        "Check your bed frame regularly to ensure no slats are broken or missing, as uneven support can cause premature sagging. "
        "For king and California king mattresses, ensure the frame has a center support bar.",
        body_style
    ))

    content.append(PageBreak())

    # Chapter 2: Cleaning
    content.append(Paragraph("Chapter 2: Cleaning Your Mattress", heading_style))

    content.append(Paragraph("<b>Regular Cleaning Schedule</b>", body_style))
    content.append(Paragraph(
        "Vacuum your mattress every 1-2 months using the upholstery attachment on your vacuum cleaner. "
        "Start from the top and work your way down, paying extra attention to seams and crevices where dust mites, "
        "dead skin cells, and other debris accumulate. If your vacuum has a HEPA filter, even better — "
        "it will capture tiny allergen particles that regular vacuums might recirculate into the air.",
        body_style
    ))
    content.append(Spacer(1, 8))

    content.append(Paragraph("<b>Spot Cleaning Stains</b>", body_style))
    content.append(Paragraph(
        "For fresh stains, act quickly. Blot (never rub) the stain with a clean cloth to absorb as much liquid as possible. "
        "For protein-based stains (blood, sweat, urine), use a solution of cold water and enzyme-based cleaner. "
        "Never use hot water on protein stains as it can set the stain permanently. "
        "For general stains, mix a small amount of mild dish soap with cold water, apply with a clean cloth, "
        "and blot with a dry cloth to remove moisture. For tough stains, a paste of baking soda and water "
        "can be applied, left for 30 minutes, then vacuumed off. "
        "Hydrogen peroxide (3%) can be effective on stubborn stains but test on an inconspicuous area first "
        "as it may bleach some fabrics. Never saturate a mattress with liquid — excess moisture can damage internal materials "
        "and promote mold growth.",
        body_style
    ))
    content.append(Spacer(1, 8))

    content.append(Paragraph("<b>Deep Cleaning</b>", body_style))
    content.append(Paragraph(
        "Deep clean your mattress every 6 months. Strip all bedding and mattress protector. "
        "Sprinkle a generous layer of baking soda over the entire mattress surface and let it sit for at least 2 hours "
        "(ideally 8 hours or overnight). The baking soda absorbs moisture, neutralizes odors, and helps break down surface oils. "
        "For added freshness, mix a few drops of essential oil (lavender or tea tree) with the baking soda before sprinkling. "
        "After the waiting period, thoroughly vacuum up all the baking soda. "
        "If possible, expose the mattress to sunlight for a few hours — UV rays naturally kill bacteria and dust mites. "
        "Several times a year, also clean under the mattress by lifting or removing it from the frame.",
        body_style
    ))

    content.append(PageBreak())

    # Chapter 3: Common Problems
    content.append(Paragraph("Chapter 3: Common Mattress Problems and Solutions", heading_style))

    content.append(Paragraph("<b>Sagging and Body Impressions</b>", body_style))
    content.append(Paragraph(
        "Some body impressions (typically up to 1-1.5 inches) are normal as a mattress breaks in — this is the foam "
        "conforming to your body shape and is not a defect. However, sagging greater than 1.5 inches may indicate "
        "a defect or worn-out mattress. To minimize sagging: rotate regularly, use a proper foundation, "
        "and avoid sitting on the edge of the bed frequently (this concentrates weight in a small area). "
        "If sagging occurs and your mattress is under warranty, document the depth with photos and measurements — "
        "most warranties cover sagging beyond 1-1.5 inches. A temporary fix for mild sagging is to place a thin mattress topper "
        "over the mattress, though this is a short-term solution.",
        body_style
    ))
    content.append(Spacer(1, 8))

    content.append(Paragraph("<b>Off-Gassing</b>", body_style))
    content.append(Paragraph(
        "New foam mattresses (memory foam, polyfoam) may emit a chemical smell when first unpacked — this is called off-gassing. "
        "It's caused by volatile organic compounds (VOCs) escaping from the foam. While the smell can be unpleasant, "
        "CertiPUR-US certified foams have been tested to ensure VOC levels are within safe limits. "
        "To minimize off-gassing: unpack the mattress in a well-ventilated room, open windows and use a fan to circulate air, "
        "and allow 24-72 hours for the smell to dissipate before sleeping on it. "
        "Some people are more sensitive to off-gassing than others. If you've had reactions to new foam products before, "
        "consider natural latex or innerspring mattresses, which have minimal to no off-gassing.",
        body_style
    ))
    content.append(Spacer(1, 8))

    content.append(Paragraph("<b>Dust Mites</b>", body_style))
    content.append(Paragraph(
        "Dust mites are microscopic creatures that feed on dead skin cells and thrive in warm, humid environments. "
        "The average mattress can contain tens of thousands to millions of dust mites. "
        "Their waste products are a major cause of allergic reactions and can trigger asthma. "
        "To control dust mites: use allergen-proof encasements (different from regular protectors — these fully enclose the mattress), "
        "wash bedding weekly in hot water (at least 130°F/54°C), maintain bedroom humidity below 50% using a dehumidifier, "
        "vacuum the mattress regularly with a HEPA filter vacuum, and consider hypoallergenic mattress materials "
        "(natural latex and memory foam are less hospitable to dust mites than innerspring).",
        body_style
    ))
    content.append(Spacer(1, 8))

    content.append(Paragraph("<b>Mold and Mildew</b>", body_style))
    content.append(Paragraph(
        "Mold growth in mattresses is caused by moisture accumulation, poor ventilation, and warm temperatures. "
        "Signs of mold include musty odors, visible black or green spots, and allergic reactions. "
        "Prevention is key: use a breathable waterproof protector, ensure adequate airflow under the mattress "
        "(don't place it directly on the floor), keep bedroom humidity low, and allow the mattress to air out "
        "when changing sheets. If mold has already formed, a mild mattress infestation can be treated by vacuuming "
        "the affected area, applying a solution of equal parts rubbing alcohol and water, "
        "and allowing it to dry completely in sunlight. Severe mold contamination usually requires mattress replacement.",
        body_style
    ))

    content.append(PageBreak())

    # Chapter 4: Lifespan Guide
    content.append(Paragraph("Chapter 4: Mattress Lifespan and Replacement Guide", heading_style))
    content.append(Paragraph(
        "Understanding when to replace your mattress is important for both sleep quality and health. "
        "Different mattress types have different expected lifespans:",
        body_style
    ))
    content.append(Spacer(1, 8))

    content.append(Paragraph(
        "<b>Innerspring:</b> 5-7 years. Coils lose tension over time together with the padding layers compressing.<br/>"
        "<b>Memory Foam:</b> 8-10 years. Higher density foams last longer. Low-quality foams may sag in 3-5 years.<br/>"
        "<b>Latex:</b> 12-20 years. Natural latex is exceptionally durable. Talalay may wear slightly faster than Dunlop.<br/>"
        "<b>Hybrid:</b> 7-10 years. The coil system determines the base lifespan, with foam layers wearing first.<br/>"
        "<b>Airbed:</b> 8-10 years. The pump mechanism typically is the first component to fail.",
        body_style
    ))
    content.append(Spacer(1, 12))

    content.append(Paragraph("<b>Signs It's Time for a New Mattress</b>", body_style))
    content.append(Paragraph(
        "Replace your mattress if you notice any of the following: "
        "visible sagging greater than 1.5 inches; waking up with aches, stiffness, or numbness that goes away during the day; "
        "sleeping better in hotels or on other beds; increased allergy symptoms at night; "
        "the mattress is more than 7-8 years old (for non-latex types); "
        "you can feel the coils through the surface; the mattress has visible lumps or unevenness; "
        "you and your partner roll toward each other unintentionally; "
        "or the mattress makes excessive noise (creaking or squeaking) when you move.",
        body_style
    ))
    content.append(Spacer(1, 12))

    # Chapter 5: Mattress Disposal
    content.append(Paragraph("Chapter 5: Responsible Mattress Disposal", heading_style))
    content.append(Paragraph(
        "When it's time to replace your mattress, dispose of it responsibly. Each year, approximately 20 million mattresses "
        "are discarded in the United States alone, and most end up in landfills where they take up significant space. "
        "Here are eco-friendly disposal options:",
        body_style
    ))
    content.append(Paragraph(
        "1. <b>Retailer take-back:</b> Many mattress retailers will remove your old mattress when delivering a new one, "
        "often for free or a small fee.<br/><br/>"
        "2. <b>Mattress recycling:</b> Up to 90% of a mattress can be recycled. Steel springs are melted down, "
        "foam is shredded for carpet padding, and fabric can be repurposed. Check for local mattress recycling facilities "
        "— organizations like the Mattress Recycling Council operate programs in several states.<br/><br/>"
        "3. <b>Donation:</b> If your mattress is still in good condition (no stains, tears, or major sagging), "
        "consider donating to local shelters, Habitat for Humanity ReStores, or other charitable organizations.<br/><br/>"
        "4. <b>Repurposing:</b> Creative options include using the springs for garden trellises, "
        "foam for pet beds or workshop padding, and fabric for upholstery projects.",
        body_style
    ))

    doc.build(content)
    print(f"✅ Created: mattress_care_maintenance_guide.pdf")


if __name__ == "__main__":
    create_buying_guide()
    create_care_guide()
    print(f"\n📁 PDFs saved to: {OUTPUT_DIR}")
