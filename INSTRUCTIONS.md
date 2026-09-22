# Implementation Instructions: Hotel Pokhara Eye Website

## 1. Project Overview & Context
- **Business**: Hotel Pokhara Eye — a premier boutique hotel situated in Pokhara, Nepal, offering panoramic vistas of the Annapurna mountain range, Machhapuchhre (Fishtail Peak), and proximity to Phewa Lake.
- **Goal**: Develop a visually stunning, responsive, luxury hospitality website featuring hotel highlights, accommodations, dining, scenic galleries, and an interactive inquiry form.
- **Database Scope**: Do not create or run any database models or migrations. The site operates as a dynamic presentation site with direct SMTP email-based inquiry processing.

---

## 2. Environment & Secrets Configuration (.env)
- **Environment Management**:
  - Integrate environment variable handling (such as with `python-dotenv`) inside the project settings.
  - Read all sensitive credentials exclusively from a `.env` file at the project root.
- **Required Environment Variables**:
  - `SECRET_KEY`: Django cryptographic signing key.
  - `DEBUG`: Boolean flag for development mode.
  - `ALLOWED_HOSTS`: Comma-separated list of permitted hostnames.
  - `EMAIL_BACKEND`: Configured for Django SMTP (`django.core.mail.backends.smtp.EmailBackend`) or console backend during offline testing.
  - `EMAIL_HOST`: SMTP host server (e.g., `smtp.gmail.com`).
  - `EMAIL_PORT`: SMTP port (e.g., `587` for TLS or `465` for SSL).
  - `EMAIL_USE_TLS`: Boolean flag for TLS encryption.
  - `EMAIL_HOST_USER`: Authenticated email address for outbound transmission.
  - `EMAIL_HOST_PASSWORD`: Application-specific password or SMTP token.
  - `DEFAULT_FROM_EMAIL`: Formatted sender address displayed to recipients.
  - `HOTEL_RECEIVER_EMAIL`: The designated hotel front desk inbox where inquiry notifications must be delivered.
- Provide a template file (`.env.example`) documenting variable names with placeholder values for quick configuration.

---

## 3. Visual Identity & Design Guidelines
- **Atmosphere**: Himalayan serene luxury, tranquility, modern boutique hospitality.
- **Color Palette**:
  - Primary Base: Deep Himalayan Slate / Midnight Navy (`#0B132B` / `#1C2541`).
  - Accent / Highlights: Warm Golden Amber / Sunrise Glow (`#D4AF37` / `#C5A059`).
  - Backgrounds: Clean warm whites and soft alpine mist (`#F8F9FA` / `#F1F5F9`).
  - Text: High-contrast charcoal slate (`#1E293B`) for body readability and deep navy for headings.
- **Typography**:
  - Display / Headings: Sophisticated serif with character (e.g., Playfair Display or Cormorant Garamond via Google Fonts).
  - Body / UI: Clean, legible sans-serif with multiple weights (e.g., Plus Jakarta Sans or Outfit via Google Fonts).
- **Styling Aesthetics**:
  - Avoid generic, flat, or bare layouts; build an immersive high-end feel.
  - Glassmorphic navigation header with subtle blur and border highlights.
  - Smooth micro-interactions, subtle hover elevations on room cards, and soft transitions.
  - Full mobile responsiveness across standard phone, tablet, laptop, and widescreen breakpoints.

---

## 4. Media Asset Mapping & Wise Usage
Integrate all existing assets located under `static/images/` deliberately across the page layout:
- **`herosection.mp4`**:
  - Feature as the background video in the hero section.
  - Configure with autoplay, muted, loop, and playsinline attributes.
  - Place a dark gradient overlay on top of the video to ensure text contrast and readability.
  - Provide a fallback background image or gradient for mobile data-saver modes.
- **`logo.jpg`**:
  - Display in the sticky navigation bar and in the website footer.
  - Ensure proper border radius or subtle circular framing to blend smoothly with dark and light navigation backgrounds.
