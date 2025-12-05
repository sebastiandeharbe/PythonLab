import re

# Genera campos desde 6 hasta 400
for i in range(6, 401):
    print(f'''field("Text Value {i}"; Rec."Text Value {i}")
{{
    ApplicationArea = All;
    Visible = FieldVisible{i};
    Editable = FieldEditable{i};
}}
''')
