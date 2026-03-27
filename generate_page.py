#!/usr/bin/env python3
import os
import argparse
import shutil

def create_landing_page(args):
    # Paths
    base_dir = os.path.dirname(os.path.abspath(__file__))
    source_file = os.path.join(base_dir, "index.html")
    
    # Create the new directory for the slug
    slug = args.city.lower().replace(" ", "-")
    output_dir = os.path.join(base_dir, slug)
    os.makedirs(output_dir, exist_ok=True)
    
    out_path = os.path.join(output_dir, "index.html")
    
    # Read the base template (we use the Orlando home page as the base template)
    with open(source_file, "r", encoding="utf-8") as f:
        content = f.read()
        
    # --- Phone Replacements ---
    # Convert formats like 413-288-6088 or (413) 288-6088 or +14132886088
    # Orlando's base phone is 407-468-0026
    
    raw_old_phone = "4074680026"
    raw_new_phone = "".join(filter(str.isdigit, args.phone))
    if len(raw_new_phone) == 10: # Ensure valid US phone
        formatted_new_phone = f"({raw_new_phone[:3]}) {raw_new_phone[3:6]}-{raw_new_phone[6:]}"
        tel_new_phone = f"{raw_new_phone[:3]}-{raw_new_phone[3:6]}-{raw_new_phone[6:]}"
        
        content = content.replace("407-468-0026", formatted_new_phone)
        content = content.replace("tel:407-468-0026", f"tel:{tel_new_phone}")
        # Clean up double formats if any
        content = content.replace(f"tel:{formatted_new_phone}", f"tel:{tel_new_phone}")
        content = content.replace("+14074680026", f"+1{raw_new_phone}")
    
    # --- Geography Replacements ---
    content = content.replace("Orlando", args.city)
    content = content.replace('"FL"', f'"{args.state.upper()}"')
    content = content.replace('FL.', f'{args.state.upper()}.')
    
    # Change maps embed strictly
    content = content.replace("Orlando%2C%20FL", f"{args.city.replace(' ', '%20')}%2C%20{args.state.upper()}")
    
    if args.zip:
        content = content.replace("32801", args.zip)
        
    # Example coordinates (Defaults to base if not provided, but maps query fixes itself usually)
    if args.lat and args.lng:
        content = content.replace("28.5383", str(args.lat))
        content = content.replace("-81.3792", str(args.lng))
        
    # --- Paths Replacements ---
    # Assuming base index.html assets are in root, so when moving to a subfolder we prefix with '../'
    content = content.replace('href="style.css"', 'href="../style.css"')
    content = content.replace('src="new-logo.png"', 'src="../new-logo.png"')
    content = content.replace('src="hero.png"', 'src="../hero.png"')
    content = content.replace('src="reference', 'src="../reference')
    content = content.replace('src="reviews1.png"', 'src="../reviews1.png"')
    content = content.replace('src="Screenshot', 'src="../Screenshot')
    
    # Write output file
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(content)
        
    print(f"✅ Successfully generated new landing page for {args.city} at: /{slug}/index.html")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a new localized Locksmith landing page.")
    parser.add_argument("--city", required=True, help="Target City (e.g., 'Boston')")
    parser.add_argument("--state", required=True, help="Target State abbreviation (e.g., 'MA')")
    parser.add_argument("--phone", required=True, help="Target Phone Number (e.g., '617-555-1234')")
    parser.add_argument("--zip", required=False, help="Target ZIP code (optional, overrides default schema)")
    parser.add_argument("--lat", required=False, help="Target Latitude (e.g., 42.3601)")
    parser.add_argument("--lng", required=False, help="Target Longitude (e.g., -71.0589)")
    
    args = parser.parse_args()
    create_landing_page(args)
