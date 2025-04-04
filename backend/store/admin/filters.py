from django.contrib.admin import SimpleListFilter
from store.model import Problem


class RelatedProblemSubjectFilter(SimpleListFilter):
    title = "Problem Subject"
    parameter_name = "problem_subject"

    def lookups(self, request, model_admin):
        subjects = set([problem.subject for problem in Problem.objects.all()])
        return [(subject, subject) for subject in subjects]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(problem__subject=self.value())
        return queryset
