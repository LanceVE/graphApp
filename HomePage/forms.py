from django import forms
from .models import GraphModel
from django.core.validators import FileExtensionValidator

ALGORITHM_CHOICES = [
    ('N/A', 'N/A'),
    ('bubbleSort', 'bubbleSort'),
    ('insertionSort', 'insertionSort'),
    ('dijkstras', 'dijkstras'),
    ('knapsackDP', 'knapsackDP'),
    ('LCS', 'LCS'),
    ('Kruskals', 'Kruskals'),
    ('Prims', 'Prims'),
    ('BellmanFord', 'BellmanFord'),
    ('KMP', 'KMP'),
    ('IntervalGreed', 'IntervalGreed'),
     ('Huffman', 'Huffman'),
]


class GraphForm(forms.ModelForm):
   class Meta:
      model = GraphModel
      fields = ('graph', )

class numbersFormDijk(forms.Form):
    starting_node = forms.CharField(label='Starting Node', max_length=3)
    graph_file = forms.FileField(label='Upload Graph File', validators=[FileExtensionValidator(allowed_extensions=['txt'])])

class csvForm(forms.Form):
    file = forms.FileField()

class numbersForm(forms.Form):
    numbers = forms.CharField(label = 'numbers', max_length=100)
    algorithm = forms.CharField(label = 'Select your algorithm', widget = forms.Select(choices = ALGORITHM_CHOICES))

    
class numbersFormKnapsack(forms.Form):
    Max_Weight = forms.CharField(label = 'Max Weight', max_length=100)
    Profit = forms.CharField(label = 'Profits', max_length=100)
    Weight = forms.CharField(label = 'Weights', max_length=100)
    
class numbersFormLCS(forms.Form):
  LCS1 = forms.CharField(label = 'String 1', max_length = 100)
  LCS2 = forms.CharField(label = 'String 2', max_length = 100)


class stringFormKMP(forms.Form):
  LCS1 = forms.CharField(label = 'Text', max_length = 100)
  LCS2 = forms.CharField(label = 'Pattern', max_length = 100)

class huffmanForm(forms.Form):
  LCS1 = forms.CharField(label = 'Character', max_length = 100)
  LCS2 = forms.CharField(label = 'Frequency', max_length = 100)

