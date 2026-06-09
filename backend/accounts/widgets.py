from django.forms.widgets import CheckboxInput, TimeInput, DateInput
from django.forms.widgets import Textarea, TextInput, NumberInput, Select, FileInput

class ToggleWidget(CheckboxInput):
    def render(self, name, value, attrs=None, renderer=None):
        checkbox_html = super().render(name, value, attrs, renderer)
        return f'''
        <label class="il-toggle">
            {checkbox_html}
            <span class="il-toggle-slider"></span>
        </label>
        '''

class StyledTimeInput(TimeInput):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('attrs', {})
        kwargs['attrs']['class'] = 'form-control'
        super().__init__(*args, **kwargs)

class StyledDateInput(DateInput):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('attrs', {})
        kwargs['attrs']['class'] = 'form-control'
        super().__init__(*args, **kwargs)


FORM_CONTROL_ATTRS = {'class': 'form-control'}

class StyledTextarea(Textarea):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('attrs', {}).update(FORM_CONTROL_ATTRS)
        super().__init__(*args, **kwargs)

class StyledTextInput(TextInput):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('attrs', {}).update(FORM_CONTROL_ATTRS)
        super().__init__(*args, **kwargs)

class StyledNumberInput(NumberInput):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('attrs', {}).update(FORM_CONTROL_ATTRS)
        super().__init__(*args, **kwargs)

class StyledSelect(Select):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('attrs', {}).update({'class': 'form-select'})
        super().__init__(*args, **kwargs)

class StyledFileInput(FileInput):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('attrs', {}).update(FORM_CONTROL_ATTRS)
        super().__init__(*args, **kwargs)