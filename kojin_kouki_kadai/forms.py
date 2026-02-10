from django import forms
from .models import Lecture, Assignment, SubmissionRecord, Grading


class LectureForm(forms.ModelForm):
    """講義フォーム"""

    class Meta:
        model = Lecture
        fields = [
            "name",
            "instructor",
            "day_of_week",
            "start_time",
            "end_time",
            "classroom",
        ]
        widgets = {
            "name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "講義名"}
            ),
            "instructor": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "講師名"}
            ),
            "day_of_week": forms.Select(attrs={"class": "form-control"}),
            "start_time": forms.TimeInput(
                attrs={"class": "form-control", "type": "time"}
            ),
            "end_time": forms.TimeInput(
                attrs={"class": "form-control", "type": "time"}
            ),
            "classroom": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "教室"}
            ),
        }


class AssignmentForm(forms.ModelForm):
    """課題フォーム"""

    class Meta:
        model = Assignment
        fields = ["lecture", "title", "description", "due_date", "priority", "status"]
        widgets = {
            "lecture": forms.Select(attrs={"class": "form-control"}),
            "title": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "課題名"}
            ),
            "description": forms.Textarea(
                attrs={"class": "form-control", "placeholder": "説明", "rows": 4}
            ),
            "due_date": forms.DateTimeInput(
                attrs={"class": "form-control", "type": "datetime-local"}
            ),
            "priority": forms.Select(attrs={"class": "form-control"}),
            "status": forms.Select(attrs={"class": "form-control"}),
        }


class SubmissionRecordForm(forms.ModelForm):
    """提出記録フォーム（学生用）"""

    class Meta:
        model = SubmissionRecord
        fields = ["assignment", "submitted_at", "notes"]
        widgets = {
            "assignment": forms.Select(attrs={"class": "form-control"}),
            "submitted_at": forms.DateTimeInput(
                attrs={"class": "form-control", "type": "datetime-local"}
            ),
            "notes": forms.Textarea(
                attrs={"class": "form-control", "placeholder": "備考", "rows": 3}
            ),
        }


class GradingForm(forms.ModelForm):
    """採点記録フォーム（先生用）"""

    class Meta:
        model = Grading
        fields = ["grade", "feedback"]
        widgets = {
            "grade": forms.NumberInput(
                attrs={"class": "form-control", "placeholder": "成績（100点満点）"}
            ),
            "feedback": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "フィードバック",
                    "rows": 3,
                }
            ),
        }
