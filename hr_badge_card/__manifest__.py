{
    "name": "Employee Badge Card",
    "version": "19.0.1.0.0",
    "category": "Human Resources/Employees",
    "summary": "Print double-sided employee badges in credit-card format, branded per agency",
    "description": """
Employee Badge Card
===================

Replaces the standard employee badge with a double-sided card in credit-card format
(86 x 54 mm), one front page and one back page per employee, printed straight from the
employee form.

Branded per agency
------------------

Create your offices or agencies under *Employees > Configuration > Badge Agencies*.
Each one carries a label, a logo and a phone number. Assign an agency to an employee and
the badge is branded accordingly, without touching a line of code.

Your colors, your signature
---------------------------

Slogan, tagline, website, back wordmark, fallback email and the four badge colors are set
per company, on the *Employee Badge* tab of the company form.

QR code
-------

Each employee gets a QR code, generated in your accent color. Its content follows this
order of priority: an image supplied by an external platform, then the *Badge QR Link*
field, then the employee barcode.

Made for printing
-----------------

The whole layout sits inside a 5 mm safe area and no solid color reaches the edge, so the
badge stays clean even on a printer without full bleed. A thin rounded frame doubles as a
cutting guide.
""",
    "author": "Croc'doo",
    "maintainer": "Xavier Vliegen",
    "website": "https://www.crocdoo.fr",
    "support": "hello@crocdoo.fr",
    "license": "LGPL-3",
    "depends": ["hr"],
    "external_dependencies": {"python": ["qrcode"]},
    "data": [
        "security/ir.model.access.csv",
        "data/report_paperformat.xml",
        "views/hr_badge_agency_views.xml",
        "views/hr_employee_views.xml",
        "views/res_company_views.xml",
        "report/hr_employee_badge.xml",
    ],
    "demo": [
        "demo/hr_badge_agency_demo.xml",
    ],
    "images": ["static/description/banner.png"],
    "installable": True,
    "application": False,
    "auto_install": False,
}
