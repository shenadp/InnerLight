from django.forms.widgets import CheckboxInput, TimeInput, DateInput

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