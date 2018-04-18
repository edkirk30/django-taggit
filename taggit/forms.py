from __future__ import unicode_literals

from django import forms
from django.utils import six
from django.utils.translation import ugettext as _

from taggit.utils import edit_string_for_tags, parse_tags

class TagWidget(forms.TextInput):

    def render(self, name, value, attrs=None):
        if value is not None and not isinstance(value, six.string_types):
            value = edit_string_for_tags([
                o.tag for o in value.select_related("tag")])
        return super(TagWidget, self).render(name, value, attrs)


class TagField(forms.CharField):
    widget = TagWidget

    def clean(self, value):
        value = super(TagField, self).clean(value)
        try:
            return parse_tags(value)
        except ValueError:
            raise forms.ValidationError(
                _("Please provide a comma-separated list of tags."))

    def has_changed(self, initial, data):
        return super().has_changed(initial, data)

    def has_changed_initial_querysets_evaluated(
        self, original_initial, original_data):

        if original_initial is not None and not isinstance(original_initial, str):
            initial = edit_string_for_tags(
                [o.tag for o in original_initial])
        else:
            initial = original_initial

        if original_data is not None and not isinstance(original_data, str):
            data = edit_string_for_tags(
                [o for o in original_data])
        else:
            data = original_data

        return super().has_changed(initial, data)
