# coding=utf-8
"""Views for projects."""
# noinspection PyUnresolvedReferences
from django.http import HttpResponse
import json
import logging

logger = logging.getLogger(__name__)

from django.core.urlresolvers import reverse
from django.views.generic import (
    CreateView,
)

from braces.views import LoginRequiredMixin
from vota.models import Vote, Ballot
from vota.forms import VoteForm


class VoteCreateUpdateView(LoginRequiredMixin, CreateView):
    context_object_name = 'vote'
    template_name = 'vote/create.html'
    model = Vote
    form_class = VoteForm

    def get_context_data(self, **kwargs):
        context = super(VoteCreateUpdateView, self).get_context_data(**kwargs)
        context['voted'] = self.voted
        return context

    def get_form_kwargs(self):
        kwargs = super(VoteCreateUpdateView, self).get_form_kwargs()
        the_ballot_slug = self.kwargs['ballotSlug']
        self.the_ballot = Ballot.objects.get(slug=the_ballot_slug)
        try:
            existing_vote = Vote.objects.filter(ballot=self.the_ballot)\
                .get(user=self.request.user)
            kwargs.update({'instance': existing_vote})
            self.voted = True
        except Vote.DoesNotExist:
            self.voted = False
            kwargs.update({'instance': self.object})
        return kwargs

    def form_valid(self, form):
        form.instance.ballot = self.the_ballot
        form.instance.user = self.request.user
        form.save()
        return HttpResponse(json.dumps({'successful': True}),
                            content_type='application/json')

    def form_invalid(self, form):
        errors = form.errors
        error_dict = {'errors': errors}
        return HttpResponse(json.dumps(error_dict),
                            content_type='application/json')

    def get_success_url(self):
        return reverse('ballot-detail',
                       kwargs={'projectSlug':
                               self.object.ballot.committee.project.slug,
                               'committeeSlug':
                               self.object.ballot.committee.slug,
                               'slug': self.object.ballot.slug
                               })
