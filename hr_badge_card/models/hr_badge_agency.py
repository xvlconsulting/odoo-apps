from odoo import fields, models


class HrBadgeAgency(models.Model):
    _name = "hr.badge.agency"
    _description = "Employee Badge Agency"
    _order = "sequence, name"

    name = fields.Char(
        string="Label",
        required=True,
        translate=True,
        help="Text printed on the badge, for example \"Paris Office\" or "
             "\"Southern Region\". Keep it short: it is printed in a small pill.",
    )
    sequence = fields.Integer(default=10)
    active = fields.Boolean(default=True)
    logo = fields.Image(
        string="Logo",
        max_width=1024,
        max_height=1024,
        help="Logo printed on the front of the badge. If empty, the company logo is used.",
    )
    phone = fields.Char(
        string="Phone",
        help="Phone number printed on the badges of the employees of this agency.",
    )
    email = fields.Char(
        string="Email",
        help="Fallback email printed when the employee has no work email. "
             "If empty, the company badge fallback email is used.",
    )
    company_id = fields.Many2one(
        "res.company",
        string="Company",
        required=True,
        default=lambda self: self.env.company,
        index=True,
    )
    employee_ids = fields.One2many("hr.employee", "badge_agency_id", string="Employees")
    employee_count = fields.Integer(compute="_compute_employee_count", string="Employees")

    def _compute_employee_count(self):
        data = self.env["hr.employee"]._read_group(
            [("badge_agency_id", "in", self.ids)],
            ["badge_agency_id"],
            ["__count"],
        )
        counts = {agency.id: count for agency, count in data}
        for agency in self:
            agency.employee_count = counts.get(agency.id, 0)
