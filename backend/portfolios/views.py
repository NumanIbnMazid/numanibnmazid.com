from django import forms
from portfolios.models import (
    Skill,
    ProfessionalExperience, ProfessionalExperienceMedia
)
from portfolios.forms import (
    SkillForm,
    ProfessionalExperienceMediaForm, ProfessionalExperienceWithMediaForm
)
from utils.mixins import CustomViewSetMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _

skill_decorators = professional_experience_decorators= [login_required]


# ----------------------------------------------------
# *** Skill ***
# ----------------------------------------------------

@method_decorator(skill_decorators, name='dispatch')
class SkillView(CustomViewSetMixin):
    template_name = "portfolios/skills/skills.html"
    model = Skill
    form_class = SkillForm
    success_url = 'portfolios:skills'
    lookup_field = 'slug'
    update_success_message = "Skill has been updated successfully."
    url_list = ["skills", "skill_create", "skill_detail", "skill_update", "skill_delete"]

    def get_queryset(self):
        return Skill.objects.all()

    def get_object(self, *args, **kwargs):
        return Skill.objects.get_by_slug(self.kwargs.get('slug'))

    def form_valid(self, form):
        # assign user to the form
        form.instance.user = self.request.user
        # validate unique skill title
        qs = Skill.objects.filter(user=self.request.user, title__iexact=form.cleaned_data.get('title')).exclude(slug__iexact=self.kwargs.get('slug'))
        if qs:
            form.add_error(
                "title", forms.ValidationError(
                    f"This skill already exists!"
                )
            )
        return super().form_valid(form)


# ----------------------------------------------------
# *** Professional Experience ***
# ----------------------------------------------------

@method_decorator(professional_experience_decorators, name='dispatch')
class ProfessionalExperienceView(CustomViewSetMixin):
    template_name = "portfolios/professional-experiences/professional-experiences.html"
    snippet_template = "portfolios/professional-experiences/professional-experiences-snippet.html"
    model = ProfessionalExperience
    form_class = ProfessionalExperienceWithMediaForm
    paginate_by = 4
    success_url = 'portfolios:professional_experiences'
    lookup_field = 'slug'
    url_list = ["professional_experiences", "professional_experience_create", "professional_experience_detail", "professional_experience_update", "professional_experience_delete"]

    def get_queryset(self):
        return ProfessionalExperience.objects.all()

    def get_object(self, *args, **kwargs):
        return ProfessionalExperience.objects.get_by_slug(self.kwargs.get('slug'))

    def get_media_delete_context_data(self, **kwargs):
        context = {}
        context["page_title"] = context["head_title"] = "Delete Professional Experience Media"
        context["action"] = "delete"
        return context

    def media_delete(self, request, *args, **kwargs):
        qs = ProfessionalExperienceMedia.objects.filter(slug=self.kwargs.get('slug'))
        experience_object = qs.first().professional_experience
        if qs:
            # delete object
            qs.delete()
            # add success message
            messages.add_message(
                self.request, messages.SUCCESS, "Media Deleted Successfully!"
            )
            return HttpResponseRedirect(self.get_success_url())
        else:
            messages.add_message(
                self.request, messages.ERROR, "Media not found!"
            )
            raise Http404(_("Object not found!"))

    def form_valid(self, form):
        if form.is_valid():

            # assign user to the form
            form.instance.user = self.request.user

            # validate unique  company name
            qs = ProfessionalExperience.objects.filter(user=self.request.user, company__iexact=form.cleaned_data.get('company')).exclude(slug__iexact=self.kwargs.get('slug'))
            if qs:
                form.add_error(
                    "title", forms.ValidationError(
                        f"This company already exists!"
                    )
                )
                return super().form_invalid(form)

            # save the form
            self.object = form.save()

            # get files from form
            files = self.request.FILES.getlist('file')

            # save professional experience media files to the database if any
            if len(files) > 0:
                for file in files:
                    professional_experience_media_form = ProfessionalExperienceMediaForm(self.request.POST, self.request.FILES)
                    if professional_experience_media_form.is_valid():
                        professional_experience_media_form.instance.professional_experience = self.object
                        # save the form
                        professional_experience_media_form.save()

        return super().form_valid(form)


# ----------------------------------------------------
# *** Education ***
# ----------------------------------------------------

# @method_decorator(professional_experience_decorators, name='dispatch')
# class EducationView(CustomViewSetMixin):
#     template_name = "portfolios/professional-experiences/professional-experiences.html"
#     snippet_template = "portfolios/professional-experiences/professional-experiences-snippet.html"
#     model = ProfessionalExperience
#     form_class = ProfessionalExperienceForm
#     paginate_by = 4
#     success_url = 'portfolios:professional_experiences'
#     lookup_field = 'slug'
#     url_list = ["professional_experiences", "professional_experience_create", "professional_experience_detail", "professional_experience_update", "professional_experience_delete"]

#     def get_queryset(self):
#         return ProfessionalExperience.objects.all()

#     def get_object(self, *args, **kwargs):
#         return ProfessionalExperience.objects.get_by_slug(self.kwargs.get('slug'))

#     def form_valid(self, form):
#         # assign user to the form
#         form.instance.user = self.request.user
#         # validate unique  company name
#         qs = ProfessionalExperience.objects.filter(user=self.request.user, company__iexact=form.cleaned_data.get('company')).exclude(slug__iexact=self.kwargs.get('slug'))
#         if qs:
#             form.add_error(
#                 "title", forms.ValidationError(
#                     f"This company already exists!"
#                 )
#             )
#         return super().form_valid(form)
