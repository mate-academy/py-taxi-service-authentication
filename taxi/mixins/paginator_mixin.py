from django.core.paginator import PageNotAnInteger, EmptyPage, Paginator


class HardLimitPagePaginator(Paginator):
    def page(self, number):
        try:
            number = self.validate_number(number)
        except PageNotAnInteger:
            number = 1
        except EmptyPage:
            number = 1 if number < 1 else self.num_pages
        return super().page(number)


class PaginationMixin:
    paginate_by = 5
    MIN_PER_PAGE = 1
    MAX_PER_PAGE = 10

    paginator_class = HardLimitPagePaginator

    def get_paginate_by(self, queryset):
        per_page = (
                self.request.GET.get('per_page', 0) or
                self.request.session.get('per_page') or
                self.paginate_by
        )

        try:
            per_page = int(per_page)
        except ValueError:
            per_page = self.paginate_by

        new_per_page = per_page

        new_per_page = max(self.MIN_PER_PAGE, min(new_per_page, self.MAX_PER_PAGE))

        self.request.session["per_page"] = new_per_page

        return new_per_page
