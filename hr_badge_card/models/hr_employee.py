import base64
import io
import logging

from odoo import api, fields, models

_logger = logging.getLogger(__name__)

try:
    import qrcode
except ImportError:  # pragma: no cover
    qrcode = None
    _logger.warning("Python library 'qrcode' is missing: badge QR codes will not be generated.")


class HrEmployee(models.Model):
    _inherit = "hr.employee"

    badge_agency_id = fields.Many2one(
        "hr.badge.agency",
        string="Badge Agency",
        index=True,
        help="Office or agency the employee is attached to. It drives the logo, "
             "the phone number and the label printed on the badge.",
    )
    badge_qr_url = fields.Char(
        string="Badge QR Link",
        help="Address encoded in the badge QR code: profile on a platform, contact page, "
             "online vCard... If empty, the employee barcode is encoded instead. "
             "Prefer a short URL: the longer it is, the finer the QR modules and the "
             "harder it is to scan at 18 mm.",
    )
    badge_qr_image = fields.Image(
        string="Badge QR Image",
        max_width=1024,
        max_height=1024,
        help="Only fill this in when a platform provides its own QR image. "
             "It is then printed as is, without recoloring.",
    )

    badge_label = fields.Char(compute="_compute_badge_fields")
    badge_phone = fields.Char(compute="_compute_badge_fields")
    badge_email = fields.Char(compute="_compute_badge_fields")
    badge_logo = fields.Binary(compute="_compute_badge_fields")
    badge_back_logo = fields.Binary(compute="_compute_badge_fields")
    badge_website = fields.Char(compute="_compute_badge_fields")
    badge_first_name = fields.Char(compute="_compute_badge_name")
    badge_last_name = fields.Char(compute="_compute_badge_name")
    badge_qr = fields.Char(compute="_compute_badge_qr")

    @api.depends("badge_agency_id", "work_email", "company_id")
    def _compute_badge_fields(self):
        for employee in self:
            agency = employee.badge_agency_id
            company = employee.company_id or self.env.company
            employee.badge_label = agency.name or ""
            employee.badge_phone = agency.phone or company.phone or ""
            employee.badge_email = (
                employee.work_email
                or agency.email
                or company.badge_fallback_email
                or company.email
                or ""
            )
            employee.badge_logo = agency.logo or company.logo
            employee.badge_back_logo = company.badge_back_logo or company.logo
            employee.badge_website = company.badge_website or company.website or ""

    @api.depends("name")
    def _compute_badge_name(self):
        """Split the name into two typographic levels on the badge.

        The first word is treated as the given name (printed light), the rest as
        the family name (printed bold). A single-word name goes entirely to the
        bold line.
        """
        for employee in self:
            parts = (employee.name or "").strip().split(" ", 1)
            if len(parts) == 2 and parts[1].strip():
                employee.badge_first_name = parts[0]
                employee.badge_last_name = parts[1].strip()
            else:
                employee.badge_first_name = False
                employee.badge_last_name = employee.name or ""

    @api.depends("barcode", "badge_qr_url", "badge_qr_image", "company_id.badge_color_qr")
    def _compute_badge_qr(self):
        """Badge QR code as a data URI, by order of priority:

        1. an image supplied by an external platform, printed as is;
        2. the link stored in ``badge_qr_url``, encoded in the company color;
        3. otherwise the employee barcode, encoded in the company color.

        Odoo's standard ``barcode`` widget only renders in black, so the image is
        generated here to allow a custom color.
        """
        for employee in self:
            employee.badge_qr = False

            if employee.badge_qr_image:
                employee.badge_qr = "data:image/png;base64,%s" % employee.badge_qr_image.decode()
                continue

            payload = employee.badge_qr_url or employee.barcode
            if not payload or qrcode is None:
                continue

            company = employee.company_id or self.env.company
            color = company.badge_color_qr or "#000000"
            try:
                qr = qrcode.QRCode(
                    error_correction=qrcode.constants.ERROR_CORRECT_M,
                    box_size=10,
                    border=1,
                )
                qr.add_data(payload)
                qr.make(fit=True)
                image = qr.make_image(fill_color=color, back_color="white")
                buffer = io.BytesIO()
                image.save(buffer, format="PNG")
                employee.badge_qr = "data:image/png;base64,%s" % base64.b64encode(
                    buffer.getvalue()
                ).decode()
            except Exception:  # pragma: no cover
                _logger.exception("Could not generate the badge QR code for %s", employee.name)
