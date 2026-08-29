from odoo import fields, models

DEFAULT_PRIMARY = "#34495E"
DEFAULT_ACCENT = "#16A085"
DEFAULT_HIGHLIGHT = "#F39C12"


class ResCompany(models.Model):
    _inherit = "res.company"

    badge_slogan = fields.Char(
        string="Badge Slogan",
        translate=True,
        help="Short signature printed at the bottom of both sides of the badge.",
    )
    badge_tagline = fields.Char(
        string="Badge Tagline",
        translate=True,
        help="Second line under the slogan, for example the list of your offices.",
    )
    badge_website = fields.Char(
        string="Badge Website",
        help="Address printed in large type on the back of the badge. "
             "If empty, the company website is used.",
    )
    badge_back_logo = fields.Image(
        string="Badge Back Logo",
        max_width=1400,
        max_height=600,
        help="Wordmark printed on the back of the badge. If empty, the company logo is used.",
    )
    badge_fallback_email = fields.Char(
        string="Badge Fallback Email",
        help="Printed when the employee has no work email and the agency has none either.",
    )
    badge_color_primary = fields.Char(string="Badge Primary Color", default=DEFAULT_PRIMARY)
    badge_color_accent = fields.Char(string="Badge Accent Color", default=DEFAULT_ACCENT)
    badge_color_highlight = fields.Char(string="Badge Highlight Color", default=DEFAULT_HIGHLIGHT)
    badge_color_qr = fields.Char(
        string="Badge QR Color",
        default=DEFAULT_ACCENT,
        help="Color of the generated QR code. Keep it dark enough to stay scannable.",
    )