- **`bedroom1.jpg` & `bedroom2.jpg`**:
  - Showcase in the Rooms & Accommodations section.
  - Represent luxury room tiers (e.g., *Deluxe Annapurna View Room* and *Executive Mountain Suite*).
  - Accompany with feature badges: King Bed, Private Balcony, High-Speed Wi-Fi, Mountain Panorama, Ensuite Bath.
- **`cafeteria1.jpg` & `cafeteria2.jpg`**:
  - Showcase in the Dining & Rooftop Cafeteria section.
  - Highlight the on-site dining experience: artisan Himalayan coffee, organic breakfast, panoramic rooftop seating, and sunset dining.
- **`view3.jpg`, `view4.jpg`, `views1.jpg`, `views2.jpg`**:
  - Curate into an interactive Scenic Gallery / Experience section.
  - Illustrate the authentic viewpoint from the hotel balconies and rooftop: sunrise over the Annapurnas, Machhapuchhre views, mist over Pokhara valley, and twilight mountain contours.

---

## 5. Website Architecture & Section Breakdown
Build a cohesive single-page luxury portal or organized modular template with the following sections:

1. **Header & Navigation Bar**:
   - Hotel logo and brand title.
   - Smooth-scroll anchor links: *About*, *Rooms*, *Dining*, *Views*, *Amenities*, *Contact*.
   - Prominent call-to-action button: *Book / Inquire Now*.
   - Mobile hamburger navigation menu with smooth reveal.
2. **Hero Section**:
   - Immersive video background (`herosection.mp4`).
   - Evocative headline (e.g., "Wake Up to the Majesty of the Annapurnas").
   - Subtitle describing the sanctuary experience in Pokhara.
   - Floating Quick Inquiry bar (Check-in, Check-out, Guests, Room Type) that auto-scrolls and populates the contact form.
3. **About Section**:
   - Story of Hotel Pokhara Eye, blending authentic Nepali warmth with contemporary comfort.
   - Key highlights: prime view location, peaceful environment away from traffic noise, yet close to Lakeside Pokhara.
4. **Rooms & Suites Section**:
   - Highlighting room categories with `bedroom1.jpg` and `bedroom2.jpg`.
   - List of room inclusions, amenities, and guest capacity.
   - "Inquire About This Room" button that pre-selects the corresponding room in the inquiry form.
5. **Rooftop Cafeteria & Dining Section**:
   - Featuring `cafeteria1.jpg` and `cafeteria2.jpg`.
   - Description of fresh local ingredients, specialty beverages, and panoramic outdoor seating.
6. **Scenic Views & Visual Gallery**:
   - Grid or masonry layout of `views1.jpg`, `views2.jpg`, `view3.jpg`, and `view4.jpg`.
   - Captions highlighting Annapurna range vistas, Fishtail sunrise, and valley scenery.
7. **Hotel Amenities & Experience**:
   - Iconic cards highlighting: 24/7 Front Desk, High-Speed Wi-Fi, Hot Shower, Airport/Bus Station Pick-up, Trekking & Paragliding Assistance, Rooftop Observation Deck.
8. **Pokhara Attractions Guide**:
   - Brief guide to nearby sights: Phewa Lake boating, World Peace Pagoda, Sarangkot sunrise point, Devi's Fall.
9. **Guest Inquiries & Contact Section**:
   - Two-column split layout:
     - **Contact Information**: Physical address (Lakeside, Pokhara, Nepal), direct telephone, reservation email, interactive map card, and a direct WhatsApp button.
     - **Inquiry Form**: Guest input fields for reservation requests.
10. **Footer**:
    - Brand description, quick navigation links, contact details, social links, and copyright notice.

---

