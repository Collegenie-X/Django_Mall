from .unit_admin import UnitTypeAdmin
from .section_admin import SectionTypeAdmin
from .problem_admin import ProblemAdmin
from .filters import RelatedProblemSubjectFilter

from store.models import UnitType, SectionType, Problem

from django.contrib import admin

admin.site.register(UnitType, UnitTypeAdmin)
admin.site.register(SectionType, SectionTypeAdmin)
admin.site.register(Problem, ProblemAdmin)
admin.site.add_action(RelatedProblemSubjectFilter)
