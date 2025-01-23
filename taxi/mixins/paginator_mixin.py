from django.core.paginator import PageNotAnInteger, EmptyPage
from django.views import generic


class PaginatorMixin(generic.ListView):
    paginate_by = 5
    MIN_PER_PAGE = 1
    MAX_PER_PAGE = 10

    def paginate_queryset(self, queryset, per_page):
        paginator = self.get_paginator(
            queryset,
            per_page,
            orphans=self.get_paginate_orphans(),
            allow_empty_first_page=self.get_allow_empty(),
        )
        page = self.kwargs.get("page") or self.request.GET.get("page") or 1
        try:
            page_number = int(page)
            if page_number < 1:
                page_number = 1
        except ValueError:
            if page == "last":
                page_number = paginator.num_pages
            else:
                page_number = 1
        try:
            page = paginator.page(page_number)
        except EmptyPage:
            page = paginator.page(paginator.num_pages)

        return (paginator, page, page.object_list, page.has_other_pages())

    def get_paginate_by(self, queryset):
        per_page = (
                int(self.request.GET.get('per_page', 0)) or
                self.request.session.get('per_page') or
                self.paginate_by
        )

        if per_page < self.MIN_PER_PAGE:
            per_page = self.MIN_PER_PAGE
        if per_page > self.MAX_PER_PAGE:
            per_page = self.MAX_PER_PAGE
        self.request.session['per_page'] = per_page

        return per_page
