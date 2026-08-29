# Employee Badge Card

Double-sided employee badges in credit-card format (**86 × 54 mm**), one front page and one
back page per employee, printed straight from the employee form (**Print → Badge**).

Replaces the layout of Odoo's standard employee badge.

## Features

- **Badge agencies** — create your offices under *Employees > Configuration > Badge Agencies*.
  Each carries a label, a logo and a phone number, printed on the badges of the employees
  assigned to it.
- **Company branding** — slogan, tagline, website, back wordmark, fallback email and four
  colors, set on the *Employee Badge* tab of the company form.
- **QR code per employee**, generated in your accent color. Content priority: supplied image,
  then the *Badge QR Link* field, then the employee barcode.
- **Print-safe layout** — everything sits inside a 5 mm safe area and no solid color reaches
  the edge, so the badge survives a printer without full bleed. The thin rounded frame doubles
  as a cutting guide.

## Configuration

1. *Employees > Configuration > Badge Agencies* — create one record per office.
2. *Settings > Users & Companies > Companies*, tab *Employee Badge* — slogan, website,
   wordmark and colors.
3. On each employee — agency, photo, job title, work email, barcode or QR link.

## Requirements

- Odoo 19.0
- Python library `qrcode` (shipped with Odoo)

## Technical notes

- The report inherits `hr.print_employee_badge` through a single xpath anchor
  (`//t[@t-foreach='docs']`), which keeps it resilient across minor Odoo updates.
- No flexbox: tables and absolute positioning only, the sole reliable rendering under
  wkhtmltopdf.
- The QR code is generated in Python rather than through the standard `barcode` widget,
  which only renders in black.
- Given and family names are derived from `name` by splitting on the first space. Write
  compound given names with a hyphen to avoid a wrong split.
- The ✉ and ☎ glyphs are Unicode characters. If your server font lacks them, replace them
  with text in the `.bc-contact` block.

## Credits

**Croc'doo** — Odoo integrator, Toulouse • Montpellier • Pau
6 Esplanade du Muretain, 31600 Muret, France
+33 5 54 54 52 00 · hello@crocdoo.fr · [www.crocdoo.fr](https://www.crocdoo.fr)

Maintainer: Xavier Vliegen · Support: hello@crocdoo.fr
License: LGPL-3
