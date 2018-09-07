# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions
import os
from collections import defaultdict
import math

from odoo import api, fields, models, _
from odoo.addons import decimal_precision as dp
from odoo.exceptions import UserError
from odoo.tools import float_compare