## 6. Inquiry Form Requirements & User Experience
- **Form Fields**:
  - Full Name (required)
  - Email Address (required, email format validation)
  - Phone Number / WhatsApp (required)
  - Check-in Date (date picker)
  - Check-out Date (date picker)
  - Room Preference (Dropdown: Deluxe Mountain View, Executive Suite, Family Room, General Inquiry)
  - Number of Guests (Adults/Children selector)
  - Message / Special Requirements (textarea)
- **Form Handling & Feedback**:
  - Secure CSRF token inclusion on submission.
  - Client-side validation ensuring required fields and realistic date sequences (check-out after check-in).
  - Clear user feedback upon submission: visual success toast or status alert notifying the guest that their inquiry has been received.
  - Graceful error notification if submission encounters network or configuration issues.

---

## 7. Dual Email Notification Workflow
Upon receiving a valid inquiry POST request, the application must execute an automated dual email dispatch via Django's email framework:

1. **Email to the Hotel (`HOTEL_RECEIVER_EMAIL`)**:
   - **Subject**: New Reservation Inquiry from [Guest Name] — Hotel Pokhara Eye
   - **Content**:
     - Complete guest contact information (Name, Email, Phone).
     - Requested booking details (Check-in, Check-out, Room Type, Number of Guests).
     - Full inquiry message / special requests.
     - Timestamp of submission.
   - **Reply-To**: Set to the guest's email address so the hotel can directly hit "Reply" to respond.

2. **Email to the Guest (`user_email`)**:
   - **Subject**: We have received your inquiry — Hotel Pokhara Eye
   - **Content**:
     - Warm, polite greeting addressing the guest by name.
     - Confirmation that their inquiry for the specified dates and room type has reached the reservations desk.
     - Reassurance: "Our team will review your dates and reach you shortly with availability and details."
     - Contact details of the hotel (phone, WhatsApp, Lakeside address) should they need immediate assistance.
     - Signature from the Management & Hospitality Team at Hotel Pokhara Eye.

3. **Resilience & Error Handling**:
   - Wrap the email dispatch routine in exception handling.
   - If SMTP credentials are invalid, missing, or the server is unreachable, log the exception cleanly and provide a helpful user-facing status message without triggering an unhandled server 500 crash.

---

## 8. Django Implementation Specifications
- **Settings Configuration**:
  - Load environment variables from `.env` on startup.
  - Set `STATIC_URL`, `STATICFILES_DIRS` pointing to `BASE_DIR / 'static'`, and `STATIC_ROOT`.
  - Set `MEDIA_URL` and `MEDIA_ROOT`. Ensure there are no stray syntax errors in setting declarations.
  - Configure standard `EMAIL_*` settings pulling from environment variables.
- **URL Routing**:
  - Route the root URL (`/`) to the main page view.
  - Route the inquiry submission endpoint (`/inquiry/` or `/contact/`) to the inquiry handler view.
  - Ensure static media serving is enabled during development under `DEBUG = True`.
- **View Logic**:
  - Render the landing page with necessary context.
  - In the inquiry view, process POST data, validate inputs, construct both email messages, dispatch via Django's email utility, and return appropriate success or error responses (supporting both traditional redirects with flash messages and asynchronous JSON responses).

---

## 9. Verification & Quality Assurance Checklist
- **Configuration Check**: Run Django's project check command to verify settings and syntax.
- **Asset Verification**: Confirm all images (`bedroom1.jpg`, `bedroom2.jpg`, `cafeteria1.jpg`, `cafeteria2.jpg`, `logo.jpg`, `views1.jpg`, `views2.jpg`, `view3.jpg`, `view4.jpg`) and the video (`herosection.mp4`) render correctly in the browser.
- **Form & Email Dispatch Test**:
  - Submit a test inquiry through the form.
  - Verify that the hotel receiving email receives the detailed guest request.
  - Verify that the guest email receives the confirmation acknowledgment.
  - Test behavior when email settings are set to console backend to confirm message layout and fields.
- **Responsive Inspection**: Test the interface on mobile and desktop viewports to verify layout hierarchy, text legibility, navigation toggle, and image scaling.
