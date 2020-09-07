# Copyright 2017-2019 Tecnativa - Pedro M. Baeza
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models
import logging
_logger = logging.getLogger(__name__)


class HrAttendance(models.Model):
    _inherit = "hr.attendance"

    theoretical_hours = fields.Float(
        compute="_compute_theoretical_hours", store=True, compute_sudo=True
    )

    time_off = fields.Float(
        compute="_compute_time_off", store=True, compute_sudo=True
    )

    @api.depends("check_in", "employee_id")
    def _compute_theoretical_hours(self):
        obj = self.env["hr.attendance.theoretical.time.report"]
        for record in self:
            record.theoretical_hours = obj._theoretical_hours(
                record.employee_id, record.check_in
            )

    @api.depends("check_in", "employee_id")
    def _compute_time_off(self):
        obj = self.env["hr.attendance.theoretical.time.report"]
        for record in self:
            hours = obj._compute_leave_hours(
                record.employee_id, record.check_in
            )
            _logger.info('Hours {}'.format(hours))
            record.time_off = hours

