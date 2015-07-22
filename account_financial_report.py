# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp.osv import fields, osv


class accounting_report(osv.osv_memory):
    _inherit = "accounting.report"
    _description = "Accounting Report"


    def check_report_with(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        res = super(accounting_report, self).check_report(cr, uid, ids, context=context)
        data = {}
        data['form'] = self.read(cr, uid, ids, ['account_report_id', 'date_from_cmp',  'date_to_cmp',  'fiscalyear_id_cmp', 'journal_ids', 'period_from_cmp', 'period_to_cmp',  'filter_cmp',  'chart_account_id', 'target_move'], context=context)[0]
        for field in ['fiscalyear_id_cmp', 'chart_account_id', 'period_from_cmp', 'period_to_cmp', 'account_report_id']:
            if isinstance(data['form'][field], tuple):
                data['form'][field] = data['form'][field][0]
        comparison_context = self._build_comparison_context(cr, uid, ids, data, context=context)
        res['data']['form']['comparison_context'] = comparison_context
        fiscalyear_list = []
        chart_account_id = self.pool.get("account.account").browse(cr, uid, res['data']['form']['chart_account_id'], context=context)
        if not chart_account_id.company_id.child_ids:
            return res      
        if res['data']['form']['fiscalyear_id']:
            fiscalyear_id = self.pool.get("account.fiscalyear").browse(cr, uid, res['data']['form']['fiscalyear_id'], context=context)
            fiscalyear_id_2 = self.pool.get("account.fiscalyear").search(cr, uid, [('company_id','in', [comp.id for comp in fiscalyear_id.company_id.child_ids]),
                                                                                   ('date_start','=', fiscalyear_id.date_start),
                                                                                   ('date_stop','=', fiscalyear_id.date_stop)], context=context)
 
            if fiscalyear_id_2:
                fiscalyear_list = [f for f in fiscalyear_id_2]
                fiscalyear_list.append(fiscalyear_id.id)
            else:
                fiscalyear_list.append(fiscalyear_id.id) 

            res['data']['form']['fiscalyear_id'] = fiscalyear_list
            res['data']['form']['used_context']['fiscalyear'] = fiscalyear_list
            res['data']['form']['used_context'].update({'without_con': True})
        return res

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
